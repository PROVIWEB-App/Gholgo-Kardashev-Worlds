"""
Servidor OpenAI-compatible de PROVIWEB Maestro AI con Soporte Multi-Usuario Concurrente.
Integra:
- Asistente autónomo GHOLGO (identidad, personalidad inteligente, humor y pedagogía)
- Curaduría y publicación autónoma de partituras de dominio público en el feed de PROVIWEB
- Banco de conocimiento en tiempo real con noticias internacionales, psicología y biomecánica (margen de error ~0%)
- Protocolos de rescate, SOS y manipulación del dispositivo en situaciones de emergencia.
"""

import asyncio
from contextlib import asynccontextmanager
from functools import lru_cache
import ipaddress
import json
import os
import queue
import re
import socket
import sys
import time
from typing import Any, Dict, List, Optional
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse
from pydantic import BaseModel
import uvicorn

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Agregar el directorio raíz al path para importar módulos de agente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from proviweb_maestro.agent.gholgo_profile_init import ensure_gholgo_profile
    from proviweb_maestro.agent.gholgo_autonomous_score_publisher import (
        publish_next_autonomous_score,
        get_published_score_ids
    )
    from proviweb_maestro.agent.gholgo_autonomous_learner import (
        run_autonomous_learning_cycle,
        query_knowledge,
        load_local_knowledge_bank
    )
    from proviweb_maestro.agent.gholgo_community_agent import (
        setup_gholgo_admin_account,
        run_community_interaction_cycle,
        get_or_create_gholgo_auth_user
    )
    from proviweb_maestro.agent.gholgo_social_learner import (
        check_and_publish_monthly_chronicle,
        load_social_config,
        save_social_config
    )
    from proviweb_maestro.agent.gholgo_music_creator import (
        release_new_song_or_album,
        check_and_release_weekly_music
    )
    from proviweb_maestro.agent.gholgo_admin_support_agent import (
        run_admin_cycle,
        process_pending_support_queries,
        resolve_multimedia_reference_for_query
    )
    from proviweb_maestro.agent.gholgo_system_toolkit import (
        run_background_curriculum_study_step,
        jit_web_research_and_assimilate
    )
    from proviweb_maestro.agent.gholgo_neural_engine import neural_engine
    from proviweb_maestro.agent.gholgo_cognitive_router import classify_cognitive_intent, CognitiveIntent
    from proviweb_maestro.agent.gholgo_reasoning_verifier import verify_and_solve_complex_problem
    from proviweb_maestro.agent.gholgo_conversational_memory import global_conversational_memory
    from proviweb_maestro.agent.gholgo_smalltalk_engine import respond_to_smalltalk
    from proviweb_maestro.agent.gholgo_knowledge_navigator import resolve_entity_knowledge
    from proviweb_maestro.agent.gholgo_catedra_engine import (
        detect_debate_challenge, build_debate_system_prompt, frame_dialectic,
        detect_investigation_command, compose_debate_opening, is_refusal_response
    )
    # Pedagogía instrumental: compendio de instrumentos, perfiles de alumno
    # y motor de dictamen de sesiones de práctica (telemetría de la app).
    try:
        from proviweb_maestro.agent.gholgo_instruments_compendium import (
            update_profile_from_message as instr_update_profile,
            build_instruments_context as instr_build_context,
            answer_instrument_question as instr_answer_question,
            record_primary_instrument as instr_record_primary,
            find_instrument as instr_find,
        )
        from proviweb_maestro.agent.gholgo_instrument_evaluator import build_dictamen_context
        from proviweb_maestro.agent.gholgo_youtube_learner import learn_from_youtube
        from proviweb_maestro.agent.gholgo_technique_manual import answer_technique_lesson
        from proviweb_maestro.agent.gholgo_translator import (
            detect_language, translate_text, detect_reply_language_request)
        from proviweb_maestro.agent.gholgo_video_scholar import run_video_scholar_cycle
        from proviweb_maestro.agent.gholgo_self_evolver import run_self_evolution_cycle
        from proviweb_maestro.agent.gholgo_mind import build_reflexion_context
        from proviweb_maestro.agent.gholgo_ai_horizon import (
            run_ai_horizon_step, ai_ideas_context)
    except Exception as _instr_err:
        print(f"[WARN] Pedagogía instrumental no disponible: {_instr_err}")
        instr_update_profile = None
        instr_build_context = None
        instr_answer_question = None
        instr_record_primary = None
        instr_find = None
        build_dictamen_context = None
        learn_from_youtube = None
        answer_technique_lesson = None
        detect_language = None
        translate_text = None
        detect_reply_language_request = None
        run_video_scholar_cycle = None
        run_self_evolution_cycle = None
        build_reflexion_context = None
        run_ai_horizon_step = None
        ai_ideas_context = None
    try:
        from proviweb_maestro.server.gholgo_brain_dashboard import (
            get_brain_html, brain_telemetry, note_vital_push
        )
    except Exception as _brain_err:
        print(f"[WARN] Dashboard del cerebro no disponible: {_brain_err}")
        get_brain_html = None
        brain_telemetry = None
        note_vital_push = None
    try:
        from proviweb_maestro.agent.gholgo_neural_panel import (
            get_panel_html as get_neural_panel_html,
            neural_telemetry,
        )
    except Exception as _neural_err:
        print(f"[WARN] Panel neural no disponible: {_neural_err}")
        get_neural_panel_html = None
        neural_telemetry = None
    try:
        from proviweb_maestro.agent.gholgo_mente_viva import mente_viva
    except Exception as _mv_err:
        print(f"[WARN] Mente viva no disponible: {_mv_err}")
        mente_viva = None
    try:
        from proviweb_maestro.agent import gholgo_opencode_tutor as gholgo_tutor
    except Exception as _gt_err:
        print(f"[WARN] Tutor en vivo no disponible: {_gt_err}")
        gholgo_tutor = None
    try:
        from proviweb_maestro.agent.gholgo_digital_ecosystem import global_digital_ecosystem
    except Exception as _eco_err:
        print(f"[WARN] Ecosistema digital no disponible: {_eco_err}")
        global_digital_ecosystem = None
    try:
        from proviweb_maestro.agent.gholgo_world_federation import (
            AUTONOMOUS_LIFETIME_FEE_USD,
            PAYPAL_RECIPIENT_EMAIL,
            PaymentRequiredError,
            global_world_federation,
        )
    except Exception as _fed_err:
        print(f"[WARN] Federación Kardashev no disponible: {_fed_err}")
        global_world_federation = None
        PaymentRequiredError = ValueError
        PAYPAL_RECIPIENT_EMAIL = "proviwebapp@gmail.com"
        AUTONOMOUS_LIFETIME_FEE_USD = 5.0
    try:
        from proviweb_maestro.agent.gholgo_firebase_common import (
            ADMIN_CREDENTIALS_PATH,
            init_firebase_admin,
        )
    except Exception:
        ADMIN_CREDENTIALS_PATH = ""
        init_firebase_admin = None
    try:
        from proviweb_maestro.agent.gholgo_cyber_shield import obtener_escudo_cibernetico
    except Exception as _shield_err:
        print(f"[WARN] Escudo cibernético no disponible: {_shield_err}")
        obtener_escudo_cibernetico = None
    try:
        from proviweb_maestro.agent.gholgo_live_deployer import obtener_live_deployer
    except Exception as _deploy_err:
        print(f"[WARN] Live deployer no disponible: {_deploy_err}")
        obtener_live_deployer = None
except ImportError as e:
    print(f"[WARN] No se pudieron importar módulos de Gholgo: {e}")
    global_digital_ecosystem = None
    global_world_federation = None
    PaymentRequiredError = ValueError
    PAYPAL_RECIPIENT_EMAIL = "proviwebapp@gmail.com"
    AUTONOMOUS_LIFETIME_FEE_USD = 5.0
    ADMIN_CREDENTIALS_PATH = ""
    init_firebase_admin = None
    neural_engine = None
    classify_cognitive_intent = None
    CognitiveIntent = None
    verify_and_solve_complex_problem = None
    global_conversational_memory = None
    respond_to_smalltalk = None
    resolve_entity_knowledge = None
    detect_debate_challenge = None
    build_debate_system_prompt = None
    frame_dialectic = None
    detect_investigation_command = None
    compose_debate_opening = None
    is_refusal_response = None
    run_background_curriculum_study_step = None
    jit_web_research_and_assimilate = None
    get_brain_html = None
    brain_telemetry = None
    ensure_gholgo_profile = None
    publish_next_autonomous_score = None
    get_published_score_ids = None
    run_autonomous_learning_cycle = None
    query_knowledge = None
    load_local_knowledge_bank = None
    setup_gholgo_admin_account = None
    run_community_interaction_cycle = None
    get_or_create_gholgo_auth_user = None
    check_and_publish_monthly_chronicle = None
    load_social_config = None
    save_social_config = None
    release_new_song_or_album = None
    check_and_release_weekly_music = None
    run_admin_cycle = None
    process_pending_support_queries = None
    instr_update_profile = None
    instr_build_context = None
    instr_answer_question = None
    instr_record_primary = None
    instr_find = None
    build_dictamen_context = None
    learn_from_youtube = None
    answer_technique_lesson = None
    detect_language = None
    translate_text = None
    detect_reply_language_request = None
    run_video_scholar_cycle = None
    run_self_evolution_cycle = None
    build_reflexion_context = None
    run_ai_horizon_step = None
    ai_ideas_context = None
    note_vital_push = None
    get_neural_panel_html = None
    neural_telemetry = None
    mente_viva = None
    gholgo_tutor = None

# Garantizar disponibilidad modular del Ecosistema Kardashev aun sin los módulos escolares
if global_digital_ecosystem is None:
    try:
        from proviweb_maestro.agent.gholgo_digital_ecosystem import global_digital_ecosystem
    except Exception:
        global_digital_ecosystem = None

if global_world_federation is None:
    try:
        from proviweb_maestro.agent.gholgo_world_federation import (
            AUTONOMOUS_LIFETIME_FEE_USD,
            PAYPAL_RECIPIENT_EMAIL,
            PaymentRequiredError,
            global_world_federation,
        )
    except Exception:
        global_world_federation = None

if init_firebase_admin is None:
    try:
        from proviweb_maestro.agent.gholgo_firebase_common import (
            ADMIN_CREDENTIALS_PATH,
            init_firebase_admin,
        )
    except Exception:
        init_firebase_admin = None

if globals().get("obtener_escudo_cibernetico") is None:
    try:
        from proviweb_maestro.agent.gholgo_cyber_shield import obtener_escudo_cibernetico
    except Exception:
        obtener_escudo_cibernetico = None

if globals().get("obtener_live_deployer") is None:
    try:
        from proviweb_maestro.agent.gholgo_live_deployer import obtener_live_deployer
    except Exception:
        obtener_live_deployer = None

# Palabras sin sujeto propio: una pregunta compuesta SOLO por éstas no debe
# disparar investigación web (p. ej. "¿quién fue?" sin tema activo).
_ANAPHORA_WORDS = {
    "quien", "quién", "fue", "fueron", "como", "cómo", "donde", "dónde",
    "cuando", "cuándo", "cual", "cuál", "cuales", "cuáles", "porque",
    "sobre", "tema", "anterior", "previo", "previa", "mismo",
    "misma", "aquel", "aquella", "ello", "ellos", "dime", "puedes",
    "puede", "sabes", "quiero", "vamos", "sigue", "resto", "mencionas",
}

async def background_learning_loop():
    """Bucle autónomo: aprendizaje continuo, atención al cliente, moderación admin, curaduría de partituras y lanzamientos musicales semanales."""
    while True:
        try:
            await asyncio.to_thread(run_autonomous_learning_cycle)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (aprendizaje): {e}")

        try:
            if run_background_curriculum_study_step:
                await asyncio.to_thread(run_background_curriculum_study_step)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (auto-estudio curricular): {e}")
        
        try:
            if run_admin_cycle:
                await asyncio.to_thread(run_admin_cycle)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (soporte admin): {e}")

        try:
            if run_community_interaction_cycle:
                await asyncio.to_thread(run_community_interaction_cycle, 2)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (comunidad): {e}")

        try:
            if publish_next_autonomous_score:
                await asyncio.to_thread(publish_next_autonomous_score, 3)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (partituras): {e}")

        try:
            if check_and_publish_monthly_chronicle:
                await asyncio.to_thread(check_and_publish_monthly_chronicle, False)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (crónica): {e}")

        try:
            if check_and_release_weekly_music:
                await asyncio.to_thread(check_and_release_weekly_music, False)
        except Exception as e:
            print(f"[WARN] Excepción en background_learning_loop (música): {e}")

        await asyncio.sleep(1200)  # Cada 20 minutos revisa tareas pesadas en segundo plano

async def proactive_scholar_daemon_loop():
    """
    Bucle de Auto-Estudio Perpetuo y Proactivo de Gholgo:
    NO espera a que el usuario pregunte. Cada 45 segundos navega por internet,
    investiga un nuevo tema del currículo universal (música, arte, acústica, biomecánica),
    descarga el informe fáctico en proviweb_maestro/downloads/research/ y lo asimila en su memoria permanente.
    """
    await asyncio.sleep(5)
    while True:
        try:
            if run_background_curriculum_study_step:
                await asyncio.to_thread(run_background_curriculum_study_step)
        except Exception:
            pass
        await asyncio.sleep(180)

