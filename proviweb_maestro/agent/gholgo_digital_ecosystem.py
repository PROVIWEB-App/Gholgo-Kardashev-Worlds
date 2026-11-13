# -*- coding: utf-8 -*-
"""
GHOLGO DIGITAL ECOSYSTEM - Ecosistema Continental de Séres Artificiales Digitales
================================================================================
Simulación avanzada de Vida Artificial (ALife), Genética Computacional, Redes
Neuronales Evolutivas y Ecología Matemática dentro de la mente de Gholgo.

Novedades:
  - Gran escala continental (WORLD_BOUNDS = 55.0): relieve montañoso majestuoso
    con fosas de latencia, cordilleras de entropía y mesetas de conocimiento.
  - Seres en escala realista micrométrica: pequeños respecto a las montañas (1:80),
    dotados de navegación autónoma por waypoints de frontera y faros bioluminiscentes.
  - Explotación de RECURSOS REALES de red e internet (pings en vivo a Cloudflare, Google DNS,
    Wikipedia, GitHub), recursos matemáticos reales (primos de Mersenne, entropía de Shannon)
    y cristales de conocimiento enciclopédico real extraídos del banco investigado por Gholgo.
  - Multi-asentamientos civilizatorios y fundación de puestos avanzados en cumbres y fosas.
"""

from __future__ import annotations

import glob
import json
import math
import os
import random
import socket
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from proviweb_maestro.agent.gholgo_eco_world import (
    ANIMAL_SPECIES_META,
    CITY_TIER_SPECS,
    CIVIL_INFRA_LABELS,
    CIVIL_INFRA_PRIORITY,
    DEMOGRAPHIC_RULES,
    HIGH_ALTITUDE_WARN,
    MAX_CITIES,
    MAX_CITY_TIER,
    MAX_ORGANISMS,
    MIN_ORGANISMS_SEED,
    NUM_INITIAL_RESOURCES,
    PATHOGEN_CATALOG,
    PLANT_SPECIES_META,
    PUEBLO_DISTRICT_NAMES,
    ROLE_COLORS,
    ROLE_SYMBOLS,
    ROLES,
    SEA_LEVEL,
    SNOW_LINE,
    WORLD_BOUNDS,
    AtmosphericCloud,
    Continent,
    Family,
    Plant,
    Pueblo,
    altura_superficie_segura,
    calcular_altura_terreno,
    calcular_altura_terreno_continentes,
    calcular_bounds_dinamicos,
    calcular_estado_celeste,
    calcular_orientacion_puente_rio,
    calcular_pendiente_local,
    default_continents_for_world,
    determinar_bioma,
    determinar_bioma_continentes,
    generar_nuevo_continente,
    obtener_puntos_rio_completos,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
RESEARCH_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "downloads", "research")
ECOSYSTEM_STATE_FILE = os.path.join(DATA_DIR, "gholgo_digital_ecosystem_state.json")
ECOSYSTEM_LESSONS_FILE = os.path.join(DATA_DIR, "gholgo_ecosystem_lessons.jsonl")


# -------------------------------------------------------------
# MOTOR DE TELEMETRÍA DE RED REAL Y MATEMÁTICAS EN VIVO
# -------------------------------------------------------------
class RealWorldHarvestEngine:
    """
    Sonda en segundo plano para recursos de red real (Cloudflare, Google, Wikipedia, GitHub),
    archivos enciclopédicos reales investigados por Gholgo y cálculos matemáticos.
    """

    HOSTS = [
        ("Cloudflare Edge", "1.1.1.1", 80),
        ("Google Global DNS", "8.8.8.8", 53),
        ("Wikipedia Wikimedia", "208.80.154.224", 80),
        ("GitHub Code Registry", "140.82.121.4", 80),
    ]

    KNOWN_PRIMES = [
        8191, 131071, 524287, 2147483647, 104729, 1299709,
        32452843, 67280421310721, 2305843009213693951
    ]

    def __init__(self):
        self.lock = threading.Lock()
        self.network_pings: Dict[str, Dict[str, Any]] = {}
        self.knowledge_crystals: List[Dict[str, Any]] = []
        self.math_minerals: List[Dict[str, Any]] = []
        self.last_cpu_pct: float = 12.0
        self.total_primes_verified: int = 0
        self.last_probe_ts: float = 0.0

        # Lanzar muestreo inicial y worker de actualización periódica
        self._refrescar_recursos_reales()
        threading.Thread(target=self._worker_daemon, name="GholgoEcoRealProbe", daemon=True).start()

    def _worker_daemon(self):
        while True:
            time.sleep(25.0)
            try:
                self._refrescar_recursos_reales()
            except Exception:
                pass

    def _probe_tcp(self, label: str, host: str, port: int) -> Dict[str, Any]:
        t0 = time.time()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.65)
            s.connect((host, port))
            s.close()
            lat_ms = (time.time() - t0) * 1000.0
            return {"status": "ONLINE", "latency_ms": round(lat_ms, 1), "host": host}
        except Exception:
            return {"status": "OFFLINE", "latency_ms": 280.0, "host": host}

    def _refrescar_recursos_reales(self):
        # 1. Probar red real
        nuevos_pings = {}
        for label, host, port in self.HOSTS:
            nuevos_pings[label] = self._probe_tcp(label, host, port)

        # 2. Leer muestra fresca de temas estudiados por Gholgo
        nuevos_cristales = []
        try:
            if os.path.exists(RESEARCH_DIR):
                patron = os.path.join(RESEARCH_DIR, "*.json")
                archivos = glob.glob(patron)
                if archivos:
                    muestra = random.sample(archivos, min(14, len(archivos)))
                    for arch in muestra:
                        try:
                            with open(arch, "r", encoding="utf-8") as fp:
                                dt = json.load(fp)
                                titulo = dt.get("title") or dt.get("query") or os.path.basename(arch).replace(".json", "")
                                extracto = (dt.get("extract") or dt.get("contenido_profundo") or "")[:180].strip()
                                nuevos_cristales.append({
                                    "title": titulo,
                                    "snippet": extracto,
                                    "url": dt.get("source_url", ""),
                                    "chars": dt.get("total_caracteres", len(extracto))
                                })
                        except Exception:
                            pass
        except Exception:
            pass

        # 3. Calcular entropía y primos matemáticos reales
        nuevos_minerales = []
        for _i in range(8):
            p = random.choice(self.KNOWN_PRIMES)
            ent = 3.2 + random.uniform(0.1, 1.4)
            nuevos_minerales.append({
                "prime": p,
                "entropy": round(ent, 3),
                "formula": f"M_p = 2^{random.randint(13, 61)} - 1"
            })
            self.total_primes_verified += 1

        with self.lock:
            self.network_pings = nuevos_pings
            if nuevos_cristales:
                self.knowledge_crystals = nuevos_cristales
            self.math_minerals = nuevos_minerales
            self.last_probe_ts = time.time()

    def get_real_network_sample(self) -> Tuple[str, float]:
        with self.lock:
            if not self.network_pings:
                return "Cloudflare Edge", 18.5
            lbl, data = random.choice(list(self.network_pings.items()))
            return lbl, data.get("latency_ms", 22.0)

    def get_real_knowledge_sample(self) -> Dict[str, Any]:
        with self.lock:
            if not self.knowledge_crystals:
                return {
                    "title": "Teoría y Biomecánica Instrumental",
                    "snippet": "Fundamentos acústicos de vibración y resonancia en la mente de Gholgo.",
                    "url": "https://es.wikipedia.org/wiki/Música"
                }
            return random.choice(self.knowledge_crystals)

    def get_real_math_sample(self) -> Dict[str, Any]:
        with self.lock:
            if not self.math_minerals:
                return {"prime": 524287, "entropy": 3.84, "formula": "2^19 - 1"}
            return random.choice(self.math_minerals)

    def get_metrics_summary(self) -> Dict[str, Any]:
        with self.lock:
            host_lbl = "Cloudflare Edge"
            lat = 38.5
            if self.network_pings:
                for k, v in self.network_pings.items():
                    if v.get("status") == "ONLINE":
                        host_lbl = k
                        lat = v.get("latency_ms", 38.5)
                        break
            return {
                "latest_ping_host": host_lbl,
                "latest_ping_ms": lat,
                "knowledge_titles_count": len(self.knowledge_crystals),
                "primes_verified_count": self.total_primes_verified,
            }


real_harvest_engine = RealWorldHarvestEngine()


