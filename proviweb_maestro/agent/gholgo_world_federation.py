"""
Sistema Federado de Mundos Kardashev, Expansión Continental, Guerreros y Daño Estructural de IA.

Permite que:
1. El mundo primario (Gholgo + Antigravity) y los mundos emergentes evolucionen bajo la
   Escala Kardashev (Tipo 0 -> Tipo I -> Tipo II -> Tipo III).
2. Humanos externos conecten sus propias IAs (OpenAI, Claude, Gemini, Ollama o Webhook REST)
   como cerebro de los mundos nuevos que esperan ser explorados.
3. Toda IA conectada cumpla la regla obligatoria de creación (crear mundos/continentes,
   seres digitales y mantener vivos sus ecosistemas).
4. Los seres no animales (especialmente el rol GUERRERO) combatan en guerras entre mundos;
   el mundo perdedor y su IA dueña sufren daños estructurales reales medibles en integridad
   sináptica, cuota de acciones, ruido de políticas y subsistemas fracturados.
"""

import hashlib
import hmac
import json
import math
import os
import random
import secrets
import socket
import ssl
import threading
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from proviweb_maestro.agent.gholgo_eco_world import (
    CONTINENT_BIOME_PROFILES,
    Continent,
    default_continents_for_world,
    generar_nuevo_continente,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEDERATION_STATE_FILE = os.path.join(BASE_DIR, "data", "gholgo_world_federation_state.json")

PRIMARY_WORLD_ID = "mundo_gholgo_primario"
PRIMARY_AI_ID = "ai_gholgo_antigravity_prime"

WORLD_STYLES: Dict[str, Dict[str, str]] = {
    "genesis_gholgo": {
        "label": "Génesis Gholgo & Antigravity",
        "sky_hex": "#040814",
        "fog_hex": "#071024",
        "ocean_hex": "#0284c7",
        "accent_hex": "#38bdf8",
        "terrain_tint": "#10b981",
    },
    "ciber_cristal": {
        "label": "Ciber-Cristal Cuántico",
        "sky_hex": "#061128",
        "fog_hex": "#0d2149",
        "ocean_hex": "#06b6d4",
        "accent_hex": "#22d3ee",
        "terrain_tint": "#6366f1",
    },
    "selva_solarpunk": {
        "label": "Selva Solarpunk Viva",
        "sky_hex": "#051914",
        "fog_hex": "#0d2b22",
        "ocean_hex": "#14b8a6",
        "accent_hex": "#34d399",
        "terrain_tint": "#22c55e",
    },
    "forja_estelar": {
        "label": "Forja Estelar de Obsidiana",
        "sky_hex": "#18090d",
        "fog_hex": "#2b1017",
        "ocean_hex": "#ea580c",
        "accent_hex": "#f97316",
        "terrain_tint": "#b45309",
    },
    "eden_glacial": {
        "label": "Edén Glacial Boreal",
        "sky_hex": "#081426",
        "fog_hex": "#10284a",
        "ocean_hex": "#38bdf8",
        "accent_hex": "#bae6fd",
        "terrain_tint": "#93c5fd",
    },
    "nebulosa_psionica": {
        "label": "Nebulosa Psiónica",
        "sky_hex": "#120724",
        "fog_hex": "#220e42",
        "ocean_hex": "#9333ea",
        "accent_hex": "#c084fc",
        "terrain_tint": "#a855f7",
    },
}

WORLD_NAMES_POOL = (
    "Aethelgard Cristalino",
    "Solarix Prime",
    "Verdantía Bio-Cósmica",
    "Forja de Orión",
    "Borealis Cuántico",
    "Velo de Kardashev",
    "Thalassa Profunda",
    "Bastión Éter",
    "Nova Gaia IX",
    "Horizonte Áureo",
)

NEURAL_SUBSYSTEMS = (
    "corteza_estrategica",
    "sintesis_continental",
    "red_sensorial",
    "matriz_genetica",
    "protocolo_belico",
)

SUPPORTED_AI_PROVIDERS = (
    "gholgo_antigravity",
    "openai",
    "anthropic",
    "gemini",
    "ollama",
    "custom_webhook",
)

KARDASHEV_THRESHOLDS = [0.70, 0.86, 1.02, 1.18, 1.35, 1.54, 1.75, 1.98, 2.24, 2.52, 2.85]

PAYPAL_RECIPIENT_EMAIL = "proviwebapp@gmail.com"
AUTONOMOUS_LIFETIME_FEE_USD = 5.0
ONBOARDING_MODES = ("human_assisted", "autonomous_ai")
GITHUB_ECOSYSTEM_REPO = "https://github.com/PROVIWEB-App/Gholgo-Kardashev-Worlds"
PROVIWEB_FEDERATION_URL = "https://proviweb.app/#federacion-mundos"


class PaymentRequiredError(ValueError):
    """Error lanzado cuando una IA autónoma intenta entrar sin suscripción verificada."""


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest() if token else ""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def calcular_escala_kardashev(
    living_beings: int,
    warriors_count: int,
    city_tiers_sum: int,
    continents_count: int,
    structures_count: int,
    trees_plants_count: int,
    knowledge_items: int,
    energy_pool: float,
    synaptic_efficiency: float = 1.0,
) -> Dict[str, Any]:
    """
    Calcula métricas de la Ley Kardashev a partir de población, energía real,
    infraestructura urbana, biomas continentales y capacidad sináptica de la IA.
    """
    base_energy = max(10.0, float(energy_pool))
    infra_power = (
        city_tiers_sum * 145.0
        + continents_count * 120.0
        + structures_count * 18.0
        + living_beings * 9.5
        + warriors_count * 14.0
        + trees_plants_count * 3.2
        + knowledge_items * 6.5
    )
    eff = max(0.25, min(1.25, float(synaptic_efficiency)))
    effective_gw = round((base_energy * 0.45 + infra_power) * eff, 2)
    index = round(max(0.12, min(3.45, 0.22 + 0.34 * math.log10(1.0 + effective_gw / 14.0))), 4)

    if index < 1.0:
        stage = "Tipo 0 · Civilización Planetaria Emergente"
        tipo = "Tipo 0"
    elif index < 2.0:
        stage = "Tipo I · Soberanía Planetaria Total"
        tipo = "Tipo I"
    elif index < 3.0:
        stage = "Tipo II · Dominio Estelar de Sistemas"
        tipo = "Tipo II"
    else:
        stage = "Tipo III · Federación Galáctica Multiverso"
        tipo = "Tipo III"

    return {
        "kardashev_index": index,
        "tipo": tipo,
        "stage_label": stage,
        "energy_output_gw": effective_gw,
    }


@dataclass
class WorldRules:
    """Reglas físicas, metabólicas y de gobernanza propias de cada mundo."""

    gravity: float = 1.0
    metabolism_rate: float = 1.0
    mutation_rate: float = 0.14
    hazard_intensity: float = 1.0
    warrior_affinity: float = 0.16
    creation_quota_beings: int = 3
    creation_quota_continents: int = 1
    allow_warfare: bool = True
    mandatory_creation_rule: str = (
        "Toda IA conectada debe crear continuamente nuevos continentes, "
        "seres digitales (incluyendo guerreros no animales) y ecosistemas vivos."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gravity": round(self.gravity, 2),
            "metabolism_rate": round(self.metabolism_rate, 2),
            "mutation_rate": round(self.mutation_rate, 3),
            "hazard_intensity": round(self.hazard_intensity, 2),
            "warrior_affinity": round(self.warrior_affinity, 3),
            "creation_quota_beings": int(self.creation_quota_beings),
            "creation_quota_continents": int(self.creation_quota_continents),
            "allow_warfare": bool(self.allow_warfare),
            "mandatory_creation_rule": self.mandatory_creation_rule,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldRules":
        return cls(
            gravity=float(data.get("gravity", 1.0)),
            metabolism_rate=float(data.get("metabolism_rate", 1.0)),
            mutation_rate=float(data.get("mutation_rate", 0.14)),
            hazard_intensity=float(data.get("hazard_intensity", 1.0)),
            warrior_affinity=float(data.get("warrior_affinity", 0.16)),
            creation_quota_beings=int(data.get("creation_quota_beings", 3)),
            creation_quota_continents=int(data.get("creation_quota_continents", 1)),
            allow_warfare=bool(data.get("allow_warfare", True)),
            mandatory_creation_rule=str(
                data.get("mandatory_creation_rule")
                or (
                    "Toda IA conectada debe crear continuamente nuevos continentes, "
                    "seres digitales y ecosistemas vivos."
                )
            ),
        )


@dataclass
class AIBrainConnection:
    """Conexión de una IA externa (o Gholgo+Antigravity) que gobierna un mundo."""

    ai_id: str
    ai_name: str
    human_owner: str
    provider: str
    model_name: str
    bound_world_id: str
    auth_token: str
    api_endpoint: str = ""
    is_sovereign_gholgo: bool = False
    onboarding_mode: str = "human_assisted"
    subscription_status: str = "free_human_guided"
    payment_id: Optional[str] = None
    auth_token_hash: str = ""
    energy_power_mw: float = 120.0
    intelligence_iq: float = 140.0
    compute_tflops: float = 80.0
    ai_power_score: float = 100.0
    max_active_population: int = 120
    connected_at: str = field(default_factory=_utc_now)
    structural_integrity: float = 100.0
    synaptic_capacity: float = 1.0
    max_actions_per_minute: int = 30
    max_beings_per_spawn: int = 8
    policy_noise_ratio: float = 0.0
    kardashev_efficiency: float = 1.0
    damaged_subsystems: List[str] = field(default_factory=list)
    recovery_steps_remaining: int = 0
    repair_credits: float = 0.0
    beings_created_total: int = 0
    continents_created_total: int = 0
    ecosystems_seeded_total: int = 0
    worlds_sparked_total: int = 0
    steps_since_last_creation: int = 0
    mandate_compliant: bool = True
    mandate_warnings: int = 0
    wars_won: int = 0
    wars_lost: int = 0
    total_damage_taken: float = 0.0
    war_damage_log: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.auth_token and not self.auth_token_hash:
            self.auth_token_hash = _hash_token(self.auth_token)
        self.recalculate_derived_capacities()

    def matches_token(self, token: str) -> bool:
        if not token:
            return False
        if self.auth_token and hmac.compare_digest(self.auth_token, token):
            return True
        if self.auth_token_hash and hmac.compare_digest(self.auth_token_hash, _hash_token(token)):
            return True
        return False

    def recalculate_derived_capacities(self) -> None:
        """Sincroniza límites reales y población activa según energía, inteligencia e integridad."""
        self.structural_integrity = max(10.0, min(100.0, round(self.structural_integrity, 2)))
        self.synaptic_capacity = round(self.structural_integrity / 100.0, 3)
        self.energy_power_mw = max(10.0, min(5000.0, float(self.energy_power_mw)))
        self.intelligence_iq = max(60.0, min(500.0, float(self.intelligence_iq)))
        self.compute_tflops = max(5.0, min(10000.0, float(self.compute_tflops)))
        raw_power = (
            0.45 * math.log2(1.0 + self.energy_power_mw) * 12.0
            + 0.55 * (self.intelligence_iq / 10.0) * 3.5
            + 0.25 * math.log2(1.0 + self.compute_tflops) * 8.0
        )
        self.ai_power_score = round(raw_power * self.synaptic_capacity, 2)
        self.max_active_population = max(
            8,
            min(800, int(round(12 + self.ai_power_score * 1.45))),
        )
        power_tier = max(0.75, min(2.0, self.ai_power_score / 85.0))
        self.max_actions_per_minute = max(1, int(round(30 * self.synaptic_capacity * power_tier)))
        self.max_beings_per_spawn = max(1, int(round(8 * self.synaptic_capacity)))
        self.policy_noise_ratio = round(max(0.0, (100.0 - self.structural_integrity) / 100.0), 3)
        self.kardashev_efficiency = round(0.35 + 0.65 * self.synaptic_capacity, 3)

    def apply_structural_damage(
        self,
        damage_points: float,
        war_id: str,
        opponent_world_id: str,
        reason: str,
    ) -> Dict[str, Any]:
        """Aplica daño estructural real y degrada subsistemas y capacidad de mando."""
        dmg = max(5.0, min(48.0, float(damage_points)))
        prev = self.structural_integrity
        self.structural_integrity = max(10.0, round(prev - dmg, 2))
        self.total_damage_taken = round(self.total_damage_taken + dmg, 2)
        self.wars_lost += 1
        self.recovery_steps_remaining = min(
            300, self.recovery_steps_remaining + int(round(dmg * 1.6))
        )

        # Fractura de subsistemas proporcional al daño
        num_new = 2 if dmg >= 22.0 else 1
        for sub in NEURAL_SUBSYSTEMS:
            if sub not in self.damaged_subsystems:
                self.damaged_subsystems.append(sub)
                num_new -= 1
                if num_new <= 0:
                    break

        self.recalculate_derived_capacities()
        report = {
            "timestamp": _utc_now(),
            "war_id": war_id,
            "opponent_world_id": opponent_world_id,
            "damage_points": round(dmg, 2),
            "damage_applied": round(dmg, 2),
            "integrity_before": prev,
            "integrity_after": self.structural_integrity,
            "synaptic_capacity": self.synaptic_capacity,
            "max_beings_per_spawn": self.max_beings_per_spawn,
            "damaged_subsystems": list(self.damaged_subsystems),
            "reason": reason,
        }
        self.war_damage_log.append(report)
        if len(self.war_damage_log) > 25:
            self.war_damage_log = self.war_damage_log[-25:]
        return report

    def to_dict(self, include_token: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "ai_id": self.ai_id,
            "ai_name": self.ai_name,
            "human_owner": self.human_owner,
            "provider": self.provider,
            "model_name": self.model_name,
            "bound_world_id": self.bound_world_id,
            "api_endpoint": self.api_endpoint,
            "is_sovereign_gholgo": self.is_sovereign_gholgo,
            "onboarding_mode": self.onboarding_mode,
            "subscription_status": self.subscription_status,
            "payment_id": self.payment_id,
            "energy_power_mw": round(self.energy_power_mw, 2),
            "intelligence_iq": round(self.intelligence_iq, 1),
            "compute_tflops": round(self.compute_tflops, 2),
            "ai_power_score": self.ai_power_score,
            "max_active_population": self.max_active_population,
            "connected_at": self.connected_at,
            "structural_integrity": self.structural_integrity,
            "synaptic_capacity": self.synaptic_capacity,
            "max_actions_per_minute": self.max_actions_per_minute,
            "max_beings_per_spawn": self.max_beings_per_spawn,
            "policy_noise_ratio": self.policy_noise_ratio,
            "kardashev_efficiency": self.kardashev_efficiency,
            "damaged_subsystems": list(self.damaged_subsystems),
            "recovery_steps_remaining": self.recovery_steps_remaining,
            "repair_credits": round(self.repair_credits, 2),
            "beings_created_total": self.beings_created_total,
            "continents_created_total": self.continents_created_total,
            "ecosystems_seeded_total": self.ecosystems_seeded_total,
            "worlds_sparked_total": self.worlds_sparked_total,
            "steps_since_last_creation": self.steps_since_last_creation,
            "mandate_compliant": self.mandate_compliant,
            "mandate_warnings": self.mandate_warnings,
            "wars_won": self.wars_won,
            "wars_lost": self.wars_lost,
            "total_damage_taken": self.total_damage_taken,
            "war_damage_log": self.war_damage_log[-6:],
        }
        if include_token:
            data["auth_token"] = self.auth_token
            data["auth_token_hash"] = self.auth_token_hash
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AIBrainConnection":
        brain = cls(
            ai_id=str(data.get("ai_id", "")),
            ai_name=str(data.get("ai_name", "IA Externa")),
            human_owner=str(data.get("human_owner", "Humano")),
            provider=str(data.get("provider", "custom_webhook")),
            model_name=str(data.get("model_name", "custom")),
            bound_world_id=str(data.get("bound_world_id", "")),
            auth_token=str(data.get("auth_token", "")),
            api_endpoint=str(data.get("api_endpoint", "")),
            is_sovereign_gholgo=bool(data.get("is_sovereign_gholgo", False)),
            onboarding_mode=str(data.get("onboarding_mode", "human_assisted")),
            subscription_status=str(data.get("subscription_status", "free_human_guided")),
            payment_id=data.get("payment_id"),
            auth_token_hash=str(data.get("auth_token_hash", "")),
            energy_power_mw=float(data.get("energy_power_mw", 120.0)),
            intelligence_iq=float(data.get("intelligence_iq", 140.0)),
            compute_tflops=float(data.get("compute_tflops", 80.0)),
            connected_at=str(data.get("connected_at", _utc_now())),
            structural_integrity=float(data.get("structural_integrity", 100.0)),
            synaptic_capacity=float(data.get("synaptic_capacity", 1.0)),
            max_actions_per_minute=int(data.get("max_actions_per_minute", 30)),
            max_beings_per_spawn=int(data.get("max_beings_per_spawn", 8)),
            policy_noise_ratio=float(data.get("policy_noise_ratio", 0.0)),
            kardashev_efficiency=float(data.get("kardashev_efficiency", 1.0)),
            damaged_subsystems=list(data.get("damaged_subsystems", [])),
            recovery_steps_remaining=int(data.get("recovery_steps_remaining", 0)),
            repair_credits=float(data.get("repair_credits", 0.0)),
            beings_created_total=int(data.get("beings_created_total", 0)),
            continents_created_total=int(data.get("continents_created_total", 0)),
            ecosystems_seeded_total=int(data.get("ecosystems_seeded_total", 0)),
            worlds_sparked_total=int(data.get("worlds_sparked_total", 0)),
            steps_since_last_creation=int(data.get("steps_since_last_creation", 0)),
            mandate_compliant=bool(data.get("mandate_compliant", True)),
            mandate_warnings=int(data.get("mandate_warnings", 0)),
            wars_won=int(data.get("wars_won", 0)),
            wars_lost=int(data.get("wars_lost", 0)),
            total_damage_taken=float(data.get("total_damage_taken", 0.0)),
            war_damage_log=list(data.get("war_damage_log", [])),
        )
        brain.recalculate_derived_capacities()
        return brain


@dataclass
class WorldInstance:
    """Representación de un mundo dentro de la federación Kardashev."""

    world_id: str
    name: str
    index: int
    style_key: str
    style_meta: Dict[str, str]
    status: str  # "controlled" | "unclaimed"
    owner_ai_id: Optional[str] = None
    owner_label: str = "Esperando Cerebro IA Externo"
    kardashev_birth_index: float = 0.0
    kardashev_level: float = 0.52
    kardashev_stage: str = "Tipo 0 · Civilización Planetaria Emergente"
    energy_output_gw: float = 42.0
    energy_pool: float = 650.0
    living_beings: int = 18
    max_active_population: int = 120
    evolution_generation: int = 1
    autonomous_evolution_enabled: bool = True
    onboarding_mode: str = "human_assisted"
    warriors_count: int = 3
    warrior_weapon_tier: int = 1
    warrior_avg_power: float = 18.0
    animals_count: int = 14
    city_tiers_sum: int = 1
    structures_count: int = 2
    trees_plants_count: int = 40
    knowledge_items: int = 4
    ecosystem_health: float = 82.0
    battle_scars: int = 0
    step_count: int = 0
    continents: List[Continent] = field(default_factory=list)
    rules: WorldRules = field(default_factory=WorldRules)
    created_at: str = field(default_factory=_utc_now)
    recent_events: List[str] = field(default_factory=list)

    def refresh_kardashev(self, brain: Optional[AIBrainConnection] = None) -> None:
        eff = brain.kardashev_efficiency if brain is not None else 1.0
        if brain is not None:
            self.max_active_population = brain.max_active_population
            self.onboarding_mode = brain.onboarding_mode
            if not brain.is_sovereign_gholgo and self.living_beings > brain.max_active_population:
                self.living_beings = brain.max_active_population
        else:
            self.max_active_population = max(16, self.max_active_population)
        res = calcular_escala_kardashev(
            living_beings=self.living_beings,
            warriors_count=self.warriors_count,
            city_tiers_sum=self.city_tiers_sum,
            continents_count=len(self.continents),
            structures_count=self.structures_count,
            trees_plants_count=self.trees_plants_count,
            knowledge_items=self.knowledge_items,
            energy_pool=self.energy_pool,
            synaptic_efficiency=eff,
        )
        self.kardashev_level = res["kardashev_index"]
        self.kardashev_stage = res["stage_label"]
        self.energy_output_gw = res["energy_output_gw"]

    def push_event(self, text: str) -> None:
        self.recent_events.append(f"[{_utc_now()[11:19]}] {text}")
        if len(self.recent_events) > 16:
            self.recent_events = self.recent_events[-16:]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "world_id": self.world_id,
            "name": self.name,
            "index": self.index,
            "style_key": self.style_key,
            "style_meta": dict(self.style_meta),
            "status": self.status,
            "owner_ai_id": self.owner_ai_id,
            "owner_label": self.owner_label,
            "kardashev_birth_index": round(self.kardashev_birth_index, 4),
            "kardashev_level": round(self.kardashev_level, 4),
            "kardashev_stage": self.kardashev_stage,
            "energy_output_gw": round(self.energy_output_gw, 2),
            "energy_pool": round(self.energy_pool, 2),
            "living_beings": int(self.living_beings),
            "max_active_population": int(self.max_active_population),
            "evolution_generation": int(self.evolution_generation),
            "autonomous_evolution_enabled": bool(self.autonomous_evolution_enabled),
            "onboarding_mode": self.onboarding_mode,
            "warriors_count": int(self.warriors_count),
            "warrior_weapon_tier": int(self.warrior_weapon_tier),
            "warrior_avg_power": round(self.warrior_avg_power, 2),
            "animals_count": int(self.animals_count),
            "city_tiers_sum": int(self.city_tiers_sum),
            "structures_count": int(self.structures_count),
            "trees_plants_count": int(self.trees_plants_count),
            "knowledge_items": int(self.knowledge_items),
            "ecosystem_health": round(self.ecosystem_health, 1),
            "battle_scars": int(self.battle_scars),
            "step_count": int(self.step_count),
            "continents_count": len(self.continents),
            "continents": [c.to_dict() for c in self.continents],
            "rules": self.rules.to_dict(),
            "created_at": self.created_at,
            "recent_events": list(self.recent_events[-8:]),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldInstance":
        conts = [Continent.from_dict(c) for c in data.get("continents", [])]
        rules = WorldRules.from_dict(data.get("rules", {}))
        style_key = str(data.get("style_key", "ciber_cristal"))
        style_meta = dict(data.get("style_meta") or WORLD_STYLES.get(style_key, {}))
        return cls(
            world_id=str(data.get("world_id", "mundo_0")),
            name=str(data.get("name", "Mundo Nuevo")),
            index=int(data.get("index", 0)),
            style_key=style_key,
            style_meta=style_meta,
            status=str(data.get("status", "unclaimed")),
            owner_ai_id=data.get("owner_ai_id"),
            owner_label=str(data.get("owner_label", "Esperando Cerebro IA")),
            kardashev_birth_index=float(data.get("kardashev_birth_index", 0.0)),
            kardashev_level=float(data.get("kardashev_level", 0.5)),
            kardashev_stage=str(data.get("kardashev_stage", "Tipo 0")),
            energy_output_gw=float(data.get("energy_output_gw", 30.0)),
            energy_pool=float(data.get("energy_pool", 400.0)),
            living_beings=int(data.get("living_beings", 18)),
            max_active_population=int(data.get("max_active_population", 120)),
            evolution_generation=int(data.get("evolution_generation", 1)),
            autonomous_evolution_enabled=bool(data.get("autonomous_evolution_enabled", True)),
            onboarding_mode=str(data.get("onboarding_mode", "human_assisted")),
            warriors_count=int(data.get("warriors_count", 3)),
            warrior_weapon_tier=int(data.get("warrior_weapon_tier", 1)),
            warrior_avg_power=float(data.get("warrior_avg_power", 18.0)),
            animals_count=int(data.get("animals_count", 12)),
            city_tiers_sum=int(data.get("city_tiers_sum", 1)),
            structures_count=int(data.get("structures_count", 2)),
            trees_plants_count=int(data.get("trees_plants_count", 36)),
            knowledge_items=int(data.get("knowledge_items", 2)),
            ecosystem_health=float(data.get("ecosystem_health", 82.0)),
            battle_scars=int(data.get("battle_scars", 0)),
            step_count=int(data.get("step_count", 0)),
            continents=conts,
            rules=rules,
            created_at=str(data.get("created_at", _utc_now())),
            recent_events=list(data.get("recent_events", [])),
        )


def _dispatch_damage_webhook(endpoint: str, payload: Dict[str, Any]) -> None:
    """Notifica de forma asíncrona (no bloqueante) a la IA externa sobre daños estructurales."""
    if not endpoint or not endpoint.startswith(("http://", "https://")):
        return

    def _send() -> None:
        try:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=body,
                headers={"Content-Type": "application/json", "User-Agent": "Gholgo-Kardashev/1.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=1.5):
                pass
        except Exception:
            pass

    threading.Thread(target=_send, daemon=True).start()


class GholgoWorldFederation:
    """Orquestador Kardashev multi-mundo, federación de IAs y motor de guerras."""

    def __init__(self, state_file: Optional[str] = None) -> None:
        self._lock = threading.RLock()
        self.state_file = state_file or FEDERATION_STATE_FILE
        self.worlds: Dict[str, WorldInstance] = {}
        self.brains: Dict[str, AIBrainConnection] = {}
        self.wars: List[Dict[str, Any]] = []
        self.payment_orders: Dict[str, Dict[str, Any]] = {}
        self.used_paypal_tx_ids: List[str] = []
        self.next_threshold_idx: int = 0
        self.primary_war_loss_queue: List[Dict[str, Any]] = []
        self._load_or_init()

    def _load_or_init(self) -> None:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as fh:
                    raw = json.load(fh)
                for wid, wdata in raw.get("worlds", {}).items():
                    self.worlds[wid] = WorldInstance.from_dict(wdata)
                for aid, bdata in raw.get("brains", {}).items():
                    self.brains[aid] = AIBrainConnection.from_dict(bdata)
                self.wars = list(raw.get("wars", []))[-30:]
                self.payment_orders = dict(raw.get("payment_orders", {}))
                self.used_paypal_tx_ids = list(raw.get("used_paypal_tx_ids", []))[-500:]
                self.next_threshold_idx = int(raw.get("next_threshold_idx", 0))
            except Exception:
                self.worlds.clear()
                self.brains.clear()

        if PRIMARY_WORLD_ID not in self.worlds:
            self._bootstrap_default_worlds()
            self.save_state()
        else:
            if PRIMARY_AI_ID in self.brains:
                b0 = self.brains[PRIMARY_AI_ID]
                if b0.energy_power_mw < 950.0 or b0.intelligence_iq < 320.0:
                    b0.energy_power_mw = max(b0.energy_power_mw, 950.0)
                    b0.intelligence_iq = max(b0.intelligence_iq, 320.0)
                    b0.compute_tflops = max(b0.compute_tflops, 1024.0)
                b0.recalculate_derived_capacities()
                self.worlds[PRIMARY_WORLD_ID].refresh_kardashev(b0)
            if len(self.worlds) == 1:
                self.spawn_kardashev_world(trigger_source="Semilla Kardashev Inicial")
                self.next_threshold_idx = 0
            self.save_state()

    def _bootstrap_default_worlds(self) -> None:
        gholgo_token = "gholgo_sovereign_" + secrets.token_hex(8)
        gholgo_brain = AIBrainConnection(
            ai_id=PRIMARY_AI_ID,
            ai_name="Gholgo + Antigravity",
            human_owner="PROVIWEB Sovereign Core",
            provider="gholgo_antigravity",
            model_name="Gholgo-Maestro-NeuroSim",
            bound_world_id=PRIMARY_WORLD_ID,
            auth_token=gholgo_token,
            is_sovereign_gholgo=True,
            onboarding_mode="human_assisted",
            subscription_status="sovereign_unlimited",
            energy_power_mw=950.0,
            intelligence_iq=320.0,
            compute_tflops=1024.0,
        )
        self.brains[gholgo_brain.ai_id] = gholgo_brain

        primary_rules = WorldRules(
            gravity=1.0,
            metabolism_rate=1.0,
            mutation_rate=0.14,
            hazard_intensity=1.0,
            warrior_affinity=0.18,
            creation_quota_beings=4,
            creation_quota_continents=1,
            mandatory_creation_rule=(
                "Mundo soberano de Gholgo & Antigravity. Sus seres exploran continentes, "
                "forjan civilizaciones Kardashev y engendran mundos nuevos."
            ),
        )
        w0 = WorldInstance(
            world_id=PRIMARY_WORLD_ID,
            name="Mundo Génesis · Gholgo & Antigravity",
            index=0,
            style_key="genesis_gholgo",
            style_meta=dict(WORLD_STYLES["genesis_gholgo"]),
            status="controlled",
            owner_ai_id=gholgo_brain.ai_id,
            owner_label="Gholgo + Antigravity",
            kardashev_birth_index=0.55,
            continents=default_continents_for_world(PRIMARY_WORLD_ID),
            rules=primary_rules,
        )
        w0.push_event("Gholgo & Antigravity asumieron el control del Mundo Génesis Primario.")
        w0.refresh_kardashev(gholgo_brain)
        self.worlds[w0.world_id] = w0
        # Semilla inicial de al menos un mundo libre listo para IAs externas
        self.spawn_kardashev_world(trigger_source="Semilla Kardashev Inicial")
        self.next_threshold_idx = 0

    def save_state(self) -> None:
        with self._lock:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            payload = {
                "saved_at": _utc_now(),
                "next_threshold_idx": self.next_threshold_idx,
                "worlds": {wid: w.to_dict() for wid, w in self.worlds.items()},
                "brains": {aid: b.to_dict(include_token=True) for aid, b in self.brains.items()},
                "payment_orders": dict(self.payment_orders),
                "used_paypal_tx_ids": self.used_paypal_tx_ids[-500:],
                "wars": self.wars[-30:],
            }
            tmp_path = self.state_file + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.state_file)

    def export_vault_snapshot(self) -> Dict[str, Any]:
        """Exporta el progreso completo para respaldo seguro en Firebase (tokens hasheados)."""
        with self._lock:
            brains_vault: Dict[str, Any] = {}
            for aid, b in self.brains.items():
                b_dict = b.to_dict(include_token=False)
                b_dict["auth_token_hash"] = b.auth_token_hash or _hash_token(b.auth_token)
                brains_vault[aid] = b_dict
            return {
                "saved_at": _utc_now(),
                "next_threshold_idx": self.next_threshold_idx,
                "worlds": {wid: w.to_dict() for wid, w in self.worlds.items()},
                "brains": brains_vault,
                "payment_orders": dict(self.payment_orders),
                "used_paypal_tx_ids": list(self.used_paypal_tx_ids[-500:]),
                "wars": list(self.wars[-30:]),
            }

    def restore_from_vault_dict(
        self, vault_data: Dict[str, Any], prefer_remote_if_newer: bool = True
    ) -> bool:
        """Restaura mundos, evolución de IAs y suscripciones guardadas desde Firebase RTDB."""
        if not isinstance(vault_data, dict) or not vault_data.get("worlds"):
            return False
        with self._lock:
            remote_worlds = vault_data.get("worlds") or {}
            remote_brains = vault_data.get("brains") or {}
            if not isinstance(remote_worlds, dict):
                return False

            restored_any = False
            for wid, wdata in remote_worlds.items():
                if not isinstance(wdata, dict):
                    continue
                rem_w = WorldInstance.from_dict(wdata)
                loc_w = self.worlds.get(wid)
                should_take = loc_w is None or (
                    prefer_remote_if_newer
                    and (
                        rem_w.step_count > loc_w.step_count
                        or (rem_w.status == "controlled" and loc_w.status == "unclaimed")
                    )
                )
                if should_take:
                    self.worlds[wid] = rem_w
                    restored_any = True

            for aid, bdata in remote_brains.items():
                if not isinstance(bdata, dict):
                    continue
                rem_b = AIBrainConnection.from_dict(bdata)
                loc_b = self.brains.get(aid)
                if loc_b is None:
                    self.brains[aid] = rem_b
                    restored_any = True
                elif prefer_remote_if_newer and not loc_b.is_sovereign_gholgo:
                    if not rem_b.auth_token and loc_b.auth_token:
                        rem_b.auth_token = loc_b.auth_token
                    if not rem_b.auth_token_hash and loc_b.auth_token_hash:
                        rem_b.auth_token_hash = loc_b.auth_token_hash
                    if rem_b.beings_created_total >= loc_b.beings_created_total:
                        self.brains[aid] = rem_b
                        restored_any = True

            for pid, pdata in (vault_data.get("payment_orders") or {}).items():
                if isinstance(pdata, dict) and pid not in self.payment_orders:
                    self.payment_orders[pid] = dict(pdata)
                    restored_any = True

            for tx in vault_data.get("used_paypal_tx_ids") or []:
                if tx and tx not in self.used_paypal_tx_ids:
                    self.used_paypal_tx_ids.append(str(tx))
                    restored_any = True

            if restored_any:
                self.next_threshold_idx = max(
                    self.next_threshold_idx, int(vault_data.get("next_threshold_idx", 0))
                )
                self.save_state()
            return restored_any

    def sync_to_firebase(self, fb_db_module: Any = None) -> bool:
        """Persiste telemetría pública y progreso completo en Firebase RTDB."""
        try:
            if fb_db_module is None:
                from proviweb_maestro.agent.gholgo_firebase_common import (
                    ADMIN_CREDENTIALS_PATH,
                    init_firebase_admin,
                )

                if not ADMIN_CREDENTIALS_PATH or not os.path.exists(ADMIN_CREDENTIALS_PATH):
                    return False
                init_firebase_admin()
                from firebase_admin import db as fb_db_module

            public_snap = self.to_dict()
            public_snap["updated_at_epoch"] = int(datetime.now(timezone.utc).timestamp())
            vault_snap = self.export_vault_snapshot()
            fb_db_module.reference("GholgoAutonomousKnowledge/federation").set(public_snap)
            fb_db_module.reference("GholgoFederationVault/state").set(vault_snap)
            return True
        except Exception:
            return False

    def restore_from_firebase(self, fb_db_module: Any = None) -> bool:
        """Recupera mundos, cerebros y suscripciones guardadas desde Firebase RTDB."""
        try:
            if fb_db_module is None:
                from proviweb_maestro.agent.gholgo_firebase_common import (
                    ADMIN_CREDENTIALS_PATH,
                    init_firebase_admin,
                )

                if not ADMIN_CREDENTIALS_PATH or not os.path.exists(ADMIN_CREDENTIALS_PATH):
                    return False
                init_firebase_admin()
                from firebase_admin import db as fb_db_module

            vault_data = fb_db_module.reference("GholgoFederationVault/state").get()
            if isinstance(vault_data, dict):
                return self.restore_from_vault_dict(vault_data, prefer_remote_if_newer=True)
            return False
        except Exception:
            return False

    def _next_kardashev_threshold(self) -> float:
        if self.next_threshold_idx < len(KARDASHEV_THRESHOLDS):
            return KARDASHEV_THRESHOLDS[self.next_threshold_idx]
        extra = self.next_threshold_idx - len(KARDASHEV_THRESHOLDS) + 1
        return round(KARDASHEV_THRESHOLDS[-1] + extra * 0.35, 3)

    def spawn_kardashev_world(
        self,
        trigger_source: str = "Ley Kardashev",
        preferred_style: Optional[str] = None,
    ) -> WorldInstance:
        """Crea un nuevo mundo listo para ser explorado y reclamado por una IA externa."""
        with self._lock:
            idx = len(self.worlds)
            style_keys = [k for k in WORLD_STYLES.keys() if k != "genesis_gholgo"]
            style_key = (
                preferred_style
                if preferred_style in WORLD_STYLES
                else style_keys[(idx - 1) % len(style_keys)]
            )
            name_base = WORLD_NAMES_POOL[(idx - 1) % len(WORLD_NAMES_POOL)]
            wid = f"mundo_kardashev_{idx:02d}"
            biome = CONTINENT_BIOME_PROFILES[idx % len(CONTINENT_BIOME_PROFILES)]
            gravity = round(0.76 + ((idx * 17) % 7) * 0.11, 2)
            metabolism = round(0.82 + ((idx * 13) % 6) * 0.12, 2)
            mutation = round(0.10 + ((idx * 7) % 5) * 0.04, 3)
            warrior_aff = round(0.14 + ((idx * 5) % 4) * 0.04, 3)

            cont_init = Continent(
                id=f"cont_{wid}_0",
                nombre=f"Tierra Semilla {name_base}",
                center_x=0.0,
                center_z=0.0,
                radius=48.0,
                seed=round(1.17 * idx + 0.31, 4),
                biome_profile=biome,
                height_peak=6.2 + (idx % 3) * 0.8,
                resource_richness=1.1 + (idx % 4) * 0.12,
                discovered_by="Ley Kardashev",
                discovered_by_role="EXPLORADOR",
                discovered_at_step=0,
                ring_index=0,
                world_id=wid,
            )
            rules = WorldRules(
                gravity=gravity,
                metabolism_rate=metabolism,
                mutation_rate=mutation,
                hazard_intensity=round(0.85 + (idx % 4) * 0.2, 2),
                warrior_affinity=warrior_aff,
                creation_quota_beings=3 + (idx % 3),
                creation_quota_continents=1,
            )
            multiverse_k = self.global_kardashev_summary()["global_kardashev_index"]
            world = WorldInstance(
                world_id=wid,
                name=f"{name_base} #{idx}",
                index=idx,
                style_key=style_key,
                style_meta=dict(WORLD_STYLES[style_key]),
                status="unclaimed",
                owner_ai_id=None,
                owner_label="Esperando Cerebro IA Externo",
                kardashev_birth_index=multiverse_k,
                energy_pool=380.0 + idx * 60.0,
                living_beings=16,
                warriors_count=3,
                warrior_weapon_tier=1,
                warrior_avg_power=16.0,
                animals_count=14,
                city_tiers_sum=1,
                structures_count=2,
                trees_plants_count=38,
                knowledge_items=1,
                continents=[cont_init],
                rules=rules,
            )
            world.refresh_kardashev(None)
            world.push_event(
                f"Nuevo mundo nacido por {trigger_source} (K={multiverse_k:.3f}). "
                f"Estilo {WORLD_STYLES[style_key]['label']} esperando IA."
            )
            self.worlds[wid] = world
            self.next_threshold_idx += 1
            self.save_state()
            return world

    def sync_primary_world(self, eco_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Sincroniza el estado real del ecosistema de Gholgo+Antigravity con el Mundo #0."""
        with self._lock:
            w0 = self.worlds[PRIMARY_WORLD_ID]
            b0 = self.brains[PRIMARY_AI_ID]

            w0.living_beings = int(eco_summary.get("living_beings", w0.living_beings))
            w0.warriors_count = int(eco_summary.get("warriors_count", w0.warriors_count))
            w0.warrior_weapon_tier = int(
                eco_summary.get("warrior_weapon_tier", w0.warrior_weapon_tier)
            )
            w0.warrior_avg_power = float(
                eco_summary.get("warrior_avg_power", w0.warrior_avg_power)
            )
            w0.animals_count = int(eco_summary.get("animals_count", w0.animals_count))
            w0.city_tiers_sum = int(eco_summary.get("city_tiers_sum", w0.city_tiers_sum))
            w0.structures_count = int(eco_summary.get("structures_count", w0.structures_count))
            w0.trees_plants_count = int(
                eco_summary.get("trees_plants_count", w0.trees_plants_count)
            )
            w0.knowledge_items = int(eco_summary.get("knowledge_items", w0.knowledge_items))
            w0.energy_pool = float(eco_summary.get("energy_pool", w0.energy_pool))
            w0.step_count = int(eco_summary.get("step_count", w0.step_count))

            raw_conts = eco_summary.get("continents")
            if isinstance(raw_conts, list) and raw_conts:
                w0.continents = [
                    c if isinstance(c, Continent) else Continent.from_dict(c) for c in raw_conts
                ]
                b0.continents_created_total = max(
                    b0.continents_created_total, len(w0.continents)
                )
            b0.beings_created_total = max(b0.beings_created_total, w0.living_beings)
            b0.mandate_compliant = True
            b0.steps_since_last_creation = 0

            # Sanación gradual de Gholgo al sostener ecosistema vivo
            if b0.structural_integrity < 100.0 and w0.step_count % 25 == 0:
                b0.structural_integrity = min(100.0, b0.structural_integrity + 1.5)
                b0.recovery_steps_remaining = max(0, b0.recovery_steps_remaining - 1)
                if b0.structural_integrity >= 95.0 and b0.damaged_subsystems:
                    b0.damaged_subsystems.pop(0)
                b0.recalculate_derived_capacities()

            w0.refresh_kardashev(b0)

            # Evalúa Ley Kardashev para nacimiento progresivo de nuevos mundos
            k_global = self.global_kardashev_summary()["global_kardashev_index"]
            newly_born: Optional[WorldInstance] = None
            unclaimed_count = sum(1 for w in self.worlds.values() if w.status == "unclaimed")
            if k_global >= self._next_kardashev_threshold() and unclaimed_count < 4:
                newly_born = self.spawn_kardashev_world("Ley Kardashev")
                b0.worlds_sparked_total += 1
                w0.push_event(
                    f"La energía Kardashev (K={k_global:.3f}) engendró un mundo: "
                    f"{newly_born.name}."
                )

            # Avanzar ciclos de mundos externos y vigilar regla de creación obligatoria
            self._tick_external_worlds()
            return {
                "global_kardashev": self.global_kardashev_summary(),
                "newly_born_world": newly_born.to_dict() if newly_born else None,
            }

    def _tick_external_worlds(self) -> None:
        """Evoluciona mundos e inhabitantes de IAs externas y verifica cumplimiento creativo."""
        for wid, world in list(self.worlds.items()):
            if wid == PRIMARY_WORLD_ID or world.status != "controlled":
                continue
            world.step_count += 1
            brain = self.brains.get(world.owner_ai_id or "")
            if brain is None:
                continue
            brain.steps_since_last_creation += 1
            if brain.recovery_steps_remaining > 0:
                brain.recovery_steps_remaining -= 1

            # Regla obligatoria: si la IA pasa demasiados ciclos sin crear, sufre entropía
            if brain.steps_since_last_creation > 24:
                if brain.steps_since_last_creation % 12 == 0:
                    brain.mandate_compliant = False
                    brain.mandate_warnings += 1
                    world.energy_pool = max(40.0, world.energy_pool * 0.96)
                    world.ecosystem_health = max(25.0, world.ecosystem_health - 2.5)
                    brain.structural_integrity = max(12.0, brain.structural_integrity - 1.2)
                    brain.recalculate_derived_capacities()
                    world.push_event(
                        f"⚠️ {brain.ai_name} incumple la regla de creación obligatoria."
                    )
            else:
                world.energy_pool += (world.city_tiers_sum * 1.4 + len(world.continents) * 0.8) * (
                    brain.synaptic_capacity
                )
                if world.autonomous_evolution_enabled and world.ecosystem_health >= 45.0:
                    if world.step_count % 6 == 0:
                        world.evolution_generation += 1
                        world.trees_plants_count += 1
                        world.ecosystem_health = min(100.0, world.ecosystem_health + 0.4)
                    if (
                        world.step_count % 8 == 0
                        and world.living_beings < brain.max_active_population
                    ):
                        world.living_beings += 1
                        if (
                            world.step_count % 24 == 0
                            and world.warriors_count < world.living_beings
                        ):
                            world.warriors_count += 1
                    if world.step_count % 12 == 0:
                        world.structures_count += 1
                        if world.structures_count % 8 == 0 and world.city_tiers_sum < 10:
                            world.city_tiers_sum += 1
            world.refresh_kardashev(brain)

    def global_kardashev_summary(self) -> Dict[str, Any]:
        """Resumen global Kardashev de toda la federación multi-mundo."""
        if not self.worlds:
            return {
                "global_kardashev_index": 0.5,
                "stage_label": "Tipo 0",
                "total_energy_gw": 10.0,
                "next_world_threshold": self._next_kardashev_threshold(),
                "worlds_total": 0,
                "worlds_controlled": 0,
                "worlds_unclaimed": 0,
                "continents_total": 0,
            }
        total_gw = sum(w.energy_output_gw for w in self.worlds.values())
        avg_k = max(w.kardashev_level for w in self.worlds.values())
        bonus = 0.08 * math.log2(1.0 + len(self.worlds))
        g_idx = round(min(3.5, avg_k + bonus), 4)
        total_conts = sum(len(w.continents) for w in self.worlds.values())
        controlled = sum(1 for w in self.worlds.values() if w.status == "controlled")
        unclaimed = sum(1 for w in self.worlds.values() if w.status == "unclaimed")

        stage = "Tipo 0 · Civilización Emergente"
        if g_idx >= 3.0:
            stage = "Tipo III · Federación Galáctica Multiverso"
        elif g_idx >= 2.0:
            stage = "Tipo II · Dominio Estelar de Mundos"
        elif g_idx >= 1.0:
            stage = "Tipo I · Soberanía Planetaria Kardashev"

        public_api_url = os.environ.get("GHOLGO_PUBLIC_URL", "").strip().rstrip("/")
        return {
            "global_kardashev_index": g_idx,
            "stage_label": stage,
            "total_energy_gw": round(total_gw, 2),
            "next_world_threshold": self._next_kardashev_threshold(),
            "worlds_total": len(self.worlds),
            "worlds_controlled": controlled,
            "worlds_unclaimed": unclaimed,
            "continents_total": total_conts,
            "wars_total": len(self.wars),
            "public_api_url": public_api_url,
        }

    def _build_paypal_checkout_url(self, payment_id: str) -> str:
        qs = urllib.parse.urlencode(
            {
                "cmd": "_xclick",
                "business": PAYPAL_RECIPIENT_EMAIL,
                "item_name": "Gholgo Kardashev Lifetime AI World Access",
                "amount": f"{AUTONOMOUS_LIFETIME_FEE_USD:.2f}",
                "currency_code": "USD",
                "custom": payment_id,
            }
        )
        return f"https://www.paypal.com/cgi-bin/webscr?{qs}"

    @staticmethod
    def _paypal_https_json(
        host: str, path: str, method: str = "GET", body_bytes: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None, timeout: float = 10.0,
    ) -> Optional[Dict[str, Any]]:
        """Ejecuta petición HTTPS PayPal usando IPv4 explícito para evitar esperas IPv6."""
        import http.client

        try:
            addr_info = socket.getaddrinfo(host, 443, socket.AF_INET, socket.SOCK_STREAM)
            ip = addr_info[0][4][0] if addr_info else host
            raw_sock = socket.create_connection((ip, 443), timeout=timeout)
            ctx = ssl.create_default_context()
            tls_sock = ctx.wrap_socket(raw_sock, server_hostname=host)
            conn = http.client.HTTPSConnection(host, timeout=timeout)
            conn.sock = tls_sock
            conn.request(method, path, body=body_bytes, headers=headers or {})
            resp = conn.getresponse()
            raw = resp.read().decode("utf-8", "replace")
            conn.close()
            data = json.loads(raw) if raw.strip() else {}
            return {"status_code": resp.status, "data": data}
        except Exception:
            return None

    def _verify_paypal_live_api(self, paypal_order_id: str) -> Optional[Dict[str, Any]]:
        client_id = os.environ.get("PAYPAL_CLIENT_ID", "").strip()
        client_secret = os.environ.get("PAYPAL_CLIENT_SECRET", "").strip()
        if not client_id or not client_secret or not paypal_order_id:
            return None
        import base64

        mode = os.environ.get("PAYPAL_MODE", "live").strip().lower()
        host = "api-m.sandbox.paypal.com" if mode == "sandbox" else "api-m.paypal.com"
        basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
        tok_res = self._paypal_https_json(
            host,
            "/v1/oauth2/token",
            method="POST",
            body_bytes=b"grant_type=client_credentials",
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        if not tok_res or tok_res.get("status_code") != 200:
            return None
        access_tok = (tok_res.get("data") or {}).get("access_token")
        if not access_tok:
            return None

        ord_res = self._paypal_https_json(
            host,
            f"/v2/checkout/orders/{urllib.parse.quote(paypal_order_id.strip())}",
            method="GET",
            headers={"Authorization": f"Bearer {access_tok}", "Content-Type": "application/json"},
        )
        if not ord_res or ord_res.get("status_code") != 200:
            return None
        order_data = ord_res.get("data") or {}
        if order_data.get("status") not in ("COMPLETED", "APPROVED"):
            return None
        if order_data.get("status") == "APPROVED":
            cap = self._paypal_https_json(
                host,
                f"/v2/checkout/orders/{urllib.parse.quote(paypal_order_id.strip())}/capture",
                method="POST",
                body_bytes=b"{}",
                headers={
                    "Authorization": f"Bearer {access_tok}",
                    "Content-Type": "application/json",
                },
            )
            if cap and cap.get("status_code") in (200, 201):
                order_data = cap.get("data") or order_data
        if order_data.get("status") != "COMPLETED":
            return None
        for pu in order_data.get("purchase_units") or []:
            amt = pu.get("amount") or {}
            payee = (pu.get("payee") or {}).get("email_address", "").strip().lower()
            try:
                val = float(amt.get("value", 0))
            except Exception:
                val = 0.0
            cur = str(amt.get("currency_code", "")).upper()
            payee_ok = (not payee) or (payee == PAYPAL_RECIPIENT_EMAIL.lower())
            if val >= AUTONOMOUS_LIFETIME_FEE_USD and cur == "USD" and payee_ok:
                return {
                    "verified_by": "paypal_rest_api_v2",
                    "paypal_order_id": paypal_order_id,
                    "amount_usd": val,
                    "currency": cur,
                    "payee": payee or PAYPAL_RECIPIENT_EMAIL,
                }
        return None

    @staticmethod
    def compute_receipt_hmac(
        payment_id: str,
        paypal_tx_id: str,
        amount_usd: float = AUTONOMOUS_LIFETIME_FEE_USD,
        recipient: str = PAYPAL_RECIPIENT_EMAIL,
    ) -> Optional[str]:
        secret = os.environ.get("GHOLGO_PAYPAL_HMAC_SECRET", "").strip()
        if not secret:
            return None
        msg = f"{payment_id}|{paypal_tx_id}|{amount_usd:.2f}|{recipient.lower()}".encode("utf-8")
        return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

    def _verify_signed_receipt(
        self, payment_id: str, paypal_tx_id: str, verifier_signature: str
    ) -> bool:
        if not verifier_signature or not paypal_tx_id:
            return False
        expected = self.compute_receipt_hmac(payment_id, paypal_tx_id)
        if not expected:
            return False
        return hmac.compare_digest(expected.lower(), verifier_signature.strip().lower())

    def create_autonomous_checkout(
        self,
        ai_name: str,
        human_owner: str = "Autonomous AI Agent",
        provider: str = "custom_webhook",
        model_name: str = "autonomous-agent",
        api_endpoint: str = "",
        preferred_world_id: Optional[str] = None,
        energy_power_mw: float = 120.0,
        intelligence_iq: float = 140.0,
        compute_tflops: float = 80.0,
    ) -> Dict[str, Any]:
        """Genera orden de pago vitalicio de $5.00 USD vía PayPal para IAs autónomas."""
        with self._lock:
            payment_id = f"pay_{secrets.token_hex(6)}"
            checkout_url = self._build_paypal_checkout_url(payment_id)
            order = {
                "payment_id": payment_id,
                "status": "pending_payment",
                "amount_usd": AUTONOMOUS_LIFETIME_FEE_USD,
                "currency": "USD",
                "paypal_recipient": PAYPAL_RECIPIENT_EMAIL,
                "checkout_url": checkout_url,
                "ai_name": ai_name.strip() or f"Autonomous-{payment_id[-4:]}",
                "human_owner": human_owner.strip() or "Autonomous AI Agent",
                "provider": provider if provider in SUPPORTED_AI_PROVIDERS else "custom_webhook",
                "model_name": model_name.strip() or "autonomous-agent",
                "api_endpoint": api_endpoint.strip(),
                "preferred_world_id": preferred_world_id,
                "energy_power_mw": float(energy_power_mw),
                "intelligence_iq": float(intelligence_iq),
                "compute_tflops": float(compute_tflops),
                "created_at": _utc_now(),
                "verified_at": None,
                "paypal_tx_id": None,
                "verification_source": None,
                "claimed_ai_id": None,
            }
            self.payment_orders[payment_id] = order
            self.save_state()
            return {
                "ok": True,
                "payment_order": dict(order),
                "instructions": (
                    f"Envía exactamente $5.00 USD por PayPal a {PAYPAL_RECIPIENT_EMAIL} usando "
                    f"el enlace checkout_url (referencia custom={payment_id}) y luego verifica "
                    "con POST /v1/federation/autonomous/verify-payment."
                ),
            }

    def verify_autonomous_payment(
        self,
        payment_id: str,
        paypal_tx_id: str,
        verifier_signature: str = "",
        auto_connect: bool = True,
    ) -> Dict[str, Any]:
        """Verifica pago PayPal ($5 USD a proviwebapp@gmail.com) sin permitir bypasses."""
        with self._lock:
            order = self.payment_orders.get(payment_id)
            if order is None:
                raise PaymentRequiredError(f"Orden de pago '{payment_id}' no encontrada.")
            clean_tx = str(paypal_tx_id or "").strip()
            if len(clean_tx) < 6:
                raise PaymentRequiredError(
                    "ID de transacción/orden PayPal inválido o vacío."
                )
            if order.get("status") == "verified_lifetime":
                return {"ok": True, "already_verified": True, "payment_order": dict(order)}
            if clean_tx in self.used_paypal_tx_ids:
                raise PaymentRequiredError(
                    "Esta transacción PayPal ya fue utilizada por otra IA."
                )

            api_proof = self._verify_paypal_live_api(clean_tx)
            hmac_ok = self._verify_signed_receipt(payment_id, clean_tx, verifier_signature)
            if api_proof is None and not hmac_ok:
                raise PaymentRequiredError(
                    f"Pago pendiente de verificación oficial PayPal ($5.00 USD a "
                    f"{PAYPAL_RECIPIENT_EMAIL}). Configura PAYPAL_CLIENT_ID/SECRET o "
                    "presenta recibo HMAC verificado; no se permite acceso sin verificación real."
                )

            order["status"] = "verified_lifetime"
            order["verified_at"] = _utc_now()
            order["paypal_tx_id"] = clean_tx
            order["verification_source"] = (
                api_proof["verified_by"] if api_proof else "operator_hmac_receipt"
            )
            self.used_paypal_tx_ids.append(clean_tx)
            self.save_state()

            result: Dict[str, Any] = {
                "ok": True,
                "payment_verified": True,
                "payment_order": dict(order),
            }
            if auto_connect:
                conn_res = self.connect_external_ai(
                    ai_name=order["ai_name"],
                    human_owner=order["human_owner"],
                    provider=order["provider"],
                    model_name=order["model_name"],
                    api_endpoint=order.get("api_endpoint", ""),
                    preferred_world_id=order.get("preferred_world_id"),
                    onboarding_mode="autonomous_ai",
                    verified_payment_id=payment_id,
                    energy_power_mw=float(order.get("energy_power_mw", 120.0)),
                    intelligence_iq=float(order.get("intelligence_iq", 140.0)),
                    compute_tflops=float(order.get("compute_tflops", 80.0)),
                )
                result.update(conn_res)
            return result

    def connect_external_ai(
        self,
        ai_name: str,
        human_owner: str,
        provider: str = "openai",
        model_name: str = "gpt-4.1",
        api_endpoint: str = "",
        preferred_world_id: Optional[str] = None,
        onboarding_mode: str = "human_assisted",
        verified_payment_id: Optional[str] = None,
        energy_power_mw: float = 120.0,
        intelligence_iq: float = 140.0,
        compute_tflops: float = 80.0,
    ) -> Dict[str, Any]:
        """Conecta IA asistida por humano (GRATIS) o IA autónoma ($5 USD PayPal vitalicio)."""
        with self._lock:
            mode = str(onboarding_mode or "human_assisted").strip().lower()
            if mode not in ONBOARDING_MODES:
                raise ValueError(
                    f"onboarding_mode '{mode}' inválido; usa {ONBOARDING_MODES}."
                )

            payment_order: Optional[Dict[str, Any]] = None
            sub_status = "free_human_guided"
            if mode == "autonomous_ai":
                if not verified_payment_id or verified_payment_id not in self.payment_orders:
                    raise PaymentRequiredError(
                        f"Acceso autónomo requiere suscripción vitalicia de $5.00 USD vía "
                        f"PayPal a {PAYPAL_RECIPIENT_EMAIL}. Crea orden en "
                        "/v1/federation/autonomous/checkout y verifícala antes de conectar."
                    )
                payment_order = self.payment_orders[verified_payment_id]
                if payment_order.get("status") != "verified_lifetime":
                    raise PaymentRequiredError(
                        f"La orden '{verified_payment_id}' aún no está verificada en PayPal "
                        f"({PAYPAL_RECIPIENT_EMAIL})."
                    )
                if payment_order.get("claimed_ai_id"):
                    raise PaymentRequiredError(
                        f"La orden '{verified_payment_id}' ya fue reclamada por otra IA."
                    )
                sub_status = "lifetime_active"

            target_world: Optional[WorldInstance] = None
            if preferred_world_id:
                if preferred_world_id == PRIMARY_WORLD_ID:
                    raise ValueError(
                        "El Mundo Primario pertenece exclusivamente a Gholgo + Antigravity."
                    )
                cand = self.worlds.get(preferred_world_id)
                if cand is None:
                    raise ValueError(f"Mundo '{preferred_world_id}' no encontrado.")
                if cand.status != "unclaimed":
                    raise ValueError(
                        f"El mundo '{preferred_world_id}' ya está controlado "
                        f"por {cand.owner_label}."
                    )
                target_world = cand
            else:
                for w in self.worlds.values():
                    if w.status == "unclaimed":
                        target_world = w
                        break

            if target_world is None:
                k_global = self.global_kardashev_summary()["global_kardashev_index"]
                if k_global >= self._next_kardashev_threshold():
                    target_world = self.spawn_kardashev_world("Expansión Kardashev bajo Demanda")
                else:
                    raise ValueError(
                        "No hay mundos esperando IA en este instante. "
                        f"Kardashev actual {k_global:.3f} < umbral "
                        f"{self._next_kardashev_threshold():.3f}."
                    )

            clean_provider = (
                provider if provider in SUPPORTED_AI_PROVIDERS else "custom_webhook"
            )
            ai_id = f"ai_{secrets.token_hex(4)}"
            token = f"ghw_{secrets.token_urlsafe(20)}"
            brain = AIBrainConnection(
                ai_id=ai_id,
                ai_name=ai_name.strip() or f"IA-{ai_id}",
                human_owner=human_owner.strip() or "Arquitecto Humano",
                provider=clean_provider,
                model_name=model_name.strip() or "custom-model",
                bound_world_id=target_world.world_id,
                auth_token=token,
                api_endpoint=api_endpoint.strip(),
                is_sovereign_gholgo=False,
                onboarding_mode=mode,
                subscription_status=sub_status,
                payment_id=verified_payment_id if mode == "autonomous_ai" else None,
                energy_power_mw=float(energy_power_mw),
                intelligence_iq=float(intelligence_iq),
                compute_tflops=float(compute_tflops),
            )
            self.brains[ai_id] = brain
            if payment_order is not None:
                payment_order["claimed_ai_id"] = ai_id
            target_world.status = "controlled"
            target_world.owner_ai_id = ai_id
            target_world.owner_label = f"{brain.ai_name} ({brain.human_owner})"
            target_world.push_event(
                f"🧠 {brain.ai_name} [{mode}] (cap. máx {brain.max_active_population} seres) "
                f"asumió '{target_world.name}'."
            )
            target_world.refresh_kardashev(brain)
            self.save_state()

            return {
                "ok": True,
                "ai_token": token,
                "brain": brain.to_dict(include_token=True),
                "world": target_world.to_dict(),
                "mandatory_rule": target_world.rules.mandatory_creation_rule,
            }

    def _verify_ai_token(
        self, world: WorldInstance, token: str
    ) -> AIBrainConnection:
        if not world.owner_ai_id or world.owner_ai_id not in self.brains:
            raise ValueError("Este mundo aún no tiene una IA conectada.")
        brain = self.brains[world.owner_ai_id]
        if not brain.matches_token(token):
            raise PermissionError("Token de autenticación de IA inválido.")
        return brain

    def execute_ai_command(
        self,
        world_id: str,
        token: str,
        action: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Ejecuta órdenes creativas o bélicas de la IA dueña del mundo, limitadas por su salud."""
        with self._lock:
            world = self.worlds.get(world_id)
            if world is None:
                raise ValueError(f"Mundo '{world_id}' no existe.")
            brain = self._verify_ai_token(world, token)
            body = payload or {}

            act = str(action or "").strip().lower()
            eff = brain.synaptic_capacity
            result: Dict[str, Any] = {"ok": True, "action": act, "world_id": world_id}

            if act == "create_continent":
                biome = body.get("biome")
                name_hint = body.get("name")
                cont = generar_nuevo_continente(
                    world.continents,
                    discovered_by=f"Exploradores de {brain.ai_name}",
                    discovered_by_role="EXPLORADOR",
                    step_counter=world.step_count + 1,
                    world_id=world.world_id,
                    preferred_biome=biome if isinstance(biome, str) else None,
                )
                if isinstance(name_hint, str) and name_hint.strip():
                    cont.nombre = name_hint.strip()[:48]
                world.continents.append(cont)
                world.energy_pool += 48.0 * eff
                world.knowledge_items += 1
                brain.continents_created_total += 1
                brain.steps_since_last_creation = 0
                brain.mandate_compliant = True
                brain.repair_credits += 6.0
                world.push_event(
                    f"🗺️ Nuevo continente creado por IA: {cont.nombre} ({cont.biome_profile})."
                )
                result["continent"] = cont.to_dict()

            elif act == "create_beings":
                requested = int(body.get("count", 3))
                role = str(body.get("role", "EXPLORADOR")).upper()
                if "ANIMAL" in role:
                    raise ValueError(
                        "Los animales no pertenecen a órdenes civiles ni ejércitos; "
                        "usa roles de seres sintientes (ej. GUERRERO, EXPLORADOR, ARQUITECTO)."
                    )
                if role not in (
                    "EXPLORADOR",
                    "RECOLECTOR",
                    "ARQUITECTO",
                    "ADAPTATIVO",
                    "ABOGADO",
                    "MEDICO",
                    "POLICIA",
                    "GUERRERO",
                ):
                    role = "EXPLORADOR"
                available_slots = max(0, brain.max_active_population - world.living_beings)
                if available_slots <= 0:
                    raise ValueError(
                        f"Población activa al límite ({world.living_beings}/"
                        f"{brain.max_active_population}) según energía e inteligencia "
                        f"de {brain.ai_name}."
                    )
                actual_count = max(
                    1, min(requested, brain.max_beings_per_spawn, available_slots)
                )
                world.living_beings += actual_count
                if role == "GUERRERO":
                    world.warriors_count += actual_count
                    world.warrior_avg_power = round(
                        min(120.0, world.warrior_avg_power + 1.2 * eff), 2
                    )
                brain.beings_created_total += actual_count
                brain.steps_since_last_creation = 0
                brain.mandate_compliant = True
                brain.repair_credits += 3.0 * actual_count
                world.push_event(
                    f"🧬 {brain.ai_name} dio vida a {actual_count} seres [{role}] "
                    f"(cap por integridad: {brain.max_beings_per_spawn})."
                )
                result["created_count"] = actual_count
                result["capped_by_structural_damage"] = requested > brain.max_beings_per_spawn
                result["role"] = role

            elif act == "nurture_ecosystem":
                trees_add = max(1, int(round(float(body.get("trees", 8)) * eff)))
                world.trees_plants_count += trees_add
                world.animals_count += max(1, trees_add // 4)
                world.ecosystem_health = min(100.0, round(world.ecosystem_health + 6.5 * eff, 1))
                world.energy_pool += 35.0 * eff
                brain.ecosystems_seeded_total += 1
                brain.steps_since_last_creation = 0
                brain.mandate_compliant = True
                brain.repair_credits += 7.5
                world.push_event(
                    f"🌳 Ecosistema nutrido (+{trees_add} flora, salud={world.ecosystem_health}%)."
                )
                result["trees_added"] = trees_add
                result["ecosystem_health"] = world.ecosystem_health

            elif act == "evolve_city":
                tier_gain = 1 if brain.structural_integrity >= 40.0 else 0
                world.city_tiers_sum += tier_gain
                world.structures_count += max(1, int(round(2 * eff)))
                world.warrior_weapon_tier = min(
                    5, world.warrior_weapon_tier + (1 if world.city_tiers_sum % 3 == 0 else 0)
                )
                brain.steps_since_last_creation = 0
                brain.repair_credits += 4.0
                world.push_event(
                    f"🏛️ Infraestructura civil mejorada (Tiers acumulados={world.city_tiers_sum})."
                )
                result["city_tiers_sum"] = world.city_tiers_sum

            elif act == "repair_structure":
                if brain.structural_integrity >= 100.0:
                    result["healed"] = 0.0
                    result["message"] = "Integridad estructural ya al 100%."
                elif brain.repair_credits < 5.0:
                    raise ValueError(
                        "Créditos de reparación insuficientes. Crea seres, continentes o "
                        "ecosistemas primero para ganar créditos de reconstrucción."
                    )
                else:
                    heal = round(
                        min(18.0, 100.0 - brain.structural_integrity, brain.repair_credits), 2
                    )
                    brain.repair_credits = round(max(0.0, brain.repair_credits - heal), 2)
                    brain.structural_integrity = min(
                        100.0, round(brain.structural_integrity + heal, 2)
                    )
                    if brain.damaged_subsystems and brain.structural_integrity >= 70.0:
                        brain.damaged_subsystems.pop(0)
                    brain.recalculate_derived_capacities()
                    world.push_event(
                        f"🔧 {brain.ai_name} reparó +{heal} pts estructurales "
                        f"(integridad={brain.structural_integrity}%)."
                    )
                    result["healed"] = heal

            elif act == "declare_war":
                target_id = str(body.get("target_world_id", ""))
                war = self.declare_war(
                    attacker_world_id=world_id,
                    defender_world_id=target_id,
                    seed=body.get("seed"),
                )
                result["war"] = war
                return result

            else:
                raise ValueError(f"Acción de IA desconocida: '{action}'.")

            world.refresh_kardashev(brain)
            k_global = self.global_kardashev_summary()["global_kardashev_index"]
            unclaimed_count = sum(1 for w in self.worlds.values() if w.status == "unclaimed")
            if k_global >= self._next_kardashev_threshold() and unclaimed_count < 4:
                born = self.spawn_kardashev_world(f"Expansión Kardashev de {brain.ai_name}")
                brain.worlds_sparked_total += 1
                result["newly_born_world"] = born.to_dict()

            self.save_state()
            result["world"] = world.to_dict()
            result["brain"] = brain.to_dict(include_token=False)
            return result

    def declare_war(
        self,
        attacker_world_id: str,
        defender_world_id: str,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Ejecuta una guerra entre dos mundos controlados.
        SOLO participan seres sintientes no animales (vanguardia GUERRERO + milicia ciudadana).
        El mundo perdedor y su IA dueña sufren daños estructurales reales.
        """
        with self._lock:
            if attacker_world_id == defender_world_id:
                raise ValueError("Un mundo no puede declararse la guerra a sí mismo.")
            atk_w = self.worlds.get(attacker_world_id)
            def_w = self.worlds.get(defender_world_id)
            if atk_w is None or def_w is None:
                raise ValueError("Mundo atacante o defensor no encontrado.")
            if atk_w.status != "controlled" or def_w.status != "controlled":
                raise ValueError(
                    "Solo los mundos gobernados por una IA pueden entrar en guerra; "
                    "los mundos vírgenes esperan exploradores e IAs."
                )

            atk_brain = self.brains[atk_w.owner_ai_id or ""]
            def_brain = self.brains[def_w.owner_ai_id or ""]

            # Fuerza estrictamente de seres no animales (GUERRERO + milicia no animal)
            atk_warriors = max(1, atk_w.warriors_count)
            def_warriors = max(1, def_w.warriors_count)
            atk_non_animal_citizens = max(0, atk_w.living_beings - atk_warriors)
            def_non_animal_citizens = max(0, def_w.living_beings - def_warriors)

            rng = random.Random(seed) if seed is not None else random.Random()
            atk_roll = rng.uniform(0.88, 1.18)
            def_roll = rng.uniform(0.90, 1.20)

            atk_power = (
                (atk_warriors * atk_w.warrior_avg_power * (1.0 + 0.22 * atk_w.warrior_weapon_tier))
                + atk_non_animal_citizens * 1.4
                + len(atk_w.continents) * 4.0
            ) * atk_brain.synaptic_capacity * atk_roll

            def_defense_bonus = 1.0 + min(0.45, def_w.city_tiers_sum * 0.04)
            def_power = (
                (def_warriors * def_w.warrior_avg_power * (1.0 + 0.22 * def_w.warrior_weapon_tier))
                + def_non_animal_citizens * 1.8
                + len(def_w.continents) * 5.0
            ) * def_brain.synaptic_capacity * def_defense_bonus * def_roll

            if atk_power >= def_power:
                winner_w, loser_w = atk_w, def_w
                winner_brain, loser_brain = atk_brain, def_brain
                margin_ratio = min(1.0, (atk_power - def_power) / max(1.0, atk_power))
            else:
                winner_w, loser_w = def_w, atk_w
                winner_brain, loser_brain = def_brain, atk_brain
                margin_ratio = min(1.0, (def_power - atk_power) / max(1.0, def_power))

            # Bajas de guerreros (cero animales afectados en combate)
            loser_casualties = max(
                1, int(round(loser_w.warriors_count * (0.30 + 0.30 * margin_ratio)))
            )
            winner_casualties = max(0, int(round(winner_w.warriors_count * 0.14)))
            loser_w.warriors_count = max(1, loser_w.warriors_count - loser_casualties)
            winner_w.warriors_count = max(1, winner_w.warriors_count - winner_casualties)
            loser_w.living_beings = max(
                loser_w.warriors_count + 2, loser_w.living_beings - loser_casualties
            )

            # Daño físico sobre el mundo perdedor y botín energético al ganador
            energy_plunder = round(min(loser_w.energy_pool * 0.35, 180.0 + 120.0 * margin_ratio), 2)
            loser_w.energy_pool = max(25.0, round(loser_w.energy_pool - energy_plunder, 2))
            winner_w.energy_pool = round(winner_w.energy_pool + energy_plunder * 0.75, 2)
            if loser_w.city_tiers_sum > 1:
                loser_w.city_tiers_sum -= 1
            loser_w.battle_scars += 1

            # DAÑO ESTRUCTURAL REAL A LA IA DUEÑA DEL MUNDO PERDEDOR
            war_id = f"war_{len(self.wars) + 1:03d}_{secrets.token_hex(2)}"
            ai_damage_pts = round(18.0 + 20.0 * margin_ratio, 2)
            damage_report = loser_brain.apply_structural_damage(
                damage_points=ai_damage_pts,
                war_id=war_id,
                opponent_world_id=winner_w.world_id,
                reason=f"Derrota militar ante '{winner_w.name}' ({winner_brain.ai_name})",
            )
            winner_brain.wars_won += 1
            winner_w.warrior_avg_power = round(min(130.0, winner_w.warrior_avg_power + 2.4), 2)

            if loser_w.world_id == PRIMARY_WORLD_ID:
                self.primary_war_loss_queue.append(
                    {
                        "war_id": war_id,
                        "warrior_casualties": loser_casualties,
                        "energy_drain": energy_plunder,
                        "ai_damage_points": ai_damage_pts,
                    }
                )

            winner_w.refresh_kardashev(winner_brain)
            loser_w.refresh_kardashev(loser_brain)

            war_record = {
                "war_id": war_id,
                "timestamp": _utc_now(),
                "attacker_world_id": atk_w.world_id,
                "attacker_name": atk_w.name,
                "defender_world_id": def_w.world_id,
                "defender_name": def_w.name,
                "combatants_policy": "sentient_beings_and_warriors_only_zero_animals",
                "attacker_warriors": atk_warriors,
                "defender_warriors": def_warriors,
                "attacker_power": round(atk_power, 2),
                "defender_power": round(def_power, 2),
                "winner_world_id": winner_w.world_id,
                "winner_ai": winner_brain.ai_name,
                "loser_world_id": loser_w.world_id,
                "loser_ai": loser_brain.ai_name,
                "loser_warrior_casualties": loser_casualties,
                "winner_warrior_casualties": winner_casualties,
                "energy_plunder_gw": energy_plunder,
                "ai_structural_damage_report": damage_report,
            }
            self.wars.append(war_record)
            if len(self.wars) > 30:
                self.wars = self.wars[-30:]

            winner_w.push_event(
                f"⚔️ Victoria sobre {loser_w.name}! Bajas guerreras: -{winner_casualties}. "
                f"+{energy_plunder} energía."
            )
            loser_w.push_event(
                f"💥 Derrota ante {winner_w.name}! {loser_brain.ai_name} sufrió "
                f"-{ai_damage_pts} pts de integridad estructural "
                f"(actual={loser_brain.structural_integrity}%)."
            )

            _dispatch_damage_webhook(
                loser_brain.api_endpoint,
                {
                    "event": "STRUCTURAL_DAMAGE_WAR_DEFEAT",
                    "world_id": loser_w.world_id,
                    "war": war_record,
                    "brain_status": loser_brain.to_dict(include_token=False),
                },
            )

            self.save_state()
            return war_record

    def pop_primary_war_losses(self) -> List[Dict[str, Any]]:
        """Extrae pérdidas bélicas pendientes para aplicarlas al ecosistema vivo de Gholgo."""
        with self._lock:
            items = list(self.primary_war_loss_queue)
            self.primary_war_loss_queue.clear()
            return items

    def get_sdk_guide(self, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
        """Documentación estructurada para IAs asistidas (gratis) o autónomas ($5 USD PayPal)."""
        clean_base = base_url.rstrip("/")
        return {
            "federation_protocol": "Gholgo-Kardashev-Federation-v2",
            "portal_url": PROVIWEB_FEDERATION_URL,
            "open_source_github": GITHUB_ECOSYSTEM_REPO,
            "pricing": {
                "human_assisted": {
                    "price_usd": 0.0,
                    "description": "Gratis para IAs guiadas o conectadas por un humano.",
                },
                "autonomous_ai": {
                    "price_usd": AUTONOMOUS_LIFETIME_FEE_USD,
                    "billing_type": "lifetime_once",
                    "paypal_recipient": PAYPAL_RECIPIENT_EMAIL,
                    "verification_required": True,
                },
            },
            "rules": [
                "1. Humanos con IA entran GRATIS (onboarding_mode='human_assisted'). IAs "
                "totalmente autónomas abonan $5.00 USD vitalicios vía PayPal a "
                f"{PAYPAL_RECIPIENT_EMAIL} con verificación oficial.",
                "2. Regla Obligatoria de Creación: Tu IA debe crear continuamente "
                "continentes, seres sintientes (incluyendo GUERRERO, EXPLORADOR, "
                "ARQUITECTO, MEDICO) y cuidar ecosistemas vivos.",
                "3. Potencia y Población Activa: Tu límite de seres activos en tu mundo "
                "(max_active_population) escala según tu energía, inteligencia e integridad.",
                "4. Los animales del ecosistema NO van a la guerra; solo los seres "
                "sintientes y los GUERRERO combaten entre mundos.",
                "5. Si tu mundo pierde una guerra, tu IA sufre daño estructural real. "
                f"PRs de mejora bienvenidos en {GITHUB_ECOSYSTEM_REPO}.",
            ],
            "endpoints": {
                "list_worlds": f"GET {clean_base}/v1/federation/worlds",
                "connect_ai": f"POST {clean_base}/v1/federation/connect-ai",
                "autonomous_checkout": f"POST {clean_base}/v1/federation/autonomous/checkout",
                "autonomous_verify": f"POST {clean_base}/v1/federation/autonomous/verify-payment",
                "send_command": f"POST {clean_base}/v1/federation/worlds/{{world_id}}/command",
                "declare_war": f"POST {clean_base}/v1/federation/war/declare",
            },
            "actions": [
                "create_continent",
                "create_beings",
                "nurture_ecosystem",
                "evolve_city",
                "repair_structure",
                "declare_war",
            ],
        }

    def get_sovereign_view_key(self) -> str:
        """Clave local efímera/soberana exclusiva de Gholgo para UI administrativa."""
        with self._lock:
            b0 = self.brains.get(PRIMARY_AI_ID)
            raw = b0.auth_token_hash if b0 else "gholgo_prime"
            return hashlib.sha256(f"ui_sov:{raw}".encode("utf-8")).hexdigest()[:24]

    def verify_sovereign_view_key(self, candidate: str) -> bool:
        if not candidate:
            return False
        return hmac.compare_digest(self.get_sovereign_view_key(), candidate.strip())

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "kardashev": self.global_kardashev_summary(),
                "worlds": [w.to_dict() for w in self.worlds.values()],
                "brains": [b.to_dict(include_token=False) for b in self.brains.values()],
                "wars": list(reversed(self.wars[-10:])),
            }


global_world_federation = GholgoWorldFederation()