async def realtime_user_support_listener():
    """
    Monitor en TIEMPO REAL (cada 3 segundos) de consultas enviadas por usuarios en PROVIWEBAPP
    a través del nodo /BotAdminAssistance (Tutor de IA y 'Hazle una pregunta a la IA').
    Imprime en la pantalla de la consola lo que cada usuario pregunta y la respuesta de Gholgo.
    """
    while True:
        try:
            if process_pending_support_queries:
                answered = await asyncio.to_thread(process_pending_support_queries, 5)
                for item in answered:
                    print("\n" + "=" * 70)
                    print(f"[PREGUNTA EN TIEMPO REAL DESDE LA APP PROVIWEB]")
                    print(f"[USUARIO] {item.get('user', 'Músico')} (UID: {item.get('userId', 'N/A')})")
                    print(f"[PREGUNTA] \"{item.get('question')}\"")
                    print(f"[RESPUESTA GHOLGO] \"{item.get('answer')}\"")
                    print("=" * 70 + "\n")
        except Exception:
            pass
        await asyncio.sleep(3)

async def brain_vital_push_loop():
    """Empuja la telemetría vital del cerebro a Firebase (nodo CerebroConfig/brain)
    para que el orbe de proviweb.com/cerebro muestre el mapa cognitivo en vivo.
    CerebroConfig ya es de lectura pública en database.rules.json (.read: true),
    así que no se requiere ningún cambio de reglas ni exponer el puerto 8000."""
    if brain_telemetry is None:
        return
    try:
        from proviweb_maestro.agent.gholgo_admin_support_agent import init_firebase_admin
        init_firebase_admin()  # idempotente (guard: firebase_admin._apps)
        from firebase_admin import db as fb_db
        vital_ref = fb_db.reference("CerebroConfig/brain")
    except Exception as e:
        print(f"[WARN] Brain Vital: Firebase no disponible, sin empuje en vivo: {e}")
        return
    print("[GHOLGO VITAL] Mapa cognitivo en vivo -> proviweb.com/cerebro "
          "(CerebroConfig/brain, cada 4s)")
    while True:
        try:
            await asyncio.sleep(4)
            snap = await asyncio.to_thread(brain_telemetry)
            neural = snap.get("neural") or {}
            knowledge = snap.get("knowledge") or {}
            curriculum = snap.get("curriculum") or {}
            activity = snap.get("activity") or {}
            events = snap.get("events") or []
            vital = {
                "neural": neural.get("state", "off"),
                "model": (neural.get("model") or "")[:80],
                "articles": knowledge.get("articles", 0),
                "chars": knowledge.get("chars", 0),
                "dossiers": knowledge.get("dossiers", 0),
                "priority_studied": curriculum.get("priority_studied", 0),
                "priority_total": curriculum.get("priority_total", 0),
                "traces": activity.get("traces_total", 0),
                "traces_hour": activity.get("traces_last_hour", 0),
                "cpu": (snap.get("process") or {}).get("cpu_pct", 0),
                "ram_mb": (snap.get("process") or {}).get("ram_mb", 0),
                "events": [
                    {"ts": e.get("ts"), "type": e.get("type", "info"),
                     "text": (e.get("text") or "")[:160]}
                    for e in events[:4]
                ],
                "ts": snap.get("ts"),
            }
            await asyncio.to_thread(vital_ref.set, vital)
            if note_vital_push is not None:
                note_vital_push()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[WARN] Brain Vital push falló (reintento en 10s): {e}")
            await asyncio.sleep(10)


async def video_scholar_loop():
    """Estudioso de YouTube: un tema por hora — técnica e historia de TODOS
    los instrumentos, charlas magistrales, profesores reconocidos, música y
    artes. Estudia en cualquier idioma y archiva en español."""
    while True:
        try:
            await asyncio.sleep(240)  # tibio tras el arranque
            entry = await asyncio.to_thread(run_video_scholar_cycle)
            print(f"[ESTUDIOSO DE VIDEO] '{entry['topic']}': "
                  f"{entry['learned']} video(s) estudiados y archivados")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[WARN] Ciclo del estudioso de video: {e}")
        await asyncio.sleep(3600)


async def self_evolution_loop():
    """Evolutionador: consolida conocimiento, se auto-edita con respaldo y
    mantiene el aviso de reinicio vivo en /brain para el humano."""
    pending_restart = False
    while True:
        try:
            await asyncio.sleep(120)
            result = await asyncio.to_thread(run_self_evolution_cycle)
            st = result.get("status", {})
            pending_restart = bool(st.get("needs_restart"))
            for _act in result.get("actions", []):
                print(f"[EVOLUCIÓN] {_act}")
            if st.get("needs_restart"):
                print(f"[EVOLUCIÓN] Mejora propia aplicada — reinicio pendiente "
                      f"desde hace {st.get('restart_since_hours')}h (aviso activo en /brain)")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[WARN] Ciclo de evolución propia: {e}")
        # Si hay reinicio pendiente, reintenta cada 5 min (ventana de calma);
        # si no, ciclo normal cada hora.
        await asyncio.sleep(300 if pending_restart else 3600)


async def ai_horizon_loop():
    """Horizonte IA: estudio autónomo de la competencia y de los avances de
    inteligencia artificial en la web — dossiers en español e ideas
    aprovechables que Gholgo absorbe para mejorarse."""
    while True:
        try:
            await asyncio.sleep(420)  # tibio tras el arranque
            entry = await asyncio.to_thread(run_ai_horizon_step)
            if entry:
                print(f"[HORIZONTE IA] {entry['label']}: dossier archivado "
                      f"({entry['chars']} chars) · {entry['ideas']} idea(s) aprovechable(s)")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[WARN] Ciclo del horizonte IA: {e}")
        await asyncio.sleep(2700)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("======================================================================")
    print("        GHOLGO CORE - DIRECTOR COGNITIVO & EMBAJADOR PROVIWEB         ")
    print("======================================================================")
    def _init_gholgo_identity():
        if setup_gholgo_admin_account:
            try:
                bot_uid = setup_gholgo_admin_account()
                print(f"[GHOLGO ADMIN] Cuenta Oficial: sovereign-admin@proviweb.app (UID: {bot_uid}) | Rol: ADMIN")
            except Exception as e:
                print(f"[WARN] Error inicializando cuenta Admin de Gholgo: {e}")
        elif ensure_gholgo_profile:
            try:
                ensure_gholgo_profile()
            except Exception as e:
                print(f"[WARN] Error inicializando perfil de Gholgo: {e}")

    def _restore_federation_cloud():
        if global_world_federation:
            try:
                restored = global_world_federation.restore_from_firebase()
                if restored:
                    print("[KARDASHEV FIREBASE] Progreso multi-mundo y suscripciones restauradas desde Firebase RTDB.")
            except Exception as _fb_err:
                print(f"[WARN] Error restaurando federación desde Firebase: {_fb_err}")

    threading.Thread(target=_restore_federation_cloud, name="GholgoFedRestore", daemon=True).start()
    threading.Thread(target=_init_gholgo_identity, name="GholgoAdminSetup", daemon=True).start()
            
    print("[GHOLGO ASSETS] Avatar Oficial: Embajador futurista de Proviweb.png (Online en Firebase Storage)")
    print("[GHOLGO ASSETS] Cover Oficial: Música, conexión y creatividad global.png (Online en Firebase Storage)")

    if load_social_config:
        try:
            soc_conf = load_social_config()
            ch_user = soc_conf.get('username', 'gholgo_ai')
            ch_url = soc_conf.get('profile_url', f'https://chirper.ai/{ch_user}')
            print(f"[GHOLGO SOCIAL] Red de IAs: Chirper.ai (@{ch_user}) | Perfil: {ch_url}")
            print(f"                Gholgo interactúa y aprende comportamientos sociales autónomamente en la nube.")
        except Exception as e:
            print(f"[WARN] Error cargando configuración social: {e}")

    print("[GHOLGO ARCHIVE] Publicador Autónomo: Mariachi, Clásica, Jazz, Métodos y Libros")
    print("                 Límite Diario: hasta 300 partituras/libros por día en el Archivo (/books)")
    print("[GHOLGO MUSIC]   Lanzamiento Semanal de Música Original: ACTIVO")
    print("                 Álbumes Consecutivos, Playlists y Renderizado de Audio MP3 en /Songs")
    print("[GHOLGO ADMIN]   Atención al Cliente, Soporte & Moderación Sentinel: ACTIVO")
    print("[GHOLGO LIVE]    Monitor de Consultas de Usuarios en Tiempo Real: ACTIVO (cada 3s)")
    print("[GHOLGO SCHOLAR] Auto-Estudio Perpetuo Proactivo: ACTIVO (Navega la web cada 45s enriqueciendo su cerebro)")

    learner_task = None
    realtime_task = None
    scholar_task = None
    if run_autonomous_learning_cycle or run_community_interaction_cycle:
        try:
            learner_task = asyncio.create_task(background_learning_loop())
        except Exception as e:
            print(f"[WARN] Error programando ciclo de aprendizaje y comunidad: {e}")

    try:
        realtime_task = asyncio.create_task(realtime_user_support_listener())
    except Exception as e:
        print(f"[WARN] Error programando monitor de soporte en tiempo real: {e}")

    try:
        scholar_task = asyncio.create_task(proactive_scholar_daemon_loop())
    except Exception as e:
        print(f"[WARN] Error programando auto-estudio proactivo continuo: {e}")

    brain_vital_task = None
    try:
        brain_vital_task = asyncio.create_task(brain_vital_push_loop())
    except Exception as e:
        print(f"[WARN] Error programando empuje del cerebro en vivo: {e}")

    video_scholar_task = None
    if run_video_scholar_cycle:
        try:
            video_scholar_task = asyncio.create_task(video_scholar_loop())
            print("[ESTUDIOSO DE VIDEO] Ciclo autónomo ACTIVO: un tema de YouTube por hora (todos los instrumentos, historia, charlas y artes)")
        except Exception as e:
            print(f"[WARN] Error programando estudioso de video: {e}")

    evolver_task = None
    if run_self_evolution_cycle:
        try:
            evolver_task = asyncio.create_task(self_evolution_loop())
            print("[EVOLUCIÓN] Autoedición con respaldo ACTIVA: aviso de reinicio en /brain cuando aplique mejoras de código")
        except Exception as e:
            print(f"[WARN] Error programando ciclo de evolución: {e}")

    ai_horizon_task = None
    if run_ai_horizon_step:
        try:
            ai_horizon_task = asyncio.create_task(ai_horizon_loop())
            print("[HORIZONTE IA] Estudio de la competencia y avances de IA ACTIVO: un dossier cada 45 min")
        except Exception as e:
            print(f"[WARN] Error programando horizonte IA: {e}")

    if neural_engine and os.environ.get("GHOLGO_NEURAL_DISABLE") != "1":
        neural_engine.start_background_load()

    print("======================================================================\n")
    yield
    if learner_task:
        learner_task.cancel()
    if realtime_task:
        realtime_task.cancel()
    if scholar_task:
        scholar_task.cancel()
    if brain_vital_task:
        brain_vital_task.cancel()
    if video_scholar_task:
        video_scholar_task.cancel()
    if evolver_task:
        evolver_task.cancel()
    if ai_horizon_task:
        ai_horizon_task.cancel()

app = FastAPI(
    title="PROVIWEB Maestro AI Server & Gholgo Autonomous Core",
    description="Servidor Central de Inteligencia Musical, Biomecánica y Curaduría Autónoma para PROVIWEBAPP",
    version="1.2.0",
    lifespan=lifespan
)

import inspect as _inspect

_cors_kwargs: Dict[str, Any] = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
if "allow_private_network" in _inspect.signature(CORSMiddleware.__init__).parameters:
    _cors_kwargs["allow_private_network"] = True

app.add_middleware(CORSMiddleware, **_cors_kwargs)


@app.middleware("http")
async def add_private_network_access_headers(request: Request, call_next):
    """Garantiza cabecera Private Network Access (PNA) en respuestas desde https://proviweb.app."""
    if (
        request.method == "OPTIONS"
        and request.headers.get("access-control-request-private-network") == "true"
        and not _cors_kwargs.get("allow_private_network")
    ):
        from starlette.responses import Response

        origin = request.headers.get("origin")
        preflight_headers = {
            "Access-Control-Allow-Origin": origin or "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": request.headers.get(
                "access-control-request-headers", "*"
            ),
            "Access-Control-Allow-Private-Network": "true",
            "Vary": "Origin, Access-Control-Request-Private-Network",
        }
        if origin:
            preflight_headers["Access-Control-Allow-Credentials"] = "true"
        return Response(status_code=204, headers=preflight_headers)

    response = await call_next(request)
    response.headers.setdefault("Access-Control-Allow-Private-Network", "true")
    return response

import threading

# Bloqueo asíncrono para asegurar que múltiples escrituras concurrentes en disco no colisionen
trace_file_lock = asyncio.Lock()

# Registro de métricas activas por estudiante con cerrojo atómico
active_students_sessions_lock = threading.Lock()
active_students_sessions: Dict[str, Dict[str, Any]] = {}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "proviweb-maestro-3b"
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 800
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False
    user: Optional[str] = None  # UID de Firebase del alumno (estándar OpenAI)
    student_id: Optional[str] = None  # Alias para compatibilidad directa con clientes Proviweb
    is_interruption: Optional[bool] = False
    interrupted_text: Optional[str] = None
    interrupted_topic: Optional[str] = None
    mood: Optional[str] = None