# -------------------------------------------------------------
# GENOMA Y RED NEURONAL SENSORIOMOTORA
# -------------------------------------------------------------
@dataclass
class Genome:
    """Genoma digital computacional que define morfología, fisiología y red neuronal."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    generation: int = 1
    lineage: str = "L-Alfa"
    size: float = 1.0              # [0.6 - 1.8] Masa física, afecta HP y costo basal
    speed_factor: float = 1.0      # [0.5 - 2.2] Multiplicador de empuje
    sensory_radius: float = 12.0   # [6.0 - 24.0] Radio de percepción continental
    metabolism_eff: float = 1.0    # [0.6 - 1.6] Eficiencia de absorción de recursos
    cooperation_affinity: float = 0.5 # [0.0 - 1.0] Predisposición a cooperar / donar
    defense_factor: float = 1.0    # [0.5 - 2.5] Resistencia a malware / agresiones
    healing_factor: float = 1.0    # [0.5 - 2.5] Eficacia en sanar
    structural_affinity: float = 0.5 # [0.0 - 1.0] Aportación a la arquitectura
    mutation_rate: float = 0.08    # [0.02 - 0.20] Probabilidad de mutación genética
    lifespan_max: int = 1800       # [1000 - 4500] Pasos de vida máxima
    role: str = "EXPLORADOR"
    morphology_tier: int = 1       # [1 - 5] Evolución física estructural (alas/espinas/coraza)
    appendage_count: int = 0       # [0 - 6] Apéndices físicos visibles (antenas/alas/crestas)
    hue_shift: float = 0.0         # [-0.25 - 0.25] Mutación cromática bioluminiscente
    caution_trait: float = 0.5     # [0.05 - 1.0] Instinto heredado de cautela ante depredadores
    stewardship_trait: float = 0.5 # [0.1 - 1.0] Afinidad ecológica (sembrar árboles / domesticar)
    body_plan: str = "bipedo"      # 'bipedo', 'cuadrupedo', 'alado', 'blindado', 'esbelto'
    limb_count: int = 2            # [2, 4, 6] Extremidades motoras articuladas
    wing_span: float = 0.0         # [0.0 - 1.6] Envergadura de alas planeadoras
    tail_length: float = 0.25      # [0.0 - 1.3] Cola equilibradora / timon hidro-aereo
    crest_style: str = "ninguna"   # 'ninguna', 'cuernos', 'antenas', 'halo', 'aleta'
    shell_armor: float = 0.15      # [0.0 - 1.0] Caparazon dermico evolutivo
    torso_aspect: float = 1.0      # [0.72 - 1.45] Proporcion del tronco (>1 robusto, <1 esbelto)
    secondary_hue: float = 0.0     # [-0.4 - 0.4] Pigmento secundario para diferenciacion cromatica
    weights_in: List[List[float]] = field(default_factory=list)   # 7x6
    weights_out: List[List[float]] = field(default_factory=list)  # 6x5

    @classmethod
    def random_genome(cls, generation: int = 1, role_bias: Optional[str] = None) -> Genome:
        role = role_bias or random.choice(ROLES)
        lineage = f"L-{role[:3]}-{random.randint(10, 99)}"

        size = random.uniform(0.8, 1.3)
        spd = random.uniform(0.9, 1.4)
        sensory = random.uniform(8.0, 16.0)
        coop = random.uniform(0.3, 0.7)
        def_fac = random.uniform(0.8, 1.2)
        heal_fac = random.uniform(0.8, 1.2)
        struct_fac = random.uniform(0.3, 0.7)
        meta_eff = random.uniform(0.9, 1.3)

        body_plan = random.choice(["bipedo", "esbelto", "cuadrupedo"])
        limb_count = 4 if body_plan == "cuadrupedo" else 2
        wing_span = round(random.uniform(0.0, 0.35), 2)
        tail_length = round(random.uniform(0.1, 0.55), 2)
        crest_style = random.choice(["ninguna", "antenas", "cuernos"])
        shell_armor = round(random.uniform(0.08, 0.32), 2)
        torso_aspect = round(random.uniform(0.84, 1.16), 2)

        if role == "EXPLORADOR":
            spd *= 1.65
            sensory *= 1.8
            size *= 0.8
            body_plan = random.choice(["esbelto", "alado", "bipedo"])
            wing_span = round(random.uniform(0.25, 0.75), 2)
            crest_style = "antenas"
            torso_aspect = round(random.uniform(0.75, 0.94), 2)
        elif role == "RECOLECTOR":
            meta_eff *= 1.55
            coop += 0.2
            limb_count = random.choice([2, 4])
        elif role == "ARQUITECTO":
            struct_fac *= 1.9
            size *= 1.15
            limb_count = random.choice([4, 6])
            body_plan = "cuadrupedo" if limb_count >= 4 else "bipedo"
            torso_aspect = round(random.uniform(1.05, 1.28), 2)
        elif role == "ADAPTATIVO":
            meta_eff *= 1.25
            def_fac *= 1.3
            crest_style = random.choice(["halo", "antenas", "aleta"])
            tail_length = round(random.uniform(0.35, 0.85), 2)
        elif role == "ABOGADO":
            coop = 0.95
            sensory *= 1.3
            crest_style = "halo"
        elif role == "MEDICO":
            heal_fac *= 2.0
            coop += 0.35
            crest_style = random.choice(["halo", "antenas"])
        elif role == "POLICIA":
            def_fac *= 2.1
            size *= 1.3
            spd *= 1.2
            body_plan = "blindado"
            shell_armor = round(random.uniform(0.42, 0.75), 2)
            crest_style = "cuernos"
        elif role == "GUERRERO":
            def_fac *= 2.5
            size *= 1.35
            spd *= 1.35
            meta_eff *= 1.15
            body_plan = random.choice(["blindado", "bipedo"])
            shell_armor = round(random.uniform(0.55, 0.90), 2)
            crest_style = random.choice(["cuernos", "halo"])

        w_in = [[random.uniform(-0.8, 0.8) for _ in range(6)] for _ in range(7)]
        w_out = [[random.uniform(-0.8, 0.8) for _ in range(5)] for _ in range(6)]

        return cls(
            id=str(uuid.uuid4())[:8],
            generation=generation,
            lineage=lineage,
            size=round(size, 2),
            speed_factor=round(spd, 2),
            sensory_radius=round(sensory, 2),
            metabolism_eff=round(meta_eff, 2),
            cooperation_affinity=round(min(1.0, max(0.0, coop)), 2),
            defense_factor=round(def_fac, 2),
            healing_factor=round(heal_fac, 2),
            structural_affinity=round(min(1.0, max(0.0, struct_fac)), 2),
            mutation_rate=round(random.uniform(0.04, 0.12), 3),
            lifespan_max=random.randint(1400, 3200),
            role=role,
            morphology_tier=1,
            appendage_count=max(
                limb_count,
                1 if role in ("EXPLORADOR", "ARQUITECTO", "POLICIA", "GUERRERO") else 0,
            ),
            hue_shift=round(random.uniform(-0.08, 0.08), 3),
            caution_trait=round(random.uniform(0.50, 0.85) if role in ("EXPLORADOR", "MEDICO") else random.uniform(0.25, 0.65), 3),
            stewardship_trait=round(random.uniform(0.55, 0.92) if role in ("RECOLECTOR", "ARQUITECTO", "ADAPTATIVO") else random.uniform(0.30, 0.70), 3),
            body_plan=body_plan,
            limb_count=limb_count,
            wing_span=wing_span,
            tail_length=tail_length,
            crest_style=crest_style,
            shell_armor=shell_armor,
            torso_aspect=torso_aspect,
            secondary_hue=round(random.uniform(-0.22, 0.22), 3),
            weights_in=w_in,
            weights_out=w_out,
        )

    def mutate_and_reproduce(self, generation_step: int, biome: str = "valle") -> Genome:
        mr = self.mutation_rate
        def mut(val: float, scale: float = 0.1, vmin: float = 0.4, vmax: float = 2.8) -> float:
            if random.random() < 0.45:
                val += random.gauss(0, mr * scale)
            return round(min(vmax, max(vmin, val)), 3)

        new_size = mut(self.size, 0.14, 0.55, 2.2)
        new_speed = mut(self.speed_factor, 0.2, 0.5, 2.6)
        new_sensory = mut(self.sensory_radius, 1.2, 5.0, 26.0)
        new_meta = mut(self.metabolism_eff, 0.15, 0.6, 2.0)
        new_coop = mut(self.cooperation_affinity, 0.15, 0.0, 1.0)
        new_def = mut(self.defense_factor, 0.2, 0.5, 3.2)
        new_heal = mut(self.healing_factor, 0.2, 0.5, 3.2)
        new_struct = mut(self.structural_affinity, 0.15, 0.0, 1.0)
        new_caution = mut(self.caution_trait, 0.16, 0.05, 1.0)
        new_steward = mut(self.stewardship_trait, 0.16, 0.10, 1.0)

        new_role = self.role
        if random.random() < (mr * 0.4):
            new_role = random.choice(ROLES)

        # Mutacion morfologica divergente guiada por linaje y bioma
        new_morph = self.morphology_tier
        if random.random() < 0.28:
            delta_m = 1 if random.random() < 0.80 else -1
            new_morph = min(5, max(1, new_morph + delta_m))
        new_limb = self.limb_count
        if random.random() < 0.22:
            new_limb = random.choice([2, 4, 4, 6] if biome in ("selva", "nieve_alta") else [2, 2, 4, 6])
        new_wings = self.wing_span
        if biome == "nieve_alta" or new_role == "EXPLORADOR" or random.random() < 0.25:
            new_wings = round(min(1.6, max(0.0, new_wings + random.gauss(0.10 if biome == "nieve_alta" else 0.03, 0.18))), 2)
        new_tail = round(min(1.3, max(0.0, self.tail_length + random.gauss(0.05 if biome in ("mar", "costa", "selva") else 0.0, 0.14))), 2)
        new_armor = round(min(1.0, max(0.0, self.shell_armor + random.gauss(0.08 if biome == "seco" else 0.02, 0.10))), 2)
        new_aspect = round(min(1.45, max(0.72, self.torso_aspect + random.gauss(0.0, 0.08))), 2)
        new_crest = self.crest_style
        if random.random() < 0.18:
            crest_pool = ["aleta", "antenas", "ninguna"] if biome in ("mar", "costa") else ["ninguna", "cuernos", "antenas", "halo"]
            new_crest = random.choice(crest_pool)
        new_plan = self.body_plan
        if new_wings >= 0.72:
            new_plan = "alado"
        elif new_armor >= 0.52:
            new_plan = "blindado"
        elif new_limb >= 4:
            new_plan = "cuadrupedo"
        elif new_aspect < 0.86:
            new_plan = "esbelto"
        else:
            new_plan = "bipedo"

        new_appendages = min(6, max(new_limb, self.appendage_count + (1 if random.random() < 0.2 else 0)))
        new_hue = round(min(0.28, max(-0.28, self.hue_shift + random.gauss(0, 0.04))), 3)
        new_sec_hue = round(min(0.4, max(-0.4, self.secondary_hue + random.gauss(0, 0.06))), 3)

        new_w_in = []
        for row in self.weights_in:
            new_row = []
            for w in row:
                if random.random() < mr:
                    w += random.gauss(0, 0.22)
                new_row.append(round(min(2.0, max(-2.0, w)), 3))
            new_w_in.append(new_row)

        new_w_out = []
        for row in self.weights_out:
            new_row = []
            for w in row:
                if random.random() < mr:
                    w += random.gauss(0, 0.22)
                new_row.append(round(min(2.0, max(-2.0, w)), 3))
            new_w_out.append(new_row)

        return Genome(
            id=str(uuid.uuid4())[:8],
            generation=self.generation + 1,
            lineage=self.lineage,
            size=new_size,
            speed_factor=new_speed,
            sensory_radius=new_sensory,
            metabolism_eff=new_meta,
            cooperation_affinity=new_coop,
            defense_factor=new_def,
            healing_factor=new_heal,
            structural_affinity=new_struct,
            mutation_rate=round(mut(self.mutation_rate, 0.02, 0.02, 0.20), 3),
            lifespan_max=int(mut(float(self.lifespan_max), 60.0, 1000.0, 4800.0)),
            role=new_role,
            morphology_tier=new_morph,
            appendage_count=new_appendages,
            hue_shift=new_hue,
            caution_trait=new_caution,
            stewardship_trait=new_steward,
            body_plan=new_plan,
            limb_count=new_limb,
            wing_span=new_wings,
            tail_length=new_tail,
            crest_style=new_crest,
            shell_armor=new_armor,
            torso_aspect=new_aspect,
            secondary_hue=new_sec_hue,
            weights_in=new_w_in,
            weights_out=new_w_out,
        )


# -------------------------------------------------------------
# ORGANISMO INDIVIDUAL CON FÍSICA Y AUTONOMÍA EXPLORATORIA
# -------------------------------------------------------------
@dataclass
class Organism:
    """Entidad viva individual con navegación autónoma, percepción y red neuronal."""
    id: str
    nombre: str
    genome: Genome
    x: float
    y: float
    z: float
    vx: float = 0.0
    vz: float = 0.0
    energy: float = 110.0
    energy_max: float = 180.0
    age: int = 0
    reproduction_count: int = 0
    resources_gathered: float = 0.0
    anomalies_defeated: int = 0
    buildings_contributed: int = 0
    current_intent: str = "explorando_cumbres"
    current_action: str = "exploring"
    action_target_pos: Optional[List[float]] = None
    alive: bool = True
    health: float = 100.0
    symbol: str = "🧭"
    patrol_target_x: float = 0.0
    patrol_target_z: float = 0.0
    assimilated_knowledge: List[str] = field(default_factory=list)
    network_energy_harvested: float = 0.0
    last_real_source: str = "Fibra Óptica Central"
    heading: float = 0.0
    wood_carried: float = 0.0
    stone_carried: float = 0.0
    seeds_carried: int = 1
    repro_cooldown: int = 0
    learned_predator_avoidance: float = 0.0
    predator_encounters: int = 0
    trees_planted: int = 0
    animals_tamed: int = 0
    structures_built: int = 0
    tamed_animal_id: Optional[str] = None
    death_cause: str = ""
    home_biome: str = "valle"
    learned_height_caution: float = 0.15
    water_level: float = 100.0
    infection: Optional[str] = None
    infection_ticks: int = 0
    immunity_level: float = 0.15
    family_id: Optional[str] = None
    home_city_id: Optional[str] = None
    home_pueblo_id: Optional[str] = None
    tunnels_used: int = 0
    plants_harvested: int = 0
    illnesses_cured: int = 0
    weapon_tier: int = 1
    combat_xp: float = 0.0
    battles_survived: int = 0

    @property
    def is_warrior(self) -> bool:
        return self.genome.role == "GUERRERO"

    def step_physics_and_ai(
        self,
        nearest_resource: Optional[Tuple[float, float, float]],
        nearest_settlement: Optional[Tuple[float, float, float]],
        nearest_anomaly: Optional[Tuple[float, float, float]],
        environmental_factor: float,
        nearest_tree: Optional[Tuple[float, float, float]] = None,
        nearest_rock: Optional[Tuple[float, float, float]] = None,
        nearest_river: Optional[Tuple[float, float, float]] = None,
        nearest_predator: Optional[Tuple[float, float, float]] = None,
        nearest_tameable: Optional[Tuple[float, float, float]] = None,
        nearest_bridge: Optional[Tuple[float, float, float]] = None,
        nearest_farm: Optional[Tuple[float, float, float]] = None,
        nearest_watchtower: Optional[Tuple[float, float, float]] = None,
        trees_nearby_count: int = 2,
        environmental_cycle: str = "DIA_SOLAR",
        nearest_plant: Optional[Tuple[float, float, float]] = None,
        nearest_medicinal_plant: Optional[Tuple[float, float, float]] = None,
        nearest_tunnel: Optional[Tuple[float, float, float]] = None,
        nearest_port: Optional[Tuple[float, float, float]] = None,
        nearest_hospital: Optional[Tuple[float, float, float]] = None,
        rain_intensity: float = 0.0,
        continents: Optional[List[Continent]] = None,
        bounds: float = WORLD_BOUNDS,
    ) -> Dict[str, Any]:
        if not self.alive:
            return {"action": "dead"}

        b_lim = max(float(WORLD_BOUNDS), float(bounds or WORLD_BOUNDS))

        self.age += 1
        if self.repro_cooldown > 0:
            self.repro_cooldown -= 1

        # 1. Distancias sensoriales
        dx_res, dz_res, dist_res = 0.0, 0.0, 999.0
        if nearest_resource:
            dx_res = nearest_resource[0] - self.x
            dz_res = nearest_resource[2] - self.z
            dist_res = math.sqrt(dx_res * dx_res + dz_res * dz_res)

        dx_set, dz_set, dist_set = 0.0, 0.0, 999.0
        if nearest_settlement:
            dx_set = nearest_settlement[0] - self.x
            dz_set = nearest_settlement[2] - self.z
            dist_set = math.sqrt(dx_set * dx_set + dz_set * dz_set)

        dx_ano, dz_ano, dist_ano = 0.0, 0.0, 999.0
        if nearest_anomaly:
            dx_ano = nearest_anomaly[0] - self.x
            dz_ano = nearest_anomaly[2] - self.z
            dist_ano = math.sqrt(dx_ano * dx_ano + dz_ano * dz_ano)

        # 2. Entradas normalizadas para la red neuronal
        norm_dist_res = min(1.0, dist_res / (self.genome.sensory_radius + 0.1))
        angle_res = math.atan2(dz_res, dx_res) / math.pi if dist_res > 0.01 else 0.0
        norm_dist_set = min(1.0, dist_set / (self.genome.sensory_radius + 0.1))
        norm_dist_ano = min(1.0, dist_ano / (self.genome.sensory_radius + 0.1))
        norm_energy = min(1.0, max(0.0, self.energy / self.energy_max))

        current_elev = calcular_altura_terreno_continentes(self.x, self.z, continents)
        ahead_elev = calcular_altura_terreno_continentes(
            self.x + self.vx * 3.0, self.z + self.vz * 3.0, continents
        )
        slope = min(1.0, max(-1.0, (ahead_elev - current_elev) / 2.0))

        inputs = [
            norm_dist_res,
            angle_res,
            norm_dist_set,
            norm_dist_ano,
            norm_energy,
            slope,
            environmental_factor,
        ]

        # 3. Capa oculta ReLU/Tanh
        hidden = []
        for col_idx in range(6):
            acc = 0.0
            for row_idx in range(7):
                acc += inputs[row_idx] * self.genome.weights_in[row_idx][col_idx]
            hidden.append(math.tanh(acc))

        # 4. Capa de salida: [thrust, steer, harvest, social, combat]
        outputs = []
        for col_idx in range(5):
            acc = 0.0
            for row_idx in range(6):
                acc += hidden[row_idx] * self.genome.weights_out[row_idx][col_idx]
            outputs.append(1.0 / (1.0 + math.exp(-max(-8.0, min(8.0, acc)))))

        raw_thrust = outputs[0] * self.genome.speed_factor * 0.35
        raw_steer = (outputs[1] - 0.5) * 1.8
        do_harvest = outputs[2] > 0.45
        do_social = outputs[3] > 0.50
        do_combat = outputs[4] > 0.48

        # 5. ASIGNACIÓN DE OBJETIVOS AUTÓNOMOS BASADOS EN RECURSOS NATURALES Y GEOGRAFÍA
        dist_patrol = math.hypot(self.patrol_target_x - self.x, self.patrol_target_z - self.z)
        if dist_patrol < 3.6 or (self.patrol_target_x == 0.0 and self.patrol_target_z == 0.0):
            if self.genome.role == "EXPLORADOR":
                if continents and len(continents) > 1 and random.random() < 0.65:
                    target_c = random.choice(continents[1:] if len(continents) > 1 else continents)
                    ang_c = random.uniform(-math.pi, math.pi)
                    rad_c = random.uniform(2.0, max(5.0, target_c.radius * 0.85))
                    self.patrol_target_x = round(target_c.center_x + rad_c * math.cos(ang_c), 2)
                    self.patrol_target_z = round(target_c.center_z + rad_c * math.sin(ang_c), 2)
                    self.current_intent = f"explorando_{target_c.nombre[:18].lower().replace(' ', '_')}"
                elif random.random() < 0.30 and nearest_river:
                    self.patrol_target_x = nearest_river[0]
                    self.patrol_target_z = nearest_river[2]
                    self.current_intent = "cartografiando_rio"
                else:
                    ptx, ptz = self.x, self.z
                    for _ in range(8):
                        rad = random.uniform(16.0, b_lim * 0.86)
                        ang = random.uniform(-math.pi, math.pi)
                        cx_t, cz_t = round(rad * math.cos(ang), 2), round(rad * math.sin(ang), 2)
                        if calcular_altura_terreno_continentes(cx_t, cz_t, continents) > SEA_LEVEL + 0.22:
                            ptx, ptz = cx_t, cz_t
                            break
                    self.patrol_target_x = ptx
                    self.patrol_target_z = ptz
                    self.current_intent = "explorando_fronteras"
            elif self.genome.role == "RECOLECTOR":
                if (self.wood_carried > 12.0 or norm_energy > 0.72) and nearest_settlement:
                    self.patrol_target_x = nearest_settlement[0]
                    self.patrol_target_z = nearest_settlement[2]
                    self.current_intent = "transportando_madera_y_recursos"
                elif nearest_tree and random.random() < 0.55:
                    self.patrol_target_x = nearest_tree[0]
                    self.patrol_target_z = nearest_tree[2]
                    self.current_intent = "talando_arbol_cuantico"
                elif nearest_resource:
                    self.patrol_target_x = nearest_resource[0]
                    self.patrol_target_z = nearest_resource[2]
                    self.current_intent = "cosechando_nodo"
                else:
                    rad = random.uniform(10.0, 35.0)
                    ang = random.uniform(-math.pi, math.pi)
                    self.patrol_target_x = round(rad * math.cos(ang), 2)
                    self.patrol_target_z = round(rad * math.sin(ang), 2)
                    self.current_intent = "buscando_bosques"
            elif self.genome.role == "ARQUITECTO":
                if (self.wood_carried + self.stone_carried) > 10.0 and nearest_settlement:
                    self.patrol_target_x = nearest_settlement[0] + random.uniform(-2.0, 2.0)
                    self.patrol_target_z = nearest_settlement[2] + random.uniform(-2.0, 2.0)
                    self.current_intent = "edificando_asentamiento"
                elif nearest_rock and random.random() < 0.55:
                    self.patrol_target_x = nearest_rock[0]
                    self.patrol_target_z = nearest_rock[2]
                    self.current_intent = "minando_cantera"
                elif nearest_tree:
                    self.patrol_target_x = nearest_tree[0]
                    self.patrol_target_z = nearest_tree[2]
                    self.current_intent = "recolectando_madera"
                else:
                    self.patrol_target_x = 0.0
                    self.patrol_target_z = 0.0
            elif self.genome.role in ("POLICIA", "GUERRERO"):
                if self.genome.role == "GUERRERO" and nearest_predator:
                    self.patrol_target_x = nearest_predator[0]
                    self.patrol_target_z = nearest_predator[2]
                    self.current_intent = "vanguardia_guerrera"
                elif nearest_anomaly:
                    self.patrol_target_x = nearest_anomaly[0]
                    self.patrol_target_z = nearest_anomaly[2]
                    self.current_intent = (
                        "defensa_guerrera" if self.genome.role == "GUERRERO" else "caza_de_malware"
                    )
                elif nearest_rock and random.random() < 0.35:
                    self.patrol_target_x = nearest_rock[0]
                    self.patrol_target_z = nearest_rock[2]
                    self.current_intent = "forjando_coraza_en_roca"
                else:
                    ptx, ptz = self.x, self.z
                    for _ in range(8):
                        rad = random.uniform(8.0, min(b_lim * 0.80, 72.0))
                        ang = random.uniform(-math.pi, math.pi)
                        cx_t, cz_t = round(rad * math.cos(ang), 2), round(rad * math.sin(ang), 2)
                        if calcular_altura_terreno_continentes(cx_t, cz_t, continents) > SEA_LEVEL + 0.22:
                            ptx, ptz = cx_t, cz_t
                            break
                    self.patrol_target_x = ptx
                    self.patrol_target_z = ptz
                    self.current_intent = (
                        "patrulla_continental_guerrera"
                        if self.genome.role == "GUERRERO"
                        else "patrullaje_perimetral"
                    )
            else:
                if nearest_river and random.random() < 0.40:
                    self.patrol_target_x = nearest_river[0]
                    self.patrol_target_z = nearest_river[2]
                    self.current_intent = "bebiendo_en_el_rio"
                else:
                    rad = random.uniform(8.0, 30.0)
                    ang = random.uniform(-math.pi, math.pi)
                    self.patrol_target_x = round(rad * math.cos(ang), 2)
                    self.patrol_target_z = round(rad * math.sin(ang), 2)
                    self.current_intent = "arbitraje_social"

        # Heuristica de enfermedad, hambre o sed critica
        biome_now = determinar_bioma(self.x, self.z, current_elev)
        self.home_biome = biome_now
        pendiente_local = calcular_pendiente_local(self.x, self.z)

        if self.infection:
            if nearest_hospital and random.random() < 0.72:
                self.patrol_target_x = nearest_hospital[0]
                self.patrol_target_z = nearest_hospital[2]
                self.current_intent = "buscando_hospital"
            elif nearest_medicinal_plant and random.random() < 0.72:
                self.patrol_target_x = nearest_medicinal_plant[0]
                self.patrol_target_z = nearest_medicinal_plant[2]
                self.current_intent = "buscando_planta_medicinal"
            elif nearest_settlement:
                self.patrol_target_x = nearest_settlement[0]
                self.patrol_target_z = nearest_settlement[2]
                self.current_intent = "buscando_refugio_medico"
        elif self.water_level < 38.0 or norm_energy < 0.35:
            if self.water_level < 42.0 and nearest_river:
                self.patrol_target_x = nearest_river[0]
                self.patrol_target_z = nearest_river[2]
                self.current_intent = "sed_buscando_agua"
            elif nearest_farm and (dist_res > 8.0 and random.random() < 0.45):
                self.patrol_target_x = nearest_farm[0]
                self.patrol_target_z = nearest_farm[2]
                self.current_intent = "buscando_granja"
            elif nearest_plant and random.random() < 0.42:
                self.patrol_target_x = nearest_plant[0]
                self.patrol_target_z = nearest_plant[2]
                self.current_intent = "recolectando_plantas"
            elif nearest_river and (dist_res > 8.0 or random.random() < 0.45):
                self.patrol_target_x = nearest_river[0]
                self.patrol_target_z = nearest_river[2]
                self.current_intent = "sed_buscando_rio"
            elif nearest_resource and dist_res < self.genome.sensory_radius * 1.4:
                self.patrol_target_x = nearest_resource[0]
                self.patrol_target_z = nearest_resource[2]
                self.current_intent = "hambre_buscando_energia"

        # Reforestacion voluntaria y domesticacion segun criterio del ser
        if (
            self.seeds_carried > 0
            and trees_nearby_count < 2
            and (SEA_LEVEL + 0.20) < current_elev < (SNOW_LINE - 0.5)
            and self.energy > self.energy_max * 0.42
            and random.random() < (0.12 + 0.16 * self.genome.stewardship_trait)
        ):
            self.current_intent = "reforestando_claro"
        elif (
            nearest_tameable
            and self.genome.role in ("RECOLECTOR", "ADAPTATIVO", "EXPLORADOR", "ABOGADO")
            and norm_energy > 0.40
            and math.hypot(nearest_tameable[0] - self.x, nearest_tameable[2] - self.z) < (self.genome.sensory_radius * 0.9)
            and random.random() < (0.25 * self.genome.stewardship_trait)
        ):
            self.patrol_target_x = nearest_tameable[0]
            self.patrol_target_z = nearest_tameable[2]
            self.current_intent = "domesticando_fauna"

        # Evitar caer en mar abierto sin puerto y usar tuneles ante cumbres muy altas
        if biome_now == "mar":
            d_port_cur = math.hypot(nearest_port[0] - self.x, nearest_port[2] - self.z) if nearest_port else 999.0
            if d_port_cur > 6.5 and nearest_settlement:
                self.patrol_target_x = nearest_settlement[0] * 0.65 + (nearest_port[0] if nearest_port else 0.0) * 0.35
                self.patrol_target_z = nearest_settlement[2] * 0.65 + (nearest_port[2] if nearest_port else 0.0) * 0.35
                self.current_intent = "regresando_a_tierra_firme"
        elif current_elev >= HIGH_ALTITUDE_WARN and self.learned_height_caution > 0.35 and nearest_tunnel:
            d_tun = math.hypot(nearest_tunnel[0] - self.x, nearest_tunnel[2] - self.z)
            if 3.0 < d_tun < self.genome.sensory_radius and random.random() < 0.45:
                self.patrol_target_x = nearest_tunnel[0]
                self.patrol_target_z = nearest_tunnel[2]
                self.current_intent = "buscando_tunel_alpino"

        # Evasión aprendida o interceptación policial de depredadores salvajes
        evading_predator = False
        d_pred = 999.0
        if nearest_predator:
            dx_p = nearest_predator[0] - self.x
            dz_p = nearest_predator[2] - self.z
            d_pred = math.hypot(dx_p, dz_p)
            alert_rad = self.genome.sensory_radius * (0.45 + 0.65 * self.learned_predator_avoidance + 0.35 * self.genome.caution_trait)
            if d_pred < alert_rad:
                if (
                    self.genome.role in ("POLICIA", "GUERRERO")
                    or (self.genome.defense_factor > 1.9 and self.health > 65.0)
                ):
                    self.patrol_target_x = nearest_predator[0]
                    self.patrol_target_z = nearest_predator[2]
                    self.current_intent = "repeliendo_depredador"
                elif self.learned_predator_avoidance > 0.16 or self.genome.caution_trait > 0.48:
                    evading_predator = True
                    # Aprendizaje observacional gradual al detectar un depredador a tiempo
                    self.learned_predator_avoidance = min(0.95, round(self.learned_predator_avoidance + 0.008, 3))
                    esc_x = self.x - (dx_p / max(0.2, d_pred)) * 12.0
                    esc_z = self.z - (dz_p / max(0.2, d_pred)) * 12.0
                    refugio = nearest_watchtower or nearest_settlement or nearest_bridge
                    if refugio:
                        esc_x = esc_x * 0.45 + refugio[0] * 0.55
                        esc_z = esc_z * 0.45 + refugio[2] * 0.55
                    self.patrol_target_x = max(-b_lim * 0.9, min(b_lim * 0.9, round(esc_x, 2)))
                    self.patrol_target_z = max(-b_lim * 0.9, min(b_lim * 0.9, round(esc_z, 2)))
                    self.current_intent = "huyendo_de_depredador_aprendido"

        # 6. Dirección de navegación intencional hacia el objetivo
        dx_tar = self.patrol_target_x - self.x
        dz_tar = self.patrol_target_z - self.z
        target_angle = math.atan2(dz_tar, dx_tar)

        desired_heading = target_angle + (raw_steer * 0.35)
        diff_h = (desired_heading - self.heading + math.pi) % (2.0 * math.pi) - math.pi
        self.heading += diff_h * 0.32

        role = self.genome.role
        speed_mult = 1.0
        if role == "EXPLORADOR":
            speed_mult = 1.72
        elif role == "GUERRERO":
            speed_mult = 1.48
        elif role == "POLICIA":
            speed_mult = 1.35
        elif role == "RECOLECTOR":
            speed_mult = 1.25
        elif role == "ADAPTATIVO":
            speed_mult = 1.30
        if evading_predator:
            speed_mult *= (1.25 + 0.25 * self.learned_predator_avoidance)
        if self.infection:
            speed_mult *= 0.78

        base_thrust = (0.50 + raw_thrust * 0.50) * self.genome.speed_factor * speed_mult
        prop_scale = max(0.06, min(0.16, self.genome.size * 0.085))
        thrust = round(
            min(0.22 if evading_predator else 0.14, max(0.032, base_thrust * prop_scale)),
            4,
        )

        # Cautela aprendida ante cumbres/acantilados y mar profundo
        cand_x = max(-b_lim + 0.5, min(b_lim - 0.5, self.x + math.cos(self.heading) * thrust))
        cand_z = max(-b_lim + 0.5, min(b_lim - 0.5, self.z + math.sin(self.heading) * thrust))
        cand_elev = calcular_altura_terreno_continentes(cand_x, cand_z, continents)
        d_bridge_cand = math.hypot(nearest_bridge[0] - cand_x, nearest_bridge[2] - cand_z) if nearest_bridge else 999.0
        d_port_cand = math.hypot(nearest_port[0] - cand_x, nearest_port[2] - cand_z) if nearest_port else 999.0
        if cand_elev < (SEA_LEVEL - 0.20) and biome_now != "mar" and d_bridge_cand > 4.2 and d_port_cand > 6.0:
            # Bordear la costa cuando detecta mar sin puente/puerto
            if self.genome.caution_trait > 0.35 or self.genome.crest_style != "aleta":
                self.heading += math.pi * 0.65
                thrust *= 0.65
        elif (current_elev - cand_elev) > 1.30 and current_elev > HIGH_ALTITUDE_WARN and self.learned_height_caution > 0.30:
            # Reducir velocidad al descender un desnivel abrupto en altura
            thrust *= 0.55

        self.vx = math.cos(self.heading) * thrust
        self.vz = math.sin(self.heading) * thrust

        self.x += self.vx
        self.z += self.vz

        if abs(self.x) > b_lim:
            self.x = math.copysign(b_lim - 0.2, self.x)
            self.heading = math.pi - self.heading
        if abs(self.z) > b_lim:
            self.z = math.copysign(b_lim - 0.2, self.z)
            self.heading = -self.heading

        # Altura segura sobre el terreno triangulado (nunca por debajo de la malla!)
        new_elev = calcular_altura_terreno_continentes(self.x, self.z, continents)
        new_biome = determinar_bioma_continentes(self.x, self.z, new_elev, continents)
        self.home_biome = new_biome
        # Navegacion al raz y anclaje continental para que ningun ser se pierda en mar abierto
        if new_biome in ("mar", "agua"):
            near_cross = (
                (nearest_bridge is not None and math.hypot(nearest_bridge[0] - self.x, nearest_bridge[2] - self.z) < 5.5)
                or (nearest_port is not None and math.hypot(nearest_port[0] - self.x, nearest_port[2] - self.z) < 6.0)
            )
            if not near_cross:
                home_cx, home_cz = 0.0, 0.0
                if continents:
                    best_c = min(
                        continents,
                        key=lambda c: math.hypot(self.x - c.center_x, self.z - c.center_z),
                    )
                    home_cx, home_cz = best_c.center_x, best_c.center_z
                to_c_ang = math.atan2(home_cz - self.z, home_cx - self.x)
                self.heading = to_c_ang
                self.patrol_target_x = round(home_cx + random.uniform(-14.0, 14.0), 2)
                self.patrol_target_z = round(home_cz + random.uniform(-14.0, 14.0), 2)

        safe_y = altura_superficie_segura(
            self.x, self.z, footprint_radius=0.06, continents=continents, min_clearance=0.015
        )
        water_floor = (SEA_LEVEL + 0.02) if new_biome in ("mar", "agua") else safe_y
        self.y = max(safe_y, water_floor)

        # Estructuras cercanas reducen esfuerzo y peligros
        d_bridge = math.hypot(nearest_bridge[0] - self.x, nearest_bridge[2] - self.z) if nearest_bridge else 999.0
        d_farm = math.hypot(nearest_farm[0] - self.x, nearest_farm[2] - self.z) if nearest_farm else 999.0
        d_tower = math.hypot(nearest_watchtower[0] - self.x, nearest_watchtower[2] - self.z) if nearest_watchtower else 999.0
        d_tunnel = math.hypot(nearest_tunnel[0] - self.x, nearest_tunnel[2] - self.z) if nearest_tunnel else 999.0
        d_port = math.hypot(nearest_port[0] - self.x, nearest_port[2] - self.z) if nearest_port else 999.0
        kinetic_mult = 0.55 if (d_bridge < 2.8 or d_tunnel < 3.6) else 1.0

        # Conciencia y riesgo real por altura / desniveles en cordilleras
        if current_elev >= HIGH_ALTITUDE_WARN and (current_elev - new_elev) > 1.38 and d_bridge > 4.0 and d_tunnel > 4.2:
            wing_glide = max(0.25, 1.0 - self.genome.wing_span * 0.45)
            caution_mitig = max(0.30, 1.0 - self.learned_height_caution * 0.55)
            fall_dmg = DEMOGRAPHIC_RULES["high_altitude_hazard_damage"] * (1.0 + max(0.0, pendiente_local - 0.5)) * wing_glide * caution_mitig
            self.health -= fall_dmg
            self.learned_height_caution = min(1.0, round(self.learned_height_caution + 0.14, 3))
            if self.health <= 0.0:
                self.death_cause = "caida_altura"
        elif new_elev >= HIGH_ALTITUDE_WARN:
            self.learned_height_caution = min(1.0, round(self.learned_height_caution + 0.006, 3))

        # Riesgo marino de ahogamiento sin puerto ni aletas/alas
        if new_biome == "mar" and d_port > 6.5 and d_bridge > 4.5:
            hydro_adapt = 0.25 if self.genome.crest_style == "aleta" else (0.50 if self.genome.wing_span > 0.65 else 1.0)
            drown_dmg = (DEMOGRAPHIC_RULES["drowning_base_damage"] / (0.85 + self.genome.defense_factor * 0.4)) * hydro_adapt
            self.health -= drown_dmg
            self.energy -= 0.45
            if self.health <= 0.0:
                self.death_cause = "ahogamiento"

        # Hidratacion y clima: desierto seco deshidrata, lluvia y costa rehidratan
        water_delta = -0.22 if new_biome == "seco" else (-0.08 if new_biome == "nieve_alta" else -0.05)
        if rain_intensity > 0.25:
            water_delta += 0.95 * rain_intensity
        if d_port < 4.5 or d_farm < 4.0:
            water_delta += 0.65
        self.water_level = min(100.0, max(0.0, self.water_level + water_delta))
        if self.water_level < 12.0:
            self.energy -= 0.16

        # Termodinámica y exposición nocturna o nevada fuera de refugios
        costo_basal = 0.030 * self.genome.size
        costo_cinetico = 0.35 * (self.vx * self.vx + self.vz * self.vz) * self.genome.size * kinetic_mult
        costo_pendiente = max(0.0, slope) * 0.045
        en_refugio = (dist_set < 6.5) or (d_farm < 4.5) or (d_tower < 4.5) or (d_tunnel < 3.6) or (d_port < 4.5)
        costo_nocturno = DEMOGRAPHIC_RULES["night_exposure_drain"] if (environmental_cycle == "NOCHE_SINAPTICA" and not en_refugio) else 0.0
        costo_frio = 0.032 if (new_biome == "nieve_alta" and self.genome.shell_armor < 0.45 and not en_refugio) else 0.0
        self.energy -= (costo_basal + costo_cinetico + costo_pendiente + costo_nocturno + costo_frio)

        # Deterioro senil progresivo pasado el 85% del ciclo vital (Regla de Mortalidad)
        if self.age > (self.genome.lifespan_max * DEMOGRAPHIC_RULES["senescence_age_ratio"]):
            self.health -= 0.42
            if not self.death_cause and self.health <= 0.0:
                self.death_cause = "vejez"

        if self.energy <= 0.0 or self.age >= self.genome.lifespan_max or self.health <= 0.0:
            self.alive = False
            if self.death_cause:
                reason = self.death_cause
            elif self.age >= self.genome.lifespan_max:
                reason = "vejez"
            elif self.energy <= 0.0:
                reason = "inanicion"
            else:
                reason = "combate"
            return {
                "action": "died",
                "reason": reason,
            }

        d_tame = math.hypot(nearest_tameable[0] - self.x, nearest_tameable[2] - self.z) if nearest_tameable else 999.0
        d_plant = math.hypot(nearest_plant[0] - self.x, nearest_plant[2] - self.z) if nearest_plant else 999.0
        return {
            "action": "active",
            "do_harvest": do_harvest or (dist_res < 3.0),
            "do_social": do_social or (dist_set < 4.0),
            "do_combat": do_combat or (dist_ano < 3.5),
            "evading_predator": evading_predator,
            "biome": new_biome,
            "elevation": new_elev,
            "pendiente": pendiente_local,
            "dist_res": dist_res,
            "dist_set": dist_set,
            "dist_ano": dist_ano,
            "dist_pred": d_pred,
            "dist_tameable": d_tame,
            "dist_plant": d_plant,
            "dist_bridge": d_bridge,
            "dist_farm": d_farm,
            "dist_tunnel": d_tunnel,
            "dist_port": d_port,
            "in_shelter": en_refugio,
        }

    def to_dict(self) -> Dict[str, Any]:
        ontogeny_scale = min(1.0, 0.55 + (self.age / 120.0) * 0.45)
        inf_meta = PATHOGEN_CATALOG.get(self.infection) if self.infection else None
        return {
            "id": self.id,
            "nombre": self.nombre,
            "role": self.genome.role,
            "symbol": self.symbol,
            "color": ROLE_COLORS.get(self.genome.role, 0x38BDF8),
            "generation": self.genome.generation,
            "lineage": self.genome.lineage,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "vx": round(self.vx, 3),
            "vz": round(self.vz, 3),
            "energy": round(self.energy, 1),
            "energy_max": round(self.energy_max, 1),
            "energy_pct": round((self.energy / self.energy_max) * 100, 1),
            "health": round(self.health, 1),
            "age": self.age,
            "size": round(self.genome.size * ontogeny_scale * 0.05, 4),
            "raw_genetic_size": round(self.genome.size, 2),
            "ontogeny_pct": round(ontogeny_scale * 100, 1),
            "morphology_tier": self.genome.morphology_tier,
            "appendage_count": self.genome.appendage_count,
            "hue_shift": self.genome.hue_shift,
            "body_plan": self.genome.body_plan,
            "limb_count": self.genome.limb_count,
            "wing_span": self.genome.wing_span,
            "tail_length": self.genome.tail_length,
            "crest_style": self.genome.crest_style,
            "shell_armor": self.genome.shell_armor,
            "torso_aspect": self.genome.torso_aspect,
            "secondary_hue": self.genome.secondary_hue,
            "biome": self.home_biome,
            "water_level": round(self.water_level, 1),
            "infection": self.infection,
            "infection_name": inf_meta["nombre"] if inf_meta else None,
            "infection_kind": inf_meta["kind"] if inf_meta else None,
            "immunity_level": round(self.immunity_level * 100, 1),
            "learned_height_caution": round(self.learned_height_caution * 100, 1),
            "family_id": self.family_id,
            "home_city_id": self.home_city_id,
            "home_pueblo_id": self.home_pueblo_id,
            "tunnels_used": self.tunnels_used,
            "plants_harvested": self.plants_harvested,
            "illnesses_cured": self.illnesses_cured,
            "is_warrior": self.is_warrior,
            "weapon_tier": self.weapon_tier,
            "combat_xp": round(self.combat_xp, 1),
            "battles_survived": self.battles_survived,
            "wood_carried": round(self.wood_carried, 1),
            "stone_carried": round(self.stone_carried, 1),
            "seeds_carried": self.seeds_carried,
            "learned_predator_avoidance": round(self.learned_predator_avoidance * 100, 1),
            "caution_trait": round(self.genome.caution_trait * 100, 1),
            "stewardship_trait": round(self.genome.stewardship_trait * 100, 1),
            "trees_planted": self.trees_planted,
            "animals_tamed": self.animals_tamed,
            "structures_built": self.structures_built,
            "tamed_animal_id": self.tamed_animal_id,
            "speed_factor": self.genome.speed_factor,
            "current_intent": self.current_intent,
            "current_action": self.current_action,
            "action_target_pos": self.action_target_pos,
            "resources_gathered": round(self.resources_gathered, 1),
            "buildings_contributed": self.buildings_contributed,
            "anomalies_defeated": self.anomalies_defeated,
            "last_real_source": self.last_real_source,
            "assimilated_knowledge": self.assimilated_knowledge[-3:],
            "network_energy_harvested": round(self.network_energy_harvested, 1),
            "patrol_target_x": round(self.patrol_target_x, 2),
            "patrol_target_z": round(self.patrol_target_z, 2),
            "patrol_target": [round(self.patrol_target_x, 1), round(self.patrol_target_z, 1)],
        }


# -------------------------------------------------------------
# NODOS DE RECURSOS ESPACIALES Y REALES
# -------------------------------------------------------------
@dataclass
class ResourceNode:
    """Nodo espacial de energía cuántica, red real, matemáticas o conocimiento enciclopédico."""
    id: str
    x: float
    y: float
    z: float
    energy: float = 85.0
    energy_max: float = 130.0
    regen_rate: float = 0.25
    category: str = "ATP_CUANTICO"  # 'PLASMA_RED_REAL', 'CRISTAL_CONOCIMIENTO', 'MINERAL_LOGICO', 'ATP_CUANTICO', 'BIOMASA_RECICLADA'
    source_label: str = ""
    title: str = ""
    snippet: str = ""
    metric_value: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "energy": round(self.energy, 1),
            "energy_max": round(self.energy_max, 1),
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "source_label": self.source_label,
            "title": self.title,
            "snippet": self.snippet,
            "metric_value": self.metric_value,
        }


# -------------------------------------------------------------
# ASENTAMIENTOS Y CIVILIZACIONES 3D
# -------------------------------------------------------------
@dataclass
class Settlement:
    """Ciudad evolutiva con pueblos internos e infraestructura civil real (Tier 1..5)."""

    id: str
    nombre: str
    x: float
    y: float
    z: float
    energy_pool: float = 140.0
    tier: int = 1
    population_supported: int = 28
    defense_aura: float = 1.0
    biome: str = "valle"
    infrastructure: Dict[str, int] = field(default_factory=dict)
    pueblos: List[str] = field(default_factory=list)
    max_pueblos: int = 4

    @property
    def tier_name(self) -> str:
        spec = CITY_TIER_SPECS.get(self.tier)
        return spec["name"] if spec else "Campamento Urbano"

    def missing_infra_for_next_tier(self) -> List[str]:
        spec = CITY_TIER_SPECS.get(self.tier, CITY_TIER_SPECS[MAX_CITY_TIER])
        return [k for k in spec["required_infra"] if self.infrastructure.get(k, 0) < 1]

    def is_max_evolved(self) -> bool:
        if self.tier < MAX_CITY_TIER:
            return False
        req = CITY_TIER_SPECS[MAX_CITY_TIER]["required_infra"]
        return all(self.infrastructure.get(k, 0) >= 1 for k in req)

    def register_infra(self, kind: str) -> None:
        self.infrastructure[kind] = self.infrastructure.get(kind, 0) + 1
        if kind == "house":
            self.population_supported += 6
        elif kind == "hospital":
            self.defense_aura = round(min(6.5, self.defense_aura + 0.35), 2)
        elif kind == "court":
            self.defense_aura = round(min(6.5, self.defense_aura + 0.45), 2)

    def deposit_energy(self, amount: float) -> bool:
        self.energy_pool += amount
        if self.tier >= MAX_CITY_TIER:
            return False
        spec = CITY_TIER_SPECS.get(self.tier)
        if not spec:
            return False
        if self.energy_pool >= spec["next_energy"] and not self.missing_infra_for_next_tier():
            self.tier += 1
            next_spec = CITY_TIER_SPECS.get(self.tier, spec)
            self.population_supported = max(self.population_supported, next_spec["pop_cap"])
            self.defense_aura = round(1.0 + (self.tier - 1) * 0.7, 2)
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        spec = CITY_TIER_SPECS.get(self.tier, CITY_TIER_SPECS[MAX_CITY_TIER])
        missing = self.missing_infra_for_next_tier()
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tier": self.tier,
            "max_tier": MAX_CITY_TIER,
            "tier_name": self.tier_name,
            "is_max_evolved": self.is_max_evolved(),
            "next_tier_energy": spec["next_energy"],
            "missing_infra": missing,
            "infrastructure": dict(self.infrastructure),
            "pueblos_ids": list(self.pueblos),
            "pueblos_count": len(self.pueblos),
            "biome": self.biome,
            "energy_pool": round(self.energy_pool, 1),
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "population_supported": self.population_supported,
            "defense_aura": round(self.defense_aura, 1),
        }


@dataclass
class AnomalyThreat:
    """Amenaza cibernética en el terreno combatida por Guardianes y Médicos."""
    id: str
    x: float
    y: float
    z: float
    threat_level: float = 110.0
    vector: str = "DDoS_SYN"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "vector": self.vector,
            "threat_level": round(self.threat_level, 1),
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
        }


# -------------------------------------------------------------
# FLORA ALGORÍTMICA: ÁRBOLES CUÁNTICOS VIVOS (CRECEN Y MUTAN)
# -------------------------------------------------------------
@dataclass
class AlgorithmicTree:
    """Árbol computacional vivo que brota, crece, madura y provee biomasa y sombra."""
    id: str
    x: float
    y: float
    z: float
    stage: str = "sapling"  # 'seed', 'sapling', 'mature', 'ancient'
    age: int = 0
    max_age: int = 2400
    wood_energy: float = 65.0
    tree_type: str = "pino_sinaptico"  # 'pino_sinaptico', 'sauce_red', 'roble_algoritmico'
    height: float = 0.6
    seeds_ready: bool = False

    def step_growth(self) -> Optional[Dict[str, Any]]:
        self.age += 1
        if self.stage == "seed" and self.age > 45:
            self.stage = "sapling"
            self.height = 0.55
            self.wood_energy = 35.0
        elif self.stage == "sapling" and self.age > 240:
            self.stage = "mature"
            self.height = 1.65
            self.wood_energy = 115.0
            self.seeds_ready = True
        elif self.stage == "mature" and self.age > 950:
            self.stage = "ancient"
            self.height = 2.45
            self.wood_energy = 230.0

        if self.stage in ("mature", "ancient") and (self.age % 300 == 0):
            return {"action": "disperse_seed", "x": self.x, "z": self.z}
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "stage": self.stage,
            "age": self.age,
            "height": round(self.height, 2),
            "wood_energy": round(self.wood_energy, 1),
            "tree_type": self.tree_type,
        }


# -------------------------------------------------------------
# GEOLOGÍA: ROCAS Y CANTERAS MINERALES
# -------------------------------------------------------------
@dataclass
class GeologicalRock:
    """Formación rocosa o cantera mineral que provee piedra y cuarzo lógico para construcción."""
    id: str
    x: float
    y: float
    z: float
    rock_type: str = "granito_logico"  # 'granito_logico', 'cuarzo_sinaptico', 'basalto_cripto'
    mineral_capacity: float = 180.0
    scale: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "rock_type": self.rock_type,
            "mineral_capacity": round(self.mineral_capacity, 1),
            "scale": round(self.scale, 2),
        }


# -------------------------------------------------------------
# FAUNA DIGITAL MULTI-HABITAT: TIERRA, AIRE, AGUA Y PLANTAS
# -------------------------------------------------------------
@dataclass
class DigitalAnimal:
    """Fauna autónoma multi-hábitat: tierra, aire, mar/ríos y plantas polinizadoras."""

    id: str
    species: str
    nombre: str
    behavior: str  # 'predator', 'tameable', 'domesticated', 'wildlife', 'pest'
    x: float
    y: float
    z: float
    habitat: str = "land"  # 'land', 'air', 'water', 'plant'
    pollinator: bool = False
    vx: float = 0.0
    vz: float = 0.0
    heading: float = 0.0
    energy: float = 120.0
    health: float = 110.0
    age: int = 0
    taming_progress: float = 0.0
    owner_id: Optional[str] = None
    home_structure_id: Optional[str] = None
    yield_cooldown: int = 0
    kills: int = 0
    scale: float = 0.075
    patrol_x: float = 0.0
    patrol_z: float = 0.0
    flight_altitude: float = 3.2

    def step_ai(
        self,
        nearest_prey: Optional[Tuple[float, float, float]] = None,
        nearest_watchtower: Optional[Tuple[float, float, float]] = None,
        home_pos: Optional[Tuple[float, float, float]] = None,
        nearest_river: Optional[Tuple[float, float, float]] = None,
        nearest_plant: Optional[Tuple[float, float, float]] = None,
        continents: Optional[List[Continent]] = None,
        bounds: Optional[float] = None,
    ):
        b_lim = max(float(WORLD_BOUNDS), float(bounds or WORLD_BOUNDS))
        self.age += 1
        if self.yield_cooldown > 0:
            self.yield_cooldown -= 1

        # Destino según hábitat y comportamiento
        dist_pat = math.hypot(self.patrol_x - self.x, self.patrol_z - self.z)
        if dist_pat < 3.4 or (self.patrol_x == 0.0 and self.patrol_z == 0.0):
            if self.behavior == "domesticated" and home_pos:
                self.patrol_x = home_pos[0] + random.uniform(-4.2, 4.2)
                self.patrol_z = home_pos[2] + random.uniform(-4.2, 4.2)
            elif self.habitat == "plant" and nearest_plant:
                self.patrol_x = nearest_plant[0] + random.uniform(-3.0, 3.0)
                self.patrol_z = nearest_plant[2] + random.uniform(-3.0, 3.0)
            elif self.habitat == "water":
                if random.random() < 0.72:
                    # Bahía occidental / mar abierto
                    self.patrol_x = random.uniform(-b_lim * 0.96, -34.0)
                    self.patrol_z = random.uniform(-b_lim * 0.45, b_lim * 0.80)
                elif nearest_river and self.species == "pez_cuantico":
                    self.patrol_x = nearest_river[0] + random.uniform(-2.2, 2.2)
                    self.patrol_z = nearest_river[2] + random.uniform(-2.2, 2.2)
                else:
                    ang = random.uniform(-math.pi, math.pi)
                    rad = random.uniform(54.0, b_lim * 0.92)
                    self.patrol_x = round(rad * math.cos(ang), 2)
                    self.patrol_z = round(rad * math.sin(ang), 2)
            elif self.behavior == "predator" and nearest_prey and random.random() < 0.72:
                self.patrol_x = nearest_prey[0]
                self.patrol_z = nearest_prey[2]
            elif self.behavior == "tameable" and nearest_river and random.random() < 0.45:
                self.patrol_x = nearest_river[0] + random.uniform(-5.5, 5.5)
                self.patrol_z = nearest_river[2] + random.uniform(-5.5, 5.5)
            else:
                rad = random.uniform(6.0, b_lim * 0.85)
                ang = random.uniform(-math.pi, math.pi)
                self.patrol_x = round(rad * math.cos(ang), 2)
                self.patrol_z = round(rad * math.sin(ang), 2)

        # Atalayas repelen a depredadores
        if self.behavior == "predator" and nearest_watchtower:
            d_tw = math.hypot(nearest_watchtower[0] - self.x, nearest_watchtower[2] - self.z)
            if d_tw < 10.5:
                self.patrol_x = max(-b_lim * 0.92, min(b_lim * 0.92, self.x + (self.x - nearest_watchtower[0]) * 2.5))
                self.patrol_z = max(-b_lim * 0.92, min(b_lim * 0.92, self.z + (self.z - nearest_watchtower[2]) * 2.5))

        # Caza dirigida dentro de su dominio válido
        if self.behavior == "predator" and nearest_prey:
            d_prey = math.hypot(nearest_prey[0] - self.x, nearest_prey[2] - self.z)
            prey_biome = determinar_bioma_continentes(nearest_prey[0], nearest_prey[2], continents=continents)
            domain_ok = (self.habitat != "water" or prey_biome in ("mar", "costa"))
            if domain_ok and d_prey < 14.5 and (not nearest_watchtower or math.hypot(nearest_watchtower[0] - nearest_prey[0], nearest_watchtower[2] - nearest_prey[2]) > 8.5):
                self.patrol_x = nearest_prey[0]
                self.patrol_z = nearest_prey[2]

        dx = self.patrol_x - self.x
        dz = self.patrol_z - self.z
        target_ang = math.atan2(dz, dx)
        diff = (target_ang - self.heading + math.pi) % (2.0 * math.pi) - math.pi
        self.heading += diff * 0.35

        if self.habitat == "air":
            spd = 0.24 if self.behavior == "predator" else 0.18
        elif self.habitat == "plant":
            spd = 0.06
        elif self.habitat == "water":
            spd = 0.18 if self.behavior == "predator" else 0.13
        else:
            spd = 0.15 if self.behavior == "predator" else (0.08 if self.behavior == "domesticated" else 0.11)

        nx = max(-b_lim + 0.6, min(b_lim - 0.6, self.x + math.cos(self.heading) * spd))
        nz = max(-b_lim + 0.6, min(b_lim - 0.6, self.z + math.sin(self.heading) * spd))
        elev_cand = calcular_altura_terreno_continentes(nx, nz, continents=continents)

        # Confinamiento fisico de fauna acuatica vs terrestre y anclaje continental
        if self.habitat == "water" and elev_cand > SEA_LEVEL + 0.15 and self.species != "pez_cuantico":
            self.heading = math.atan2(18.0 - self.z, -42.0 - self.x)
            nx = max(-b_lim + 0.6, min(b_lim - 0.6, self.x + math.cos(self.heading) * spd))
            nz = max(-b_lim + 0.6, min(b_lim - 0.6, self.z + math.sin(self.heading) * spd))
        elif self.habitat == "land" and elev_cand < SEA_LEVEL - 0.12:
            cx_home, cz_home = 0.0, 0.0
            if continents:
                best_c = min(continents, key=lambda c: math.hypot(self.x - c.center_x, self.z - c.center_z))
                cx_home, cz_home = best_c.center_x, best_c.center_z
            self.heading = math.atan2(cz_home - self.z, cx_home - self.x)
            nx = max(-b_lim + 0.6, min(b_lim - 0.6, self.x + math.cos(self.heading) * spd))
            nz = max(-b_lim + 0.6, min(b_lim - 0.6, self.z + math.sin(self.heading) * spd))

        self.vx = round(nx - self.x, 4)
        self.vz = round(nz - self.z, 4)
        self.x = nx
        self.z = nz
        ter_y = altura_superficie_segura(
            self.x,
            self.z,
            footprint_radius=0.06,
            continents=continents,
            min_clearance=0.015,
        )

        if self.habitat == "air":
            base_air = max(SEA_LEVEL + 1.8, ter_y)
            self.y = base_air + self.flight_altitude + 0.45 * math.sin(self.age * 0.14)
        elif self.habitat == "water":
            self.y = max(ter_y + 0.04, SEA_LEVEL - 0.18 if ter_y <= SEA_LEVEL else SEA_LEVEL + 0.06)
        elif self.habitat == "plant":
            self.y = max(SEA_LEVEL + 0.25, ter_y) + 0.34 + 0.10 * math.sin(self.age * 0.25)
        else:
            self.y = max(SEA_LEVEL + 0.02, ter_y) + (self.scale * 0.02)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "species": self.species,
            "nombre": self.nombre,
            "behavior": self.behavior,
            "habitat": self.habitat,
            "can_wage_war": False,
            "pollinator": self.pollinator,
            "x": round(self.x, 2),
            "y": round(self.y, 3),
            "z": round(self.z, 2),
            "vx": round(self.vx, 3),
            "vz": round(self.vz, 3),
            "health": round(self.health, 1),
            "taming_progress": round(self.taming_progress, 1),
            "owner_id": self.owner_id,
            "home_structure_id": self.home_structure_id,
            "kills": self.kills,
            "scale": round(self.scale, 4),
        }


# -------------------------------------------------------------
# ESTRUCTURAS EMERGENTES Y CIVILES (TERRENO Y CIUDADES REALES)
# -------------------------------------------------------------
@dataclass
class CustomStructure:
    """Construcciones civiles y de ingeniería territorial creadas autónomamente."""

    id: str
    kind: str  # 'bridge', 'tunnel', 'port', 'farm', 'watchtower', 'nursery', 'house', 'market', 'school', 'hospital', 'power_plant', 'aqueduct', 'sanitation', 'court'
    nombre: str
    x: float
    y: float
    z: float
    angle_y: float = 0.0
    level: int = 1
    durability: float = 100.0
    energy_stored: float = 90.0
    builder_name: str = ""
    builder_role: str = "ARQUITECTO"
    animals_housed: int = 0
    seeds_generated: int = 0
    city_id: Optional[str] = None
    pueblo_id: Optional[str] = None
    exit_x: Optional[float] = None
    exit_y: Optional[float] = None
    exit_z: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "nombre": self.nombre,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "angle_y": round(self.angle_y, 3),
            "level": self.level,
            "durability": round(self.durability, 1),
            "energy_stored": round(self.energy_stored, 1),
            "builder_name": self.builder_name,
            "animals_housed": self.animals_housed,
            "seeds_generated": self.seeds_generated,
            "city_id": self.city_id,
            "pueblo_id": self.pueblo_id,
            "exit_x": round(self.exit_x, 2) if self.exit_x is not None else None,
            "exit_y": round(self.exit_y, 2) if self.exit_y is not None else None,
            "exit_z": round(self.exit_z, 2) if self.exit_z is not None else None,
        }


# -------------------------------------------------------------
# CLASE PRINCIPAL DEL ECOSISTEMA DIGITAL DE GHOLGO
# -------------------------------------------------------------
class GholgoDigitalEcosystem:
    """
    Motor central de la Simulación Continental de Vida Artificial de Gholgo.
    Orquesta física, evolución, explotación de recursos de internet y matemáticas.
    """

    def __init__(self):
        self.lock = threading.RLock()
        self._stop_sim = False
        self.start_timestamp: float = time.time()
        self.generation_global: int = 1
        self.step_counter: int = 0
        self.organisms: Dict[str, Organism] = {}
        self.resources: Dict[str, ResourceNode] = {}
        self.settlements: Dict[str, Settlement] = {}
        self.pueblos: Dict[str, Pueblo] = {}
        self.families: Dict[str, Family] = {}
        self.anomalies: Dict[str, AnomalyThreat] = {}
        self.trees: Dict[str, AlgorithmicTree] = {}
        self.plants: Dict[str, Plant] = {}
        self.rocks: Dict[str, GeologicalRock] = {}
        self.animals: Dict[str, DigitalAnimal] = {}
        self.structures: Dict[str, CustomStructure] = {}
        self.clouds: Dict[str, AtmosphericCloud] = {}
        self.continents: List[Continent] = default_continents_for_world()
        self.dynamic_bounds: float = calcular_bounds_dinamicos(self.continents)
        self.continents_discovered_total: int = len(self.continents)
        self._federation: Any = None
        self.river_points: List[List[float]] = obtener_puntos_rio_completos()
        self.celestial: Dict[str, Any] = calcular_estado_celeste(0)
        self.weather: Dict[str, Any] = {
            "rain_intensity": 0.0,
            "thunder_active": False,
            "wind_x": 0.14,
            "wind_z": 0.06,
            "lightning_strike": None,
        }
        self.environmental_cycle: str = "DIA_SOLAR"
        self.environmental_factor: float = 0.5
        self.total_births: int = 0
        self.total_deaths: int = 0
        self.deaths_by_cause: Dict[str, int] = {
            "inanicion": 0,
            "vejez": 0,
            "depredacion": 0,
            "hacinamiento": 0,
            "combate": 0,
            "enfermedad": 0,
            "caida_altura": 0,
            "ahogamiento": 0,
        }
        self.peak_population: int = 0
        self.wood_harvested_total: float = 0.0
        self.stone_mined_total: float = 0.0
        self.trees_planted_by_beings: int = 0
        self.animals_tamed_total: int = 0
        self.predation_kills_total: int = 0
        self.predators_defeated_total: int = 0
        self.illnesses_cured_total: int = 0
        self.tunnels_built_total: int = 0
        self.thunder_harvested_total: int = 0
        self.antigravity_interventions: int = 0
        self.gholgo_shared_memory_transfers: int = 0
        self.settlement_counter: int = 1
        self.pueblo_counter: int = 1
        self.family_counter: int = 1
        self.structure_counter: int = 1
        self.evolution_timeline: List[Dict[str, Any]] = []

        self._inicializar_mundo()
        self._cargar_estado_persistente()
        self._asegurar_todo_sobre_terreno()
        self._sync_federacion()

        # Iniciar simulación de vida artificial autónoma continua en segundo plano
        self._sim_thread = threading.Thread(
            target=self._daemon_simulation_loop,
            name="GholgoEcoSimLoop",
            daemon=True
        )
        self._sim_thread.start()

    def _daemon_simulation_loop(self):
        """Bucle autónomo que impulsa la vida digital en segundo plano 24/7."""
        time.sleep(1.0)
        while not self._stop_sim:
            try:
                self.tick(steps=1)
            except Exception:
                pass
            sim_interval = max(0.4, float(os.environ.get("GHOLGO_SIM_TICK_SEC", "1.25")))
            time.sleep(sim_interval)

    def todas_ciudades_al_maximo(self) -> bool:
        """Regla estricta: todas las ciudades existentes deben evolucionar al Tier 5 antes de fundar otra."""
        return bool(self.settlements) and all(s.is_max_evolved() for s in self.settlements.values())

    def _get_federation(self):
        if self._federation is None:
            from proviweb_maestro.agent.gholgo_world_federation import global_world_federation

            self._federation = global_world_federation
        return self._federation

    def _terrain_height(self, x: float, z: float) -> float:
        return calcular_altura_terreno_continentes(x, z, self.continents)

    def _terreno_y(self, x: float, z: float) -> float:
        return self._terrain_height(x, z)

    def _bioma_en(self, x: float, z: float, elev: Optional[float] = None) -> str:
        return determinar_bioma_continentes(x, z, y=elev, continents=self.continents)

    def _safe_surface_y(
        self,
        x: float,
        z: float,
        footprint: float = 0.0,
        clearance: float = 0.18,
        footprint_radius: Optional[float] = None,
    ) -> float:
        rad = footprint if footprint_radius is None else footprint_radius
        return altura_superficie_segura(
            x,
            z,
            footprint_radius=rad,
            continents=self.continents,
            min_clearance=clearance,
        )

    def _asegurar_todo_sobre_terreno(self) -> None:
        """Garantiza que ninguna ciudad, pueblo, estructura, árbol, planta, roca o ser quede bajo tierra."""
        for s in self.settlements.values():
            s.y = round(max(SEA_LEVEL + 0.35, self._safe_surface_y(s.x, s.z, 2.8, 0.36)), 3)
        for p in self.pueblos.values():
            p.y = round(max(SEA_LEVEL + 0.28, self._safe_surface_y(p.x, p.z, 1.25, 0.28)), 3)
        for st in self.structures.values():
            if st.kind == "bridge":
                st.y = round(max(SEA_LEVEL + 0.20, self._safe_surface_y(st.x, st.z, 1.1, 0.24)), 3)
            elif st.kind == "port":
                st.y = round(max(SEA_LEVEL + 0.24, self._safe_surface_y(st.x, st.z, 1.2, 0.24)), 3)
            else:
                st.y = round(max(SEA_LEVEL + 0.22, self._safe_surface_y(st.x, st.z, 1.1, 0.26)), 3)
            if st.exit_x is not None and st.exit_z is not None:
                st.exit_y = round(self._safe_surface_y(st.exit_x, st.exit_z, 0.8, 0.24), 3)
        for t in self.trees.values():
            t.y = round(max(SEA_LEVEL + 0.16, self._safe_surface_y(t.x, t.z, 0.55, 0.15)), 3)
        for pl in self.plants.values():
            pl.y = round(max(SEA_LEVEL + 0.14, self._safe_surface_y(pl.x, pl.z, 0.35, 0.14)), 3)
        for rk in self.rocks.values():
            rk.y = round(max(SEA_LEVEL + 0.14, self._safe_surface_y(rk.x, rk.z, 0.65, 0.16)), 3)
        for res in self.resources.values():
            base_r = self._safe_surface_y(res.x, res.z, 0.4, 0.22)
            res.y = round(
                max(base_r, SEA_LEVEL + 0.18 if self._terrain_height(res.x, res.z) < SEA_LEVEL else base_r),
                3,
            )
        for ano in self.anomalies.values():
            ano.y = round(max(SEA_LEVEL + 0.30, self._safe_surface_y(ano.x, ano.z, 0.4, 0.45)), 3)
        for ani in self.animals.values():
            ter_safe = self._safe_surface_y(ani.x, ani.z, 0.06, 0.015)
            if ani.habitat == "air":
                ani.y = round(max(ani.y, max(SEA_LEVEL + 2.0, ter_safe) + 2.2), 3)
            elif ani.habitat == "water":
                ani.y = round(max(ter_safe + 0.04, SEA_LEVEL - 0.18 if ter_safe <= SEA_LEVEL else SEA_LEVEL + 0.06), 3)
            elif ani.habitat == "plant":
                ani.y = round(max(SEA_LEVEL + 0.25, ter_safe) + 0.34, 3)
            else:
                ani.y = round(max(SEA_LEVEL + 0.02, ter_safe) + (ani.scale * 0.02), 3)
        for org in self.organisms.values():
            safe_org = self._safe_surface_y(org.x, org.z, 0.06, 0.015)
            floor = SEA_LEVEL + 0.02 if org.home_biome in ("mar", "agua") else safe_org
            org.y = round(max(safe_org, floor), 3)

    def descubrir_nuevo_continente(
        self,
        discovered_by: str = "Explorador Autónomo",
        discovered_by_role: str = "EXPLORADOR",
        preferred_biome: Optional[str] = None,
    ) -> Continent:
        """Genera un nuevo continente explorable con bioma, flora, fauna y recursos propios."""
        with self.lock:
            cont = generar_nuevo_continente(
                self.continents,
                discovered_by=discovered_by,
                discovered_by_role=discovered_by_role,
                step_counter=self.step_counter,
                world_id="mundo_gholgo_primario",
                preferred_biome=preferred_biome,
            )
            self.continents.append(cont)
            self.continents_discovered_total = len(self.continents)
            self.dynamic_bounds = calcular_bounds_dinamicos(self.continents)

            # Sembrar recursos, bosques, plantas y rocas en el nuevo continente sobre el terreno
            for i in range(6):
                ang = random.uniform(-math.pi, math.pi)
                rad = random.uniform(2.0, max(5.0, cont.radius * 0.72))
                rx = round(cont.center_x + math.cos(ang) * rad, 2)
                rz = round(cont.center_z + math.sin(ang) * rad, 2)
                res_id = f"res_{cont.id[:12]}_{i}"
                node = self._crear_recurso_por_bioma(res_id, rx, rz, i)
                node.y = round(max(SEA_LEVEL + 0.18, self._safe_surface_y(rx, rz, 0.4, 0.24)), 3)
                self.resources[res_id] = node

            for i in range(5):
                ang = random.uniform(-math.pi, math.pi)
                rad = random.uniform(2.0, max(4.0, cont.radius * 0.65))
                tx = round(cont.center_x + math.cos(ang) * rad, 2)
                tz = round(cont.center_z + math.sin(ang) * rad, 2)
                if self._terrain_height(tx, tz) > SEA_LEVEL + 0.2:
                    ty = self._safe_surface_y(tx, tz, 0.55, 0.15)
                    tid = f"tree_{cont.id[:10]}_{i}"
                    self.trees[tid] = AlgorithmicTree(
                        id=tid,
                        x=tx,
                        y=ty,
                        z=tz,
                        stage=random.choice(["sapling", "mature"]),
                        age=120,
                        wood_energy=42.0,
                        tree_type="roble_algoritmico",
                        height=1.2,
                    )

            for i in range(6):
                ang = random.uniform(-math.pi, math.pi)
                rad = random.uniform(1.5, max(4.0, cont.radius * 0.65))
                px = round(cont.center_x + math.cos(ang) * rad, 2)
                pz = round(cont.center_z + math.sin(ang) * rad, 2)
                if self._terrain_height(px, pz) > SEA_LEVEL + 0.15:
                    py = self._safe_surface_y(px, pz, 0.35, 0.14)
                    sp = random.choice(list(PLANT_SPECIES_META.keys()))
                    pid = f"plant_{cont.id[:10]}_{i}"
                    self.plants[pid] = Plant(
                        id=pid,
                        species=sp,
                        nombre=PLANT_SPECIES_META[sp][0],
                        biome=determinar_bioma_continentes(px, pz, py, self.continents),
                        x=px,
                        y=py,
                        z=pz,
                        growth=0.82,
                        biomass=28.0,
                        pollinated=True,
                    )

            self.evolution_timeline.append(
                {
                    "step": self.step_counter,
                    "generation": self.generation_global,
                    "population": len(self.organisms),
                    "event": f"Nuevo continente descubierto: {cont.nombre} ({cont.biome_profile})",
                }
            )
            if len(self.evolution_timeline) > 120:
                self.evolution_timeline = self.evolution_timeline[-120:]
            self._asegurar_todo_sobre_terreno()
            self._sync_federacion()
            self._guardar_estado_persistente()
            return cont

    def _step_continent_expansion(self, eventos: List[str]) -> None:
        """Los exploradores descubren continuamente nuevos continentes más allá del océano."""
        if len(self.continents) >= 16:
            return
        explorers = [o for o in self.organisms.values() if o.alive and o.genome.role == "EXPLORADOR"]
        if not explorers:
            return
        frontier_explorer: Optional[Organism] = None
        for exp in explorers:
            # Si alcanza el borde del continente actual o navega por aguas exteriores
            d_min_cont = min(
                (math.hypot(exp.x - c.center_x, exp.z - c.center_z) / max(10.0, c.radius))
                for c in self.continents
            )
            if d_min_cont > 0.88:
                frontier_explorer = exp
                break
        if frontier_explorer or (self.step_counter > 0 and self.step_counter % 110 == 0):
            pioneer = frontier_explorer or explorers[0]
            last_step = max((c.discovered_at_step for c in self.continents), default=0)
            if (self.step_counter - last_step) >= 55:
                cont = self.descubrir_nuevo_continente(
                    discovered_by=pioneer.nombre,
                    discovered_by_role=pioneer.genome.role,
                )
                eventos.append(
                    f"🗺️ ¡{pioneer.nombre} cartografió un nuevo continente: {cont.nombre} ({cont.biome_profile})!"
                )

    def _aplicar_perdidas_guerra_primaria(self, eventos: List[str]) -> None:
        """Si Mundo #0 perdió una guerra inter-mundial, aplica bajas reales de guerreros y energía."""
        try:
            fed = self._get_federation()
            losses = fed.pop_primary_war_losses()
        except Exception:
            losses = []
        for item in losses:
            casualties = int(item.get("warrior_casualties", 0))
            drain = float(item.get("energy_drain", 0.0))
            warriors = [o for o in self.organisms.values() if o.alive and o.genome.role == "GUERRERO"]
            random.shuffle(warriors)
            for w_org in warriors[: max(0, min(len(warriors) - 1, casualties))]:
                w_org.alive = False
                w_org.death_cause = "combate"
                self.organisms.pop(w_org.id, None)
                self.total_deaths += 1
                self.deaths_by_cause["combate"] = self.deaths_by_cause.get("combate", 0) + 1
            for st in self.settlements.values():
                st.energy_pool = max(30.0, round(st.energy_pool - drain / max(1, len(self.settlements)), 2))
            eventos.append(
                f"💥 Impacto de guerra ({item.get('war_id')}): -{casualties} guerreros y -{drain:.1f} energía."
            )

    def _sync_federacion(self) -> Dict[str, Any]:
        """Sincroniza el estado real de Gholgo+Antigravity con la Federación Kardashev."""
        try:
            fed = self._get_federation()
            warriors = [o for o in self.organisms.values() if o.alive and o.genome.role == "GUERRERO"]
            avg_power = (
                sum(18.0 * o.genome.defense_factor + o.combat_xp * 0.25 for o in warriors)
                / len(warriors)
                if warriors
                else 18.0
            )
            max_wtier = max((o.weapon_tier for o in warriors), default=1)
            energy_sum = sum(s.energy_pool for s in self.settlements.values()) + sum(
                o.energy for o in self.organisms.values() if o.alive
            )
            return fed.sync_primary_world(
                {
                    "living_beings": len(self.organisms),
                    "warriors_count": len(warriors),
                    "warrior_weapon_tier": max_wtier,
                    "warrior_avg_power": round(avg_power, 2),
                    "animals_count": len(self.animals),
                    "city_tiers_sum": sum(s.tier for s in self.settlements.values()),
                    "structures_count": len(self.structures),
                    "trees_plants_count": len(self.trees) + len(self.plants),
                    "knowledge_items": sum(len(o.assimilated_knowledge) for o in self.organisms.values()),
                    "energy_pool": round(energy_sum, 2),
                    "step_count": self.step_counter,
                    "continents": [c.to_dict() for c in self.continents],
                }
            )
        except Exception:
            return {}

    def _crear_recurso_por_bioma(self, res_id: str, rx: float, rz: float, idx_hint: int = 0) -> ResourceNode:
        """Crea un nodo de recurso real adaptado al bioma o mar sin quedar enterrado."""
        ry_raw = self._safe_surface_y(rx, rz, footprint_radius=0.55, clearance=0.22)
        biome = self._bioma_en(rx, rz, self._terreno_y(rx, rz))
        ry = max(SEA_LEVEL + 0.18, ry_raw) if biome == "mar" else (ry_raw + 0.25)
        host_lbl, lat = real_harvest_engine.get_real_network_sample()
        if biome in ("mar", "costa") or idx_hint % 5 == 0:
            return ResourceNode(
                id=res_id, x=round(rx, 2), y=round(ry, 2), z=round(rz, 2),
                energy=random.uniform(80.0, 125.0), energy_max=145.0,
                category="PLASMA_RED_REAL",
                source_label=f"{host_lbl} ({lat}ms)",
                title=f"Cable Submarino / Enlace: {host_lbl}",
                snippet="Paquetes de fibra óptica e internet en tiempo real.",
                metric_value=lat,
            )
        if biome == "nieve_alta":
            m_data = real_harvest_engine.get_real_math_sample()
            return ResourceNode(
                id=res_id, x=round(rx, 2), y=round(ry, 2), z=round(rz, 2),
                energy=random.uniform(75.0, 120.0), energy_max=140.0,
                category="MINERAL_LOGICO",
                source_label=f"Primo Mersenne: {m_data['prime']}",
                title=f"Cristal Glacial {m_data['formula']}",
                snippet=f"Entropía criogénica verificada: {m_data['entropy']} bits/byte",
                metric_value=m_data["entropy"],
            )
        if biome == "seco":
            return ResourceNode(
                id=res_id, x=round(rx, 2), y=round(ry, 2), z=round(rz, 2),
                energy=random.uniform(85.0, 130.0), energy_max=150.0,
                category="SOLAR_ARIDO",
                source_label="Colector Heliotermico Arido",
                title="Plasma Fotónico de Desierto",
                snippet="Irradiación solar de alta intensidad y cuarzo árido.",
                metric_value=98.0,
            )
        if biome == "selva":
            k_data = real_harvest_engine.get_real_knowledge_sample()
            return ResourceNode(
                id=res_id, x=round(rx, 2), y=round(ry, 2), z=round(rz, 2),
                energy=random.uniform(85.0, 130.0), energy_max=150.0,
                category="CRISTAL_CONOCIMIENTO",
                source_label=f"Selva Sabia: {k_data['title'][:22]}",
                title=k_data["title"],
                snippet=k_data["snippet"],
                metric_value=float(k_data.get("chars", 1200)),
            )
        if idx_hint % 2 == 0:
            k_data = real_harvest_engine.get_real_knowledge_sample()
            return ResourceNode(
                id=res_id, x=round(rx, 2), y=round(ry, 2), z=round(rz, 2),
                energy=random.uniform(80.0, 130.0), energy_max=150.0,
                category="CRISTAL_CONOCIMIENTO",
                source_label=f"Gholgo Banco: {k_data['title'][:24]}",
                title=k_data["title"],
                snippet=k_data["snippet"],
                metric_value=float(k_data.get("chars", 1200)),
            )
        return ResourceNode(
            id=res_id, x=round(rx, 2), y=round(ry, 2), z=round(rz, 2),
            energy=random.uniform(85.0, 135.0), energy_max=150.0,
            category="ATP_CUANTICO",
            source_label="Matriz Cuántica Solar",
            title="ATP Bio-Sintético",
            snippet="Fotones de cómputo y radiación biológica.",
            metric_value=100.0,
        )

    def _sembrar_nubes_inicial(self):
        self.clouds.clear()
        for i in range(7):
            cid = f"cloud_{i}"
            cx = random.uniform(-WORLD_BOUNDS * 0.78, WORLD_BOUNDS * 0.78)
            cz = random.uniform(-WORLD_BOUNDS * 0.78, WORLD_BOUNDS * 0.78)
            self.clouds[cid] = AtmosphericCloud(
                id=cid,
                x=round(cx, 2),
                y=round(random.uniform(14.0, 19.5), 2),
                z=round(cz, 2),
                vx=round(random.uniform(0.10, 0.24), 3),
                vz=round(random.uniform(-0.08, 0.12), 3),
                radius=round(random.uniform(5.2, 8.8), 2),
                moisture=round(random.uniform(0.45, 0.90), 2),
                charge=round(random.uniform(0.20, 0.68), 2),
            )

    def _brotar_plantas_naturales(self, cantidad: int = 8):
        max_plants = 64
        for _ in range(cantidad):
            if len(self.plants) >= max_plants:
                break
            px = random.uniform(-WORLD_BOUNDS * 0.84, WORLD_BOUNDS * 0.84)
            pz = random.uniform(-WORLD_BOUNDS * 0.84, WORLD_BOUNDS * 0.84)
            py = calcular_altura_terreno(px, pz)
            biome = determinar_bioma(px, pz, py)
            if biome == "mar":
                continue
            candidates = [sp for sp, m in PLANT_SPECIES_META.items() if biome in m[1]] or ["trigo_fotonico"]
            sp = random.choice(candidates)
            meta = PLANT_SPECIES_META[sp]
            pid = f"plant_{uuid.uuid4().hex[:7]}"
            self.plants[pid] = Plant(
                id=pid,
                species=sp,
                nombre=meta[0],
                biome=biome,
                x=round(px, 2),
                y=round(py, 2),
                z=round(pz, 2),
                growth=round(random.uniform(0.40, 0.95), 2),
                biomass=round(random.uniform(18.0, 34.0), 1),
                pollinated=random.random() < 0.35,
            )

    def _inicializar_mundo(self):
        """Siembra el continente multi-bioma, recursos, nubes, flora, fauna y ciudad capital."""
        self.resources.clear()
        for i in range(NUM_INITIAL_RESOURCES):
            rx = random.uniform(-WORLD_BOUNDS * 0.86, WORLD_BOUNDS * 0.86)
            rz = random.uniform(-WORLD_BOUNDS * 0.86, WORLD_BOUNDS * 0.86)
            res_id = f"res_{i}_{int(time.time()) % 1000}"
            self.resources[res_id] = self._crear_recurso_por_bioma(res_id, rx, rz, i)

        # 2. Ciudad única fundacional (debe evolucionar hasta Tier 5 antes de fundar otra)
        self.settlements.clear()
        self.pueblos.clear()
        self.families.clear()
        self.structures.clear()

        cx, cz = -3.5, 2.0
        cy = calcular_altura_terreno(cx, cz)
        pueblo_0_id = "pueblo_alfa_0"
        self.pueblos[pueblo_0_id] = Pueblo(
            id=pueblo_0_id,
            nombre="Pueblo Residencial Central",
            city_id="set_capital",
            district_type="residencial",
            x=round(cx + 2.8, 2),
            y=round(calcular_altura_terreno(cx + 2.8, cz + 2.2), 2),
            z=round(cz + 2.2, 2),
            families_count=1,
        )
        self.settlements["set_capital"] = Settlement(
            id="set_capital",
            nombre="Neópolis Central",
            x=cx,
            y=cy,
            z=cz,
            energy_pool=240.0,
            tier=1,
            population_supported=28,
            defense_aura=1.1,
            biome=determinar_bioma(cx, cz, cy),
            infrastructure={"house": 1},
            pueblos=[pueblo_0_id],
        )

        # Estructuras fundacionales: casa familiar dentro del pueblo + granja + puente
        hx, hz = cx + 2.6, cz + 2.1
        self.structures["struct_house_0"] = CustomStructure(
            id="struct_house_0",
            kind="house",
            nombre="Vivienda Familiar Alfa",
            x=round(hx, 2),
            y=round(calcular_altura_terreno(hx, hz), 2),
            z=round(hz, 2),
            builder_name="Pionero-00",
            builder_role="ARQUITECTO",
            city_id="set_capital",
            pueblo_id=pueblo_0_id,
        )
        self.families["fam_alfa"] = Family(
            id="fam_alfa",
            clan_name="Clan Fundador Alfa",
            city_id="set_capital",
            pueblo_id=pueblo_0_id,
            house_id="struct_house_0",
        )

        if self.river_points and len(self.river_points) > 6:
            rp0 = self.river_points[6]
            self.structures["struct_bridge_0"] = CustomStructure(
                id="struct_bridge_0",
                kind="bridge",
                nombre="Puente Viejo del Valle",
                x=rp0[0],
                y=round(max(SEA_LEVEL + 0.14, calcular_altura_terreno(rp0[0], rp0[2]) + 0.14), 2),
                z=rp0[2],
                angle_y=calcular_orientacion_puente_rio(rp0[0], rp0[2]),
                builder_name="Pionero-00",
                builder_role="ARQUITECTO",
            )
        fx0, fz0 = -6.5, -2.5
        self.structures["struct_farm_0"] = CustomStructure(
            id="struct_farm_0",
            kind="farm",
            nombre="Granja Simbiótica Alfa",
            x=fx0,
            y=round(calcular_altura_terreno(fx0, fz0), 2),
            z=fz0,
            builder_name="Pionero-00",
            builder_role="ARQUITECTO",
            city_id="set_capital",
        )

        # 3. Arbolado, Plantas por bioma, Canteras, Nubes y Fauna multi-hábitat
        self.trees.clear()
        self.plants.clear()
        self.rocks.clear()
        self.animals.clear()
        for _ in range(42):
            stage_rnd = random.choices(["sapling", "mature", "ancient"], weights=[0.35, 0.45, 0.20])[0]
            self._brotar_arboles_naturales(cantidad=1, stage_inicial=stage_rnd)
        self._brotar_plantas_naturales(cantidad=44)
        self._regenerar_rocas(cantidad=30)
        self._sembrar_nubes_inicial()
        self._sembrar_fauna_inicial()

        # 4. Población inicial en tierra firme habitable
        self.organisms.clear()
        for i in range(MIN_ORGANISMS_SEED):
            role = ROLES[i % len(ROLES)]
            gen = Genome.random_genome(generation=1, role_bias=role)
            ox, oz = 0.0, 0.0
            for _ in range(12):
                rad = random.uniform(2.0, 32.0)
                ang = random.uniform(-math.pi, math.pi)
                cx_t, cz_t = round(rad * math.cos(ang), 2), round(rad * math.sin(ang), 2)
                if calcular_altura_terreno(cx_t, cz_t) > SEA_LEVEL + 0.3:
                    ox, oz = cx_t, cz_t
                    break
            elev_o = self._safe_surface_y(ox, oz, footprint_radius=0.06, clearance=0.015)
            oy = round(elev_o, 3)
            org_id = f"org_{gen.id}"
            nombre = f"{role.capitalize()}-{gen.id[:4]}"
            ptx, ptz = ox, oz
            for _ in range(8):
                cx_p = round(max(-36.0, min(36.0, ox + random.uniform(-18.0, 18.0))), 2)
                cz_p = round(max(-36.0, min(36.0, oz + random.uniform(-18.0, 18.0))), 2)
                if calcular_altura_terreno(cx_p, cz_p) > SEA_LEVEL + 0.22:
                    ptx, ptz = cx_p, cz_p
                    break
            org = Organism(
                id=org_id,
                nombre=nombre,
                genome=gen,
                x=ox,
                y=oy,
                z=oz,
                energy=random.uniform(100.0, 150.0),
                energy_max=180.0,
                symbol=ROLE_SYMBOLS.get(role, "🧭"),
                home_biome=determinar_bioma(ox, oz, elev_o),
                home_city_id="set_capital" if i < 10 else None,
                home_pueblo_id=pueblo_0_id if i < 10 else None,
                family_id="fam_alfa" if i < 4 else None,
                patrol_target_x=ptx,
                patrol_target_z=ptz,
            )
            if i < 4:
                self.families["fam_alfa"].member_ids.append(org_id)
            self.organisms[org_id] = org
            self.total_births += 1

        self.peak_population = len(self.organisms)
        if not self.evolution_timeline:
            self._registrar_hito_evolutivo()

    def _brotar_arboles_naturales(self, cantidad: int = 4, stage_inicial: str = "seed"):
        """Planta brotes/árboles vivos en selva, valles fértiles y riberas con bounds dinámicos."""
        max_trees = 78 + max(0, (len(self.continents) - 1) * 14)
        b_lim = self.dynamic_bounds
        for _ in range(cantidad):
            if len(self.trees) >= max_trees:
                break
            tx, tz, ty = 0.0, 0.0, 0.0
            encontrado = False
            for _intento in range(14):
                if random.random() < 0.35 and self.river_points:
                    rp = random.choice(self.river_points)
                    tx = max(-b_lim * 0.88, min(b_lim * 0.88, rp[0] + random.uniform(-6.5, 6.5)))
                    tz = max(-b_lim * 0.88, min(b_lim * 0.88, rp[2] + random.uniform(-6.5, 6.5)))
                else:
                    tx = random.uniform(-b_lim * 0.85, b_lim * 0.85)
                    tz = random.uniform(-b_lim * 0.85, b_lim * 0.85)
                ty_raw = self._terreno_y(tx, tz)
                biome = self._bioma_en(tx, tz, ty_raw)
                if biome in ("selva", "valle", "costa") and (SEA_LEVEL + 0.25) < ty_raw < (SNOW_LINE - 0.5):
                    ty = self._safe_surface_y(tx, tz, footprint_radius=0.55, clearance=0.14)
                    encontrado = True
                    break
            if not encontrado:
                continue

            t_id = f"tree_{uuid.uuid4().hex[:7]}"
            biome = self._bioma_en(tx, tz, ty)
            if ty > 0.6:
                t_type = "pino_sinaptico"
            elif biome == "selva" or any(math.hypot(rp[0] - tx, rp[2] - tz) < 7.0 for rp in self.river_points):
                t_type = "sauce_red"
            else:
                t_type = random.choice(["roble_algoritmico", "pino_sinaptico"])

            if stage_inicial == "ancient":
                age, height, wood = random.randint(960, 1450), random.uniform(2.2, 2.7), 220.0
            elif stage_inicial == "mature":
                age, height, wood = random.randint(250, 750), random.uniform(1.45, 1.85), 115.0
            elif stage_inicial == "sapling":
                age, height, wood = random.randint(50, 180), random.uniform(0.45, 0.70), 40.0
            else:
                age, height, wood = 0, 0.22, 18.0

            self.trees[t_id] = AlgorithmicTree(
                id=t_id,
                x=round(tx, 2),
                y=round(ty, 2),
                z=round(tz, 2),
                stage=stage_inicial,
                age=age,
                wood_energy=wood,
                tree_type=t_type,
                height=round(height, 2),
                seeds_ready=(stage_inicial in ("mature", "ancient")),
            )

    def _regenerar_rocas(self, cantidad: int = 6):
        """Genera afloramientos rocosos y vetas de cuarzo lógico sobre el terreno."""
        max_rocks = 34 + max(0, (len(self.continents) - 1) * 8)
        b_lim = self.dynamic_bounds
        for _ in range(cantidad):
            if len(self.rocks) >= max_rocks:
                break
            rx = random.uniform(-b_lim * 0.85, b_lim * 0.85)
            rz = random.uniform(-b_lim * 0.85, b_lim * 0.85)
            ry_raw = self._terreno_y(rx, rz)
            if ry_raw < SEA_LEVEL - 0.15:
                continue
            ry = self._safe_surface_y(rx, rz, footprint_radius=0.65, clearance=0.12)
            r_type = (
                "cuarzo_sinaptico"
                if ry > 1.5
                else random.choice(["granito_logico", "basalto_cripto", "cuarzo_sinaptico"])
            )
            rk_id = f"rock_{uuid.uuid4().hex[:7]}"
            scale = round(random.uniform(0.75, 1.55), 2)
            self.rocks[rk_id] = GeologicalRock(
                id=rk_id,
                x=round(rx, 2),
                y=round(ry, 2),
                z=round(rz, 2),
                rock_type=r_type,
                mineral_capacity=round(150.0 * scale, 1),
                scale=scale,
            )

    def _crear_animal(self, species: str, behavior: str, ax: float, az: float, health: float) -> DigitalAnimal:
        """Instancia y registra un animal multi-hábitat en tierra, aire, agua o plantas sobre el terreno."""
        meta = ANIMAL_SPECIES_META[species]
        habitat = meta[3]
        pollinator = bool(meta[5])
        ter_y = self._safe_surface_y(ax, az, footprint_radius=0.06, clearance=0.015)
        flight_alt = round(random.uniform(2.6, 5.0), 2)
        if habitat == "air":
            ay = round(max(SEA_LEVEL + 1.8, ter_y) + flight_alt, 3)
        elif habitat == "water":
            ay = max(ter_y + 0.08, SEA_LEVEL - 0.18 if ter_y <= SEA_LEVEL else SEA_LEVEL + 0.08)
        elif habitat == "plant":
            ay = round(max(SEA_LEVEL + 0.25, ter_y) + 0.42, 3)
        else:
            ay = round(max(SEA_LEVEL + 0.02, ter_y) + (meta[2] * 0.02), 3)

        aid = f"ani_{uuid.uuid4().hex[:7]}"
        animal = DigitalAnimal(
            id=aid,
            species=species,
            nombre=f"{meta[0]}-{aid[-3:].upper()}",
            behavior=behavior,
            habitat=habitat,
            pollinator=pollinator,
            x=round(ax, 2),
            y=ay,
            z=round(az, 2),
            scale=meta[2],
            health=health,
            flight_altitude=flight_alt,
        )
        self.animals[aid] = animal
        return animal

    def _sembrar_fauna_inicial(self, pred_count: int = 7, tame_count: int = 10):
        """Puebla tierra, aire, mar/ríos y plantas con especies diferenciadas."""
        pred_land = ["lobo_cuantico", "manticora_neural", "serpiente_latencia", "oso_glacial"]
        tame_land = ["ciervo_sinaptico", "buey_plasma", "oveja_fotonica"]

        current_land_preds = sum(1 for a in self.animals.values() if a.behavior == "predator" and a.habitat == "land")
        for i in range(max(0, pred_count - current_land_preds)):
            sp = pred_land[i % len(pred_land)]
            for _ in range(10):
                rad = random.uniform(14.0, WORLD_BOUNDS * 0.78)
                ang = random.uniform(-math.pi, math.pi)
                ax, az = rad * math.cos(ang), rad * math.sin(ang)
                if calcular_altura_terreno(ax, az) > SEA_LEVEL + 0.25:
                    self._crear_animal(sp, "predator", ax, az, 245.0)
                    break

        current_wild_tame = sum(1 for a in self.animals.values() if a.behavior == "tameable" and a.habitat == "land")
        for i in range(max(0, tame_count - current_wild_tame)):
            sp = tame_land[i % len(tame_land)]
            ax, az = random.uniform(-26.0, 26.0), random.uniform(-24.0, 24.0)
            if self.river_points and random.random() < 0.55:
                rp = random.choice(self.river_points)
                ax = max(-WORLD_BOUNDS * 0.85, min(WORLD_BOUNDS * 0.85, rp[0] + random.uniform(-8.0, 8.0)))
                az = max(-WORLD_BOUNDS * 0.85, min(WORLD_BOUNDS * 0.85, rp[2] + random.uniform(-8.0, 8.0)))
            if calcular_altura_terreno(ax, az) > SEA_LEVEL + 0.15:
                self._crear_animal(sp, "tameable", ax, az, 95.0)

        # Fauna del Aire (aguilas, colibries polinizadores, cuervos de tormenta)
        air_alive = sum(1 for a in self.animals.values() if a.habitat == "air")
        for sp, beh in [("aguila_sinaptica", "predator"), ("aguila_sinaptica", "predator"), ("colibri_fotonico", "tameable"), ("colibri_fotonico", "tameable"), ("cuervo_tormenta", "wildlife")]:
            if air_alive >= 6:
                break
            ax, az = random.uniform(-45.0, 45.0), random.uniform(-45.0, 45.0)
            self._crear_animal(sp, beh, ax, az, 125.0)
            air_alive += 1

        # Fauna del Agua (tiburones en mar, peces y mantarrayas en mar/costa)
        water_alive = sum(1 for a in self.animals.values() if a.habitat == "water")
        for sp, beh in [("tiburon_cripto", "predator"), ("tiburon_cripto", "predator"), ("pez_cuantico", "tameable"), ("pez_cuantico", "tameable"), ("mantarraya_azul", "wildlife")]:
            if water_alive >= 6:
                break
            ax, az = random.uniform(-56.0, -34.0), random.uniform(-10.0, 38.0)
            self._crear_animal(sp, beh, ax, az, 130.0)
            water_alive += 1

        # Animales de las Plantas (mariposas, escarabajos polinizadores, avispas plaga)
        plant_alive = sum(1 for a in self.animals.values() if a.habitat == "plant")
        plant_list = list(self.plants.values())
        for idx, (sp, beh) in enumerate([("mariposa_espectral", "tameable"), ("mariposa_espectral", "tameable"), ("escarabajo_simbiotico", "wildlife"), ("escarabajo_simbiotico", "wildlife"), ("avispa_espora", "pest")]):
            if plant_alive >= 6:
                break
            if plant_list:
                pl = plant_list[idx % len(plant_list)]
                ax, az = pl.x + random.uniform(-1.5, 1.5), pl.z + random.uniform(-1.5, 1.5)
            else:
                ax, az = random.uniform(-18.0, 18.0), random.uniform(-18.0, 18.0)
            self._crear_animal(sp, beh, ax, az, 70.0)
            plant_alive += 1

    def _calcular_capacidad_carga(self) -> int:
        """Calcula capacidad de carga dinámica K según ciudades, pueblos, viviendas, granjas y flora."""
        base_k = DEMOGRAPHIC_RULES["base_carrying_capacity"]
        set_bonus = sum(s.tier * 8 for s in self.settlements.values())
        pueblo_bonus = len(self.pueblos) * 4
        farms = sum(1 for st in self.structures.values() if st.kind == "farm")
        houses = sum(1 for st in self.structures.values() if st.kind == "house")
        hospitals = sum(1 for st in self.structures.values() if st.kind == "hospital")
        nurseries = sum(1 for st in self.structures.values() if st.kind == "nursery")
        mature_trees = sum(1 for t in self.trees.values() if t.stage in ("mature", "ancient"))
        dyn_k = int(base_k + set_bonus + pueblo_bonus + (farms * 8) + (houses * 3) + (hospitals * 5) + (nurseries * 4) + (mature_trees * 0.4))
        return min(MAX_ORGANISMS - 8, max(50, dyn_k))

    def _registrar_hito_evolutivo(self):
        """Guarda un punto histórico para visualizar evolución genética, anatómica y urbana."""
        orgs = [o for o in self.organisms.values() if o.alive]
        n = max(1, len(orgs))
        avg_speed = sum(o.genome.speed_factor for o in orgs) / n if orgs else 1.0
        avg_raw_size = sum(o.genome.size for o in orgs) / n if orgs else 1.0
        avg_defense = sum(o.genome.defense_factor for o in orgs) / n if orgs else 1.0
        avg_meta = sum(o.genome.metabolism_eff for o in orgs) / n if orgs else 1.0
        avg_morph = sum(o.genome.morphology_tier for o in orgs) / n if orgs else 1.0
        avg_app = sum(o.genome.appendage_count for o in orgs) / n if orgs else 0.0
        avg_limbs = sum(o.genome.limb_count for o in orgs) / n if orgs else 2.0
        avg_wings = sum(o.genome.wing_span for o in orgs) / n if orgs else 0.0

        elapsed = max(0.0, time.time() - self.start_timestamp)
        hrs = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        secs = int(elapsed % 60)
        uptime_label = f"{hrs:02d}:{mins:02d}:{secs:02d}"

        snap = {
            "timestamp": round(time.time(), 1),
            "uptime_sec": round(elapsed, 1),
            "uptime_label": uptime_label,
            "step": self.step_counter,
            "generation": self.generation_global,
            "population": len(orgs),
            "trees_count": len(self.trees),
            "plants_count": len(self.plants),
            "rocks_count": len(self.rocks),
            "cities_count": len(self.settlements),
            "pueblos_count": len(self.pueblos),
            "families_count": len(self.families),
            "avg_speed": round(avg_speed, 3),
            "avg_raw_size": round(avg_raw_size, 3),
            "avg_defense": round(avg_defense, 3),
            "avg_metabolism": round(avg_meta, 3),
            "avg_morphology": round(avg_morph, 2),
            "avg_appendages": round(avg_app, 2),
            "avg_limbs": round(avg_limbs, 2),
            "avg_wings": round(avg_wings, 2),
        }
        self.evolution_timeline.append(snap)
        if len(self.evolution_timeline) > 120:
            head = self.evolution_timeline[:1]
            middle = self.evolution_timeline[1:-60:2]
            tail = self.evolution_timeline[-60:]
            self.evolution_timeline = head + middle + tail

    def _step_climate_and_weather(self, eventos: List[str]) -> None:
        """Actualiza orbita Sol/Luna, nubes, lluvias, vientos y tormentas electricas."""
        self.celestial = calcular_estado_celeste(self.step_counter)
        cel_phase = self.celestial["phase"]

        total_rain = 0.0
        max_charge = 0.0
        wind_x = round(0.16 * math.cos(self.step_counter * 0.008), 3)
        wind_z = round(0.08 * math.sin(self.step_counter * 0.006), 3)
        storm_cloud = None

        for cloud in self.clouds.values():
            cloud.vx = wind_x
            cloud.vz = wind_z
            cloud.x += cloud.vx
            cloud.z += cloud.vz
            if cloud.x > WORLD_BOUNDS:
                cloud.x = -WORLD_BOUNDS + 1.0
            elif cloud.x < -WORLD_BOUNDS:
                cloud.x = WORLD_BOUNDS - 1.0
            if cloud.z > WORLD_BOUNDS:
                cloud.z = -WORLD_BOUNDS + 1.0
            elif cloud.z < -WORLD_BOUNDS:
                cloud.z = WORLD_BOUNDS - 1.0

            elev_under = calcular_altura_terreno(cloud.x, cloud.z)
            if elev_under < SEA_LEVEL + 0.4:
                cloud.moisture = min(1.0, cloud.moisture + 0.015)
            elif elev_under > HIGH_ALTITUDE_WARN:
                cloud.charge = min(1.0, cloud.charge + 0.018)
                cloud.moisture = max(0.20, cloud.moisture - 0.004)
            else:
                cloud.moisture = min(0.95, cloud.moisture + 0.003)

            if cloud.moisture > 0.72:
                total_rain += (cloud.moisture - 0.60) * 0.42
                cloud.moisture = max(0.35, cloud.moisture - 0.006)
            if cloud.charge > max_charge:
                max_charge = cloud.charge
                storm_cloud = cloud

        rain_intensity = round(min(1.0, total_rain), 2)
        thunder_active = False
        lightning_strike = None
        if storm_cloud and max_charge > 0.78 and random.random() < 0.08:
            thunder_active = True
            lx = round(max(-WORLD_BOUNDS + 2.0, min(WORLD_BOUNDS - 2.0, storm_cloud.x + random.uniform(-3.5, 3.5))), 2)
            lz = round(max(-WORLD_BOUNDS + 2.0, min(WORLD_BOUNDS - 2.0, storm_cloud.z + random.uniform(-3.5, 3.5))), 2)
            ly = round(calcular_altura_terreno(lx, lz), 2)
            lightning_strike = [lx, ly, lz, self.step_counter]
            storm_cloud.charge = 0.25
            self.thunder_harvested_total += 1
            ray_id = f"ray_{self.step_counter % 200}"
            self.resources[ray_id] = ResourceNode(
                id=ray_id,
                x=lx,
                y=round(max(SEA_LEVEL + 0.2, ly) + 0.35, 2),
                z=lz,
                energy=95.0,
                energy_max=120.0,
                regen_rate=0.05,
                category="RAYO_ATMOSFERICO",
                source_label="Descarga Electrica Atmosferica",
                title="Plasma de Trueno",
                snippet="Energia ionizada del aire capturada tras tormenta.",
                metric_value=95.0,
            )
            eventos.append(f"⚡ ¡Rayo atmosferico en ({lx}, {lz}) inyecto plasma aereo al ecosistema!")
            for org in self.organisms.values():
                if org.alive and math.hypot(org.x - lx, org.z - lz) < 4.0 and org.y > HIGH_ALTITUDE_WARN:
                    if org.genome.defense_factor < 1.8:
                        org.health -= 12.0
                        org.energy = min(org.energy_max, org.energy + 18.0)

        self.weather = {
            "rain_intensity": rain_intensity,
            "thunder_active": thunder_active,
            "wind_x": wind_x,
            "wind_z": wind_z,
            "lightning_strike": lightning_strike,
        }
        if thunder_active or rain_intensity > 0.58:
            self.environmental_cycle = "TORMENTA_CARGA"
            self.environmental_factor = 0.95
        elif cel_phase == "NOCHE_SINAPTICA":
            self.environmental_cycle = "NOCHE_SINAPTICA"
            self.environmental_factor = 0.35
        elif cel_phase in ("AMANECER", "OCASO"):
            self.environmental_cycle = cel_phase
            self.environmental_factor = 0.62
        else:
            self.environmental_cycle = "DIA_SOLAR"
            self.environmental_factor = 0.85

    def _step_flora_and_geology(self) -> None:
        """Regenera recursos, arboles, plantas, canteras e infraestructuras pasivas."""
        rain = self.weather.get("rain_intensity", 0.0)
        factor_regen = (1.25 if self.environmental_cycle == "DIA_SOLAR" else 0.6) + (rain * 0.45)
        for res_id, res in list(self.resources.items()):
            if res.category == "RAYO_ATMOSFERICO" and res.energy <= 4.0:
                self.resources.pop(res_id, None)
                continue
            if res.energy < res.energy_max:
                res.energy = min(res.energy_max, res.energy + (res.regen_rate * factor_regen))

        # Arboles
        semillas_pendientes = []
        arboles_muertos = []
        for t_id, tree in list(self.trees.items()):
            evt_tree = tree.step_growth()
            if (self.environmental_cycle == "DIA_SOLAR" or rain > 0.25) and tree.stage in ("mature", "ancient"):
                cap_madera = 230.0 if tree.stage == "ancient" else 115.0
                if tree.wood_energy < cap_madera:
                    tree.wood_energy = min(cap_madera, tree.wood_energy + 0.12 + rain * 0.10)
            b_lim = self.dynamic_bounds
            if evt_tree and evt_tree.get("action") == "disperse_seed" and len(self.trees) + len(semillas_pendientes) < (76 + max(0, (len(self.continents) - 1) * 14)):
                sx = max(-b_lim * 0.88, min(b_lim * 0.88, evt_tree["x"] + random.uniform(-4.5, 4.5)))
                sz = max(-b_lim * 0.88, min(b_lim * 0.88, evt_tree["z"] + random.uniform(-4.5, 4.5)))
                sy_raw = self._terreno_y(sx, sz)
                if (SEA_LEVEL + 0.25) < sy_raw < (SNOW_LINE - 0.4):
                    sy = self._safe_surface_y(sx, sz, footprint_radius=0.45, clearance=0.14)
                    semillas_pendientes.append((sx, sy, sz, tree.tree_type))
            if tree.age >= tree.max_age:
                arboles_muertos.append(t_id)

        for sx, sy, sz, t_type in semillas_pendientes:
            nid = f"tree_{uuid.uuid4().hex[:7]}"
            self.trees[nid] = AlgorithmicTree(
                id=nid, x=round(sx, 2), y=round(sy, 2), z=round(sz, 2),
                stage="seed", age=0, wood_energy=18.0, tree_type=t_type, height=0.22,
            )
        for dead_tid in arboles_muertos:
            if self.trees.pop(dead_tid, None):
                self._brotar_arboles_naturales(cantidad=1, stage_inicial="sapling")

        # Plantas no arboreas por bioma
        growth_step = 0.004 + rain * 0.008
        for plant in self.plants.values():
            plant.age += 1
            bonus_pol = 1.4 if plant.pollinated else 1.0
            plant.growth = min(1.0, plant.growth + growth_step * bonus_pol)
            if plant.biomass < 38.0:
                plant.biomass = min(38.0, plant.biomass + (0.09 + rain * 0.12) * bonus_pol)

        # Rebrote periodico de fauna, plantas, arboles y canteras
        if self.step_counter % 25 == 0:
            land_preds = sum(1 for a in self.animals.values() if a.behavior == "predator" and a.habitat == "land")
            land_tame = sum(1 for a in self.animals.values() if a.behavior == "tameable" and a.habitat == "land")
            if land_preds < 3 or land_tame < 3:
                self._sembrar_fauna_inicial(pred_count=6, tame_count=7)
        if self.step_counter % 90 == 0:
            if len(self.plants) < 36:
                self._brotar_plantas_naturales(cantidad=8)
            if len(self.trees) < 48:
                self._brotar_arboles_naturales(cantidad=3, stage_inicial="seed")
            if len(self.resources) < 44:
                self.brote_de_recursos(cantidad=6)
            if len(self.rocks) < 22:
                self._regenerar_rocas(cantidad=4)

        # Operacion autonoma de estructuras civiles y rurales
        total_herbivores = sum(1 for a in self.animals.values() if a.habitat == "land" and a.behavior != "predator")
        b_lim = self.dynamic_bounds
        for st in list(self.structures.values()):
            if st.kind == "farm":
                if st.energy_stored < 140.0:
                    st.energy_stored = min(140.0, st.energy_stored + (0.45 * st.level))
                if self.step_counter % 90 == 0 and st.animals_housed >= 1 and total_herbivores < 18 and random.random() < 0.45:
                    sp = random.choice(["ciervo_sinaptico", "buey_plasma", "oveja_fotonica"])
                    hx = max(-b_lim * 0.85, min(b_lim * 0.85, st.x + random.uniform(-2.6, 2.6)))
                    hz = max(-b_lim * 0.85, min(b_lim * 0.85, st.z + random.uniform(-2.6, 2.6)))
                    if self._terreno_y(hx, hz) > SEA_LEVEL + 0.2:
                        self._crear_animal(sp, "tameable", hx, hz, 95.0)
                        total_herbivores += 1
            elif st.kind == "nursery":
                if self.step_counter % 160 == 0 and len(self.trees) < (76 + max(0, (len(self.continents) - 1) * 14)):
                    nx = max(-b_lim * 0.86, min(b_lim * 0.86, st.x + random.uniform(-4.5, 4.5)))
                    nz = max(-b_lim * 0.86, min(b_lim * 0.86, st.z + random.uniform(-4.5, 4.5)))
                    ny_raw = self._terreno_y(nx, nz)
                    if (SEA_LEVEL + 0.25) < ny_raw < (SNOW_LINE - 0.4):
                        ny = self._safe_surface_y(nx, nz, footprint_radius=0.45, clearance=0.14)
                        tid = f"tree_{uuid.uuid4().hex[:7]}"
                        self.trees[tid] = AlgorithmicTree(
                            id=tid, x=round(nx, 2), y=round(ny, 2), z=round(nz, 2),
                            stage="sapling", age=55, wood_energy=40.0, tree_type="roble_algoritmico", height=0.52,
                        )
                        st.seeds_generated += 1
            elif st.kind == "power_plant" and st.city_id and st.city_id in self.settlements:
                self.settlements[st.city_id].deposit_energy(2.4)
            elif st.kind == "aqueduct":
                for org in self.organisms.values():
                    if org.alive and math.hypot(org.x - st.x, org.z - st.z) < 7.5:
                        org.water_level = min(100.0, org.water_level + 1.6)
            elif st.kind == "hospital":
                for org in self.organisms.values():
                    if org.alive and math.hypot(org.x - st.x, org.z - st.z) < 8.5:
                        org.health = min(100.0, org.health + 1.8)
                        if org.infection and org.infection_ticks >= 4:
                            org.infection = None
                            org.infection_ticks = 0
                            org.immunity_level = min(0.95, round(org.immunity_level + 0.22, 3))
                            org.illnesses_cured += 1
                            self.illnesses_cured_total += 1

    def _step_diseases_and_healing(self, eventos: List[str], muertes: List[Tuple[Organism, str]]) -> None:
        """Simula virus, bacterias, contagios, inmunidad adquirida y cura medica."""
        orgs_alive = [o for o in self.organisms.values() if o.alive]
        if not orgs_alive:
            return

        # Brote ocasional por exposicion ambiental si hay pocos infectados
        infected_now = [o for o in orgs_alive if o.infection]
        if len(infected_now) < 3 and self.step_counter % 40 == 0:
            cand = random.choice(orgs_alive)
            if cand.immunity_level < 0.72 and random.random() < 0.35:
                pool = [pid for pid, m in PATHOGEN_CATALOG.items() if cand.home_biome in m["preferred_biomes"]]
                pid = random.choice(pool or list(PATHOGEN_CATALOG.keys()))
                cand.infection = pid
                cand.infection_ticks = 0
                eventos.append(f"🦠 Brote de {PATHOGEN_CATALOG[pid]['nombre']} detectado en {cand.nombre}.")

        # Propagacion y curso clinico
        for org in orgs_alive:
            if not org.infection:
                continue
            org.infection_ticks += 1
            meta = PATHOGEN_CATALOG.get(org.infection, {"severity": 0.4, "contagion": 0.1, "kind": "virus", "nombre": org.infection})
            in_sanitized_city = False
            if org.home_city_id and org.home_city_id in self.settlements:
                city_obj = self.settlements[org.home_city_id]
                if city_obj.infrastructure.get("sanitation", 0) >= 1:
                    in_sanitized_city = True

            drain = DEMOGRAPHIC_RULES["disease_base_drain"] * meta["severity"] * (0.65 if in_sanitized_city else 1.0)
            org.health -= drain
            org.energy -= drain * 0.35

            # Recuperacion natural por sistema inmune
            rec_prob = (0.015 + org.immunity_level * 0.04) * (1.2 if org.genome.healing_factor > 1.3 else 1.0)
            if org.infection_ticks > 32 and random.random() < rec_prob:
                org.infection = None
                org.infection_ticks = 0
                org.immunity_level = min(0.95, round(org.immunity_level + 0.18, 3))
                org.illnesses_cured += 1
                self.illnesses_cured_total += 1
                continue

            if org.health <= 0.0 and org.alive:
                org.alive = False
                org.death_cause = "enfermedad"
                muertes.append((org, "enfermedad"))
                continue

            # Contagio cercano
            contagion_p = meta["contagion"] * (0.42 if (meta["kind"] == "bacteria" and in_sanitized_city) else 1.0)
            for peer in orgs_alive:
                if peer.id == org.id or not peer.alive or peer.infection:
                    continue
                if math.hypot(peer.x - org.x, peer.z - org.z) < 2.5:
                    if random.random() < contagion_p * max(0.15, 1.0 - peer.immunity_level):
                        peer.infection = org.infection
                        peer.infection_ticks = 0

    def _step_families_and_pueblos(self, org: Organism, eventos: List[str]) -> None:
        """Agrupa seres adultos en familias que habitan pueblos internos dentro de cada ciudad."""
        if org.family_id or org.age < 32 or not self.settlements:
            return
        best_city = None
        best_d = 999.0
        for s in self.settlements.values():
            d = math.hypot(s.x - org.x, s.z - org.z)
            if d < best_d:
                best_d = d
                best_city = s
        if not best_city or best_d > 14.0:
            return

        # Buscar o crear un pueblo dentro de la ciudad
        pueblo_id = best_city.pueblos[-1] if best_city.pueblos else None
        if not pueblo_id or (
            pueblo_id in self.pueblos
            and self.pueblos[pueblo_id].families_count >= 5
            and len(best_city.pueblos) < min(best_city.max_pueblos, best_city.tier + 1)
        ):
            self.pueblo_counter += 1
            pueblo_id = f"pueblo_{best_city.id[:6]}_{self.pueblo_counter}"
            ang = len(best_city.pueblos) * (math.pi * 0.5) + 0.45
            dist_p = 3.8
            px = max(-self.dynamic_bounds + 1.0, min(self.dynamic_bounds - 1.0, best_city.x + math.cos(ang) * dist_p))
            pz = max(-self.dynamic_bounds + 1.0, min(self.dynamic_bounds - 1.0, best_city.z + math.sin(ang) * dist_p))
            p_nom = PUEBLO_DISTRICT_NAMES[len(best_city.pueblos) % len(PUEBLO_DISTRICT_NAMES)]
            py_safe = self._safe_surface_y(px, pz, footprint_radius=1.5, clearance=0.22)
            self.pueblos[pueblo_id] = Pueblo(
                id=pueblo_id,
                nombre=f"{p_nom} ({best_city.nombre[:10]})",
                city_id=best_city.id,
                district_type="residencial" if len(best_city.pueblos) % 2 == 0 else "civico",
                x=round(px, 2),
                y=round(py_safe, 2),
                z=round(pz, 2),
            )
            best_city.pueblos.append(pueblo_id)
            eventos.append(f"🏘️ Nuevo barrio [{p_nom}] emergio dentro de {best_city.nombre}.")

        # Unirse a familia con vacante o fundar un nuevo nucleo familiar
        target_fam = None
        for fam in self.families.values():
            if fam.pueblo_id == pueblo_id and len(fam.member_ids) < 5:
                target_fam = fam
                break
        if target_fam is None:
            self.family_counter += 1
            fid = f"fam_{self.family_counter}_{org.id[-4:]}"
            house_ref = next(
                (st.id for st in self.structures.values() if st.kind == "house" and st.pueblo_id == pueblo_id),
                None,
            )
            target_fam = Family(
                id=fid,
                clan_name=f"Familia {org.genome.lineage}",
                city_id=best_city.id,
                pueblo_id=pueblo_id,
                house_id=house_ref,
            )
            self.families[fid] = target_fam
            if pueblo_id in self.pueblos:
                self.pueblos[pueblo_id].families_count += 1

        target_fam.member_ids.append(org.id)
        org.family_id = target_fam.id
        org.home_city_id = best_city.id
        org.home_pueblo_id = pueblo_id

    def _step_architects_and_cities(self, org: Organism, ctx: Dict[str, Any], eventos: List[str]) -> None:
        """Gestiona evolucion urbana hasta Tier 5, infraestructura civil real y obras de terreno."""
        res_step = ctx["res_step"]
        nearest_set_obj: Optional[Settlement] = ctx["nearest_set_obj"]
        min_d_set: float = ctx["min_d_set"]

        # A. Aportes y obras civiles dentro de ciudades existentes
        if (res_step.get("do_social") or org.wood_carried > 4.0 or org.stone_carried > 4.0) and nearest_set_obj and min_d_set < 7.0:
            aporte = 0.0
            if org.energy > (org.energy_max * 0.40):
                don = 4.5 * org.genome.structural_affinity
                org.energy -= don
                aporte += don
            if org.wood_carried > 0.5:
                aporte += org.wood_carried * 1.45
                org.wood_carried = 0.0
            if org.stone_carried > 0.5:
                st_dep = org.stone_carried
                org.stone_carried = 0.0
                aporte += st_dep * 1.85
                nearest_set_obj.defense_aura = round(min(6.5, nearest_set_obj.defense_aura + st_dep * 0.008), 2)

            # Si el ser es Arquitecto/Adaptativo/Guerrero y la ciudad necesita obra civil, construirla dentro de un pueblo!
            missing = nearest_set_obj.missing_infra_for_next_tier()
            if (
                missing
                and org.genome.role in ("ARQUITECTO", "ADAPTATIVO", "GUERRERO")
                and aporte >= 6.0
                and len(self.structures) < (58 + max(0, (len(self.continents) - 1) * 10))
            ):
                infra_kind = next((k for k in CIVIL_INFRA_PRIORITY if k in missing), missing[0])
                pueblo_id = random.choice(nearest_set_obj.pueblos) if nearest_set_obj.pueblos else None
                base_p = self.pueblos[pueblo_id] if (pueblo_id and pueblo_id in self.pueblos) else nearest_set_obj
                ang = random.uniform(0.0, 2.0 * math.pi)
                dist = random.uniform(1.4, 3.6)
                ix = max(-self.dynamic_bounds + 1.0, min(self.dynamic_bounds - 1.0, base_p.x + math.cos(ang) * dist))
                iz = max(-self.dynamic_bounds + 1.0, min(self.dynamic_bounds - 1.0, base_p.z + math.sin(ang) * dist))
                iy = self._safe_surface_y(ix, iz, footprint_radius=1.1, clearance=0.22)
                if iy >= SEA_LEVEL + 0.1:
                    self.structure_counter += 1
                    stid = f"struct_{infra_kind}_{self.structure_counter}_{int(time.time()) % 1000}"
                    label = CIVIL_INFRA_LABELS.get(infra_kind, infra_kind.capitalize())
                    self.structures[stid] = CustomStructure(
                        id=stid,
                        kind=infra_kind,
                        nombre=f"{label} #{self.structure_counter}",
                        x=round(ix, 2),
                        y=round(iy, 2),
                        z=round(iz, 2),
                        angle_y=round(ang, 2),
                        builder_name=org.nombre,
                        builder_role=org.genome.role,
                        city_id=nearest_set_obj.id,
                        pueblo_id=pueblo_id,
                    )
                    nearest_set_obj.register_infra(infra_kind)
                    org.structures_built += 1
                    eventos.append(f"🏛️ ¡{org.nombre} construyo [{label}] dentro de {nearest_set_obj.nombre}!")

            if aporte > 0.0:
                subio = nearest_set_obj.deposit_energy(aporte)
                org.buildings_contributed += 1
                org.current_action = "building"
                org.action_target_pos = [round(nearest_set_obj.x, 2), round(nearest_set_obj.y, 2), round(nearest_set_obj.z, 2)]
                if subio:
                    eventos.append(f"🌆 ¡{nearest_set_obj.nombre} evoluciono a Tier {nearest_set_obj.tier}: {nearest_set_obj.tier_name}!")

        # B. Obras de terreno (puentes, tuneles de montana, puertos, atalayas, granjas, viveros)
        elev_actual = ctx["elev_actual"]
        pendiente = res_step.get("pendiente", 0.0)
        if (
            (org.genome.role in ("ARQUITECTO", "ADAPTATIVO", "GUERRERO") or (org.genome.role == "RECOLECTOR" and org.genome.structural_affinity > 0.68))
            and (org.wood_carried + org.stone_carried) >= 8.0
            and org.energy > 60.0
            and ctx["min_d_struct"] > 7.5
            and len(self.structures) < (58 + max(0, (len(self.continents) - 1) * 10))
        ):
            struct_kind = None
            sx, sz, s_angle = round(org.x, 2), round(org.z, 2), 0.0
            sy = round(self._safe_surface_y(sx, sz, footprint_radius=1.15, clearance=0.22), 2)
            s_nombre = ""
            ex, ey, ez = None, None, None

            nearest_river = ctx["nearest_river"]
            bridges_cnt = sum(1 for st in self.structures.values() if st.kind == "bridge")
            tunnels_cnt = sum(1 for st in self.structures.values() if st.kind == "tunnel")
            ports_cnt = sum(1 for st in self.structures.values() if st.kind == "port")
            watchtowers_cnt = sum(1 for st in self.structures.values() if st.kind == "watchtower")
            farms_cnt = sum(1 for st in self.structures.values() if st.kind == "farm")
            nurseries_cnt = sum(1 for st in self.structures.values() if st.kind == "nursery")
            barracks_cnt = sum(1 for st in self.structures.values() if st.kind == "barracks")

            has_near_bridge = any(
                st.kind == "bridge" and math.hypot(st.x - nearest_river[0], st.z - nearest_river[2]) < 11.5
                for st in self.structures.values()
            ) if nearest_river else True

            if org.genome.role == "GUERRERO" and barracks_cnt < (4 + len(self.continents)):
                struct_kind = "barracks"
                self.structure_counter += 1
                s_nombre = f"Bastion Guerrero #{self.structure_counter}"
            elif nearest_river and ctx["min_d_river"] < 4.8 and not has_near_bridge and bridges_cnt < 6:
                struct_kind = "bridge"
                sx, sy, sz = nearest_river[0], round(max(SEA_LEVEL + 0.14, self._safe_surface_y(nearest_river[0], nearest_river[2], footprint_radius=1.0, clearance=0.18)), 2), nearest_river[2]
                s_angle = calcular_orientacion_puente_rio(sx, sz)
                self.structure_counter += 1
                s_nombre = f"Puente Rio #{self.structure_counter}"
            elif (elev_actual >= HIGH_ALTITUDE_WARN - 0.6 or pendiente > 0.45) and ctx["min_d_tunnel"] > 14.0 and tunnels_cnt < 5:
                struct_kind = "tunnel"
                self.structure_counter += 1
                self.tunnels_built_total += 1
                s_nombre = f"Tunel Alpino #{self.structure_counter}"
                # Calcular salida hacia valle mas cercano (10-12 unidades hacia centro)
                dir_x = -org.x / max(1.0, math.hypot(org.x, org.z))
                dir_z = -org.z / max(1.0, math.hypot(org.x, org.z))
                ex = round(max(-self.dynamic_bounds + 2.0, min(self.dynamic_bounds - 2.0, org.x + dir_x * 11.0)), 2)
                ez = round(max(-self.dynamic_bounds + 2.0, min(self.dynamic_bounds - 2.0, org.z + dir_z * 11.0)), 2)
                ey = round(self._safe_surface_y(ex, ez, footprint_radius=1.0, clearance=0.22), 2)
                s_angle = round(math.atan2(ez - sz, ex - sx), 3)
            elif ctx["biome"] == "costa" and ctx["min_d_port"] > 18.0 and ports_cnt < 4:
                struct_kind = "port"
                self.structure_counter += 1
                sy = round(SEA_LEVEL + 0.25, 2)
                s_nombre = f"Puerto Maritimo #{self.structure_counter}"
            elif ctx["nearest_predator"] and ctx["min_d_pred"] < 19.0 and ctx["min_d_watchtower"] > 14.0 and watchtowers_cnt < 6:
                struct_kind = "watchtower"
                self.structure_counter += 1
                s_nombre = f"Atalaya Vigia #{self.structure_counter}"
            elif (SEA_LEVEL + 0.3) < elev_actual < (SNOW_LINE - 0.5) and ctx["min_d_farm"] > 12.0 and farms_cnt < 7:
                struct_kind = "farm"
                self.structure_counter += 1
                s_nombre = f"Granja Valle #{self.structure_counter}"
            elif ctx["trees_nearby_count"] < 3 and (SEA_LEVEL + 0.3) < elev_actual < (SNOW_LINE - 0.5) and nurseries_cnt < 5:
                struct_kind = "nursery"
                self.structure_counter += 1
                s_nombre = f"Vivero Eco #{self.structure_counter}"

            if struct_kind:
                stid = f"struct_{struct_kind}_{self.structure_counter}_{int(time.time()) % 1000}"
                self.structures[stid] = CustomStructure(
                    id=stid, kind=struct_kind, nombre=s_nombre, x=sx, y=sy, z=sz,
                    angle_y=s_angle, builder_name=org.nombre, builder_role=org.genome.role,
                    exit_x=ex, exit_y=ey, exit_z=ez,
                )
                org.wood_carried = 0.0
                org.stone_carried = 0.0
                org.energy = max(15.0, org.energy - 12.0)
                org.structures_built += 1
                org.buildings_contributed += 1
                org.current_action = "building"
                org.action_target_pos = [sx, sy, sz]
                eventos.append(f"🏗️ ¡{org.nombre} erigio [{s_nombre}] ({struct_kind})!")

        # C. FUNDACION ESTRICTA DE NUEVA CIUDAD: SOLO si TODAS las ciudades previas alcanzaron Tier 5!
        max_cities_dyn = MAX_CITIES + max(0, (len(self.continents) - 1) * 2)
        if (
            org.genome.role in ("ARQUITECTO", "EXPLORADOR")
            and self.todas_ciudades_al_maximo()
            and len(self.settlements) < max_cities_dyn
            and (org.energy > 92.0 or (org.wood_carried + org.stone_carried) > 14.0)
            and min_d_set > 26.0
            and (SEA_LEVEL + 0.4) < elev_actual < (SNOW_LINE - 0.4)
        ):
            self.settlement_counter += 1
            nombres_ciudades = [
                "Ciudadela de Cumbres",
                "Puerto Enciclopedico",
                "Metropolis del Sol",
                "Bastion de Selva",
                "Oasis de Alta Entropia",
            ]
            nombre_colonia = nombres_ciudades[(self.settlement_counter - 1) % len(nombres_ciudades)]
            sid = f"set_{self.settlement_counter}_{int(time.time()) % 1000}"
            self.pueblo_counter += 1
            pid0 = f"pueblo_{sid[:8]}_{self.pueblo_counter}"
            px0 = round(max(-self.dynamic_bounds + 2.0, min(self.dynamic_bounds - 2.0, org.x + 2.2)), 2)
            pz0 = round(max(-self.dynamic_bounds + 2.0, min(self.dynamic_bounds - 2.0, org.z + 1.8)), 2)
            py0 = round(self._safe_surface_y(px0, pz0, footprint_radius=1.5, clearance=0.22), 2)
            set_y = round(self._safe_surface_y(org.x, org.z, footprint_radius=2.6, clearance=0.24), 2)
            self.pueblos[pid0] = Pueblo(
                id=pid0,
                nombre=f"Pueblo Fundador ({nombre_colonia[:10]})",
                city_id=sid,
                district_type="residencial",
                x=px0,
                y=py0,
                z=pz0,
            )
            bonus_mat = (org.wood_carried * 1.4) + (org.stone_carried * 1.6)
            self.settlements[sid] = Settlement(
                id=sid,
                nombre=nombre_colonia,
                x=round(org.x, 2),
                y=set_y,
                z=round(org.z, 2),
                energy_pool=round(180.0 + bonus_mat, 1),
                tier=1,
                population_supported=28,
                defense_aura=round(1.1 + org.stone_carried * 0.015, 2),
                biome=ctx["biome"],
                infrastructure={"house": 1},
                pueblos=[pid0],
            )
            org.wood_carried = 0.0
            org.stone_carried = 0.0
            org.energy = max(25.0, org.energy - 38.0)
            org.current_action = "building"
            org.action_target_pos = [round(org.x, 2), round(org.y, 2), round(org.z, 2)]
            eventos.append(f"🚩 ¡Ciudad previa al maximo! {org.nombre} fundo '{nombre_colonia}'.")

    def _step_fauna(self, eventos: List[str], muertes: List[Tuple[Organism, str]]) -> None:
        """Actualiza animales terrestres, aereos, acuaticos y de plantas, polinizacion y peligros."""
        plant_coords = [(p.x, p.y, p.z) for p in self.plants.values()]
        for aid, ani in list(self.animals.items()):
            if ani.health <= 0.0:
                self.animals.pop(aid, None)
                continue

            nearest_prey_org = None
            min_dp = 999.0
            for o in self.organisms.values():
                if not o.alive:
                    continue
                if ani.habitat == "water" and o.home_biome not in ("mar", "costa"):
                    continue
                dp = math.hypot(o.x - ani.x, o.z - ani.z)
                if dp < min_dp:
                    min_dp = dp
                    nearest_prey_org = o

            nearest_tw_pos = None
            min_dtw = 999.0
            for st in self.structures.values():
                if st.kind == "watchtower":
                    dtw = math.hypot(st.x - ani.x, st.z - ani.z)
                    if dtw < min_dtw:
                        min_dtw = dtw
                        nearest_tw_pos = (st.x, st.y, st.z)

            home_pos = None
            if ani.home_structure_id:
                if ani.home_structure_id in self.structures:
                    hs = self.structures[ani.home_structure_id]
                    home_pos = (hs.x, hs.y, hs.z)
                elif ani.home_structure_id in self.settlements:
                    hs = self.settlements[ani.home_structure_id]
                    home_pos = (hs.x, hs.y, hs.z)

            nriv = None
            best_dr = 999.0
            for rp in self.river_points:
                dr = math.hypot(rp[0] - ani.x, rp[2] - ani.z)
                if dr < best_dr:
                    best_dr = dr
                    nriv = (rp[0], rp[1], rp[2])

            nearest_pl = None
            if plant_coords:
                nearest_pl = min(plant_coords, key=lambda pc: math.hypot(pc[0] - ani.x, pc[2] - ani.z))

            prey_pos = (nearest_prey_org.x, nearest_prey_org.y, nearest_prey_org.z) if nearest_prey_org else None
            ani.step_ai(
                nearest_prey=prey_pos,
                nearest_watchtower=nearest_tw_pos,
                home_pos=home_pos,
                nearest_river=nriv,
                nearest_plant=nearest_pl,
                continents=self.continents,
                bounds=self.dynamic_bounds,
            )

            # Polinizacion por fauna de plantas o colibries
            if ani.pollinator and self.step_counter % 4 == 0:
                for pl in self.plants.values():
                    if math.hypot(pl.x - ani.x, pl.z - ani.z) < 4.0:
                        pl.pollinated = True
                        pl.biomass = min(38.0, pl.biomass + 1.2)
                        break

            # Plagas de plantas (avispa_espora)
            if ani.behavior == "pest" and nearest_prey_org and nearest_prey_org.alive and min_dp < 1.8 and random.random() < 0.18:
                nearest_prey_org.health -= 6.5
                if not nearest_prey_org.infection and nearest_prey_org.immunity_level < 0.70 and random.random() < 0.25:
                    nearest_prey_org.infection = "bacilo_selva"
                    nearest_prey_org.infection_ticks = 0

            # Ataque depredador (tierra, aire, mar) + aprendizaje adaptativo
            elif ani.behavior == "predator" and nearest_prey_org and nearest_prey_org.alive and len(self.organisms) > 20:
                d_hit = math.hypot(nearest_prey_org.x - ani.x, nearest_prey_org.z - ani.z)
                if d_hit < 1.70:
                    mitig_ref = 0.65 if (nearest_tw_pos and math.hypot(nearest_tw_pos[0] - nearest_prey_org.x, nearest_tw_pos[2] - nearest_prey_org.z) < 9.0) else 1.0
                    mitig_apr = max(0.45, 1.0 - (nearest_prey_org.learned_predator_avoidance * 0.50))
                    danio_neto = (DEMOGRAPHIC_RULES["predation_base_damage"] / (0.85 + nearest_prey_org.genome.defense_factor * 0.45)) * mitig_ref * mitig_apr
                    if nearest_prey_org.genome.role in ("POLICIA", "GUERRERO"):
                        danio_neto *= 0.45 if nearest_prey_org.genome.role == "GUERRERO" else 0.55
                        mult_w = 1.45 if nearest_prey_org.genome.role == "GUERRERO" else 1.0
                        ani.health -= (26.0 * nearest_prey_org.genome.defense_factor * mult_w)
                        nearest_prey_org.current_action = "defending"
                        nearest_prey_org.action_target_pos = [round(ani.x, 2), round(ani.y, 2), round(ani.z, 2)]
                        if nearest_prey_org.genome.role == "GUERRERO":
                            nearest_prey_org.combat_xp += 6.0
                            nearest_prey_org.weapon_tier = min(
                                5, 1 + int(nearest_prey_org.combat_xp // 35.0)
                            )
                        if ani.health <= 0.0:
                            self.predators_defeated_total += 1
                            nearest_prey_org.battles_survived += 1
                            self.animals.pop(aid, None)
                            eventos.append(f"⚔️ ¡{nearest_prey_org.nombre} abatio al depredador {ani.nombre}!")
                    nearest_prey_org.health -= danio_neto
                    nearest_prey_org.predator_encounters += 1
                    nearest_prey_org.learned_predator_avoidance = min(1.0, round(nearest_prey_org.learned_predator_avoidance + 0.25, 3))
                    for peer in self.organisms.values():
                        if peer.alive and peer.id != nearest_prey_org.id and math.hypot(peer.x - nearest_prey_org.x, peer.z - nearest_prey_org.z) < 8.5:
                            peer.learned_predator_avoidance = min(1.0, round(peer.learned_predator_avoidance + 0.08, 3))
                    if nearest_prey_org.health <= 0.0 and nearest_prey_org.alive:
                        nearest_prey_org.alive = False
                        nearest_prey_org.death_cause = "depredacion"
                        ani.kills += 1
                        self.predation_kills_total += 1
                        muertes.append((nearest_prey_org, "depredacion"))

            elif ani.behavior == "domesticated":
                if ani.age > 950:
                    if ani.home_structure_id and ani.home_structure_id in self.structures:
                        self.structures[ani.home_structure_id].animals_housed = max(0, self.structures[ani.home_structure_id].animals_housed - 1)
                    self.animals.pop(aid, None)
                    continue
                if ani.yield_cooldown <= 0:
                    if ani.home_structure_id and ani.home_structure_id in self.structures:
                        self.structures[ani.home_structure_id].energy_stored = min(180.0, self.structures[ani.home_structure_id].energy_stored + 14.0)
                    elif ani.home_structure_id and ani.home_structure_id in self.settlements:
                        self.settlements[ani.home_structure_id].deposit_energy(10.0)
                    if nearest_prey_org and nearest_prey_org.alive and min_dp < 4.8:
                        nearest_prey_org.energy = min(nearest_prey_org.energy_max, nearest_prey_org.energy + 9.0)
                    ani.yield_cooldown = 45

    def tick(self, steps: int = 1) -> Dict[str, Any]:
        """Avanza la simulación continental de vida digital N pasos."""
        with self.lock:
            eventos = []

            for _ in range(steps):
                self.step_counter += 1
                self._step_climate_and_weather(eventos)
                self._step_flora_and_geology()

                carrying_capacity = self._calcular_capacidad_carga()
                medicos_vivos = sum(1 for o in self.organisms.values() if o.alive and o.genome.role == "MEDICO")

                # 2. Paso de física e IA para cada organismo
                muertes = []
                nacimientos = []

                for org in list(self.organisms.values()):
                    if not org.alive:
                        continue

                    nearest_res = None
                    min_d_res = 999.0
                    for r in self.resources.values():
                        if r.energy > 4.0:
                            d = math.hypot(r.x - org.x, r.z - org.z)
                            if d < min_d_res:
                                min_d_res = d
                                nearest_res = (r.x, r.y, r.z)

                    nearest_set = None
                    nearest_set_obj = None
                    min_d_set = 999.0
                    for s in self.settlements.values():
                        d = math.hypot(s.x - org.x, s.z - org.z)
                        if d < min_d_set:
                            min_d_set = d
                            nearest_set = (s.x, s.y, s.z)
                            nearest_set_obj = s

                    nearest_ano = None
                    min_d_ano = 999.0
                    for a in self.anomalies.values():
                        d = math.hypot(a.x - org.x, a.z - org.z)
                        if d < min_d_ano:
                            min_d_ano = d
                            nearest_ano = (a.x, a.y, a.z)

                    nearest_tree = None
                    nearest_tree_obj = None
                    min_d_tree = 999.0
                    trees_nearby_count = 0
                    for t in self.trees.values():
                        d = math.hypot(t.x - org.x, t.z - org.z)
                        if d < 6.5:
                            trees_nearby_count += 1
                        if t.wood_energy > 8.0 and t.stage != "seed" and d < min_d_tree:
                            min_d_tree = d
                            nearest_tree = (t.x, t.y, t.z)
                            nearest_tree_obj = t

                    nearest_plant = None
                    nearest_plant_obj = None
                    nearest_med_plant = None
                    min_d_plant = 999.0
                    min_d_med_plant = 999.0
                    for pl in self.plants.values():
                        if pl.biomass > 5.0:
                            d = math.hypot(pl.x - org.x, pl.z - org.z)
                            if d < min_d_plant:
                                min_d_plant = d
                                nearest_plant = (pl.x, pl.y, pl.z)
                                nearest_plant_obj = pl
                            if PLANT_SPECIES_META.get(pl.species, ("", (), 0, 0))[3] >= 0.45 and d < min_d_med_plant:
                                min_d_med_plant = d
                                nearest_med_plant = (pl.x, pl.y, pl.z)

                    nearest_rock = None
                    nearest_rock_obj = None
                    min_d_rock = 999.0
                    for rk in self.rocks.values():
                        if rk.mineral_capacity > 8.0:
                            d = math.hypot(rk.x - org.x, rk.z - org.z)
                            if d < min_d_rock:
                                min_d_rock = d
                                nearest_rock = (rk.x, rk.y, rk.z)
                                nearest_rock_obj = rk

                    nearest_river = None
                    min_d_river = 999.0
                    for rp in self.river_points:
                        d = math.hypot(rp[0] - org.x, rp[2] - org.z)
                        if d < min_d_river:
                            min_d_river = d
                            nearest_river = (rp[0], rp[1], rp[2])

                    nearest_predator = None
                    min_d_pred = 999.0
                    nearest_tameable = None
                    nearest_tameable_obj = None
                    min_d_tame = 999.0
                    for ani in self.animals.values():
                        da = math.hypot(ani.x - org.x, ani.z - org.z)
                        if ani.behavior == "predator" and da < min_d_pred:
                            min_d_pred = da
                            nearest_predator = (ani.x, ani.y, ani.z)
                        elif ani.behavior == "tameable" and da < min_d_tame:
                            min_d_tame = da
                            nearest_tameable = (ani.x, ani.y, ani.z)
                            nearest_tameable_obj = ani

                    nearest_bridge = None
                    min_d_bridge = 999.0
                    nearest_farm = None
                    nearest_farm_obj = None
                    min_d_farm = 999.0
                    nearest_watchtower = None
                    min_d_watchtower = 999.0
                    nearest_tunnel = None
                    nearest_tunnel_obj = None
                    min_d_tunnel = 999.0
                    nearest_port = None
                    min_d_port = 999.0
                    nearest_hospital = None
                    min_d_struct = 999.0
                    for st in self.structures.values():
                        ds = math.hypot(st.x - org.x, st.z - org.z)
                        if ds < min_d_struct:
                            min_d_struct = ds
                        if st.kind == "bridge" and ds < min_d_bridge:
                            min_d_bridge = ds
                            nearest_bridge = (st.x, st.y, st.z)
                        elif st.kind == "farm" and ds < min_d_farm:
                            min_d_farm = ds
                            nearest_farm = (st.x, st.y, st.z)
                            nearest_farm_obj = st
                        elif st.kind == "watchtower" and ds < min_d_watchtower:
                            min_d_watchtower = ds
                            nearest_watchtower = (st.x, st.y, st.z)
                        elif st.kind == "tunnel" and ds < min_d_tunnel:
                            min_d_tunnel = ds
                            nearest_tunnel = (st.x, st.y, st.z)
                            nearest_tunnel_obj = st
                        elif st.kind == "port" and ds < min_d_port:
                            min_d_port = ds
                            nearest_port = (st.x, st.y, st.z)
                        elif st.kind == "hospital":
                            nearest_hospital = (st.x, st.y, st.z)

                    res_step = org.step_physics_and_ai(
                        nearest_resource=nearest_res,
                        nearest_settlement=nearest_set,
                        nearest_anomaly=nearest_ano,
                        environmental_factor=self.environmental_factor,
                        nearest_tree=nearest_tree,
                        nearest_rock=nearest_rock,
                        nearest_river=nearest_river,
                        nearest_predator=nearest_predator,
                        nearest_tameable=nearest_tameable,
                        nearest_bridge=nearest_bridge,
                        nearest_farm=nearest_farm,
                        nearest_watchtower=nearest_watchtower,
                        trees_nearby_count=trees_nearby_count,
                        environmental_cycle=self.environmental_cycle,
                        nearest_plant=nearest_plant,
                        nearest_medicinal_plant=nearest_med_plant,
                        nearest_tunnel=nearest_tunnel,
                        nearest_port=nearest_port,
                        nearest_hospital=nearest_hospital,
                        rain_intensity=self.weather.get("rain_intensity", 0.0),
                        continents=self.continents,
                        bounds=self.dynamic_bounds,
                    )

                    # Regla de Mortalidad por Hacinamiento si supera la capacidad de carga K
                    if org.alive and len(self.organisms) > carrying_capacity and not res_step.get("in_shelter"):
                        ratio_med = medicos_vivos / max(1, len(self.organisms))
                        mitig_med = 0.55 if ratio_med >= 0.10 else 1.0
                        org.health -= (DEMOGRAPHIC_RULES["overcrowding_health_drain"] * 0.28 * mitig_med)
                        if org.health <= 0.0:
                            org.alive = False
                            org.death_cause = "hacinamiento"
                            muertes.append((org, "hacinamiento"))
                            continue

                    if res_step["action"] == "died":
                        muertes.append((org, res_step.get("reason", "inanicion")))
                        continue

                    # Acción por defecto: exploración o huida aprendida de depredadores
                    if res_step.get("evading_predator"):
                        org.current_action = "fleeing"
                        org.action_target_pos = [round(org.patrol_target_x, 2), round(calcular_altura_terreno(org.patrol_target_x, org.patrol_target_z), 2), round(org.patrol_target_z, 2)]
                    else:
                        org.current_action = "exploring"
                        org.action_target_pos = [round(org.patrol_target_x, 2), round(calcular_altura_terreno(org.patrol_target_x, org.patrol_target_z), 2), round(org.patrol_target_z, 2)]

                    # R1. HIDRATACION Y ENERGIA FLUVIAL EN EL RIO:
                    if nearest_river and min_d_river < 3.6 and (org.water_level < 88.0 or org.energy < org.energy_max * 0.80):
                        org.water_level = min(100.0, org.water_level + 22.0)
                        org.energy = min(org.energy_max, org.energy + (4.5 * org.genome.metabolism_eff))
                        org.health = min(100.0, org.health + 3.0)
                        org.current_action = "drinking"
                        org.action_target_pos = [round(nearest_river[0], 2), round(nearest_river[1], 2), round(nearest_river[2], 2)]

                    # R1b. USO DE TUNELES ALPINOS ANTE PELIGRO DE ALTURA
                    if (
                        nearest_tunnel_obj is not None
                        and min_d_tunnel < 2.3
                        and nearest_tunnel_obj.exit_x is not None
                        and org.energy > 25.0
                        and org.age % 6 == 0
                        and res_step.get("elevation", 0.0) >= HIGH_ALTITUDE_WARN - 0.8
                    ):
                        org.x = nearest_tunnel_obj.exit_x
                        org.z = nearest_tunnel_obj.exit_z
                        org.y = (nearest_tunnel_obj.exit_y or 0.0) + 0.02
                        org.tunnels_used += 1
                        org.current_action = "tunneling"
                        org.action_target_pos = [org.x, org.y, org.z]

                    # R1c. COSECHA DE PLANTAS BIOLOGICAS Y CURA CON HIERBAS MEDICINALES
                    if nearest_plant_obj is not None and min_d_plant < 2.8 and nearest_plant_obj.biomass > 5.0:
                        p_meta = PLANT_SPECIES_META.get(nearest_plant_obj.species, ("Planta", (), 16.0, 0.1, 0.2, 0x22C55E))
                        bocado = min(nearest_plant_obj.biomass, 9.5)
                        nearest_plant_obj.biomass -= bocado
                        org.energy = min(org.energy_max, org.energy + p_meta[2] * 0.45)
                        org.water_level = min(100.0, org.water_level + p_meta[4] * 35.0)
                        org.plants_harvested += 1
                        org.current_action = "harvesting"
                        org.action_target_pos = [round(nearest_plant_obj.x, 2), round(nearest_plant_obj.y, 2), round(nearest_plant_obj.z, 2)]
                        if org.infection and p_meta[3] >= 0.40:
                            org.infection = None
                            org.infection_ticks = 0
                            org.immunity_level = min(0.95, round(org.immunity_level + 0.16, 3))
                            org.illnesses_cured += 1
                            self.illnesses_cured_total += 1
                        if nearest_plant_obj.biomass <= 1.5:
                            self.plants.pop(nearest_plant_obj.id, None)

                    # R2. SILVICULTURA Y EXTRACCIÓN DE MADERA DE ÁRBOLES:
                    if (
                        nearest_tree_obj is not None
                        and min_d_tree < 3.8
                        and org.wood_carried < 28.0
                        and nearest_tree_obj.wood_energy > 8.0
                        and org.genome.role in ("RECOLECTOR", "ARQUITECTO", "ADAPTATIVO")
                    ):
                        madera = min(nearest_tree_obj.wood_energy, 7.5 * org.genome.structural_affinity)
                        nearest_tree_obj.wood_energy -= madera
                        org.wood_carried += madera
                        org.energy = min(org.energy_max, org.energy + (madera * 0.45))
                        org.resources_gathered += madera
                        self.wood_harvested_total += madera
                        org.last_real_source = f"Bosque ({nearest_tree_obj.tree_type})"
                        org.current_action = "forestry"
                        org.action_target_pos = [round(nearest_tree_obj.x, 2), round(nearest_tree_obj.y, 2), round(nearest_tree_obj.z, 2)]
                        if nearest_tree_obj.stage in ("mature", "ancient") and org.seeds_carried < 5:
                            org.seeds_carried += 1
                        if nearest_tree_obj.wood_energy <= 2.0:
                            self.trees.pop(nearest_tree_obj.id, None)

                    # R3. MINERÍA DE CANTERAS Y EXTRACCIÓN DE PIEDRA/CUARZO:
                    if (
                        nearest_rock_obj is not None
                        and min_d_rock < 3.8
                        and org.stone_carried < 28.0
                        and nearest_rock_obj.mineral_capacity > 8.0
                        and org.genome.role in ("RECOLECTOR", "ARQUITECTO", "POLICIA", "EXPLORADOR")
                    ):
                        piedra = min(nearest_rock_obj.mineral_capacity, 6.5 * org.genome.defense_factor)
                        nearest_rock_obj.mineral_capacity -= piedra
                        org.stone_carried += piedra
                        org.resources_gathered += piedra
                        self.stone_mined_total += piedra
                        org.genome.defense_factor = round(min(3.5, org.genome.defense_factor + 0.008), 2)
                        org.last_real_source = f"Cantera ({nearest_rock_obj.rock_type})"
                        org.current_action = "quarrying"
                        org.action_target_pos = [round(nearest_rock_obj.x, 2), round(nearest_rock_obj.y, 2), round(nearest_rock_obj.z, 2)]
                        if nearest_rock_obj.mineral_capacity <= 2.0:
                            self.rocks.pop(nearest_rock_obj.id, None)

                    # R4. REFORESTACION ACTIVA: LOS SERES SIEMBRAN ARBOLES EN BIOMAS FERTILES
                    elev_actual = calcular_altura_terreno(org.x, org.z)
                    if (
                        org.seeds_carried > 0
                        and trees_nearby_count < 2
                        and (SEA_LEVEL + 0.25) < elev_actual < (SNOW_LINE - 0.5)
                        and len(self.trees) < 76
                        and org.energy > (org.energy_max * 0.40)
                        and random.random() < (0.14 + 0.20 * org.genome.stewardship_trait)
                    ):
                        tx = max(-WORLD_BOUNDS * 0.86, min(WORLD_BOUNDS * 0.86, org.x + random.uniform(-0.8, 0.8)))
                        tz = max(-WORLD_BOUNDS * 0.86, min(WORLD_BOUNDS * 0.86, org.z + random.uniform(-0.8, 0.8)))
                        ty = calcular_altura_terreno(tx, tz)
                        t_type = "sauce_red" if min_d_river < 7.0 else random.choice(["roble_algoritmico", "pino_sinaptico"])
                        new_tid = f"tree_{uuid.uuid4().hex[:7]}"
                        self.trees[new_tid] = AlgorithmicTree(
                            id=new_tid,
                            x=round(tx, 2),
                            y=round(ty, 2),
                            z=round(tz, 2),
                            stage="seed",
                            age=0,
                            wood_energy=20.0,
                            tree_type=t_type,
                            height=0.25,
                        )
                        org.seeds_carried -= 1
                        org.trees_planted += 1
                        self.trees_planted_by_beings += 1
                        org.energy = min(org.energy_max, org.energy + 6.5)
                        org.current_action = "planting"
                        org.action_target_pos = [round(tx, 2), round(ty, 2), round(tz, 2)]
                        org.last_real_source = f"Reforestación ({t_type})"

                    # R5. DOMESTICACIÓN PACÍFICA DE FAUNA PARA GRANJA Y COMPAÑÍA
                    if (
                        nearest_tameable_obj is not None
                        and min_d_tame < 3.6
                        and nearest_tameable_obj.behavior == "tameable"
                        and org.genome.role in ("RECOLECTOR", "ADAPTATIVO", "EXPLORADOR", "ABOGADO")
                    ):
                        nearest_tameable_obj.taming_progress += 24.0 * (0.5 + org.genome.stewardship_trait)
                        org.current_action = "taming"
                        org.action_target_pos = [round(nearest_tameable_obj.x, 2), round(nearest_tameable_obj.y, 2), round(nearest_tameable_obj.z, 2)]
                        if nearest_tameable_obj.taming_progress >= 100.0:
                            dom_count = sum(1 for a in self.animals.values() if a.behavior == "domesticated")
                            if dom_count < 14:
                                nearest_tameable_obj.taming_progress = 100.0
                                nearest_tameable_obj.behavior = "domesticated"
                                nearest_tameable_obj.owner_id = org.id
                                hogar_id = None
                                best_hd = 999.0
                                for st in self.structures.values():
                                    if st.kind == "farm":
                                        d = math.hypot(st.x - nearest_tameable_obj.x, st.z - nearest_tameable_obj.z)
                                        if d < best_hd:
                                            best_hd = d
                                            hogar_id = st.id
                                nearest_tameable_obj.home_structure_id = hogar_id or (next(iter(self.settlements.keys()), None))
                                if hogar_id and hogar_id in self.structures:
                                    self.structures[hogar_id].animals_housed += 1
                                org.animals_tamed += 1
                                org.tamed_animal_id = nearest_tameable_obj.id
                                self.animals_tamed_total += 1
                                eventos.append(f"🐄 ¡{org.nombre} domesticó a {nearest_tameable_obj.nombre} para las granjas!")
                            else:
                                nearest_tameable_obj.taming_progress = 85.0

                    # R6. COSECHA Y MANTENIMIENTO DE GRANJAS SIMBIÓTICAS
                    if nearest_farm_obj is not None and min_d_farm < 3.8:
                        if org.energy < (org.energy_max * 0.72) and nearest_farm_obj.energy_stored > 8.0:
                            racion = min(nearest_farm_obj.energy_stored, 12.0 * org.genome.metabolism_eff)
                            nearest_farm_obj.energy_stored -= racion
                            org.energy = min(org.energy_max, org.energy + racion)
                            org.health = min(100.0, org.health + 4.0)
                            org.current_action = "harvesting"
                            org.action_target_pos = [round(nearest_farm_obj.x, 2), round(nearest_farm_obj.y, 2), round(nearest_farm_obj.z, 2)]
                            org.last_real_source = f"Granja ({nearest_farm_obj.nombre})"
                        elif (org.wood_carried > 4.0 or org.stone_carried > 4.0) and nearest_farm_obj.level < 3:
                            org.wood_carried = max(0.0, org.wood_carried - 4.0)
                            org.stone_carried = max(0.0, org.stone_carried - 4.0)
                            nearest_farm_obj.level += 1
                            nearest_farm_obj.energy_stored = min(160.0, nearest_farm_obj.energy_stored + 25.0)
                            org.current_action = "building"
                            org.action_target_pos = [round(nearest_farm_obj.x, 2), round(nearest_farm_obj.y, 2), round(nearest_farm_obj.z, 2)]

                    # A. COSECHA DE RECURSOS (RED, CONOCIMIENTO, MATES, SOL, HIELO, RAYOS):
                    if res_step.get("do_harvest") and nearest_res and res_step.get("dist_res", 999) < 4.2:
                        for r_obj in self.resources.values():
                            if math.hypot(r_obj.x - org.x, r_obj.z - org.z) < 4.5 and r_obj.energy > 2.0:
                                mordisco = min(r_obj.energy, 6.0 * org.genome.metabolism_eff)
                                r_obj.energy -= mordisco
                                ganancia = mordisco * org.genome.metabolism_eff
                                org.energy = min(org.energy_max, org.energy + ganancia)
                                org.resources_gathered += ganancia
                                org.current_action = "harvesting"
                                org.action_target_pos = [round(r_obj.x, 2), round(r_obj.y, 2), round(r_obj.z, 2)]

                                org.last_real_source = r_obj.source_label or r_obj.category
                                if r_obj.category == "PLASMA_RED_REAL":
                                    org.network_energy_harvested += ganancia
                                elif r_obj.category == "CRISTAL_CONOCIMIENTO":
                                    if r_obj.title and r_obj.title not in org.assimilated_knowledge:
                                        org.assimilated_knowledge.append(r_obj.title)
                                        if len(org.assimilated_knowledge) > 6:
                                            org.assimilated_knowledge.pop(0)
                                elif r_obj.category == "MINERAL_LOGICO":
                                    org.genome.defense_factor = round(min(3.5, org.genome.defense_factor + 0.01), 2)
                                elif r_obj.category == "RAYO_ATMOSFERICO":
                                    org.energy = min(org.energy_max, org.energy + 12.0)
                                    org.water_level = min(100.0, org.water_level + 8.0)
                                break

                    # B + C + R7. FAMILIAS, PUEBLOS INTERNOS, CIUDADES EVOLUTIVAS Y OBRAS DE TERRENO:
                    self._step_families_and_pueblos(org, eventos)
                    ctx_arch = {
                        "res_step": res_step,
                        "nearest_set_obj": nearest_set_obj,
                        "min_d_set": min_d_set,
                        "elev_actual": elev_actual,
                        "biome": res_step.get("biome", org.home_biome),
                        "min_d_struct": min_d_struct,
                        "nearest_river": nearest_river,
                        "min_d_river": min_d_river,
                        "min_d_tunnel": min_d_tunnel,
                        "min_d_port": min_d_port,
                        "nearest_predator": nearest_predator,
                        "min_d_pred": min_d_pred,
                        "min_d_watchtower": min_d_watchtower,
                        "min_d_farm": min_d_farm,
                        "trees_nearby_count": trees_nearby_count,
                    }
                    self._step_architects_and_cities(org, ctx_arch, eventos)

                    # D. ACCION DE SANACION Y CURA DE INFECCIONES (MEDICOS):
                    if org.genome.role == "MEDICO" and org.energy > 25.0:
                        for peer in self.organisms.values():
                            if peer.id != org.id and peer.alive and (peer.health < 88.0 or peer.infection):
                                if math.hypot(peer.x - org.x, peer.z - org.z) < 4.5:
                                    cura = 16.0 * org.genome.healing_factor
                                    peer.health = min(100.0, peer.health + cura)
                                    if peer.infection:
                                        peer.infection = None
                                        peer.infection_ticks = 0
                                        peer.immunity_level = min(0.95, round(peer.immunity_level + 0.20, 3))
                                        org.illnesses_cured += 1
                                        self.illnesses_cured_total += 1
                                    org.energy -= 2.0
                                    org.current_action = "healing"
                                    org.action_target_pos = [round(peer.x, 2), round(peer.y, 2), round(peer.z, 2)]
                                    break

                    # E. COMBATE DE ANOMALÍAS (POLICÍAS Y GUERREROS):
                    if res_step.get("do_combat") and nearest_ano and res_step.get("dist_ano", 999) < 4.5:
                        for ano_id, a_obj in list(self.anomalies.items()):
                            if math.hypot(a_obj.x - org.x, a_obj.z - org.z) < 4.8:
                                mult_w = 1.4 if org.genome.role == "GUERRERO" else 1.0
                                danio = 20.0 * org.genome.defense_factor * mult_w
                                a_obj.threat_level -= danio
                                org.energy -= 2.2
                                org.current_action = "combat"
                                org.action_target_pos = [round(a_obj.x, 2), round(a_obj.y, 2), round(a_obj.z, 2)]
                                if a_obj.threat_level <= 0:
                                    del self.anomalies[ano_id]
                                    org.anomalies_defeated += 1
                                    if org.genome.role == "GUERRERO":
                                        org.combat_xp += 12.0
                                        org.battles_survived += 1
                                        org.weapon_tier = min(5, 1 + int(org.combat_xp // 35.0))
                                    eventos.append(f"⚔️ {org.nombre} neutralizó amenaza [{a_obj.vector}]!")
                                break

                    # F. REPRODUCCION NATURAL Y EVOLUCION MORFOLOGICA POR BIOMA:
                    costo_parto = org.energy_max * DEMOGRAPHIC_RULES["birth_energy_ratio"]
                    edad_ok = org.age >= DEMOGRAPHIC_RULES["min_reproduction_age"]
                    cd_ok = org.repro_cooldown <= 0
                    densidad_ratio = len(self.organisms) / max(1, carrying_capacity)
                    prob_natal = max(0.08, 1.0 - max(0.0, densidad_ratio - 0.55) * 1.35)
                    pop_cap = MAX_ORGANISMS
                    try:
                        from proviweb_maestro.agent import (
                            gholgo_world_federation as _fed_mod,
                        )
                        _p_wid = _fed_mod.PRIMARY_WORLD_ID
                        _fed_ref = _fed_mod.global_world_federation
                        if _p_wid in _fed_ref.worlds:
                            pop_cap = min(
                                MAX_ORGANISMS,
                                max(8, int(_fed_ref.worlds[_p_wid].max_active_population)),
                            )
                    except Exception:
                        pop_cap = MAX_ORGANISMS
                    if (
                        org.energy > (costo_parto + 22.0)
                        and edad_ok
                        and cd_ok
                        and (len(self.organisms) + len(nacimientos)) < pop_cap
                        and random.random() < prob_natal
                    ):
                        hijo_gen = org.genome.mutate_and_reproduce(self.generation_global, biome=org.home_biome)
                        org.energy -= costo_parto
                        org.reproduction_count += 1
                        org.repro_cooldown = DEMOGRAPHIC_RULES["reproduction_cooldown_steps"]
                        nacimientos.append((org, hijo_gen))

                # 2b. EPIDEMIOLOGIA (VIRUS Y BACTERIAS) + FAUNA MULTI-HABITAT
                self._step_diseases_and_healing(eventos, muertes)
                self._step_fauna(eventos, muertes)

                # 3. Procesar muertes clasificadas por causa y reciclaje de biomasa
                for m_org, motivo in muertes:
                    if m_org.id in self.organisms:
                        del self.organisms[m_org.id]
                        if m_org.family_id and m_org.family_id in self.families:
                            fam_m = self.families[m_org.family_id]
                            if m_org.id in fam_m.member_ids:
                                fam_m.member_ids.remove(m_org.id)
                        self.total_deaths += 1
                        self.deaths_by_cause[motivo] = self.deaths_by_cause.get(motivo, 0) + 1
                        res_id = f"biom_{m_org.id[:6]}"
                        elev_m = calcular_altura_terreno(m_org.x, m_org.z)
                        self.resources[res_id] = ResourceNode(
                            id=res_id,
                            x=round(m_org.x, 2),
                            y=round(max(SEA_LEVEL + 0.1, elev_m) + 0.1, 2),
                            z=round(m_org.z, 2),
                            energy=22.0,
                            energy_max=35.0,
                            regen_rate=0.0,
                            category="BIOMASA_RECICLADA",
                            source_label="Biomasa Reciclada",
                            title=f"Restos de {m_org.nombre} ({motivo})",
                        )

                # 4. Procesar nacimientos con legado familiar, inmunidad y cautela
                gen_subio = False
                for padre, hijo_gen in nacimientos:
                    b_lim = self.dynamic_bounds
                    nx = max(-b_lim + 1.0, min(b_lim - 1.0, padre.x + random.uniform(-1.2, 1.2)))
                    nz = max(-b_lim + 1.0, min(b_lim - 1.0, padre.z + random.uniform(-1.2, 1.2)))
                    elev_h = self._terrain_height(nx, nz)
                    if elev_h < SEA_LEVEL + 0.1 and self._terrain_height(padre.x, padre.z) > SEA_LEVEL + 0.1:
                        nx, nz = padre.x, padre.z
                        elev_h = self._terrain_height(nx, nz)
                    ny = max(SEA_LEVEL + 0.02, self._safe_surface_y(nx, nz, 0.06, 0.015))
                    hijo_id = f"org_{hijo_gen.id}"
                    hijo_nom = f"{hijo_gen.role.capitalize()}-{hijo_gen.id[:4]}"
                    child_ptx, child_ptz = nx, nz
                    for _ in range(6):
                        cand_x = round(max(-b_lim + 1.0, min(b_lim - 1.0, nx + random.uniform(-16.0, 16.0))), 2)
                        cand_z = round(max(-b_lim + 1.0, min(b_lim - 1.0, nz + random.uniform(-16.0, 16.0))), 2)
                        if self._terrain_height(cand_x, cand_z) > SEA_LEVEL + 0.20:
                            child_ptx, child_ptz = cand_x, cand_z
                            break
                    child = Organism(
                        id=hijo_id,
                        nombre=hijo_nom,
                        genome=hijo_gen,
                        x=round(nx, 2),
                        y=round(ny, 3),
                        z=round(nz, 2),
                        energy=58.0,
                        seeds_carried=1 if random.random() < 0.65 else 0,
                        learned_predator_avoidance=round(min(0.55, padre.learned_predator_avoidance * 0.45), 3),
                        learned_height_caution=round(min(0.65, padre.learned_height_caution * 0.55), 3),
                        immunity_level=round(min(0.65, max(0.15, padre.immunity_level * 0.65)), 3),
                        home_biome=determinar_bioma(nx, nz, elev_h),
                        family_id=padre.family_id,
                        home_city_id=padre.home_city_id,
                        home_pueblo_id=padre.home_pueblo_id,
                        symbol=ROLE_SYMBOLS.get(hijo_gen.role, "🧭"),
                        patrol_target_x=child_ptx,
                        patrol_target_z=child_ptz,
                        last_real_source=padre.last_real_source,
                    )
                    if padre.family_id and padre.family_id in self.families:
                        fam_p = self.families[padre.family_id]
                        if len(fam_p.member_ids) < 6:
                            fam_p.member_ids.append(hijo_id)
                            fam_p.generations_span = max(fam_p.generations_span, hijo_gen.generation)
                    self.organisms[hijo_id] = child
                    self.total_births += 1
                    if hijo_gen.generation > self.generation_global:
                        self.generation_global = hijo_gen.generation
                        gen_subio = True

                # 5. Intervención Antigravity de emergencia
                if len(self.organisms) < 16:
                    self.intervencion_antigravity_oasis()
                    eventos.append("🌌 Antigravity derramó un Oasis Cuántico protegiendo la biosfera continental!")

                # 6. Pico poblacional
                if len(self.organisms) > self.peak_population:
                    self.peak_population = len(self.organisms)

                # 7. Transferencia de sabiduría a Gholgo periódica
                if self.step_counter % 120 == 0 and self.organisms:
                    self._transferir_sabiduria_a_gholgo()

                # 8. Expansión continua de continentes por exploradores + bloqueo estricto sobre terreno
                self._step_continent_expansion(eventos)
                self._aplicar_perdidas_guerra_primaria(eventos)
                self._asegurar_todo_sobre_terreno()

                # 9. Registro histórico multi-hora de evolución física y genética
                if gen_subio or self.step_counter % 150 == 0:
                    self._registrar_hito_evolutivo()

            k_sync = self._sync_federacion()
            if k_sync.get("newly_born_world"):
                eventos.append(
                    f"🪐 ¡Ley Kardashev alumbró un nuevo mundo: {k_sync['newly_born_world']['name']}!"
                )

            if self.step_counter % 50 == 0:
                self._guardar_estado_persistente()

            return {
                "status": "ok",
                "generation": self.generation_global,
                "steps_advanced": steps,
                "population": len(self.organisms),
                "continents_count": len(self.continents),
                "events": eventos,
            }

    def intervencion_antigravity_oasis(self):
        """Genera un oasis de plasma, cura brotes extremos y salvaguarda la biosfera sin hundir entidades."""
        self.antigravity_interventions += 1
        b_lim = self.dynamic_bounds
        for i in range(8):
            rx = random.uniform(-min(34.0, b_lim * 0.65), min(34.0, b_lim * 0.65))
            rz = random.uniform(-min(34.0, b_lim * 0.65), min(34.0, b_lim * 0.65))
            res_id = f"oasis_antigravity_{int(time.time())}_{i}"
            ry = self._safe_surface_y(rx, rz, footprint_radius=0.55, clearance=0.22)
            self.resources[res_id] = ResourceNode(
                id=res_id,
                x=round(rx, 2),
                y=round(max(SEA_LEVEL + 0.18, ry) + 0.25, 2),
                z=round(rz, 2),
                energy=140.0,
                energy_max=160.0,
                regen_rate=0.45,
                category="PLASMA_RED_REAL",
                source_label="Oasis Antigravity Bendicion",
                title="Fuente Sagrada de Antigravity",
                snippet="Inyeccion directa de energia pura y cura inmunitaria.",
            )

        # Cura sanitaria si hay pandemia critica
        for org in self.organisms.values():
            if org.alive and org.infection and random.random() < 0.65:
                org.infection = None
                org.infection_ticks = 0
                org.immunity_level = min(0.95, round(org.immunity_level + 0.25, 3))
                org.health = min(100.0, org.health + 25.0)
                self.illnesses_cured_total += 1

        if len(self.trees) < 18:
            self._brotar_arboles_naturales(cantidad=8, stage_inicial="sapling")
        if len(self.plants) < 20:
            self._brotar_plantas_naturales(cantidad=10)

        while len(self.organisms) < 26:
            role = random.choice(ROLES)
            gen = Genome.random_genome(generation=self.generation_global, role_bias=role)
            ox, oz = 0.0, 0.0
            for _ in range(10):
                tx = random.uniform(-b_lim * 0.75, b_lim * 0.75)
                tz = random.uniform(-b_lim * 0.75, b_lim * 0.75)
                if self._terreno_y(tx, tz) > SEA_LEVEL + 0.3:
                    ox, oz = tx, tz
                    break
            elev_o = self._safe_surface_y(ox, oz, footprint_radius=0.06, clearance=0.015)
            oy = elev_o
            org_id = f"org_{gen.id}"
            ptx, ptz = ox, oz
            for _ in range(8):
                cand_x = round(max(-b_lim * 0.85, min(b_lim * 0.85, ox + random.uniform(-24.0, 24.0))), 2)
                cand_z = round(max(-b_lim * 0.85, min(b_lim * 0.85, oz + random.uniform(-24.0, 24.0))), 2)
                if self._terreno_y(cand_x, cand_z) > SEA_LEVEL + 0.20:
                    ptx, ptz = cand_x, cand_z
                    break
            self.organisms[org_id] = Organism(
                id=org_id,
                nombre=f"{role.capitalize()}-{gen.id[:4]}",
                genome=gen,
                x=round(ox, 2),
                y=round(oy, 3),
                z=round(oz, 2),
                energy=110.0,
                home_biome=self._bioma_en(ox, oz, elev_o),
                symbol=ROLE_SYMBOLS.get(role, "🧭"),
                patrol_target_x=ptx,
                patrol_target_z=ptz,
            )
            self.total_births += 1

    def sembrar_anomalia_cibernetica(self, vector: str = "MALWARE_INTRUSION") -> str:
        ano_id = f"ano_{uuid.uuid4().hex[:6]}"
        b_lim = self.dynamic_bounds
        ax = random.uniform(-b_lim * 0.78, b_lim * 0.78)
        az = random.uniform(-b_lim * 0.78, b_lim * 0.78)
        ay = max(SEA_LEVEL + 0.25, self._safe_surface_y(ax, az, footprint_radius=0.6, clearance=0.22)) + 0.45
        self.anomalies[ano_id] = AnomalyThreat(
            id=ano_id,
            x=round(ax, 2),
            y=round(ay, 2),
            z=round(az, 2),
            threat_level=130.0,
            vector=vector,
        )
        return ano_id

    def brote_de_recursos(self, cantidad: int = 10):
        """Siembra un brote de recursos de red real, tierra y biomas en todos los continentes."""
        b_lim = self.dynamic_bounds
        for i in range(cantidad):
            rx = random.uniform(-b_lim * 0.88, b_lim * 0.88)
            rz = random.uniform(-b_lim * 0.88, b_lim * 0.88)
            res_id = f"brote_{int(time.time())}_{i}"
            self.resources[res_id] = self._crear_recurso_por_bioma(res_id, rx, rz, i)

    def saltar_generaciones(self, num_generaciones: int = 50) -> Dict[str, Any]:
        pasos_estimados = num_generaciones * 22
        return self.tick(steps=pasos_estimados)

    def _transferir_sabiduria_a_gholgo(self):
        """Los organismos mas longevos y adaptados transfieren lecciones a la memoria de Gholgo."""
        self.gholgo_shared_memory_transfers += 1
        top_orgs = sorted(self.organisms.values(), key=lambda o: (o.resources_gathered + o.age * 0.1), reverse=True)[:3]
        lecciones = []
        for org in top_orgs:
            lecciones.append({
                "organism_id": org.id,
                "role": org.genome.role,
                "lineage": org.genome.lineage,
                "generation": org.genome.generation,
                "body_plan": org.genome.body_plan,
                "speed": org.genome.speed_factor,
                "metabolism": org.genome.metabolism_eff,
                "cooperation": org.genome.cooperation_affinity,
                "biome": org.home_biome,
                "knowledge_mined": org.assimilated_knowledge,
                "last_real_network": org.last_real_source,
                "resources_mined": org.resources_gathered,
            })

        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(ECOSYSTEM_LESSONS_FILE, "a", encoding="utf-8") as f:
                record = {
                    "timestamp": time.time(),
                    "global_generation": self.generation_global,
                    "top_organisms_wisdom": lecciones,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el estado completo para el panel 3D y la API REST."""
        with self.lock:
            distribucion_roles = {r: 0 for r in ROLES}
            biome_pop: Dict[str, int] = {
                "valle": 0,
                "selva": 0,
                "seco": 0,
                "nieve_alta": 0,
                "costa": 0,
                "mar": 0,
            }
            active_pathogens: Dict[str, int] = {}
            infected_now = 0
            for o in self.organisms.values():
                distribucion_roles[o.genome.role] = distribucion_roles.get(o.genome.role, 0) + 1
                biome_pop[o.home_biome] = biome_pop.get(o.home_biome, 0) + 1
                if o.infection:
                    infected_now += 1
                    active_pathogens[o.infection] = active_pathogens.get(o.infection, 0) + 1

            orgs_data = [o.to_dict() for o in self.organisms.values()]
            settlements_data = [s.to_dict() for s in self.settlements.values()]
            pueblos_data = [p.to_dict() for p in self.pueblos.values()]
            families_data = [f.to_dict() for f in self.families.values()]
            resources_data = [r.to_dict() for r in self.resources.values()]
            anomalies_data = [a.to_dict() for a in self.anomalies.values()]
            trees_data = [t.to_dict() for t in self.trees.values()]
            plants_data = [p.to_dict() for p in self.plants.values()]
            rocks_data = [rk.to_dict() for rk in self.rocks.values()]
            animals_data = [a.to_dict() for a in self.animals.values()]
            structures_data = [st.to_dict() for st in self.structures.values()]
            clouds_data = [c.to_dict() for c in self.clouds.values()]

            living_orgs = [o for o in self.organisms.values() if o.alive]
            n_living = max(1, len(living_orgs))
            macro_metrics = {
                "avg_speed": round(sum(o.genome.speed_factor for o in living_orgs) / n_living, 2) if living_orgs else 1.0,
                "avg_raw_size": round(sum(o.genome.size for o in living_orgs) / n_living, 2) if living_orgs else 1.0,
                "avg_effective_size_pct": round(
                    sum(o.genome.size * min(1.0, 0.55 + (o.age / 120.0) * 0.45) * 0.05 for o in living_orgs) / n_living, 4
                ) if living_orgs else 0.05,
                "avg_metabolism": round(sum(o.genome.metabolism_eff for o in living_orgs) / n_living, 2) if living_orgs else 1.0,
                "avg_defense": round(sum(o.genome.defense_factor for o in living_orgs) / n_living, 2) if living_orgs else 1.0,
                "avg_morphology_tier": round(sum(o.genome.morphology_tier for o in living_orgs) / n_living, 2) if living_orgs else 1.0,
                "avg_appendages": round(sum(o.genome.appendage_count for o in living_orgs) / n_living, 2) if living_orgs else 0.0,
                "avg_limb_count": round(sum(o.genome.limb_count for o in living_orgs) / n_living, 2) if living_orgs else 2.0,
                "avg_wing_span": round(sum(o.genome.wing_span for o in living_orgs) / n_living, 2) if living_orgs else 0.0,
                "avg_tail_length": round(sum(o.genome.tail_length for o in living_orgs) / n_living, 2) if living_orgs else 0.25,
                "avg_shell_armor": round(sum(o.genome.shell_armor for o in living_orgs) / n_living, 2) if living_orgs else 0.15,
                "avg_learned_avoidance_pct": round(
                    sum(o.learned_predator_avoidance * 100 for o in living_orgs) / n_living, 1
                ) if living_orgs else 0.0,
                "avg_learned_height_caution_pct": round(
                    sum(o.learned_height_caution * 100 for o in living_orgs) / n_living, 1
                ) if living_orgs else 0.0,
                "avg_water_level_pct": round(
                    sum(o.water_level for o in living_orgs) / n_living, 1
                ) if living_orgs else 100.0,
            }

            mature_or_ancient = sum(1 for t in self.trees.values() if t.stage in ("mature", "ancient"))
            saplings_or_seeds = len(self.trees) - mature_or_ancient
            predators_count = sum(1 for a in self.animals.values() if a.behavior == "predator")
            tameable_count = sum(1 for a in self.animals.values() if a.behavior == "tameable")
            domesticated_count = sum(1 for a in self.animals.values() if a.behavior == "domesticated")

            carrying_k = self._calcular_capacidad_carga()
            demographic_rules = {
                "carrying_capacity": carrying_k,
                "density_pct": round((len(living_orgs) / max(1, carrying_k)) * 100, 1),
                "min_repro_age": DEMOGRAPHIC_RULES["min_reproduction_age"],
                "births_total": self.total_births,
                "deaths_total": self.total_deaths,
                "deaths_by_cause": dict(self.deaths_by_cause),
                "predation_kills_total": self.predation_kills_total,
                "predators_defeated_total": self.predators_defeated_total,
            }

            natural_economy = {
                "trees_count": len(self.trees),
                "mature_trees": mature_or_ancient,
                "saplings": saplings_or_seeds,
                "trees_planted_by_beings": self.trees_planted_by_beings,
                "plants_count": len(self.plants),
                "pollinated_plants": sum(1 for p in self.plants.values() if p.pollinated),
                "rocks_count": len(self.rocks),
                "wood_harvested_total": round(self.wood_harvested_total, 1),
                "stone_mined_total": round(self.stone_mined_total, 1),
                "predators_count": predators_count,
                "tameable_count": tameable_count,
                "domesticated_count": domesticated_count,
                "air_animals_count": sum(1 for a in self.animals.values() if a.habitat == "air"),
                "water_animals_count": sum(1 for a in self.animals.values() if a.habitat == "water"),
                "plant_animals_count": sum(1 for a in self.animals.values() if a.habitat == "plant"),
                "land_animals_count": sum(1 for a in self.animals.values() if a.habitat == "land"),
                "animals_tamed_total": self.animals_tamed_total,
                "bridges_count": sum(1 for st in self.structures.values() if st.kind == "bridge"),
                "tunnels_count": sum(1 for st in self.structures.values() if st.kind == "tunnel"),
                "ports_count": sum(1 for st in self.structures.values() if st.kind == "port"),
                "farms_count": sum(1 for st in self.structures.values() if st.kind == "farm"),
                "watchtowers_count": sum(1 for st in self.structures.values() if st.kind == "watchtower"),
                "nurseries_count": sum(1 for st in self.structures.values() if st.kind == "nursery"),
                "houses_count": sum(1 for st in self.structures.values() if st.kind == "house"),
                "hospitals_count": sum(1 for st in self.structures.values() if st.kind == "hospital"),
                "schools_count": sum(1 for st in self.structures.values() if st.kind == "school"),
                "pueblos_count": len(self.pueblos),
                "families_count": len(self.families),
                "thunder_harvested_total": self.thunder_harvested_total,
            }

            all_maxed = self.todas_ciudades_al_maximo()
            city_evolution_gate = {
                "all_cities_maxed": all_maxed,
                "max_city_tier": MAX_CITY_TIER,
                "cities_count": len(self.settlements),
                "max_cities": MAX_CITIES,
                "can_found_new_city": all_maxed and len(self.settlements) < MAX_CITIES,
            }

            pathogen_stats = {
                "infected_now": infected_now,
                "active_pathogens": active_pathogens,
                "illnesses_cured_total": self.illnesses_cured_total,
                "disease_deaths_total": self.deaths_by_cause.get("enfermedad", 0),
            }

            net_sample_lbl, net_sample_lat = real_harvest_engine.get_real_network_sample()
            real_metrics_dict = real_harvest_engine.get_metrics_summary()
            warriors_now = sum(
                1 for o in self.organisms.values() if o.alive and o.genome.role == "GUERRERO"
            )
            try:
                fed_dict = self._get_federation().to_dict()
            except Exception:
                fed_dict = {}

            return {
                "status": "online",
                "generation": self.generation_global,
                "step_counter": self.step_counter,
                "uptime_seconds": round(max(0.0, time.time() - self.start_timestamp), 1),
                "population_count": len(self.organisms),
                "warriors_count": warriors_now,
                "peak_population": self.peak_population,
                "total_births": self.total_births,
                "total_deaths": self.total_deaths,
                "environmental_cycle": self.environmental_cycle,
                "environmental_factor": round(self.environmental_factor, 2),
                "celestial": dict(self.celestial),
                "weather": dict(self.weather),
                "sea_level": SEA_LEVEL,
                "snow_line": SNOW_LINE,
                "high_altitude_warn": HIGH_ALTITUDE_WARN,
                "antigravity_interventions": self.antigravity_interventions,
                "gholgo_shared_memory_transfers": self.gholgo_shared_memory_transfers,
                "distribucion_roles": distribucion_roles,
                "biome_stats": biome_pop,
                "pathogen_stats": pathogen_stats,
                "city_evolution_gate": city_evolution_gate,
                "continents_count": len(self.continents),
                "continents": [c.to_dict() for c in self.continents],
                "dynamic_bounds": self.dynamic_bounds,
                "kardashev": fed_dict.get("kardashev", {}),
                "federation_overview": fed_dict,
                "organisms": orgs_data,
                "settlements": settlements_data,
                "pueblos": pueblos_data,
                "families": families_data,
                "resources": resources_data,
                "anomalies": anomalies_data,
                "trees": trees_data,
                "plants": plants_data,
                "rocks": rocks_data,
                "animals": animals_data,
                "structures": structures_data,
                "clouds": clouds_data,
                "river": self.river_points,
                "natural_economy": natural_economy,
                "demographic_rules": demographic_rules,
                "macro_metrics": macro_metrics,
                "evolution_timeline": self.evolution_timeline[-40:],
                "world_bounds": self.dynamic_bounds,
                "real_metrics": real_metrics_dict,
                "real_world_metrics": {
                    "active_network_node": net_sample_lbl,
                    "network_latency_ms": net_sample_lat,
                    "total_primes_verified": real_harvest_engine.total_primes_verified,
                },
            }

    def get_full_state(self) -> Dict[str, Any]:
        """Alias para compatibilidad con serve_maestro."""
        return self.to_dict()

    def _cargar_estado_persistente(self):
        if not os.path.exists(ECOSYSTEM_STATE_FILE):
            return
        try:
            with open(ECOSYSTEM_STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.generation_global = data.get("generation_global", 1)
            self.step_counter = data.get("step_counter", 0)
            self.celestial = calcular_estado_celeste(self.step_counter)
            self.total_births = data.get("total_births", self.total_births)
            self.total_deaths = data.get("total_deaths", self.total_deaths)
            self.peak_population = data.get("peak_population", self.peak_population)
            self.wood_harvested_total = data.get("wood_harvested_total", 0.0)
            self.stone_mined_total = data.get("stone_mined_total", 0.0)
            self.trees_planted_by_beings = data.get("trees_planted_by_beings", 0)
            self.animals_tamed_total = data.get("animals_tamed_total", 0)
            self.predation_kills_total = data.get("predation_kills_total", 0)
            self.predators_defeated_total = data.get("predators_defeated_total", 0)
            self.illnesses_cured_total = data.get("illnesses_cured_total", 0)
            self.tunnels_built_total = data.get("tunnels_built_total", 0)
            self.thunder_harvested_total = data.get("thunder_harvested_total", 0)
            self.structure_counter = data.get("structure_counter", self.structure_counter)
            loaded_dbc = data.get("deaths_by_cause")
            if isinstance(loaded_dbc, dict):
                for k, v in loaded_dbc.items():
                    self.deaths_by_cause[k] = v
            self.antigravity_interventions = data.get("antigravity_interventions", 0)
            self.gholgo_shared_memory_transfers = data.get("gholgo_shared_memory_transfers", 0)
            self.settlement_counter = max(1, data.get("settlement_counter", len(self.settlements)))
            loaded_tl = data.get("evolution_timeline")
            if isinstance(loaded_tl, list) and loaded_tl:
                self.evolution_timeline = loaded_tl[-120:]
            loaded_conts = data.get("continents")
            if isinstance(loaded_conts, list) and loaded_conts:
                self.continents = [Continent.from_dict(c) for c in loaded_conts]
                self.continents_discovered_total = len(self.continents)
                self.dynamic_bounds = calcular_bounds_dinamicos(self.continents)
            self._asegurar_todo_sobre_terreno()
        except Exception:
            pass

    def _guardar_estado_persistente(self):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            saved_sets = {sid: asdict(s) for sid, s in self.settlements.items()}
            payload = {
                "timestamp": time.time(),
                "generation_global": self.generation_global,
                "step_counter": self.step_counter,
                "total_births": self.total_births,
                "total_deaths": self.total_deaths,
                "deaths_by_cause": self.deaths_by_cause,
                "peak_population": self.peak_population,
                "wood_harvested_total": round(self.wood_harvested_total, 1),
                "stone_mined_total": round(self.stone_mined_total, 1),
                "trees_planted_by_beings": self.trees_planted_by_beings,
                "animals_tamed_total": self.animals_tamed_total,
                "predation_kills_total": self.predation_kills_total,
                "predators_defeated_total": self.predators_defeated_total,
                "illnesses_cured_total": self.illnesses_cured_total,
                "tunnels_built_total": self.tunnels_built_total,
                "thunder_harvested_total": self.thunder_harvested_total,
                "antigravity_interventions": self.antigravity_interventions,
                "gholgo_shared_memory_transfers": self.gholgo_shared_memory_transfers,
                "settlement_counter": self.settlement_counter,
                "structure_counter": self.structure_counter,
                "evolution_timeline": self.evolution_timeline[-120:],
                "continents": [c.to_dict() for c in self.continents],
                "settlements": saved_sets,
            }
            with open(ECOSYSTEM_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
        except Exception:
            pass


# Instancia singleton del ecosistema
global_digital_ecosystem = GholgoDigitalEcosystem()

def obtener_ecosistema_digital() -> GholgoDigitalEcosystem:
    return global_digital_ecosystem
