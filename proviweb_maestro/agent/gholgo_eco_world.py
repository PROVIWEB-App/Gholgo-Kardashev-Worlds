# -*- coding: utf-8 -*-
"""
GHOLGO ECO WORLD - Atlas Continental, Astronomia, Clima, Biomas, Patogenos y Civilizacion
==========================================================================================
Modulo auxiliar limpio y cohesivo para `gholgo_digital_ecosystem.py`.
Centraliza:
  - Topografia expandida (`WORLD_BOUNDS = 72.0`), nivel del mar (`SEA_LEVEL = -4.3`),
    cota nival (`SNOW_LINE = 4.2`) y clasificacion de 6 biomas reales (`mar`, `costa`,
    `nieve_alta`, `selva`, `seco`, `valle`).
  - Mecanica astronómica Sol/Luna (`DIA_SOLAR`, `NOCHE_SINAPTICA`, `AMANECER`, `OCASO`) y
    sistema atmosferico de nubes, lluvia, viento y rayos.
  - Catalogos biologicos (plantas por bioma, fauna terrestre/aerea/acuatica/fitofila,
    virus y bacterias) y reglas de evolucion urbana (`MAX_CITY_TIER = 5`) con pueblos internos.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

WORLD_BOUNDS = 72.0
SEA_LEVEL = -4.3
HIGH_ALTITUDE_WARN = 2.6
SNOW_LINE = 4.2
DAY_CYCLE_STEPS = 2400  # Ciclo solar/lunar 4x mas lento para evolucion consistente por horas
MAX_ORGANISMS = 140
MIN_ORGANISMS_SEED = 40
NUM_INITIAL_RESOURCES = 56
MAX_CITY_TIER = 5
MAX_CITIES = 6

ROLES = [
    "EXPLORADOR",
    "RECOLECTOR",
    "ARQUITECTO",
    "ADAPTATIVO",
    "ABOGADO",
    "MEDICO",
    "POLICIA",
    "GUERRERO",
]

ROLE_COLORS = {
    "EXPLORADOR": 0x38BDF8,
    "RECOLECTOR": 0xFBBF24,
    "ARQUITECTO": 0x10B981,
    "ADAPTATIVO": 0xA855F7,
    "ABOGADO": 0x6366F1,
    "MEDICO": 0x2DD4BF,
    "POLICIA": 0xF43F5E,
    "GUERRERO": 0xF97316,
}

ROLE_SYMBOLS = {
    "EXPLORADOR": "🧭",
    "RECOLECTOR": "🌾",
    "ARQUITECTO": "🏛️",
    "ADAPTATIVO": "🔮",
    "ABOGADO": "⚖️",
    "MEDICO": "🧪",
    "POLICIA": "🛡️",
    "GUERRERO": "⚔️",
}

DEMOGRAPHIC_RULES: Dict[str, Any] = {
    "min_reproduction_age": 38,
    "reproduction_cooldown_steps": 45,
    "birth_energy_ratio": 0.45,
    "base_carrying_capacity": 65,
    "max_population_hard_cap": MAX_ORGANISMS,
    "senescence_age_ratio": 0.85,
    "night_exposure_drain": 0.032,
    "predation_base_damage": 32.0,
    "overcrowding_health_drain": 1.4,
    "high_altitude_hazard_damage": 3.2,
    "drowning_base_damage": 8.5,
    "disease_base_drain": 0.65,
}

# Cauce continuo desde las cumbres nevadas del Noreste hasta la Bahia del Mar Occidental
RIVER_WAYPOINTS = [
    [34.0, -20.6],
    [26.0, -15.6],
    [18.0, -10.7],
    [10.0, -5.7],
    [2.0, -0.7],
    [-6.0, 4.2],
    [-15.0, 9.8],
    [-25.0, 16.0],
    [-35.0, 20.5],
    [-44.0, 21.8],
]


def calcular_altura_terreno(x: float, z: float) -> float:
    """
    Elevacion determinista del continente [-8.0, +9.5], identica en Python y Three.js.
    Incluye mar perimetral y bahia occidental, valles, selva, meseta seca y picos nevados.
    """
    r = math.hypot(x, z)
    valle = math.sin(x * 0.065) * math.cos(z * 0.065) * 1.9
    colinas = math.sin(x * 0.13 + 0.9) * math.cos(z * 0.13 - 0.6) * 1.6
    pico_ne = 8.8 * math.exp(-((x - 28.0) ** 2 + (z + 28.0) ** 2) / 260.0)
    pico_no = 8.4 * math.exp(-((x + 24.0) ** 2 + (z + 28.0) ** 2) / 240.0)
    cresta_alpina = 4.6 * math.exp(-((z + 24.0) ** 2) / 150.0) * (0.5 + 0.5 * math.cos(x * 0.11))
    meseta_se = 2.8 * math.exp(-((x - 28.0) ** 2 + (z - 22.0) ** 2) / 320.0)
    bahia_oeste = -4.2 * math.exp(-((x + 42.0) ** 2 + (z - 18.0) ** 2) / 240.0)
    borde_mar = -max(0.0, (r - 50.0) * 0.34)
    cauce = (
        -1.35 * math.exp(-(((z + 0.62 * x) - 0.5) ** 2) / 26.0)
        if (-46.0 <= x <= 38.0)
        else 0.0
    )
    y = (
        valle
        + colinas
        + pico_ne
        + pico_no
        + cresta_alpina
        + meseta_se
        + bahia_oeste
        + borde_mar
        + cauce
        - 2.3
    )
    return float(max(-8.0, min(9.5, y)))


def determinar_bioma(x: float, z: float, y: Optional[float] = None) -> str:
    """Clasifica el bioma geografico exacto en una coordenada del mundo."""
    elev = calcular_altura_terreno(x, z) if y is None else y
    if elev < SEA_LEVEL - 0.12:
        return "mar"
    if elev < SEA_LEVEL + 0.55:
        return "costa"
    if elev >= SNOW_LINE:
        return "nieve_alta"
    if x > 14.0 and z > 10.0:
        return "seco"
    if x < 14.0 and z > 14.0:
        return "selva"
    return "valle"


def calcular_pendiente_local(x: float, z: float, delta: float = 1.4) -> float:
    """Devuelve la magnitud aproximada de pendiente alrededor de (x, z)."""
    hx = calcular_altura_terreno(x + delta, z) - calcular_altura_terreno(x - delta, z)
    hz = calcular_altura_terreno(x, z + delta) - calcular_altura_terreno(x, z - delta)
    return round(math.hypot(hx, hz) / (2.0 * delta), 3)


def obtener_puntos_rio_completos() -> List[List[float]]:
    """Calcula las cotas 3D exactas a lo largo del cauce fluvial hacia el mar."""
    puntos = []
    for pt in RIVER_WAYPOINTS:
        x, z = pt[0], pt[1]
        y = max(SEA_LEVEL + 0.05, calcular_altura_terreno(x, z) + 0.08)
        puntos.append([round(x, 2), round(y, 2), round(z, 2)])
    return puntos


def calcular_orientacion_puente_rio(x: float, z: float) -> float:
    """Devuelve el angulo Y en Three.js para que un puente cruce perpendicular al rio."""
    best_idx = 0
    best_d = 999.0
    for idx, pt in enumerate(RIVER_WAYPOINTS):
        d = math.hypot(pt[0] - x, pt[1] - z)
        if d < best_d:
            best_d = d
            best_idx = idx
    i0 = max(0, best_idx - 1)
    i1 = min(len(RIVER_WAYPOINTS) - 1, best_idx + 1)
    tx = RIVER_WAYPOINTS[i1][0] - RIVER_WAYPOINTS[i0][0]
    tz = RIVER_WAYPOINTS[i1][1] - RIVER_WAYPOINTS[i0][1]
    mag = math.hypot(tx, tz) or 1.0
    nx = -tz / mag
    nz = tx / mag
    return round(math.atan2(-nz, nx), 3)


def calcular_estado_celeste(step_counter: int) -> Dict[str, Any]:
    """Calcula posicion orbital 3D del Sol y la Luna y fase dia/noche."""
    prog = (step_counter % DAY_CYCLE_STEPS) / float(DAY_CYCLE_STEPS)
    ang = prog * 2.0 * math.pi
    sun_x = round(math.cos(ang) * 86.0, 2)
    sun_y = round(math.sin(ang) * 78.0, 2)
    sun_z = 18.0
    moon_x = round(-sun_x * 0.94, 2)
    moon_y = round(-sun_y * 0.94, 2)
    moon_z = -18.0
    sun_elev = round(math.sin(ang), 3)
    if sun_elev >= 0.16:
        phase = "DIA_SOLAR"
    elif sun_elev > -0.14:
        phase = "AMANECER" if math.cos(ang) > 0 else "OCASO"
    else:
        phase = "NOCHE_SINAPTICA"
    day_num = (step_counter // DAY_CYCLE_STEPS) + 1
    hour_24 = round((prog * 24.0 + 6.0) % 24.0, 1)
    return {
        "day_number": day_num,
        "hour_24": hour_24,
        "day_progress": round(prog, 3),
        "phase": phase,
        "sun_elevation": sun_elev,
        "sun_pos": [sun_x, sun_y, sun_z],
        "moon_pos": [moon_x, moon_y, moon_z],
        "moon_phase": round(0.5 + 0.5 * math.sin(step_counter * 0.003), 2),
    }


@dataclass
class AtmosphericCloud:
    """Nube atmosferica movil que transporta humedad, lluvia y carga electrica."""

    id: str
    x: float
    y: float
    z: float
    vx: float
    vz: float
    radius: float = 5.5
    moisture: float = 0.65
    charge: float = 0.35

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "radius": round(self.radius, 2),
            "moisture": round(self.moisture, 2),
            "charge": round(self.charge, 2),
        }


# Flora no arborea: plantas curativas, cultivos, deserticas, glaciares y ribereñas
# (nombre, biomas_preferidos, energia_yield, poder_medicinal, hidratacion_yield, color_hex)
PLANT_SPECIES_META: Dict[str, tuple] = {
    "hierba_medicinal": ("Hierba Medicinal", ("selva", "valle"), 14.0, 0.85, 0.15, 0x2DD4BF),
    "trigo_fotonico": ("Trigo Fotonico", ("valle",), 24.0, 0.05, 0.10, 0xFACC15),
    "junco_fluvial": ("Junco Fluvial", ("costa", "valle"), 16.0, 0.20, 0.45, 0x38BDF8),
    "cactus_solar": ("Cactus Solar", ("seco",), 20.0, 0.25, 0.80, 0x84CC16),
    "liquen_glacial": ("Liquen Glacial", ("nieve_alta",), 18.0, 0.55, 0.25, 0xA5F3FC),
    "liana_orquidea": ("Orquidea de Selva", ("selva",), 19.0, 0.45, 0.35, 0xEC4899),
}


@dataclass
class Plant:
    """Planta silvestre o cultivada que crece con lluvia, polinizacion y nutre/sana."""

    id: str
    species: str
    nombre: str
    biome: str
    x: float
    y: float
    z: float
    growth: float = 0.45  # 0.0 .. 1.0
    biomass: float = 22.0
    pollinated: bool = False
    age: int = 0

    @property
    def stage(self) -> str:
        if self.growth < 0.35:
            return "brote"
        if self.growth < 0.78:
            return "creciendo"
        return "florecida"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "species": self.species,
            "nombre": self.nombre,
            "biome": self.biome,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "stage": self.stage,
            "growth": round(self.growth, 2),
            "biomass": round(self.biomass, 1),
            "pollinated": self.pollinated,
        }


# Fauna multi-habitat: tierra, aire, agua (mar/rios) y plantas
# (nombre, behavior, scale, habitat, biomas_preferidos, polinizador)
ANIMAL_SPECIES_META: Dict[str, tuple] = {
    # Tierra - depredadores y domesticables
    "lobo_cuantico": ("Lobo Cuantico", "predator", 0.085, "land", ("valle", "selva"), False),
    "manticora_neural": ("Manticora Neural", "predator", 0.105, "land", ("seco", "valle"), False),
    "serpiente_latencia": ("Vibora Latencia", "predator", 0.070, "land", ("selva", "seco"), False),
    "oso_glacial": ("Oso Glacial", "predator", 0.115, "land", ("nieve_alta",), False),
    "ciervo_sinaptico": ("Ciervo Sinaptico", "tameable", 0.072, "land", ("valle", "selva"), False),
    "buey_plasma": ("Buey de Plasma", "tameable", 0.095, "land", ("valle", "seco"), False),
    "oveja_fotonica": ("Oveja Fotonica", "tameable", 0.062, "land", ("valle", "nieve_alta"), False),
    # Aire
    "aguila_sinaptica": (
        "Aguila Sinaptica",
        "predator",
        0.088,
        "air",
        ("nieve_alta", "valle"),
        False,
    ),
    "colibri_fotonico": (
        "Colibri Fotonico",
        "tameable",
        0.048,
        "air",
        ("selva", "valle"),
        True,
    ),
    "cuervo_tormenta": (
        "Cuervo Tormenta",
        "wildlife",
        0.068,
        "air",
        ("seco", "nieve_alta"),
        False,
    ),
    # Agua (mar y rios)
    "tiburon_cripto": ("Tiburon Cripto", "predator", 0.110, "water", ("mar",), False),
    "pez_cuantico": ("Pez Cuantico", "tameable", 0.056, "water", ("mar", "costa", "valle"), False),
    "mantarraya_azul": ("Mantarraya Azul", "wildlife", 0.085, "water", ("mar",), False),
    # Animales de las plantas (fitofilos / polinizadores)
    "mariposa_espectral": (
        "Mariposa Espectral",
        "tameable",
        0.042,
        "plant",
        ("selva", "valle"),
        True,
    ),
    "escarabajo_simbiotico": (
        "Escarabajo Simbiotico",
        "wildlife",
        0.045,
        "plant",
        ("selva", "seco"),
        True,
    ),
    "avispa_espora": ("Avispa Espora", "pest", 0.044, "plant", ("selva", "costa"), False),
}

# Patogenos reales digitales: bacterias y virus
PATHOGEN_CATALOG: Dict[str, Dict[str, Any]] = {
    "bacilo_selva": {
        "kind": "bacteria",
        "nombre": "Bacilo de Selva",
        "contagion": 0.08,
        "severity": 0.42,
        "preferred_biomes": ("selva", "costa"),
    },
    "vibrio_marino": {
        "kind": "bacteria",
        "nombre": "Vibrio Abisal",
        "contagion": 0.09,
        "severity": 0.48,
        "preferred_biomes": ("mar", "costa"),
    },
    "espora_arida": {
        "kind": "bacteria",
        "nombre": "Espora Desierto",
        "contagion": 0.05,
        "severity": 0.38,
        "preferred_biomes": ("seco",),
    },
    "virus_sinaptico": {
        "kind": "virus",
        "nombre": "Virus Sinaptico",
        "contagion": 0.24,
        "severity": 0.56,
        "preferred_biomes": ("valle", "selva", "nieve_alta"),
    },
    "gripe_neuronal": {
        "kind": "virus",
        "nombre": "Gripe Neuronal",
        "contagion": 0.28,
        "severity": 0.45,
        "preferred_biomes": ("valle", "costa", "nieve_alta"),
    },
}

# Regla estricta de evolucion urbana: una ciudad debe alcanzar Tier 5 con su
# infraestructura civil completa antes de poder fundar una nueva ciudad.
CITY_TIER_SPECS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Campamento Urbano",
        "next_energy": 420.0,
        "pop_cap": 28,
        "required_infra": ["house"],
    },
    2: {
        "name": "Aldea en Expansion",
        "next_energy": 1150.0,
        "pop_cap": 52,
        "required_infra": ["house", "market", "aqueduct"],
    },
    3: {
        "name": "Ciudad Civil",
        "next_energy": 2400.0,
        "pop_cap": 85,
        "required_infra": ["house", "market", "aqueduct", "school", "hospital"],
    },
    4: {
        "name": "Metropolis Avanzada",
        "next_energy": 4400.0,
        "pop_cap": 130,
        "required_infra": [
            "house",
            "market",
            "aqueduct",
            "school",
            "hospital",
            "power_plant",
            "sanitation",
            "court",
        ],
    },
    5: {
        "name": "Megapolis Maxima",
        "next_energy": 999999.0,
        "pop_cap": 200,
        "required_infra": [
            "house",
            "market",
            "aqueduct",
            "school",
            "hospital",
            "power_plant",
            "sanitation",
            "court",
        ],
    },
}

CIVIL_INFRA_PRIORITY = [
    "house",
    "aqueduct",
    "market",
    "school",
    "hospital",
    "sanitation",
    "power_plant",
    "court",
]

CIVIL_INFRA_LABELS: Dict[str, str] = {
    "house": "Vivienda Familiar",
    "market": "Mercado Central",
    "school": "Escuela Gholgo",
    "hospital": "Hospital Medico",
    "power_plant": "Central Eolica/Solar",
    "aqueduct": "Acueducto y Agua",
    "sanitation": "Saneamiento Urbano",
    "court": "Juzgado Civico",
}

PUEBLO_DISTRICT_NAMES = [
    "Pueblo Residencial",
    "Pueblo Agrario",
    "Barrio Universitario",
    "Distrito Sanitario",
]


@dataclass
class Pueblo:
    """Sub-pueblo interno que crece dentro del perimetro de una ciudad."""

    id: str
    nombre: str
    city_id: str
    district_type: str
    x: float
    y: float
    z: float
    families_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "city_id": self.city_id,
            "district_type": self.district_type,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "z": round(self.z, 2),
            "families_count": self.families_count,
        }


@dataclass
class Family:
    """Nucleo familiar formado por los seres dentro de los pueblos de una ciudad."""

    id: str
    clan_name: str
    city_id: str
    pueblo_id: str
    house_id: Optional[str] = None
    member_ids: List[str] = field(default_factory=list)
    generations_span: int = 1
    shared_energy: float = 40.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "clan_name": self.clan_name,
            "city_id": self.city_id,
            "pueblo_id": self.pueblo_id,
            "house_id": self.house_id,
            "members_count": len(self.member_ids),
            "generations_span": self.generations_span,
            "shared_energy": round(self.shared_energy, 1),
        }


CONTINENT_BIOME_PROFILES = (
    "templado",
    "bosque",
    "selva",
    "montana_nevada",
    "desierto_seco",
    "cristalino",
    "volcanico",
)

CONTINENT_NAME_PREFIXES = (
    "Archipiélago",
    "Continente",
    "Tierra",
    "Meseta",
    "Bastión",
    "Aurora",
    "Senda",
    "Cordillera",
)

CONTINENT_NAME_ROOTS = (
    "Alba",
    "Kardashev",
    "Boreal",
    "Solarix",
    "Cromático",
    "Esmeralda",
    "Obsidiana",
    "Estelar",
    "Céfiro",
    "Aethel",
    "Lumina",
    "Orión",
)


@dataclass
class Continent:
    """Masa continental procedural explorable en un mundo."""

    id: str
    nombre: str
    center_x: float
    center_z: float
    radius: float
    seed: float
    biome_profile: str = "templado"
    height_peak: float = 5.4
    resource_richness: float = 1.0
    discovered_by: str = "Gholgo"
    discovered_by_role: str = "EXPLORADOR"
    discovered_at_step: int = 0
    ring_index: int = 0
    world_id: str = "mundo_gholgo_primario"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "center_x": round(float(self.center_x), 2),
            "center_z": round(float(self.center_z), 2),
            "radius": round(float(self.radius), 2),
            "seed": round(float(self.seed), 4),
            "biome_profile": self.biome_profile,
            "height_peak": round(float(self.height_peak), 2),
            "resource_richness": round(float(self.resource_richness), 2),
            "discovered_by": self.discovered_by,
            "discovered_by_role": self.discovered_by_role,
            "discovered_at_step": int(self.discovered_at_step),
            "ring_index": int(self.ring_index),
            "world_id": self.world_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Continent":
        return cls(
            id=str(data.get("id", "cont_0")),
            nombre=str(data.get("nombre", "Continente Desconocido")),
            center_x=float(data.get("center_x", 0.0)),
            center_z=float(data.get("center_z", 0.0)),
            radius=float(data.get("radius", 22.0)),
            seed=float(data.get("seed", 1.0)),
            biome_profile=str(data.get("biome_profile", "templado")),
            height_peak=float(data.get("height_peak", 5.2)),
            resource_richness=float(data.get("resource_richness", 1.0)),
            discovered_by=str(data.get("discovered_by", "Explorador")),
            discovered_by_role=str(data.get("discovered_by_role", "EXPLORADOR")),
            discovered_at_step=int(data.get("discovered_at_step", 0)),
            ring_index=int(data.get("ring_index", 1)),
            world_id=str(data.get("world_id", "mundo_gholgo_primario")),
        )


def default_continents_for_world(world_id: str = "mundo_gholgo_primario") -> List[Continent]:
    """Devuelve el continente central mas islas fronterizas iniciales."""
    return [
        Continent(
            id="cont_primario",
            nombre="Pangea Génesis Gholgo",
            center_x=0.0,
            center_z=0.0,
            radius=54.0,
            seed=0.0,
            biome_profile="templado",
            height_peak=8.8,
            resource_richness=1.15,
            discovered_by="Gholgo & Antigravity",
            discovered_by_role="EXPLORADOR",
            discovered_at_step=0,
            ring_index=0,
            world_id=world_id,
        ),
        Continent(
            id="cont_alba_1",
            nombre="Archipiélago del Alba",
            center_x=74.0,
            center_z=24.0,
            radius=21.0,
            seed=1.732,
            biome_profile="selva",
            height_peak=5.8,
            resource_richness=1.25,
            discovered_by="Pionero del Horizonte",
            discovered_by_role="EXPLORADOR",
            discovered_at_step=1,
            ring_index=1,
            world_id=world_id,
        ),
    ]


def calcular_bounds_dinamicos(continents: Optional[List[Continent]]) -> float:
    """Calcula el limite espacial dinamico para abarcar todos los continentes."""
    if not continents:
        return float(WORLD_BOUNDS)
    max_reach = float(WORLD_BOUNDS)
    for cont in continents:
        reach = max(abs(cont.center_x), abs(cont.center_z)) + cont.radius + 16.0
        if reach > max_reach:
            max_reach = reach
    return round(min(260.0, max_reach), 2)


def generar_nuevo_continente(
    existing_continents: List[Continent],
    discovered_by: str = "Explorador Autónomo",
    discovered_by_role: str = "EXPLORADOR",
    step_counter: int = 0,
    world_id: str = "mundo_gholgo_primario",
    preferred_biome: Optional[str] = None,
    seed_hint: Optional[float] = None,
) -> Continent:
    """Genera un continente nuevo no solapado usando espiral aurea para exploracion continua."""
    idx = len(existing_continents)
    golden_angle = 2.399963229728653
    seed_val = (
        float(seed_hint)
        if seed_hint is not None
        else round(((idx * 1.6180339 + (step_counter % 97) * 0.037) % 12.0) + 0.5, 4)
    )
    radius = round(17.5 + ((idx * 3 + step_counter) % 9) * 1.15, 2)
    base_ring = max(1, (idx // 5) + 1)

    chosen_x = 0.0
    chosen_z = 0.0
    placed = False
    for attempt in range(48):
        angle = idx * golden_angle + attempt * 0.41 + seed_val * 0.23
        ring_dist = 76.0 + base_ring * 24.0 + (attempt * 6.5)
        ring_dist = min(ring_dist, 185.0)
        cx = math.cos(angle) * ring_dist
        cz = math.sin(angle) * ring_dist
        collision = False
        for c in existing_continents:
            min_gap = radius + c.radius + 11.0
            if math.hypot(cx - c.center_x, cz - c.center_z) < min_gap:
                collision = True
                break
        if not collision:
            chosen_x = cx
            chosen_z = cz
            placed = True
            break

    if not placed:
        angle = idx * golden_angle
        ring_dist = 82.0 + idx * 14.0
        chosen_x = math.cos(angle) * min(200.0, ring_dist)
        chosen_z = math.sin(angle) * min(200.0, ring_dist)

    biome = (
        preferred_biome
        if preferred_biome in CONTINENT_BIOME_PROFILES
        else CONTINENT_BIOME_PROFILES[(idx + step_counter) % len(CONTINENT_BIOME_PROFILES)]
    )
    prefix = CONTINENT_NAME_PREFIXES[idx % len(CONTINENT_NAME_PREFIXES)]
    root = CONTINENT_NAME_ROOTS[(idx * 3 + len(biome)) % len(CONTINENT_NAME_ROOTS)]
    nombre = f"{prefix} {root} {idx}"

    height_map = {
        "montana_nevada": 7.6,
        "volcanico": 6.9,
        "cristalino": 6.4,
        "desierto_seco": 4.9,
        "selva": 5.3,
        "bosque": 5.6,
        "templado": 5.5,
    }
    height_peak = height_map.get(biome, 5.4) + ((idx % 4) * 0.35)

    return Continent(
        id=f"cont_{world_id[:8]}_{idx}_{step_counter}",
        nombre=nombre,
        center_x=round(chosen_x, 2),
        center_z=round(chosen_z, 2),
        radius=radius,
        seed=seed_val,
        biome_profile=biome,
        height_peak=round(height_peak, 2),
        resource_richness=round(1.0 + (idx % 5) * 0.14, 2),
        discovered_by=discovered_by,
        discovered_by_role=discovered_by_role,
        discovered_at_step=int(step_counter),
        ring_index=base_ring,
        world_id=world_id,
    )


def _elevacion_continente_secundario(x: float, z: float, cont: Continent) -> float:
    """Elevacion determinista para masas continentales adicionales (identica Python y Three.js)."""
    dx = x - cont.center_x
    dz = z - cont.center_z
    dist = math.hypot(dx, dz)
    r_lim = max(8.0, cont.radius)
    if dist >= r_lim * 1.28:
        return -8.0

    norm = dist / r_lim
    shelf = max(0.0, 1.0 - (norm ** 2.35))
    relief = (
        math.sin(dx * 0.14 + cont.seed) * math.cos(dz * 0.14 - cont.seed * 0.7) * 1.65
        + math.sin(dx * 0.07 - cont.seed * 0.4) * 0.9
    )
    peak = cont.height_peak * math.exp(-(norm ** 2) * 3.0)
    biome_mod = 0.0
    if cont.biome_profile == "montana_nevada":
        biome_mod = 1.65 * shelf
    elif cont.biome_profile == "desierto_seco":
        biome_mod = 1.15 * shelf - abs(relief) * 0.22
    elif cont.biome_profile == "selva":
        biome_mod = 0.65 * shelf + math.cos(norm * 5.0) * 0.45

    raw_y = -6.4 + shelf * (4.35 + relief + biome_mod) + peak
    return float(max(-8.0, min(9.5, raw_y)))


def calcular_altura_terreno_continentes(
    x: float, z: float, continents: Optional[List[Continent]] = None
) -> float:
    """Evalúa elevación considerando el continente central y los descubiertos."""
    y_best = calcular_altura_terreno(x, z)
    if not continents:
        return y_best
    for cont in continents:
        if cont.id == "cont_primario":
            continue
        yc = _elevacion_continente_secundario(x, z, cont)
        if yc > y_best:
            y_best = yc
    return float(max(-8.0, min(9.5, y_best)))


def altura_superficie_segura(
    x: float,
    z: float,
    footprint_radius: float = 0.0,
    continents: Optional[List[Continent]] = None,
    min_clearance: float = 0.18,
    mesh_grid_step: float = 1.35,
) -> float:
    """
    Calcula la altura maxima segura sobre el terreno considerando una huella radial y
    la discretizacion de malla, garantizando que nada quede atrapado debajo del terreno.
    """
    samples = [calcular_altura_terreno_continentes(x, z, continents)]
    half_cell = max(0.35, mesh_grid_step * 0.55)
    for ox in (-half_cell, half_cell):
        for oz in (-half_cell, half_cell):
            samples.append(calcular_altura_terreno_continentes(x + ox, z + oz, continents))

    if footprint_radius > 0.05:
        for ring_factor in (0.55, 1.0):
            rad = footprint_radius * ring_factor
            for k in range(8):
                ang = (math.tau * k) / 8.0
                sx = x + math.cos(ang) * rad
                sz = z + math.sin(ang) * rad
                samples.append(calcular_altura_terreno_continentes(sx, sz, continents))

    return float(round(max(samples) + max(0.06, min_clearance), 3))


def determinar_bioma_continentes(
    x: float,
    z: float,
    y: Optional[float] = None,
    continents: Optional[List[Continent]] = None,
) -> str:
    """Determina el bioma considerando todos los continentes activos."""
    elev = calcular_altura_terreno_continentes(x, z, continents) if y is None else float(y)
    if elev < SEA_LEVEL - 0.12:
        return "mar"
    if elev < SEA_LEVEL + 0.55:
        return "costa"
    if elev >= SNOW_LINE:
        return "nieve_alta"
    if continents:
        for cont in continents:
            if cont.id == "cont_primario":
                continue
            if math.hypot(x - cont.center_x, z - cont.center_z) <= cont.radius * 0.92:
                if cont.biome_profile == "desierto_seco":
                    return "seco"
                if cont.biome_profile == "montana_nevada":
                    return "nieve_alta" if elev >= SNOW_LINE - 0.5 else "valle"
                if cont.biome_profile in ("selva", "bosque", "cristalino", "volcanico"):
                    return "selva" if cont.biome_profile in ("selva", "bosque") else "valle"
                return "valle"
    return determinar_bioma(x, z, elev)