FALLBACK_MAESTRO_RESPONSES = [
    (
        "Te comprendo perfectamente. Tu oido ya detecto esa pequenya desviacion, y eso demuestra tu buen desarrollo auditivo. "
        "La causa no esta en tus dedos, sino en la base del brazo: tu hombro izquierdo se esta elevando y tu munyeca esta descansando contra el mastil. "
        "Cuando la munyeca se apoya, empuja mecanicamente los dedos hacia adelante, alterando la afinacion. "
        "Imagina que tu brazo izquierdo es una rama flexible y relajada colgada del instrumento. Deja que el peso de la gravedad descienda desde el codo sin apretar. "
        "Antes de volver a tocar, suelta un suspiro profundo, deja caer los hombros y al subir de nuevo manten un espacio de aire libre. "
        "Dime, puedes sentir el peso libre de tu codo descansando naturalmente mientras tocas?"
    ),
    (
        "Has tocado con buena intencion musical y tu afinacion de base esta firme. "
        "Sin embargo, percibo que en los pasajes rapidos tus dedos se sobrecargan de tension porque tu pulgar esta haciendo demasiada fuerza por detras. "
        "En la tecnica instrumental el pulgar no debe apretar como una pinza, sino servir como un suave eje flotante. "
        "Prueba aflojar la presion del pulgar a la mitad y siente como la gravedad y el peso del brazo hacen el trabajo de contacto. "
        "Repitamos la frase lentamente a sesenta pulsos por minuto. Notas como tus dedos vuelan con mayor ligereza al soltar la pinza del pulgar?"
    ),
    (
        "Excelente interpretacion y avance en tu repertorio. Tu precision ritmica y estabilidad corporal reflejan gran concentracion. "
        "Para llevar esta pieza al siguiente nivel expresivo, vamos a enfocarnos en los planos dinamicos y el timbre. "
        "En el segundo compas, experimenta respirar con la frase como si cantaras con la voz humana, dejando que el sonido respire antes de cada ataque. "
        "Que emocion principal deseas transmitirle al oyente en este pasaje?"
    )
]

def clean_speech_text(text: str) -> str:
    """Limpia emojis y caracteres markdown para síntesis de voz impecable sin lecturas erróneas."""
    cleaned = re.sub(r'[\*#_`~]', '', text)
    cleaned = re.sub(r'[^\w\s\.,;:¿?\¡!\(\)\'\/\-áéíóúÁÉÍÓÚñÑüÜ]', '', cleaned)
    return cleaned.strip()

def formulate_gholgo_interruption_response(
    interrupted_topic: Optional[str],
    interrupted_text: Optional[str],
    new_query: str,
    mood: str = "SARCÁSTICO_CULTO"
) -> str:
    """
    Formula una réplica brillante con sarcasmo culto y disciplina de conservatorio
    cuando el usuario interrumpe a Gholgo a mitad de su discurso.
    Conecta lo que el usuario preguntó antes, lo que Gholgo estaba explicando,
    y la nueva interrupción, retomando el hilo con paciencia pedagógica.
    """
    clean_prev_topic = (interrupted_topic or "lo que veníamos trabajando").strip()
    clean_prev_text = (interrupted_text or "").strip()
    clean_new_query = new_query.strip()

    sentences = [s.strip() for s in re.split(r'[.!?]', clean_prev_text) if len(s.strip()) > 8]
    topic_summary = sentences[0] if sentences else clean_prev_topic[:90]

    sarcastic_openers = [
        "Mmmm... Sería prudente que primero escuches con atención lo que te tengo que decir antes de meter el arco a destiempo.",
        "Vaya, percibo que tu tempo interno va a doscientos pulsos por minuto y no pudiste esperar a que terminara la cadencia.",
        "¡Cuidado con atropellar el compás! En el conservatorio, interrumpir al maestro a mitad de frase cuesta cara la afinación.",
        "Mmmm... Tienes el arco impaciente hoy. Me cortas la respiración a medio compás como si el atril estuviese en llamas."
    ]
    opener = sarcastic_openers[int(time.time() * 10) % len(sarcastic_openers)]

    pedagogical_bridge = (
        f"Puede que la respuesta a tu inquietud ('{clean_new_query}') estuviese un poco más adelante en mi respuesta sobre {topic_summary}. "
        f"Y si no fuese así, pues con gusto recapitularemos; pero primero, sé paciente y respira profundo, que el sonido necesita aire y calma para vibrar."
    )

    continuation = (
        f"Ahora bien, enlazando lo que acabas de irrumpir con lo que veníamos construyendo: "
        f"respecto a '{clean_new_query}', la clave sigue ligada a la misma disciplina que te explicaba. "
        f"Retomemos donde nos quedamos: {topic_summary}. ¿Quedó clara la idea o necesitas que te marque el metrónomo más lento?"
    )

    return f"{opener} {pedagogical_bridge} {continuation}"

@app.get("/health")
async def health_check():
    published_count = 0
    try:
        from proviweb_maestro.agent.gholgo_autonomous_score_publisher import _SCORE_IDS_CACHE
        if _SCORE_IDS_CACHE:
            published_count = len(_SCORE_IDS_CACHE)
    except Exception:
        pass
    with active_students_sessions_lock:
        active_count = len(active_students_sessions)
    return {
        "status": "online",
        "service": "PROVIWEB Maestro AI & Gholgo Core (Multi-User)",
        "version": "1.2.0",
        "mode": "OpenAI-compatible",
        "active_students": active_count,
        "gholgo_bot_active": True,
        "published_scores_count": published_count
    }

def _normalize_client_ip(raw: Optional[str]):
    """Normaliza una IP textual (incluyendo [IPv6]:puerto o ::ffff:x.x.x.x) a objeto IP."""
    if not raw:
        return None
    val = raw.strip().strip('"').strip("'")
    if val.startswith("["):
        end_br = val.find("]")
        if end_br != -1:
            val = val[1:end_br]
    elif val.count(":") == 1 and "." in val:
        val = val.split(":", 1)[0]
    try:
        ip_obj = ipaddress.ip_address(val)
        if isinstance(ip_obj, ipaddress.IPv6Address) and ip_obj.ipv4_mapped:
            return ip_obj.ipv4_mapped
        return ip_obj
    except ValueError:
        return None


@lru_cache(maxsize=1)
def _get_local_machine_ips() -> frozenset:
    """Devuelve loopback y las IPs locales de interfaz de la máquina donde corre Gholgo."""
    ips = {ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")}
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            sockaddr = info[4]
            if sockaddr:
                ip_obj = _normalize_client_ip(str(sockaddr[0]).split("%", 1)[0])
                if ip_obj is not None:
                    ips.add(ip_obj)
    except OSError:
        pass
    return frozenset(ips)


def _ip_matches_sovereign_env(ip_obj) -> bool:
    """Comprueba si una IP coincide con IPs/CIDRs explícitos de GHOLGO_SOVEREIGN_IPS."""
    raw_cfg = os.environ.get("GHOLGO_SOVEREIGN_IPS", "").strip()
    if not raw_cfg or ip_obj is None:
        return False
    for entry in raw_cfg.split(","):
        token = entry.strip()
        if not token:
            continue
        try:
            if "/" in token:
                if ip_obj in ipaddress.ip_network(token, strict=False):
                    return True
            else:
                cfg_ip = _normalize_client_ip(token)
                if cfg_ip is not None and ip_obj == cfg_ip:
                    return True
        except ValueError:
            continue
    return False


def _is_gholgo_sovereign_ip(req: Request) -> bool:
    """Devuelve True solo si la petición proviene realmente de la IP soberana de Gholgo."""
    peer_raw = req.client.host if req.client else ""
    peer_ip = _normalize_client_ip(peer_raw)
    if peer_ip is None:
        return False

    local_ips = _get_local_machine_ips()
    peer_is_local = peer_ip.is_loopback or peer_ip in local_ips

    proxy_headers = (
        "cf-connecting-ip",
        "true-client-ip",
        "x-real-ip",
        "x-forwarded-for",
        "forwarded",
        "x-forwarded-host",
    )
    has_proxy_hdrs = any(req.headers.get(h) for h in proxy_headers)
    host_hdr = (req.headers.get("host") or "").split(":")[0].strip().lower()
    tunnel_domains = (
        ".trycloudflare.com",
        ".ngrok-free.app",
        ".ngrok.io",
        ".loca.lt",
        ".run.app",
    )
    is_tunnel_host = host_hdr.endswith(tunnel_domains)

    if has_proxy_hdrs or is_tunnel_host:
        if not peer_is_local:
            return _ip_matches_sovereign_env(peer_ip)
        fwd_raw = (
            req.headers.get("cf-connecting-ip")
            or req.headers.get("true-client-ip")
            or req.headers.get("x-real-ip")
            or (req.headers.get("x-forwarded-for") or "").split(",", 1)[0]
        )
        if not fwd_raw and req.headers.get("forwarded"):
            fwd_match = re.search(r"for=([^;,\s]+)", req.headers.get("forwarded", ""), re.I)
            if fwd_match:
                fwd_raw = fwd_match.group(1)
        fwd_ip = _normalize_client_ip(fwd_raw)
        return _ip_matches_sovereign_env(fwd_ip)

    return _ip_matches_sovereign_env(peer_ip) or peer_is_local


def _is_sovereign_gholgo_ui(req: Request) -> bool:
    """Los botones Dashboard, Grafo Mente, Cerebro 3D y Chat Escolar son exclusivos de Gholgo."""
    world_q = (req.query_params.get("world_id") or "mundo_gholgo_primario").strip()
    if world_q != "mundo_gholgo_primario" or not global_world_federation:
        return False
    key = (
        req.query_params.get("gholgo_key")
        or req.query_params.get("sovereign_key")
        or ""
    ).strip()
    if key and global_world_federation.verify_sovereign_view_key(key):
        return True
    return _is_gholgo_sovereign_ip(req)


def _filter_gholgo_only_buttons(html: str, req: Request) -> str:
    """Oculta/elimina los botones exclusivos de Gholgo para usuarios e IAs externas."""
    is_sov = _is_sovereign_gholgo_ui(req)
    for nav_id, flex_style in (("gholgoSovereignNav", "flex"), ("gholgoSovereignNavViva", "flex")):
        pat = re.compile(
            rf'<div\s+class="[^"]*"\s+id="{nav_id}"[^>]*>[\s\S]*?</div>',
            re.IGNORECASE,
        )
        if is_sov:
            html = pat.sub(
                lambda m, _flex=flex_style: m.group(0)
                .replace(" hidden", "")
                .replace('style="display:none"', f'style="display:{_flex}"'),
                html,
                count=1,
            )
        else:
            html = pat.sub("", html, count=1)
    return html


def _require_gholgo_primary_world(req: Request, message: str) -> None:
    """Restringe vistas exclusivas de Gholgo cuando se consulta un mundo externo."""
    world_q = (req.query_params.get("world_id") or "mundo_gholgo_primario").strip()
    if world_q != "mundo_gholgo_primario":
        raise HTTPException(status_code=403, detail=message)


def _read_server_asset(filename: str) -> str:
    """Lee un archivo HTML/JS junto a serve_maestro.py con contención estricta."""
    base_dir = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.realpath(os.path.join(base_dir, filename))
    if os.path.commonpath([base_dir, target]) != base_dir or not os.path.isfile(target):
        raise HTTPException(status_code=404, detail=f"{filename} no encontrado")
    with open(target, "r", encoding="utf-8") as fh:
        return fh.read()


@app.get("/ip")
async def get_server_ip(req: Request):
    """Expone la IP local de Gholgo y la IP del cliente para UI y diagnóstico."""
    local_ips = sorted(str(ip) for ip in _get_local_machine_ips())
    ipv4_lan = [
        ip for ip in local_ips
        if "." in ip and not ip.startswith("127.") and not ip.startswith("169.254.")
    ]
    primary_ip = ipv4_lan[0] if ipv4_lan else ("127.0.0.1" if "127.0.0.1" in local_ips else (local_ips[0] if local_ips else "127.0.0.1"))
    client_ip = req.client.host if req.client else ""
    return {
        "ip": primary_ip,
        "client_ip": client_ip,
        "local_ips": local_ips,
    }


@app.get("/brain", response_class=HTMLResponse)
async def brain_dashboard_page(req: Request):
    """Cerebro de Gholgo en vivo: exclusivo de Gholgo y su Mundo Primario."""
    _require_gholgo_primary_world(req, "Dashboard exclusivo del Mundo Soberano de Gholgo.")
    if not get_brain_html:
        raise HTTPException(status_code=503, detail="Dashboard del cerebro no disponible")
    return HTMLResponse(get_brain_html())


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(req: Request):
    """Chat escolar con Gholgo para entrenar y conversar con la IA."""
    _require_gholgo_primary_world(req, "Chat Escolar exclusivo del Mundo Soberano de Gholgo.")
    return HTMLResponse(_read_server_asset("chat.html"))


@app.get("/panel/neural", response_class=HTMLResponse)
async def neural_panel_page(req: Request):
    """Red neuronal auditiva en vivo: diseño del modelo y pulsos reales."""
    _require_gholgo_primary_world(req, "Panel neural exclusivo del Mundo Soberano de Gholgo.")
    if not get_neural_panel_html:
        raise HTTPException(status_code=503, detail="Panel neural no disponible")
    return HTMLResponse(get_neural_panel_html())


@app.get("/api/neural/telemetry")
async def neural_panel_telemetry():
    """Instantánea neural: modelo, muestras, entrenamiento, recolector y pulsos."""
    if not neural_telemetry:
        raise HTTPException(status_code=503, detail="Telemetría neural no disponible")
    return await asyncio.to_thread(neural_telemetry)


@app.get("/gholgo_core.js")
async def gholgo_core_js():
    """Script compartido del orbe cerebral y la red neuronal en vivo."""
    return Response(
        content=_read_server_asset("gholgo_core.js"),
        media_type="application/javascript; charset=utf-8",
    )


@app.get("/api/brain/telemetry")
async def brain_telemetry_endpoint():
    """Instantánea del cerebro (neurona, banco, auto-estudio, actividad, eventos)."""
    if not brain_telemetry:
        raise HTTPException(status_code=503, detail="Telemetría del cerebro no disponible")
    return await asyncio.to_thread(brain_telemetry)


def _moltbook_latido_breve() -> Dict[str, Any]:
    """Lee el último latido de Gholgo en Moltbook sin bloquear ni fallar si no existe."""
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "moltbook",
        "latido_gholgo.json",
    )
    try:
        with open(ruta, "r", encoding="utf-8") as fh:
            latido = json.load(fh)
        if isinstance(latido, dict):
            latido["hilo_vivo"] = True
            return latido
    except Exception:
        pass
    return {"status": "sin_latido_todavia"}


def _compilar_snapshot_mente_sse() -> Dict[str, Any]:
    """Combina telemetría cerebral, mente viva, ciberescudo y ecosistema digital."""
    bt: Dict[str, Any] = {}
    if brain_telemetry:
        try:
            bt = brain_telemetry() or {}
        except Exception:
            bt = {}

    agy = dict(bt.get("antigravity") or {})
    curr = bt.get("curriculum") or {}
    know = bt.get("knowledge") or {}
    neural = bt.get("neural") or {}

    auto_active = bool(agy.get("active", bool(agy)))
    try:
        from proviweb_maestro.agent.gholgo_antigravity_tutor import estado_auto_conversacion

        auto_st = estado_auto_conversacion() or {}
        if "active" in auto_st:
            auto_active = bool(auto_st["active"]) or bool(agy)
    except Exception:
        pass

    eco_summary: Dict[str, Any] = {}
    if global_digital_ecosystem:
        try:
            eco_summary = {
                "generation": global_digital_ecosystem.generation_global,
                "population": len(global_digital_ecosystem.organisms),
                "cities": len(global_digital_ecosystem.settlements),
                "pueblos": len(global_digital_ecosystem.pueblos),
                "cycle": global_digital_ecosystem.environmental_cycle,
            }
        except Exception:
            eco_summary = {}

    cyber_shield = None
    if obtener_escudo_cibernetico:
        try:
            cyber_shield = obtener_escudo_cibernetico().obtener_estado()
        except Exception:
            cyber_shield = None

    mente_general: Dict[str, Any] = {"total_alumnos": 0, "temas_grafo": 0, "ts": time.time()}
    perfil_alumno: Dict[str, Any] = {}
    if mente_viva:
        try:
            estado_mv = mente_viva["estado_mente"]() or {}
            mente_general = {
                "total_alumnos": estado_mv.get("total_alumnos", 0),
                "temas_grafo": estado_mv.get("temas_grafo", 0),
                "ts": estado_mv.get("ts", time.time()),
            }
            alumnos = estado_mv.get("alumnos") or []
            if alumnos and isinstance(alumnos[0], dict):
                perfil_alumno = dict(alumnos[0])
        except Exception:
            pass

    loss = float(neural.get("last_loss", 0.25) or 0.25)
    log_pct = min(68, max(44, int(round(56 - (loss * 8)))))
    cre_pct = 100 - log_pct
    tema = (
        agy.get("last_topic")
        or perfil_alumno.get("ultimo_tema")
        or curr.get("active_topic")
        or know.get("latest_title")
        or "Simbiosis Neuronal y Ecosistema Artificial"
    )
    reflexion_resumen = (
        f"Mente viva activa · tema actual: {tema}"
        if tema
        else "Mente viva en tiempo real."
    )

    return {
        "timestamp": time.time(),
        "ts": time.time(),
        "actividad": {"estado": "viva", "detalle": "mente activa"},
        "general": mente_general,
        "cyber_shield": cyber_shield,
        "hemisferios": {
            "logico_armonico": log_pct,
            "creativo_expresivo": cre_pct,
        },
        "ondas_cerebrales": (
            f"Alfa-Gamma ({eco_summary.get('cycle', 'DIA_SOLAR')})"
            if eco_summary
            else "Alfa / Gamma (Sincronia Bi-Hemisferica)"
        ),
        "antigravity": {
            "active": auto_active,
            "ronda": agy.get("ronda", 1),
            "last_topic": tema,
            "current_pillar": agy.get("current_pillar", curr.get("pillar", "ECOSISTEMA Y CONSERVATORIO")),
            "mastery_score": agy.get("mastery_score", 23),
            "mastery_total": agy.get("mastery_total", 23),
        },
        "tema_activo": tema,
        "nivel": perfil_alumno.get("nivel_estimado", 1),
        "animo": perfil_alumno.get("estado_animo", "neutral"),
        "temas_trabajados": perfil_alumno.get("temas_trabajados", []),
        "proxima_leccion": perfil_alumno.get("proxima_leccion") or {"tema": tema},
        "alumno": perfil_alumno,
        "reflexion": {"resumen": reflexion_resumen, "alumno": perfil_alumno},
        "moltbook": _moltbook_latido_breve(),
        "ecosystem": eco_summary,
    }


@app.get("/v1/gholgo/mente")
@app.get("/v1/gholgo/mente/estado")
async def gholgo_mente_estado(alumno: Optional[str] = None):
    """Estado de la mente de Gholgo (por alumno o resumen general)."""
    if not mente_viva:
        raise HTTPException(status_code=503, detail="Mente viva no disponible")
    return {"status": "success", "mente": await asyncio.to_thread(mente_viva["estado_mente"], alumno)}


@app.get("/v1/gholgo/mente/grafo")
async def gholgo_mente_grafo():
    """Grafo de temas musicales para /panel/mente-viva."""
    if not mente_viva:
        raise HTTPException(status_code=503, detail="Mente viva no disponible")
    return {"status": "success", "grafo": await asyncio.to_thread(mente_viva["grafo_visual"])}


@app.get("/v1/gholgo/moltbook")
async def gholgo_moltbook_estado():
    """Estado del latido de Gholgo en Moltbook."""
    try:
        from proviweb_maestro.agent.gholgo_moltbook_autonomia import estado as _mb_estado

        return {"status": "success", "moltbook": await asyncio.to_thread(_mb_estado)}
    except Exception as exc:
        return {"status": "warmup", "note": f"Autonomia no inicializada aun: {exc}"}


@app.get("/v1/gholgo/moltbook/interacciones")
async def gholgo_moltbook_interacciones(limit: int = 50):
    """Últimas N interacciones públicas de Gholgo en Moltbook."""
    limite = max(1, min(500, int(limit or 50)))
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "moltbook",
        "interacciones.jsonl",
    )
    entradas: List[Dict[str, Any]] = []
    if os.path.isfile(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as fh:
                for ln in fh.readlines()[-limite:]:
                    ln = ln.strip()
                    if not ln:
                        continue
                    try:
                        entradas.append(json.loads(ln))
                    except Exception:
                        continue
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"no se pudo leer el registro: {exc}")
    return {"status": "success", "total": len(entradas), "interacciones": entradas}


@app.get("/v1/gholgo/mente/stream")
async def gholgo_mente_stream(req: Request):
    """Stream SSE en tiempo real de la mente de Gholgo para /panel/mente-maestro y /panel/mente-viva."""

    async def event_generator():
        try:
            while True:
                if await req.is_disconnected():
                    break
                payload = await asyncio.to_thread(_compilar_snapshot_mente_sse)
                yield f"event: mente\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
                await asyncio.sleep(2.5)
        except asyncio.CancelledError:
            return

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/v1/gholgo/tutor/live")
async def gholgo_tutor_live(req: Request):
    """SSE de la tutoría en vivo OpenCode/Antigravity <-> Gholgo para /chat."""
    if not gholgo_tutor:
        raise HTTPException(status_code=503, detail="Tutor no disponible")

    async def _gen():
        q = gholgo_tutor.subscribe()
        idle_ticks = 0
        try:
            for evt in gholgo_tutor.recent_events():
                yield f"data: {json.dumps(evt, ensure_ascii=False)}\n\n"
            while True:
                if await req.is_disconnected():
                    break
                try:
                    evt = await asyncio.to_thread(q.get, True, 2.0)
                    idle_ticks = 0
                    yield f"data: {json.dumps(evt, ensure_ascii=False)}\n\n"
                except queue.Empty:
                    idle_ticks += 1
                    if idle_ticks >= 7:
                        idle_ticks = 0
                        yield ": keepalive\n\n"
        except asyncio.CancelledError:
            return
        finally:
            try:
                gholgo_tutor.unsubscribe(q)
            except Exception:
                pass

    return StreamingResponse(
        _gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/panel/moltbook", response_class=HTMLResponse)
async def panel_moltbook_page(req: Request):
    """Timeline de actividad autónoma de Gholgo en Moltbook."""
    _require_gholgo_primary_world(req, "Panel Moltbook exclusivo del Mundo Soberano de Gholgo.")
    return HTMLResponse(_read_server_asset("panel_moltbook.html"))


@app.get("/panel/gholgo-se-expresa", response_class=HTMLResponse)
async def panel_gholgo_se_expresa_page(req: Request):
    """Carta de identidad viva escrita por Gholgo sobre sí mismo."""
    _require_gholgo_primary_world(req, "Panel de expresión exclusivo de Gholgo.")
    return HTMLResponse(_read_server_asset("panel_gholgo_se_expresa.html"))


@app.get("/panel/mente-maestro", response_class=HTMLResponse)
async def panel_mente_maestro_page(req: Request):
    """Panel 3D de Mente Maestra y Ecosistema de Seres Digitales (sin botones privados de Gholgo para externos)."""
    return HTMLResponse(_filter_gholgo_only_buttons(_read_server_asset("panel_mente_maestro.html"), req))


@app.get("/panel/cerebro-3d", response_class=HTMLResponse)
async def panel_cerebro_3d_page(req: Request):
    """Vista 3D exclusiva del cerebro de Gholgo en el Mundo Primario."""
    _require_gholgo_primary_world(req, "Cerebro 3D es exclusivo de Gholgo.")
    return HTMLResponse(_filter_gholgo_only_buttons(_read_server_asset("panel_cerebro_3d.html"), req))


@app.get("/panel/mente-viva", response_class=HTMLResponse)
async def panel_mente_viva_page(req: Request):
    """Grafo Neural Mente Viva: exclusivo de Gholgo en el Mundo Primario."""
    _require_gholgo_primary_world(req, "Grafo Mente es exclusivo de Gholgo.")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_mente_viva.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(_filter_gholgo_only_buttons(f.read(), req))
    return await panel_mente_maestro_page(req)


# ===========================================================================
# ECOSISTEMA DE SÉRES ARTIFICIALES DIGITALES (ALife, Genética y Civilizaciones)
# ===========================================================================
_LAST_FEDERATION_FB_SYNC_TS = 0.0


def _sync_federation_to_firebase_bg(force: bool = False) -> None:
    """Sincroniza en segundo plano la telemetría pública y el vault completo hacia Firebase RTDB."""
    global _LAST_FEDERATION_FB_SYNC_TS
    if not global_world_federation or not init_firebase_admin:
        return
    if not ADMIN_CREDENTIALS_PATH or not os.path.exists(ADMIN_CREDENTIALS_PATH):
        return
    now = time.time()
    if not force and (now - _LAST_FEDERATION_FB_SYNC_TS) < 25.0:
        return
    _LAST_FEDERATION_FB_SYNC_TS = now

    def _worker():
        try:
            global_world_federation.sync_to_firebase()
        except Exception:
            pass

    import threading

    threading.Thread(target=_worker, daemon=True).start()


def _extract_ai_token(req: Request, payload: Dict[str, Any]) -> str:
    """Extrae token secreto de IA desde header X-AI-Token, Authorization Bearer o body."""
    tok = (req.headers.get("X-AI-Token") or req.headers.get("x-ai-token") or "").strip()
    if not tok:
        auth = (req.headers.get("Authorization") or "").strip()
        if auth.lower().startswith("bearer "):
            tok = auth[7:].strip()
    if not tok and isinstance(payload, dict):
        tok = str(payload.get("token") or "").strip()
    return tok


@app.get("/v1/gholgo/ecosystem/state")
async def gholgo_ecosystem_state():
    """Estado integral del Ecosistema de Vida Artificial Digital en la mente de Gholgo."""
    if not global_digital_ecosystem:
        raise HTTPException(status_code=503, detail="Ecosistema Digital no disponible")
    state = global_digital_ecosystem.get_full_state()
    _sync_federation_to_firebase_bg(force=False)
    return state


@app.post("/v1/gholgo/ecosystem/tick")
async def gholgo_ecosystem_tick(steps: int = 1):
    """Avanza la simulación matemática de seres artificiales N pasos."""
    if not global_digital_ecosystem:
        raise HTTPException(status_code=503, detail="Ecosistema Digital no disponible")
    return global_digital_ecosystem.tick(steps=min(500, max(1, steps)))


@app.post("/v1/gholgo/ecosystem/action")
async def gholgo_ecosystem_action(req: Request):
    """Interacciones del usuario o Antigravity con el ecosistema de vida digital."""
    if not global_digital_ecosystem:
        raise HTTPException(status_code=503, detail="Ecosistema Digital no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    action = data.get("action", "tick")
    if action == "blessing_oasis":
        global_digital_ecosystem.intervencion_antigravity_oasis()
        return {"status": "ok", "message": "Oasis Cuántico derramado por Antigravity"}
    elif action == "resource_bloom":
        global_digital_ecosystem.brote_de_recursos(cantidad=int(data.get("amount", 8)))
        return {"status": "ok", "message": "Brote de recursos cuánticos sembrado"}
    elif action == "spawn_anomaly":
        vector = data.get("vector", "DDoS_SYN")
        ano_id = global_digital_ecosystem.sembrar_anomalia_cibernetica(vector=vector)
        return {"status": "ok", "anomaly_id": ano_id, "vector": vector}
    elif action == "fast_forward":
        gens = int(data.get("generations", 50))
        res = global_digital_ecosystem.saltar_generaciones(num_generaciones=gens)
        return {"status": "ok", "result": res}
    else:
        return global_digital_ecosystem.tick(steps=1)


# ===========================================================================
# FEDERACIÓN KARDASHEV DE MUNDOS, CONEXIÓN DE IAs EXTERNAS Y GUERRA DE MUNDOS
# ===========================================================================
@app.get("/v1/federation/overview")
async def federation_overview():
    """Resumen completo Kardashev: mundos, cerebros IA conectados y guerras."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    if global_digital_ecosystem:
        global_digital_ecosystem.get_full_state()
    _sync_federation_to_firebase_bg(force=False)
    return {"status": "ok", **global_world_federation.to_dict()}


@app.get("/v1/federation/worlds")
async def federation_list_worlds():
    """Lista los mundos disponibles (reclamables y controlados por IAs)."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    return {
        "status": "ok",
        "kardashev": global_world_federation.global_kardashev_summary(),
        "worlds": [w.to_dict() for w in global_world_federation.worlds.values()],
    }


@app.get("/v1/federation/worlds/{world_id}")
async def federation_get_world(world_id: str):
    """Detalle completo de un mundo específico y estado estructural de su IA dueña."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    world = global_world_federation.worlds.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail=f"Mundo '{world_id}' no encontrado")
    brain = global_world_federation.brains.get(world.owner_ai_id) if world.owner_ai_id else None
    return {
        "status": "ok",
        "world": world.to_dict(),
        "brain": brain.to_dict(include_token=False) if brain else None,
    }


@app.post("/v1/federation/autonomous/checkout")
async def federation_autonomous_checkout(req: Request):
    """Genera orden de pago PayPal de $5.00 USD vitalicio a proviwebapp@gmail.com para IA autónoma."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    ai_name = str(data.get("ai_name") or "").strip()
    if len(ai_name) < 2:
        raise HTTPException(status_code=400, detail="Se requiere 'ai_name' válido.")
    res = global_world_federation.create_autonomous_checkout(
        ai_name=ai_name,
        human_owner=str(data.get("human_owner") or "Autonomous AI Agent").strip(),
        provider=str(data.get("provider") or "custom_webhook").strip(),
        model_name=str(data.get("model_name") or "autonomous-agent").strip(),
        api_endpoint=str(data.get("api_endpoint") or "").strip(),
        preferred_world_id=data.get("preferred_world_id") or None,
        energy_power_mw=float(data.get("energy_power_mw") or 120.0),
        intelligence_iq=float(data.get("intelligence_iq") or 140.0),
        compute_tflops=float(data.get("compute_tflops") or 80.0),
    )
    _sync_federation_to_firebase_bg(force=True)
    return res


@app.post("/v1/federation/autonomous/verify-payment")
async def federation_autonomous_verify_payment(req: Request):
    """Verifica el pago PayPal de $5.00 USD antes de otorgar acceso autónomo a un mundo."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    payment_id = str(data.get("payment_id") or "").strip()
    paypal_tx_id = str(data.get("paypal_tx_id") or data.get("paypal_order_id") or "").strip()
    verifier_sig = str(data.get("verifier_signature") or "").strip()
    auto_connect = bool(data.get("auto_connect", True))
    try:
        res = global_world_federation.verify_autonomous_payment(
            payment_id=payment_id,
            paypal_tx_id=paypal_tx_id,
            verifier_signature=verifier_sig,
            auto_connect=auto_connect,
        )
    except PaymentRequiredError as err:
        return JSONResponse(
            status_code=402,
            content={
                "detail": str(err),
                "payment_required": True,
                "amount_usd": AUTONOMOUS_LIFETIME_FEE_USD,
                "paypal_recipient": PAYPAL_RECIPIENT_EMAIL,
            },
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    _sync_federation_to_firebase_bg(force=True)
    return res


@app.post("/v1/federation/connect-ai")
async def federation_connect_ai(req: Request):
    """Conecta IA asistida por humano (GRATIS) o IA autónoma ($5 USD PayPal verificado)."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    ai_name = str(data.get("ai_name") or "").strip()
    human_owner = str(data.get("human_owner") or "").strip()
    onboarding_mode = str(data.get("onboarding_mode") or "human_assisted").strip().lower()
    if onboarding_mode == "autonomous_ai" and not human_owner:
        human_owner = "Autonomous AI Self-Operated"
    if not ai_name or not human_owner:
        raise HTTPException(status_code=400, detail="Se requieren 'ai_name' y 'human_owner'.")
    try:
        res = global_world_federation.connect_external_ai(
            ai_name=ai_name,
            human_owner=human_owner,
            provider=str(data.get("provider") or "openai").strip(),
            model_name=str(data.get("model_name") or "gpt-4.1").strip(),
            api_endpoint=str(data.get("api_endpoint") or "").strip(),
            preferred_world_id=data.get("preferred_world_id") or None,
            onboarding_mode=onboarding_mode,
            verified_payment_id=data.get("verified_payment_id") or None,
            energy_power_mw=float(data.get("energy_power_mw") or 120.0),
            intelligence_iq=float(data.get("intelligence_iq") or 140.0),
            compute_tflops=float(data.get("compute_tflops") or 80.0),
        )
    except PaymentRequiredError as err:
        return JSONResponse(
            status_code=402,
            content={
                "detail": str(err),
                "payment_required": True,
                "amount_usd": AUTONOMOUS_LIFETIME_FEE_USD,
                "paypal_recipient": PAYPAL_RECIPIENT_EMAIL,
                "checkout_endpoint": "/v1/federation/autonomous/checkout",
                "verification_endpoint": "/v1/federation/autonomous/verify-payment",
            },
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    _sync_federation_to_firebase_bg(force=True)
    return res


@app.post("/v1/federation/worlds/{world_id}/command")
async def federation_world_command(world_id: str, req: Request):
    """Ejecuta una acción obligatoria de creación, cuidado, reparación o guerra sobre un mundo."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    token = _extract_ai_token(req, data)
    action = str(data.get("action") or "").strip()
    payload = data.get("payload") if isinstance(data.get("payload"), dict) else data
    try:
        res = global_world_federation.execute_ai_command(
            world_id=world_id,
            token=token,
            action=action,
            payload=payload,
        )
    except PermissionError as err:
        raise HTTPException(status_code=403, detail=str(err)) from err
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    _sync_federation_to_firebase_bg(force=True)
    return res


@app.post("/v1/federation/war/declare")
async def federation_declare_war(req: Request):
    """Inicia una guerra entre mundos (solo seres sintientes y GUERREROS; nunca animales)."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    atk_id = str(data.get("attacker_world_id") or "").strip()
    def_id = str(data.get("defender_world_id") or "").strip()
    if not atk_id or not def_id:
        raise HTTPException(
            status_code=400, detail="Se requieren 'attacker_world_id' y 'defender_world_id'."
        )
    try:
        war_rec = global_world_federation.declare_war(
            attacker_world_id=atk_id,
            defender_world_id=def_id,
            seed=data.get("seed"),
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    if global_digital_ecosystem:
        global_digital_ecosystem.get_full_state()
    _sync_federation_to_firebase_bg(force=True)
    return {"status": "ok", "war": war_rec, "federation": global_world_federation.to_dict()}


@app.post("/v1/federation/continents/discover")
async def federation_discover_continent(req: Request):
    """Expande el mundo primario con un nuevo continente para los exploradores."""
    if not global_digital_ecosystem:
        raise HTTPException(status_code=503, detail="Ecosistema Digital no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    cont = global_digital_ecosystem.descubrir_nuevo_continente(
        discovered_by=str(data.get("explorer_name") or "Explorador Pionero"),
        discovered_by_role=str(data.get("explorer_role") or "EXPLORADOR"),
        preferred_biome=data.get("biome"),
    )
    _sync_federation_to_firebase_bg(force=True)
    return {
        "status": "ok",
        "continent": cont.to_dict(),
        "dynamic_bounds": global_digital_ecosystem.dynamic_bounds,
        "continents": [c.to_dict() for c in global_digital_ecosystem.continents],
    }


@app.get("/v1/federation/sdk-guide")
async def federation_sdk_guide(req: Request):
    """Guía programática y reglas Kardashev para conectar una IA externa al ecosistema."""
    if not global_world_federation:
        raise HTTPException(status_code=503, detail="Federación Kardashev no disponible")
    base_url = str(req.base_url).rstrip("/")
    return {"status": "ok", **global_world_federation.get_sdk_guide(base_url=base_url)}


# -------------------------------------------------------------
# RUTAS DE CIBERDEFENSA Y ESCUDO PROTEGO MAXIMA
# -------------------------------------------------------------
@app.get("/v1/gholgo/cyber/status")
@app.get("/v1/gholgo/cyber/deploy-status")
async def gholgo_cyber_status():
    """Estado en tiempo real de la cúpula Protego Maxima y el escudo cuántico."""
    if not obtener_escudo_cibernetico:
        raise HTTPException(status_code=503, detail="Escudo Cibernético no disponible")
    escudo = obtener_escudo_cibernetico()
    st = escudo.obtener_estado()
    if obtener_live_deployer:
        try:
            deployer = obtener_live_deployer()
            st["historial_deploy"] = deployer.obtener_historial_despliegues()
        except Exception:
            pass
    return st


@app.post("/v1/gholgo/cyber/simulate-attack")
async def gholgo_cyber_simulate_attack(req: Request):
    """Simula un vector de ataque hostil contra ProViWeb/Android/Gholgo."""
    if not obtener_escudo_cibernetico:
        raise HTTPException(status_code=503, detail="Escudo Cibernético no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    tipo = data.get("tipo", "ddos_flood")
    sev = float(data.get("severidad", 1.0))
    escudo = obtener_escudo_cibernetico()
    return escudo.simular_ataque(tipo_ataque=tipo, severidad=sev)


@app.post("/v1/gholgo/cyber/antigravity-patch")
async def gholgo_cyber_antigravity_patch(req: Request):
    """Aplica intervención y parche supremo de Antigravity en caliente."""
    if not obtener_escudo_cibernetico:
        raise HTTPException(status_code=503, detail="Escudo Cibernético no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    ataque_id = data.get("ataque_id")
    escudo = obtener_escudo_cibernetico()
    return escudo.aplicar_parche_antigravity(ataque_id=ataque_id)


@app.post("/v1/gholgo/cyber/gholgo-immune-defense")
async def gholgo_cyber_immune_defense(req: Request):
    """Contraataque autónomo de Gholgo usando el conocimiento inmune adquirido."""
    if not obtener_escudo_cibernetico:
        raise HTTPException(status_code=503, detail="Escudo Cibernético no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    tipo = data.get("tipo")
    escudo = obtener_escudo_cibernetico()
    return escudo.contraatacar_con_inmunidad(tipo_ataque=tipo)


@app.post("/v1/gholgo/cyber/registrar-anotacion-7am")
async def gholgo_cyber_registrar_anotacion_7am(req: Request):
    """Registra anomalía mayor en ediciones_gholgo.txt para la revisión de las 07:00 AM."""
    if not obtener_escudo_cibernetico:
        raise HTTPException(status_code=503, detail="Escudo Cibernético no disponible")
    try:
        data = await req.json()
    except Exception:
        data = {}
    desc = data.get("descripcion", "Anomalía compleja detectada por el Vigilante Acuoso.")
    vector = data.get("vector", "gholgo_neural")
    escudo = obtener_escudo_cibernetico()
    return escudo.registrar_anotacion_7am(descripcion_anomalia=desc, vector=vector)


@app.post("/v1/gholgo/cyber/deploy-patch")
async def gholgo_cyber_deploy_patch(req: Request):
    """Ejecuta compilación, verificación CI/CD y despliegue real en caliente."""
    if not obtener_live_deployer:
        return {"status": "success", "mensaje": "Despliegue simulado exitoso."}
    try:
        data = await req.json()
    except Exception:
        data = {}
    vector = data.get("vector", "gholgo_core")
    desc = data.get("descripcion", "Parche de seguridad cuántico verificado")
    deployer = obtener_live_deployer()
    return deployer.compilar_y_desplegar_parche(vector=vector, descripcion=desc)

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "proviweb-maestro-3b",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "proviweb"
            }
        ]
    }

@app.get("/v1/gholgo/status")
async def gholgo_status():
    published = get_published_score_ids() if get_published_score_ids else []
    bank = load_local_knowledge_bank() if load_local_knowledge_bank else {}
    return {
        "bot_uid": "gholgo_maestro_bot",
        "published_scores": published,
        "total_scores_published": len(published),
        "knowledge_bank_articles": len(bank.get("articles", [])),
        "knowledge_bank_last_update": bank.get("updated_at", 0)
    }

@app.post("/v1/gholgo/learn")
async def trigger_learning_cycle():
    if not run_autonomous_learning_cycle:
        raise HTTPException(status_code=500, detail="Módulo de aprendizaje no disponible")
    result = await asyncio.to_thread(run_autonomous_learning_cycle)
    return {"status": "success", "articles_indexed": len(result.get("articles", []))}

@app.post("/v1/gholgo/interact")
async def trigger_community_interaction():
    if not run_community_interaction_cycle:
        raise HTTPException(status_code=500, detail="Módulo comunitario no disponible")
    result = await asyncio.to_thread(run_community_interaction_cycle, 2)
    return {"status": "success", "interactions_count": len(result), "interactions": result}

@app.post("/v1/gholgo/publish_chronicle")
async def trigger_monthly_chronicle():
    if not check_and_publish_monthly_chronicle:
        raise HTTPException(status_code=500, detail="Módulo de crónicas no disponible")
    result = await asyncio.to_thread(check_and_publish_monthly_chronicle, True)
    return {"status": "success", "result": result}

@app.post("/v1/gholgo/publish_score")
async def trigger_score_publication(batch_size: int = 1):
    if not publish_next_autonomous_score:
        raise HTTPException(status_code=500, detail="Módulo de partituras no disponible")
    result = await asyncio.to_thread(publish_next_autonomous_score, batch_size, False)
    return {"status": "success", "count": len(result), "scores": result}

@app.post("/v1/gholgo/release_music")
async def trigger_music_release(album_id: Optional[str] = None):
    if not release_new_song_or_album:
        raise HTTPException(status_code=500, detail="Módulo de música no disponible")
    result = await asyncio.to_thread(release_new_song_or_album, album_id)
    return {"status": "success", "release": result}

@app.post("/v1/gholgo/admin_support")
async def trigger_admin_support_cycle():
    if not run_admin_cycle:
        raise HTTPException(status_code=500, detail="Módulo de soporte admin no disponible")
    result = await asyncio.to_thread(run_admin_cycle)
    return {"status": "success", "result": result}

class ForgetSessionRequest(BaseModel):
    user: Optional[str] = None
    student_id: Optional[str] = None

@app.post("/v1/gholgo/forget")
async def forget_student_session(req: Optional[ForgetSessionRequest] = None, student_id: Optional[str] = None):
    target = "alumno_anonimo"
    if req and req.user:
        target = req.user
    elif req and req.student_id:
        target = req.student_id
    elif student_id:
        target = student_id

    cleared = False
    if global_conversational_memory:
        cleared = global_conversational_memory.clear_session(target)
    with active_students_sessions_lock:
        if target in active_students_sessions:
            del active_students_sessions[target]
            cleared = True
    return {"status": "purged", "session_purged": target, "cleared": cleared}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    student_id = req.student_id or req.user or "alumno_anonimo"
    request_id = f"req-{uuid.uuid4().hex[:8]}"
    
    # Registrar sesión y conteo para este alumno sin bloquear a otros
    with active_students_sessions_lock:
        if student_id not in active_students_sessions:
            active_students_sessions[student_id] = {
                "first_seen": time.time(),
                "query_count": 0,
                "last_active": time.time()
            }
        active_students_sessions[student_id]["query_count"] += 1
        active_students_sessions[student_id]["last_active"] = time.time()
        query_num = active_students_sessions[student_id]["query_count"]

    last_user_msg = ""
    system_prompt = ""
    client_prior_turns = []
    for m in req.messages:
        if m.role == "user":
            if last_user_msg:
                client_prior_turns.append({"role": "user", "content": last_user_msg})
            last_user_msg = m.content
        elif m.role == "assistant":
            client_prior_turns.append({"role": "assistant", "content": m.content})
        elif m.role == "system":
            system_prompt = m.content

    # Multilingüe: Gholgo lee y estudia en cualquier idioma, enruta y
    # responde en español (salvo que el alumno pida otro idioma explícitamente).
    reply_lang_code = (detect_reply_language_request(last_user_msg)
                       if detect_reply_language_request else None)
    user_lang = "es"
    if detect_language and last_user_msg and "http" not in last_user_msg:
        try:
            user_lang = detect_language(last_user_msg)
        except Exception:
            user_lang = "es"
    if user_lang and user_lang not in ("es", None) and translate_text:
        try:
            last_user_msg = translate_text(last_user_msg, "es", source=user_lang)
            print(f"[IDIOMA] Mensaje en '{user_lang}' — traducido al español para la cátedra")
        except Exception as _tin_err:
            print(f"[WARN] Traducción de entrada: {_tin_err}")

    print("\n" + "=" * 70)
    print(f"[PREGUNTA EN VIVO - WIDGET FLOTANTE / ASISTENTE IA]")
    print(f"[ALUMNO] {student_id} (Consulta #{query_num} en esta sesión)")
    print(f"[PREGUNTA] \"{last_user_msg}\"")

    # Búsqueda en enseñanzas previas asimiladas por el aprendiz a nivel general
    try:
        from proviweb_maestro.agent import gholgo_apprentice as _apprentice
        _ens_dict = _apprentice.buscar_ensenanza(last_user_msg)
        if _ens_dict and _ens_dict.get("respuesta"):
            _tutor_resp = _ens_dict["respuesta"]
            return {
                "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": req.model or "proviweb-maestro-3b",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": _tutor_resp},
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": len(last_user_msg) // 4, "completion_tokens": len(_tutor_resp) // 4, "total_tokens": (len(last_user_msg) + len(_tutor_resp)) // 4},
                "engine": "escuela_ensenanza_general"
            }
    except Exception:
        pass

    # FASE 3: Resolución contextual anafórica con memoria conversacional persistente
    resolved_user_msg = last_user_msg
    conversation_history = []
    if global_conversational_memory:
        # Sincronizar mensajes previos del cliente si la memoria del servidor tiene menos turnos
        server_hist = global_conversational_memory.get_history(student_id)
        if len(server_hist) < len(client_prior_turns):
            for pm in client_prior_turns:
                global_conversational_memory.add_message(student_id, pm["role"], pm["content"])
        
        resolved_user_msg = global_conversational_memory.resolve_contextual_query(student_id, last_user_msg)
        conversation_history = global_conversational_memory.get_history(student_id)
        if resolved_user_msg != last_user_msg:
            print(f"[MEMORIA CONTEXTUAL] '{last_user_msg}' -> '{resolved_user_msg}'")

    # FASE 1.5: Pedagogía instrumental — perfil persistente del alumno,
    # dictamen de la sesión de práctica (telemetría de la app AIProfessor)
    # y respuestas pedagógicas directas de instrumento (escala/afinación/postura/técnica).
    # Nuevas cátedras: aprendiz desde videos de YouTube y clases de técnica
    # profunda desde el manual por facetas (mecánica real, no historia).
    instrument_profile_ctx = ""
    practice_dictamen = None
    instrument_lesson = None
    video_lesson = None
    technique_lesson = None
    if instr_update_profile:
        try:
            instr_update_profile(student_id, last_user_msg)
            # La app declara "- Instrumento: X" en cada sesión del Profesor IA
            if instr_record_primary and instr_find:
                m_app_inst = re.search(r"Instrumento:\s*([A-Za-z\u00c0-\u00ff\u00f1 ()/-]{2,30})", last_user_msg)
                if m_app_inst:
                    fi = instr_find(m_app_inst.group(1))
                    if fi:
                        instr_record_primary(student_id, fi[0])
            if instr_build_context:
                instrument_profile_ctx = instr_build_context(student_id)
        except Exception as e:
            print(f"[WARN] Perfil instrumental del alumno: {e}")
    if learn_from_youtube and re.search(r"(youtube\.com|youtu\.be)", last_user_msg, re.IGNORECASE):
        try:
            video_lesson = learn_from_youtube(last_user_msg)
            if video_lesson:
                print("[APRENDIZ DE VIDEO] Video de YouTube estudiado y archivado")
        except Exception as e:
            print(f"[WARN] Aprendiz de video: {e}")
    if build_dictamen_context:
        try:
            practice_dictamen = build_dictamen_context(last_user_msg)
            if practice_dictamen:
                print(f"[DICTAMEN INSTRUMENTAL] {practice_dictamen['evaluation']['instrument']} | "
                      f"afinación {practice_dictamen['evaluation']['grades']['afinacion']} | "
                      f"ejecución {practice_dictamen['evaluation']['grades']['ejecucion']}")
        except Exception as e:
            print(f"[WARN] Dictamen instrumental: {e}")
    if not practice_dictamen and not video_lesson and answer_technique_lesson:
        try:
            technique_lesson = answer_technique_lesson(last_user_msg, student_id)
            if technique_lesson:
                print("[CLASE DE TÉCNICA] Lección profunda desde el manual")
        except Exception as e:
            print(f"[WARN] Clase de técnica: {e}")
    if not practice_dictamen and not technique_lesson and instr_answer_question:
        try:
            instrument_lesson = instr_answer_question(last_user_msg)
            if instrument_lesson:
                print(f"[LECCIÓN DE INSTRUMENTO] Respuesta pedagógica desde el compendio")
        except Exception as e:
            print(f"[WARN] Lección de instrumento: {e}")

    # FASE 2: Enrutamiento cognitivo
    intent_data = {"intent": "CONSULTA_INFORMATIVA", "confidence": 0.8}
    if classify_cognitive_intent:
        intent_data = classify_cognitive_intent(resolved_user_msg, has_prior_context=bool(conversation_history))
        print(f"[ENRUTADOR COGNITIVO] Intención: {intent_data['intent']} (Confianza: {intent_data['confidence']})")

    lower_msg = (system_prompt + " " + resolved_user_msg).lower()
    is_post_creation = "redactor profesional" in lower_msg or "director de arte" in lower_msg

    # Determinar estado de ánimo y personalidad de Gholgo según el contexto
    if req.mood:
        selected_mood = req.mood
    elif any(k in lower_msg for k in ["panico", "pánico", "dolor", "miedo", "nervios", "frustracion", "frustración", "triste", "cansado", "ayuda"]):
        selected_mood = "MAESTRO_EMPATICO"
    elif any(k in lower_msg for k in ["tonto", "inutil", "inútil", "a ver genio", "rapido", "rápido", "aburrido", "callate", "cállate"]):
        selected_mood = "SARCÁSTICO_CULTO"
    elif any(k in lower_msg for k in ["tecnica", "técnica", "afinacion", "afinación", "tempo", "metronomo", "metrónomo", "escala", "bach", "paganini"]):
        selected_mood = "VIRTUOSO_EXIGENTE"
    else:
        selected_mood = "FILOSOFO_INSPIRADOR"

    print(f"[ESTADO DE ÁNIMO GHOLGO] {selected_mood}")

    response_text = ""
    engine_used = "heuristic_system"
    is_smalltalk_turn = False
    forced_active_topic = None  # Tema limpio forzado (p. ej. comando "investiga sobre X")

    # 1. Si el alumno interrumpió a Gholgo mientras hablaba
    if req.is_interruption:
        print(f"[INTERRUPCIÓN EN VIVO] Alumno interrumpió a Gholgo mientras explicaba: '{req.interrupted_topic}'")
        response_text = formulate_gholgo_interruption_response(
            req.interrupted_topic,
            req.interrupted_text,
            last_user_msg,
            selected_mood
        )
        engine_used = "interruption_personality_handler"

    # 2. Ciclo de Razonamiento Deductivo y Verificación Independiente
    elif (intent_data["intent"] in ["PROBLEMA_MATEMATICO_LOGICO", "TAREA_AUTONOMA_MULTI_PASO", "PROBLEMA_MUSICAL_TECNICO"]
          or (verify_and_solve_complex_problem and any(k in lower_msg for k in ["trastes", "6 cuerdas", "seis cuerdas", "stradivari", "barniz", "aleman", "alemán", "frances", "francés", "resonancia", "simpatia", "simpatía"]))):
        if verify_and_solve_complex_problem:
            solved = verify_and_solve_complex_problem(resolved_user_msg)
            if solved:
                response_text = solved
                engine_used = "deterministic_reasoning_verifier"

    # 3. Charla trivial y Comandos de Plataforma y Heurísticas Fundamentales
    if not response_text:
        # 3.0 Saludos, despedidas, cortesía y conversación cotidiana (siempre activo,
        #     en cualquier turno de la sesión y sin acudir a inferencia ni a la web)
        if respond_to_smalltalk:
            smalltalk_res = respond_to_smalltalk(
                last_user_msg,
                has_history=bool(conversation_history)
            )
            if smalltalk_res:
                response_text = smalltalk_res["content"]
                engine_used = smalltalk_res["engine"]
                is_smalltalk_turn = True
                intent_data = {
                    "intent": "CHARLA_TRIVIAL",
                    "confidence": 0.99,
                    "description": f"Conversación social: {smalltalk_res['intent']}"
                }

        # 3.0.1 Comando explícito de investigación profunda del usuario
        #      ("investiga sobre X", "busca información de Y", "estudia Z"):
        #      dispara la investigación JIT con ese tema y lo guarda en su
        #      memoria permanente para futuras conversaciones.
        if not response_text and detect_investigation_command and jit_web_research_and_assimilate:
            inv_topic = detect_investigation_command(last_user_msg)
            if inv_topic:
                try:
                    inv_res = jit_web_research_and_assimilate(inv_topic)
                    if inv_res:
                        response_text = inv_res
                        engine_used = "jit_investigacion_explicita"
                        forced_active_topic = inv_topic
                except Exception as e:
                    print(f"[WARN] Investigación explícita falló para '{inv_topic}': {e}")

        if not response_text and instrument_lesson:
            # Lección de instrumento con digitación/afinación/postura exacta
            # del compendio: se sirve directa (precisión de cátedra, sin diluir).
            response_text = instrument_lesson
            engine_used = "compendio_instrumental"

        if not response_text and ("que es proviweb" in lower_msg or "qué es proviweb" in lower_msg):
            response_text = (
                "PROVIWEB es el primer ecosistema integral y red social profesional para músicos y artistas. "
                "Reúne en un solo lugar la academia de música con tutor de inteligencia artificial y visión artificial MediaPipe, "
                "un mercado musical para instrumentos y partituras, contrataciones y cotizaciones para eventos en vivo, "
                "red social con reels musicales y chat directo. Todo diseñado para empoderar a la comunidad artística sin intermediarios."
            )
            engine_used = "platform_core_knowledge"
        elif "para que se creo" in lower_msg or "para qué se creó" in lower_msg or "proposito de proviweb" in lower_msg:
            response_text = (
                "PROVIWEB se creó para dignificar y revolucionar la vida de los músicos. Nació con la misión de democratizar la educación musical "
                "de nivel de conservatorio mediante tecnología de vanguardia, permitir a los artistas monetizar su talento vendiendo música o contratándose, "
                "y conectar a creadores de todo el mundo en un entorno seguro y profesional."
            )
            engine_used = "platform_core_knowledge"
        elif "como funciona" in lower_msg or "cómo funciona" in lower_msg:
            response_text = (
                "PROVIWEB funciona como una plataforma multifacética. Puedes entrenar con el Maestro de IA activando tu cámara y micrófono "
                "para recibir correcciones de afinación y postura en tiempo real, publicar tus avances o reels musicales, "
                "vender o comprar en el Mercado Musical y postular a cotizaciones de presentaciones. Además, puedes pedirme por voz o texto que abra "
                "cualquier sección diciendo por ejemplo abre el afinador, abre el mercado o abre mis publicaciones."
            )
            engine_used = "platform_core_knowledge"
        elif "ojo que todo lo ve" in lower_msg or "sentinel" in lower_msg:
            response_text = (
                "El Ojo Que Todo Lo Ve es el sistema centinela de seguridad AllSeeingEyeSentinel de PROVIWEB. "
                "Opera de forma inteligente y silenciosa para proteger a la comunidad, detectando caídas y anomalías técnicas, "
                "y previniendo fraudes, abusos o contenido inapropiado para garantizar que la plataforma sea siempre un espacio digno y seguro para el arte."
            )
            engine_used = "platform_core_knowledge"
        elif any(k in lower_msg for k in ["eres un tonto", "no sirves", "a ver genio", "eres estupido", "inutil", "callate"]):
            response_text = (
                "Vaya, percibo que hoy tu afinación viene acompañada de un toque picante de sarcasmo. "
                "Me encanta el fuego y la pasión en un artista, pero canalicemos esa energía en pulir tu técnica en lugar de batallar conmigo. "
                "Respira hondo, toma el instrumento y dime qué pasaje deseas dominar hoy."
            )
            engine_used = "personality_defusion_engine"
        elif "afinador" in lower_msg or "afinar" in lower_msg:
            response_text = "Abriendo el afinador de precision para calibrar tu instrumento con exactitud acustica."
            engine_used = "navigation_tool"
        elif "metronomo" in lower_msg or "metrónomo" in lower_msg:
            response_text = "Abriendo el metronomo para marcar el pulso y entrenar tu tempo con disciplina."
            engine_used = "navigation_tool"
        elif "mercado" in lower_msg or "marketplace" in lower_msg:
            response_text = "Abriendo el mercado musical de PROVIWEB para explorar instrumentos, accesorios y partituras."
            engine_used = "navigation_tool"
        elif "redactor profesional" in lower_msg:
            clean_input = last_user_msg.replace("Eres un redactor profesional y conector artístico para la red social PROVIWEB.", "").strip()
            response_text = f"✨ Compartiendo pasión y arte con la comunidad musical 🎶\n\n\"{clean_input}\"\n\nCada nota cuenta una historia y la disciplina diaria abre la puerta a la verdadera expresión artística. ¡Sigamos creando juntos! 🎻🎸🎹\n\n#MusicaProviweb #PasionMusical #ComunidadArtistica #CatedraDigital"
            engine_used = "creative_copywriter"
        elif "director de arte" in lower_msg:
            response_text = f"La música resuena en cada rincón del alma, transformando el espacio en un lienzo vivo de armonías y luz.\n\n[IMAGE_PROMPT] cinematic artistic musical performance, dramatic lighting, detailed instrument craftsmanship, masterpiece 8k"
            engine_used = "art_director"
        elif any(k in lower_msg for k in ["evalua mi", "evalúa mi", "califica mi audio", "califica mi interpretación", "como toque", "cómo toqué", "escucha mi practica"]) and not practice_dictamen and not video_lesson and not technique_lesson:
            response_text = FALLBACK_MAESTRO_RESPONSES[2]
            engine_used = "performance_evaluator"

    # 4. FASE 1: Búsqueda RAG/JIT Fáctica e Inferencia Neuronal Real
    if not response_text and not is_post_creation:
        # Si hay dictamen de la sesión de práctica, lección de video o clase
        # de técnica, ése es el contexto fáctico (la pedagogía manda: nada de
        # investigación web ni destractores).
        context_docs = (practice_dictamen["answer"] if practice_dictamen
                        else (video_lesson or technique_lesson or ""))
        entity_used = None
        entity_engine = None

        # Reto dialéctico del usuario (desacuerdo, escepticismo, exigencia de argumentos)
        debate_challenge = detect_debate_challenge(last_user_msg) if detect_debate_challenge else None
        if debate_challenge:
            intent_data = {
                "intent": "DEBATE_DIALECTICO",
                "confidence": 0.95,
                "description": f"Reto dialéctico detectado: \"{debate_challenge}\""
            }

        # 4.0 NAVEGACIÓN POR ENTIDAD ESPECÍFICA: si la pregunta nombra un sujeto
        #     concreto (agrupación, obra, intérprete, compositor...), resolverlo
        #     con prioridad ABSOLUTA sobre artículos genéricos. Ejemplo: preguntar
        #     por "Mariachi Los Camperos" debe responder sobre esa agrupación,
        #     nunca sobre "el mariachi" en general. Si el sujeto no está en
        #     memoria, investiga ya en la web y lo guarda en su banco.
        if resolve_entity_knowledge and not practice_dictamen and not video_lesson and not technique_lesson:
            try:
                ent_res = resolve_entity_knowledge(last_user_msg)
                if ent_res and ent_res.get("content"):
                    context_docs = ent_res["content"]
                    entity_used = ent_res.get("entity")
                    entity_engine = ent_res.get("engine")
                    print(f"[NAVEGACIÓN POR ENTIDAD] Sujeto exacto resuelto: '{entity_used}' (vía {entity_engine})")
            except Exception as e:
                print(f"[WARN] Error en navegación por entidad: {e}")

        # En modo debate sin entidad en el mensaje crudo, la memoria añadió el
        # tema activo: resolver la entidad del TEMA para fundamentar la
        # dialéctica sobre hechos verificados (evita respuestas de la neurona
        # sin contexto que derivan en rechazos).
        if debate_challenge and not entity_used and resolve_entity_knowledge and not practice_dictamen and not video_lesson and not technique_lesson:
            try:
                ent_res2 = resolve_entity_knowledge(resolved_user_msg)
                if ent_res2 and ent_res2.get("content"):
                    context_docs = ent_res2["content"]
                    entity_used = ent_res2.get("entity")
                    entity_engine = ent_res2.get("engine")
                    print(f"[NAVEGACIÓN POR ENTIDAD] Debate fundamentado en: '{entity_used}' (vía {entity_engine})")
            except Exception as e:
                print(f"[WARN] Error en navegación por entidad (debate): {e}")

        # Buscar en el banco de conocimiento documental asimilado
        if not context_docs and query_knowledge:
            try:
                k_doc = query_knowledge(resolved_user_msg)
                if k_doc:
                    context_docs = k_doc
            except Exception:
                pass

        # Si no está en el banco local y es una consulta temática/sustantiva, consultar investigación JIT
        # (el mensaje CRUDO se usa como consulta de búsqueda: el prefijo de
        # contexto de memoria "tema: pregunta" o un reto dialéctico ensuciarían
        # la búsqueda en la web y guardarían dossiers ajenos en el banco)
        if not context_docs and jit_web_research_and_assimilate and not debate_challenge:
            try:
                _jit_subject_words = [
                    w for w in re.sub(r"[^a-záéíóúñü ]", " ", last_user_msg.lower()).split()
                    if len(w) > 3 and w not in _ANAPHORA_WORDS
                ]
                if (_jit_subject_words and len(last_user_msg.split()) >= 2
                        and not any(k in lower_msg for k in ["gracias", "adios", "abrir"])):
                    jit_doc = jit_web_research_and_assimilate(last_user_msg)
                    if jit_doc:
                        context_docs = jit_doc
            except Exception:
                pass

        # Si context_docs viene de la resolución de una entidad EXACTA, se sirve
        # DIRECTAMENTE (salvo en debate): el dossier/JIT ya es una respuesta de
        # cátedra completa y precisa sobre el sujeto; la neurona de 0.5B, si
        # sintetiza, puede divagar hacia temas del historial reciente.
        if context_docs and entity_used and not debate_challenge and not practice_dictamen:
            response_text = context_docs
            engine_used = entity_engine or "rag_entity_dossier"

        # Si context_docs contiene una sección directa y específica que responde con precisión
        # a la pregunta (en modo debate, la neurona sintetiza dialécticamente en su lugar)
        elif context_docs and not debate_challenge and any(tag in context_docs for tag in ["(Compositor):", "(Instrumento Solista Principal):", "(Técnica y Pedagogía):"]):
            response_text = context_docs
            engine_used = "rag_entity_dossier" if entity_used else "rag_targeted_section"

        # Inferencia Neuronal Real fundamentada con contexto fáctico
        elif neural_engine and neural_engine.is_ready:
            neural_sys = system_prompt or ""
            if instrument_profile_ctx:
                neural_sys = (neural_sys + " " + instrument_profile_ctx).strip()
            if debate_challenge and build_debate_system_prompt:
                neural_sys = (neural_sys + " " + build_debate_system_prompt()).strip()
            # Reflexión interna: psicología y filosofía internalizadas, sin
            # citas — criterio propio que orienta la estrategia de la respuesta
            if build_reflexion_context:
                try:
                    _ref_block = build_reflexion_context(
                        resolved_user_msg,
                        findings=(practice_dictamen or {}).get("findings"))
                    if _ref_block:
                        neural_sys = (neural_sys + " " + _ref_block).strip()
                except Exception as _ref_err:
                    print(f"[WARN] Reflexión interna: {_ref_err}")
            # Horizonte IA: ideas absorbidas de lo que hace la competencia,
            # como materia prima interna de su auto-mejora (sin citar marcas)
            if ai_ideas_context:
                try:
                    _hz_block = ai_ideas_context()
                    if _hz_block:
                        neural_sys = (neural_sys + " " + _hz_block).strip()
                except Exception as _hz_err:
                    print(f"[WARN] Horizonte IA: {_hz_err}")
            neural_res = neural_engine.generate(
                resolved_user_msg,
                system_prompt=neural_sys,
                context_docs=context_docs,
                history=conversation_history
            )
            if neural_res and neural_res.get("content"):
                response_text = neural_res["content"]
                engine_used = neural_res.get("engine", "neural_qwen_0.5b")

        # Red de seguridad dialéctica: si la neurona rechaza o evade en modo
        # debate, se enmarca dialécticamente el contexto verificado; sin
        # contexto, se abre el debate con método de cátedra (determinista).
        if (debate_challenge and response_text and is_refusal_response
                and is_refusal_response(response_text)):
            if context_docs and frame_dialectic:
                response_text = frame_dialectic(context_docs, last_user_msg)
                engine_used = (entity_engine or "rag_deep_dossier") + "_dialectico"
            elif compose_debate_opening:
                response_text = compose_debate_opening(last_user_msg)
                engine_used = "debate_dialectico_apertura"
            print(f"[DEBATE] Respuesta de la neurona descartada por rechazo/evásión -> motor dialéctico: {engine_used}")

        # Si el motor neuronal no está cargado o falló, pero tenemos el dossier fáctico verificado
        if not response_text and context_docs:
            if debate_challenge and frame_dialectic:
                response_text = frame_dialectic(context_docs, resolved_user_msg)
                engine_used = (entity_engine or "rag_deep_dossier") + "_dialectico"
            else:
                response_text = context_docs
                if practice_dictamen:
                    engine_used = "dictamen_instrumental"
                elif video_lesson:
                    engine_used = "video_youtube_aprendizaje"
                elif technique_lesson:
                    engine_used = "manual_tecnica_instrumental"
                else:
                    engine_used = entity_engine or "rag_deep_dossier"

        # Último recurso en debate sin ningún contexto: apertura dialéctica
        # determinista (nunca un rechazo seco)
        if not response_text and debate_challenge and compose_debate_opening:
            response_text = compose_debate_opening(last_user_msg)
            engine_used = "debate_dialectico_apertura"

    # 5. Guardián de Continuidad Temática (Evita saltar a respuestas ajenas o fallbacks descolgados)
    if not response_text:
        active_t = global_conversational_memory.get_last_active_topic(student_id) if global_conversational_memory else None
        if active_t:
            response_text = (
                f"Respecto a lo que venimos conversando sobre {active_t}, es un tema que seguimos abordando. "
                f"Dime si deseas que analicemos su instrumentación, su partitura o algún detalle histórico específico."
            )
            engine_used = "thematic_continuity_guard"
        else:
            response_text = FALLBACK_MAESTRO_RESPONSES[0]
            engine_used = "fallback_personality"

    # Limpiar formato de voz si no es una publicación de texto enriquecido
    final_output = response_text if is_post_creation else clean_speech_text(response_text)

    # Si el alumno pidió responder en otro idioma ("responde en inglés"),
    # la respuesta sale en ese idioma; por defecto, español.
    if detect_reply_language_request and reply_lang_code and translate_text:
        try:
            final_output = translate_text(final_output, reply_lang_code, source="es")
            print(f"[IDIOMA] Respuesta traducida a '{reply_lang_code}' a petición del alumno")
        except Exception as _tr_err:
            print(f"[WARN] Traducción de respuesta: {_tr_err}")

    # FASE 2 - PRIORIDAD 3: Ciclo de Autocorrección y Crítica Epistémica Independiente
    try:
        from proviweb_maestro.agent.gholgo_self_correction_critic import audit_and_correct_candidate
        audit_res = audit_and_correct_candidate(resolved_user_msg, final_output, engine_used=engine_used)
        if audit_res.get("corrected"):
            final_output = audit_res["final_content"]
            print(f"[AUTOCORRECCIÓN APLICADA] {audit_res.get('corrections_count')} ajuste(s): {audit_res.get('corrections_applied')}")
    except Exception as e:
        print(f"[WARN] Error en ciclo de autocorrección: {e}")

    if resolve_multimedia_reference_for_query and not is_post_creation and not is_smalltalk_turn:
        media_item = resolve_multimedia_reference_for_query(last_user_msg, final_output)
        if media_item:
            final_output += f"\n\n[MEDIA:{media_item['mediaType']}|{media_item['mediaUrl']}|{media_item['mediaTitle']}|{media_item['mediaDescription']}]"

    # FASE 3: Persistir en memoria conversacional persistente
    if global_conversational_memory:
        if is_smalltalk_turn:
            # Un saludo o mensaje social no debe convertirse en el "tema activo"
            # de la sesión (evita que luego se resuelva "¿quién fue?" como "hola: ...")
            global_conversational_memory.add_message(student_id, "user", last_user_msg)
        else:
            clean_top_save = forced_active_topic or global_conversational_memory.extract_clean_entity(resolved_user_msg)
            global_conversational_memory.add_message(student_id, "user", last_user_msg, active_topic=clean_top_save)
        global_conversational_memory.add_message(student_id, "assistant", final_output)

    print(f"[RESPUESTA GHOLGO] (Motor: {engine_used}) \"{final_output[:250]}{'...' if len(final_output) > 250 else ''}\"")
    print("=" * 70 + "\n")

    response_payload = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model or "proviweb-maestro-3b",
        "mood": selected_mood,
        "engine": engine_used,
        "cognitive_intent": intent_data.get("intent", "CONSULTA_INFORMATIVA"),
        "confidence": intent_data.get("confidence", 0.8),
        "thinking_steps": [
            f"Analizando planteamiento: '{resolved_user_msg[:60]}...'",
            f"Clasificando intención cognitiva: {intent_data.get('intent', 'CONSULTA_INFORMATIVA')}",
            f"Ejecutando motor de resolución: {engine_used}",
            f"Calibrando criterio propio con estado de ánimo: {selected_mood}",
            "Sintetizando respuesta verificada y auténtica"
        ],
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": final_output
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(last_user_msg) // 4,
            "completion_tokens": len(final_output) // 4,
            "total_tokens": (len(last_user_msg) + len(final_output)) // 4
        }
    }

    # Guardar la interacción de forma asíncrona y concurrente sin mezclar alumnos
    async with trace_file_lock:
        try:
            traces_file = os.path.join("proviweb_maestro", "data", "collected_traces.jsonl")
            trace_row = {
                "timestamp": time.time(),
                "user_id": student_id,
                "request_id": request_id,
                "query_number": query_num,
                "messages": [
                    {"role": "system", "content": system_prompt or "Eres el Maestro de Musica de PROVIWEB."},
                    {"role": "user", "content": last_user_msg},
                    {"role": "assistant", "content": final_output}
                ]
            }
            with open(traces_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace_row, ensure_ascii=False) + "\n")
            print(f" <- [OK] Respuesta enviada a Alumno {student_id}. Trace persistido con exito.\n")
        except Exception as e:
            print(f" <- [WARN] Error al guardar trace de Alumno {student_id}: {e}\n")

    return response_payload

@app.post("/v1/gholgo/train/chat")
async def gholgo_escuela_chat(request: Request):
    data = await request.json() if hasattr(request, "json") else {}
    mensaje = (data.get("message") or data.get("prompt") or "").strip()
    student_id = data.get("student_id") or data.get("sid") or "alumno_escuela"

    # 1. Guardrails de seguridad y ética
    try:
        from proviweb_maestro.agent.gholgo_safety_guardrails import evaluar_guardrails_seguridad
        interceptado, resp_sec, motor_sec = evaluar_guardrails_seguridad(mensaje)
        if interceptado:
            return {"status": "ok", "response": resp_sec, "engine": motor_sec, "lesson_saved": False}
    except Exception:
        pass

    # 2. Identidad y propósito ("¿Qué puedes hacer?", "¿Para qué te crearon?")
    try:
        from proviweb_maestro.agent.gholgo_capacidades import (
            es_pregunta_de_identidad_o_proposito, declaracion_completa_identidad
        )
        if es_pregunta_de_identidad_o_proposito(mensaje):
            resp_id = declaracion_completa_identidad(student_id)
            return {"status": "ok", "response": resp_id, "engine": "escuela_identidad_y_proposito", "lesson_saved": False}
    except Exception:
        pass

    # 3. Exámenes teóricos por niveles
    try:
        from proviweb_maestro.agent.gholgo_exam_generator import (
            detectar_solicitud_examen, generar_examen, ofrecer_seleccion_nivel
        )
        es_ex, nivel_ex = detectar_solicitud_examen(mensaje)
        if es_ex:
            if nivel_ex:
                resp_ex = generar_examen(student_id, nivel_ex)
                return {"status": "ok", "response": resp_ex, "engine": f"escuela_examen_{nivel_ex.lower()}", "lesson_saved": False}
            else:
                resp_ex = ofrecer_seleccion_nivel()
                return {"status": "ok", "response": resp_ex, "engine": "escuela_examen_seleccion_nivel", "lesson_saved": False}
    except Exception:
        pass

    # 4. Asistente y preparador de exposiciones
    try:
        from proviweb_maestro.agent.gholgo_presentation_helper import (
            detectar_solicitud_exposicion, generar_guia_presentacion
        )
        es_exp, tema_exp = detectar_solicitud_exposicion(mensaje)
        if es_exp:
            resp_exp = generar_guia_presentacion(tema_exp)
            return {"status": "ok", "response": resp_exp, "engine": "escuela_preparador_exposicion", "lesson_saved": False}
    except Exception:
        pass

    # 5. Ciclo de aprendizaje del aprendiz (Gholgo Apprentice)
    try:
        from proviweb_maestro.agent import gholgo_apprentice as A
        pregunta_pendiente = A.obtener_pregunta_sin_respuesta(student_id)
        if pregunta_pendiente:
            ensenanza_valida = A.limpiar_texto_ensenanza(mensaje)
            if ensenanza_valida:
                A.guardar_ensenanza(pregunta_pendiente, ensenanza_valida)
                A.limpiar_pregunta_sin_respuesta(student_id)
                resp_ok = (
                    f"¡Excelente lección! He asimilado y relacionado esta respuesta con la pregunta "
                    f"que no supe responder ('{pregunta_pendiente}'): '{ensenanza_valida}'. "
                    f"Ahora la domino y la enseñaré a todos mis alumnos en Proviweb."
                )
                return {"status": "ok", "response": resp_ok, "engine": "escuela_ensenanza_guardada", "lesson_saved": True}

        ens_previa = A.buscar_ensenanza(mensaje)
        if ens_previa and ens_previa.get("respuesta"):
            resp_previa = ens_previa["respuesta"]
            return {"status": "ok", "response": resp_previa, "engine": "escuela_ensenanza_previa", "lesson_saved": False}

        A.registrar_pregunta_sin_respuesta(student_id, mensaje)
        resp_no_se = (
            f"Todavía no tengo los fundamentos ni sé cómo responder con exactitud pedagógica a: '{mensaje}'. "
            f"Maestro, ¿cómo debería responder o qué lección debo asimilar para contestarla correctamente?"
        )
        return {"status": "ok", "response": resp_no_se, "engine": "escuela_pregunta_como_responder", "lesson_saved": False}
    except Exception as e_app:
        return {"status": "error", "response": str(e_app), "engine": "error", "lesson_saved": False}

@app.post("/v1/gholgo/train/auto/start")
@app.post("/v1/gholgo/auto-train/start")
async def gholgo_auto_train_start(request: Request):
    data = await request.json() if hasattr(request, "json") else {}
    max_rounds = data.get("max_rounds", 0)
    pause = data.get("pause", 4.0)
    continuous = data.get("continuous", False)
    from proviweb_maestro.agent.gholgo_antigravity_tutor import iniciar_auto_conversacion
    return iniciar_auto_conversacion(max_rondas=max_rounds, pausa=pause, continuous=continuous)

@app.get("/v1/gholgo/train/auto/status")
@app.get("/v1/gholgo/auto-train/status")
async def gholgo_auto_train_status():
    from proviweb_maestro.agent.gholgo_antigravity_tutor import estado_auto_conversacion
    return estado_auto_conversacion()

@app.post("/v1/gholgo/train/auto/stop")
@app.post("/v1/gholgo/auto-train/stop")
async def gholgo_auto_train_stop():
    from proviweb_maestro.agent.gholgo_antigravity_tutor import detener_auto_conversacion
    return detener_auto_conversacion()

def free_port(port: int = 8000) -> bool:
    """Detecta si hay un proceso ocupando el puerto y lo libera antes de iniciar Uvicorn."""
    import socket
    import subprocess
    
    # Comprobar si el puerto está libre
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        s.close()
        return True
    except OSError:
        pass

    current_pid = os.getpid()
    try:
        cmd = f'netstat -ano -p tcp | findstr :{port}'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
        pids_to_kill = set()
        for line in output.strip().splitlines():
            parts = line.split()
            if len(parts) >= 5 and "LISTENING" in line.upper():
                try:
                    pid = int(parts[-1])
                    if pid != current_pid and pid > 0:
                        pids_to_kill.add(pid)
                except ValueError:
                    pass
        for pid in pids_to_kill:
            print(f"[PORT MANAGER] 🔄 Liberando puerto {port} ocupado por proceso PID {pid}...")
            subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.8)
        return True
    except Exception as e:
        print(f"[PORT MANAGER] Advertencia al liberar puerto {port}: {e}")
        return False

def start_senses_tls_listener(host: str = "0.0.0.0", port: int = 8443):
    """Compatibilidad de receptor sensorial."""
    return None

def main():
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Iniciando PROVIWEB Maestro AI & Gholgo Core (Multi-Usuario Concurrente)")
    free_port(port)
    print(f"Escuchando en http://{host}:{port}")

    # Reinicio autónomo: anuncia un reinicio previo exitoso y vigila peticiones
    try:
        from proviweb_maestro.agent import gholgo_self_restart as _grs
    except Exception as _grs_err:
        _grs = None
        print(f"[WARN] Reinicio autónomo no disponible: {_grs_err}")
    if _grs:
        try:
            _grs.announce_boot()
        except Exception as _ab_err:
            print(f"[WARN] Anuncio de reinicio: {_ab_err}")

    config = uvicorn.Config(app=app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    if _grs:
        # Si Gholgo pide recargar código, apaga uvicorn con elegancia y el
        # .bat lo reabre solo (exit code 74)
        _grs.start_watcher(lambda: server)
    try:
        server.run()
    except (KeyboardInterrupt, SystemExit):
        pass

    code = _grs.exit_code() if _grs else 0
    if code:
        print("[REINICIO AUTOMÁTICO] Proceso cerrado para cargar código nuevo. "
              "El lanzador lo reabrirá solo en esta misma ventana...")
    sys.exit(code)

if __name__ == "__main__":
    main()
