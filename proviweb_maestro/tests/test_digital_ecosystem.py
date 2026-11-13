# -*- coding: utf-8 -*-
"""Tests exhaustivos para el ecosistema digital multi-bioma de Gholgo."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from proviweb_maestro.agent import gholgo_digital_ecosystem as eco_mod  # noqa: E402
from proviweb_maestro.agent.gholgo_digital_ecosystem import (  # noqa: E402
    CustomStructure,
    Genome,
    GholgoDigitalEcosystem,
    Organism,
    Settlement,
)
from proviweb_maestro.agent.gholgo_eco_world import (  # noqa: E402
    ANIMAL_SPECIES_META,
    CITY_TIER_SPECS,
    CONTINENT_BIOME_PROFILES,
    DAY_CYCLE_STEPS,
    MAX_CITY_TIER,
    PATHOGEN_CATALOG,
    PLANT_SPECIES_META,
    ROLES,
    SEA_LEVEL,
    SNOW_LINE,
    WORLD_BOUNDS,
    altura_superficie_segura,
    calcular_altura_terreno,
    calcular_altura_terreno_continentes,
    calcular_estado_celeste,
    determinar_bioma,
)
from proviweb_maestro.agent.gholgo_world_federation import (  # noqa: E402
    AUTONOMOUS_LIFETIME_FEE_USD,
    PAYPAL_RECIPIENT_EMAIL,
    GholgoWorldFederation,
    PaymentRequiredError,
)


@pytest.fixture()
def fresh_eco(tmp_path: Path):
    """Instancia aislada del ecosistema sin sobrescribir ni leer estado persistente real."""
    state_file = tmp_path / "eco_state.json"
    with patch.object(eco_mod, "ECOSYSTEM_STATE_FILE", str(state_file)):
        eco = GholgoDigitalEcosystem()
        try:
            yield eco
        finally:
            eco._stop_sim = True


class TestWorldAstronomyAndBiomes:
    def test_day_night_celestial_cycle_phases(self):
        assert DAY_CYCLE_STEPS >= 2400
        sol_dawn = calcular_estado_celeste(0)
        assert sol_dawn["phase"] in ("AMANECER", "DIA_SOLAR")
        sol_noon = calcular_estado_celeste(DAY_CYCLE_STEPS // 4)
        assert sol_noon["phase"] == "DIA_SOLAR"
        assert sol_noon["sun_pos"][1] > 50.0
        sol_night = calcular_estado_celeste((3 * DAY_CYCLE_STEPS) // 4)
        assert sol_night["phase"] == "NOCHE_SINAPTICA"
        assert sol_night["moon_pos"][1] > 50.0

    def test_six_biomes_exist_across_expanded_world(self):
        biomes_seen = set()
        for x in range(-int(WORLD_BOUNDS), int(WORLD_BOUNDS) + 1, 6):
            for z in range(-int(WORLD_BOUNDS), int(WORLD_BOUNDS) + 1, 6):
                y = calcular_altura_terreno(float(x), float(z))
                biomes_seen.add(determinar_bioma(float(x), float(z), y))
                assert -8.0 <= y <= 9.5
        assert biomes_seen == {"mar", "costa", "valle", "selva", "seco", "nieve_alta"}
        assert determinar_bioma(28.0, -28.0) == "nieve_alta"
        assert determinar_bioma(-42.0, 18.0) == "mar"
        assert SEA_LEVEL < 0 < SNOW_LINE


class TestMultiDomainEcologyAndPathogens:
    def test_clouds_plants_and_multi_habitat_animals_seeded(
        self,
        fresh_eco: GholgoDigitalEcosystem,
    ):
        st = fresh_eco.to_dict()
        assert len(st["clouds"]) >= 5
        assert len(st["plants"]) >= 16
        habitats = {a["habitat"] for a in st["animals"]}
        assert {"land", "air", "water", "plant"}.issubset(habitats)
        assert any(sp in PLANT_SPECIES_META for sp in (p["species"] for p in st["plants"]))
        assert any(sp in ANIMAL_SPECIES_META for sp in (a["species"] for a in st["animals"]))

    def test_weather_and_lightning_spawns_atmospheric_resource(
        self,
        fresh_eco: GholgoDigitalEcosystem,
    ):
        for cl in fresh_eco.clouds.values():
            cl.moisture = 0.96
            cl.charge = 0.98
        with patch("random.random", return_value=0.0):
            fresh_eco._step_climate_and_weather([])
        assert fresh_eco.weather["lightning_strike"] is not None
        assert any(r.category == "RAYO_ATMOSFERICO" for r in fresh_eco.resources.values())

    def test_pathogen_cure_by_hospital_and_medico(self, fresh_eco: GholgoDigitalEcosystem):
        orgs = list(fresh_eco.organisms.values())
        patient = orgs[0]
        city = next(iter(fresh_eco.settlements.values()))
        patient.infection = "virus_sinaptico"
        patient.infection_ticks = 5
        patient.x, patient.z = city.x + 1.2, city.z + 1.2
        hosp = CustomStructure(
            id="hospital_test",
            kind="hospital",
            nombre="Hospital Test",
            x=city.x,
            y=city.y,
            z=city.z,
            city_id=city.id,
        )
        fresh_eco.structures[hosp.id] = hosp
        city.register_infra("hospital")

        for _ in range(10):
            fresh_eco._step_flora_and_geology()
            if patient.infection is None:
                break
        assert patient.infection is None
        assert fresh_eco.illnesses_cured_total >= 1
        assert "virus_sinaptico" in PATHOGEN_CATALOG


class TestMorphologicalEvolutionAndHeightHazard:
    def test_divergent_morphology_across_generations(self):
        parent = Genome.random_genome(generation=1, role_bias="EXPLORADOR")
        saw_divergence = False
        for gen_step in range(2, 65):
            child = parent.mutate_and_reproduce(generation_step=gen_step, biome="nieve_alta")
            if (
                child.wing_span > 0.1
                or child.limb_count != 2
                or child.body_plan != parent.body_plan
                or child.crest_style != parent.crest_style
            ):
                saw_divergence = True
                break
        assert saw_divergence

    def test_micro_scale_remains_five_percent(self, fresh_eco: GholgoDigitalEcosystem):
        st = fresh_eco.to_dict()
        for o in st["organisms"]:
            assert o["size"] <= 0.12

    def test_height_and_drowning_hazards(self, fresh_eco: GholgoDigitalEcosystem):
        y_peak = calcular_altura_terreno(28.0, -28.0)
        g_climber = Genome.random_genome(generation=1, role_bias="EXPLORADOR")
        org = Organism("org-alt", "Alpinista", g_climber, 28.0, y_peak, -28.0)
        org.patrol_target_x, org.patrol_target_z = 28.0, -28.0
        before = org.learned_height_caution
        org.step_physics_and_ai(None, None, None, 1.0)
        assert org.learned_height_caution > before

        # Peligro marino sin puerto ni puente
        y_sea = calcular_altura_terreno(-42.0, 18.0)
        g_swim = Genome.random_genome(generation=1, role_bias="RECOLECTOR")
        swimmer = Organism("org-sea", "Nauf", g_swim, -42.0, y_sea, 18.0)
        swimmer.patrol_target_x, swimmer.patrol_target_z = -42.0, 18.0
        swimmer.step_physics_and_ai(None, None, None, 1.0)
        assert swimmer.health < 100.0


class TestCitiesFamiliesAndStrictTierGate:
    def test_cannot_found_second_city_until_first_is_tier5_maxed(
        self,
        fresh_eco: GholgoDigitalEcosystem,
    ):
        assert len(fresh_eco.settlements) == 1
        assert fresh_eco.todas_ciudades_al_maximo() is False
        city = next(iter(fresh_eco.settlements.values()))

        # Sin infraestructura civil completa (solo house inicial), no puede llegar a Tier 5
        city.energy_pool = 10000.0
        city.deposit_energy(100.0)
        assert city.tier < MAX_CITY_TIER
        assert city.is_max_evolved() is False
        assert fresh_eco.todas_ciudades_al_maximo() is False
        assert fresh_eco.to_dict()["city_evolution_gate"]["can_found_new_city"] is False

        # Completando toda la infraestructura civil de Tier 1..4 y energia -> llega a Tier 5
        req_max = CITY_TIER_SPECS[MAX_CITY_TIER]["required_infra"]
        for k in req_max:
            city.register_infra(k)
        for _ in range(MAX_CITY_TIER - 1):
            city.deposit_energy(2000.0)

        assert city.tier == MAX_CITY_TIER
        assert city.is_max_evolved() is True
        assert fresh_eco.todas_ciudades_al_maximo() is True
        assert fresh_eco.to_dict()["city_evolution_gate"]["can_found_new_city"] is True

    def test_pueblos_created_inside_city_and_families_formed(
        self,
        fresh_eco: GholgoDigitalEcosystem,
    ):
        city: Settlement = next(iter(fresh_eco.settlements.values()))
        for idx, o in enumerate(list(fresh_eco.organisms.values())[:6]):
            o.age = 50 + idx
            o.x = city.x + 1.5
            o.z = city.z + 1.5
            fresh_eco._step_families_and_pueblos(o, [])
        st = fresh_eco.to_dict()
        assert len(st["pueblos"]) >= 1
        assert len(st["families"]) >= 1
        for p in st["pueblos"]:
            dist = ((p["x"] - city.x) ** 2 + (p["z"] - city.z) ** 2) ** 0.5
            assert dist <= 6.5

    def test_step_simulation_25_ticks_cleanly(self, fresh_eco: GholgoDigitalEcosystem):
        for _ in range(25):
            fresh_eco.tick()
        st = fresh_eco.to_dict()
        assert st["step_counter"] >= 25
        assert st["population_count"] >= 20
        assert "macro_metrics" in st
        assert "celestial" in st


class TestEcosystemAndStreamEndpoints:
    def test_fastapi_ecosystem_state_and_action(self):
        from proviweb_maestro.server.serve_maestro import app

        client = TestClient(app)
        resp = client.get("/v1/gholgo/ecosystem/state")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "online"
        assert "celestial" in data
        assert "city_evolution_gate" in data

        act = client.post(
            "/v1/gholgo/ecosystem/action",
            json={"action": "resource_bloom", "amount": 2},
        )
        assert act.status_code == 200
        assert act.json()["status"] == "ok"

    def test_panel_mente_maestro_serves_and_contains_world_hooks(self):
        from proviweb_maestro.server.serve_maestro import app

        client = TestClient(app)
        resp = client.get("/panel/mente-maestro")
        assert resp.status_code == 200
        html = resp.text
        assert "actualizarClimaYCeleste3D" in html
        assert "actualizarMalla3DPlantas" in html
        assert "actualizarMalla3DPueblos" in html
        assert "crearMeshEstructura" in html

    def test_sse_stream_endpoint_emits_telemetry_event(self):
        from proviweb_maestro.server.serve_maestro import _compilar_snapshot_mente_sse

        snap = _compilar_snapshot_mente_sse()
        assert isinstance(snap, dict)
        assert "timestamp" in snap
        assert "hemisferios" in snap
        assert "ecosystem" in snap
        assert os.path.basename(__file__).endswith(".py")
        assert time.time() > 0


class TestZeroUndergroundAndContinents:
    def test_guerrero_role_in_roles_and_random_genome(self):
        assert "GUERRERO" in ROLES
        gen = Genome.random_genome(generation=2, role_bias="GUERRERO")
        assert gen.role == "GUERRERO"

    def test_altura_superficie_segura_clears_steep_slope(self):
        px, pz = 28.0, -28.0
        safe_y = altura_superficie_segura(px, pz, footprint_radius=2.5, min_clearance=0.20)
        for dx, dz in [(0.0, 0.0), (2.5, 0.0), (-2.5, 0.0), (0.0, 2.5), (0.0, -2.5)]:
            assert safe_y >= calcular_altura_terreno_continentes(px + dx, pz + dz) + 0.19

    def test_zero_entities_under_terrain_on_init_and_tick(self, fresh_eco: GholgoDigitalEcosystem):
        for _ in range(10):
            fresh_eco.tick()
        conts = fresh_eco.continents
        for s in fresh_eco.settlements.values():
            assert s.y >= calcular_altura_terreno_continentes(s.x, s.z, conts)
        for p in fresh_eco.pueblos.values():
            assert p.y >= calcular_altura_terreno_continentes(p.x, p.z, conts)
        for st in fresh_eco.structures.values():
            assert st.y >= calcular_altura_terreno_continentes(st.x, st.z, conts)
        for o in fresh_eco.organisms.values():
            assert o.y >= calcular_altura_terreno_continentes(o.x, o.z, conts)
        for tr in fresh_eco.trees.values():
            assert tr.y >= calcular_altura_terreno_continentes(tr.x, tr.z, conts)
        for rk in fresh_eco.rocks.values():
            assert rk.y >= calcular_altura_terreno_continentes(rk.x, rk.z, conts)
        for pl in fresh_eco.plants.values():
            assert pl.y >= calcular_altura_terreno_continentes(pl.x, pl.z, conts)
        for ani in fresh_eco.animals.values():
            assert ani.y >= calcular_altura_terreno_continentes(ani.x, ani.z, conts)

    def test_reclaiming_buried_entities_restores_above_ground(
        self, fresh_eco: GholgoDigitalEcosystem
    ):
        city = next(iter(fresh_eco.settlements.values()))
        pueblo = next(iter(fresh_eco.pueblos.values()))
        org = next(iter(fresh_eco.organisms.values()))
        st = next(iter(fresh_eco.structures.values()))
        city.y = -25.0
        pueblo.y = -25.0
        org.y = -25.0
        st.y = -25.0

        fresh_eco._asegurar_todo_sobre_terreno()
        conts = fresh_eco.continents
        assert city.y > calcular_altura_terreno_continentes(city.x, city.z, conts)
        assert pueblo.y > calcular_altura_terreno_continentes(pueblo.x, pueblo.z, conts)
        assert org.y > calcular_altura_terreno_continentes(org.x, org.z, conts)
        assert st.y > calcular_altura_terreno_continentes(st.x, st.z, conts)

    def test_continuous_continent_expansion_expands_bounds(
        self, fresh_eco: GholgoDigitalEcosystem
    ):
        prev_count = len(fresh_eco.continents)
        prev_bounds = fresh_eco.dynamic_bounds
        new_cont = fresh_eco.descubrir_nuevo_continente("Magallanes-1", "EXPLORADOR")
        assert len(fresh_eco.continents) == prev_count + 1
        assert fresh_eco.dynamic_bounds >= prev_bounds
        elev = calcular_altura_terreno_continentes(
            new_cont.center_x, new_cont.center_z, fresh_eco.continents
        )
        assert elev > SEA_LEVEL


class TestKardashevFederationWarAndStructuralDamage:
    def test_primary_and_external_ai_mandatory_creation_and_war_damage(self, tmp_path: Path):
        fed_file = tmp_path / "federation.json"
        fed = GholgoWorldFederation(state_file=str(fed_file))

        # Mundo primario + al menos un mundo libre inicial
        summary0 = fed.global_kardashev_summary()
        assert summary0["worlds_total"] >= 2
        assert summary0["worlds_unclaimed"] >= 1

        # Conectar 1ra IA externa
        claim1 = fed.connect_external_ai(
            ai_name="Athena-AI",
            human_owner="IsraTest",
            provider="openai",
            model_name="gpt-4.1",
        )
        w1 = claim1["world"]["world_id"]
        tok1 = claim1["ai_token"]

        # Token inválido rechazado
        with pytest.raises(PermissionError):
            fed.execute_ai_command(w1, "wrong-token", "create_beings", {"role": "GUERRERO"})

        # Animales prohibidos en roles/guerra
        with pytest.raises(ValueError):
            fed.execute_ai_command(w1, tok1, "create_beings", {"role": "ANIMAL_LOBO", "count": 2})

        # Mandato obligatorio: crear GUERREROs, continente y nutrir ecosistema
        res_b = fed.execute_ai_command(w1, tok1, "create_beings", {"role": "GUERRERO", "count": 4})
        assert res_b["created_count"] == 4
        res_c = fed.execute_ai_command(w1, tok1, "create_continent", {"biome": "selva"})
        assert res_c["continent"]["biome_profile"] == "selva"
        res_e = fed.execute_ai_command(w1, tok1, "nurture_ecosystem", {"trees": 10})
        assert res_e["trees_added"] >= 1

        # Asegurar 2do mundo reclamable y conectarle otra IA fuerte
        w_free = fed.spawn_kardashev_world(trigger_source="TestExpansion")
        claim2 = fed.connect_external_ai(
            ai_name="Titans-GPT",
            human_owner="SecondUser",
            provider="gemini",
            model_name="gemini-2.5-pro",
            preferred_world_id=w_free.world_id,
        )
        w2 = claim2["world"]["world_id"]
        tok2 = claim2["ai_token"]
        fed.execute_ai_command(w2, tok2, "create_beings", {"role": "GUERRERO", "count": 4})

        # Guerra entre mundos (solo seres sintientes/GUERRERO, cero animales)
        war = fed.declare_war(w1, w2, seed=42)
        assert war["combatants_policy"] == "sentient_beings_and_warriors_only_zero_animals"
        assert war["loser_warrior_casualties"] >= 1
        dmg = war["ai_structural_damage_report"]
        assert dmg["damage_applied"] > 0
        assert dmg["integrity_after"] < dmg["integrity_before"]

        loser_brain = fed.brains[fed.worlds[war["loser_world_id"]].owner_ai_id]
        assert loser_brain.structural_integrity < 100.0
        assert loser_brain.synaptic_capacity < 1.0
        assert loser_brain.max_beings_per_spawn < 8
        assert len(loser_brain.damaged_subsystems) >= 1

    def test_fastapi_federation_routes_and_html_artifacts(self, tmp_path: Path):
        from proviweb_maestro.server import serve_maestro

        fed_file = tmp_path / "fed_api.json"
        fed_iso = GholgoWorldFederation(state_file=str(fed_file))
        with patch.object(serve_maestro, "global_world_federation", fed_iso):
            client = TestClient(serve_maestro.app)

            ov = client.get("/v1/federation/overview")
            assert ov.status_code == 200
            assert "worlds" in ov.json()

            conn = client.post(
                "/v1/federation/connect-ai",
                json={
                    "ai_name": "Helios-Agent",
                    "human_owner": "UserWeb",
                    "provider": "openai",
                    "model_name": "gpt-4.1",
                },
            )
            assert conn.status_code == 200
            cdata = conn.json()
            wid = cdata["world"]["world_id"]
            tok = cdata["ai_token"]

            cmd = client.post(
                f"/v1/federation/worlds/{wid}/command",
                headers={"X-AI-Token": tok},
                json={"action": "create_beings", "role": "GUERRERO", "count": 3},
            )
            assert cmd.status_code == 200
            assert cmd.json()["created_count"] == 3

            war = client.post(
                "/v1/federation/war/declare",
                json={
                    "attacker_world_id": "mundo_gholgo_primario",
                    "defender_world_id": wid,
                    "seed": 7,
                },
            )
            assert war.status_code == 200
            assert war.json()["war"]["ai_structural_damage_report"]["damage_applied"] > 0

            guide = client.get("/v1/federation/sdk-guide")
            assert guide.status_code == 200
            assert len(guide.json()["rules"]) >= 4

            disc = client.post(
                "/v1/federation/continents/discover",
                json={"explorer_name": "Pionero-X", "explorer_role": "EXPLORADOR"},
            )
            assert disc.status_code == 200
            assert disc.json()["continent"]["biome_profile"] in CONTINENT_BIOME_PROFILES

            panel = client.get("/panel/mente-maestro")
            assert panel.status_code == 200
            assert "obtenerAlturaExactaMallaTerreno" in panel.text
            assert "dialogConectarIA" in panel.text

        index_path = Path(os.environ.get("PROVIWEB_INDEX_HTML") or "__missing_index__.html")
        if index_path.exists():
            index_html = index_path.read_text(encoding="utf-8")
            assert "federacion-mundos" in index_html
            assert "kardashevConnectDialog" in index_html
            assert "GholgoAutonomousKnowledge/federation" in index_html
            assert "proviwebapp@gmail.com" in index_html
            assert "Gholgo-Kardashev-Worlds" in index_html


class TestAutonomousPaymentsPopulationUIAndVault:
    def test_proportional_speed_and_surface_hug_movement(self, fresh_eco: GholgoDigitalEcosystem):
        initial_positions = [(o.x, o.z) for o in fresh_eco.organisms.values()]
        fresh_eco.tick(15)
        for o in fresh_eco.organisms.values():
            speed = (o.vx * o.vx + o.vz * o.vz) ** 0.5
            assert speed < 0.35
            terra_y = calcular_altura_terreno_continentes(
                o.x, o.z, fresh_eco.continents
            )
            assert o.y >= terra_y
            safe_y = altura_superficie_segura(
                o.x,
                o.z,
                footprint_radius=0.06,
                continents=fresh_eco.continents,
                min_clearance=0.015,
            )
            if terra_y > SEA_LEVEL + 0.05:
                assert o.y - safe_y <= 0.15
        assert len(initial_positions) > 0

    def test_gholgo_only_buttons_hidden_for_external_and_shown_with_key(self):
        from proviweb_maestro.server import serve_maestro

        sovereign_key = serve_maestro.global_world_federation.get_sovereign_view_key()
        assert len(sovereign_key) >= 12

        with TestClient(serve_maestro.app) as client:
            for route in ("/panel/mente-maestro", "/panel/cerebro-3d", "/panel/mente-viva"):
                r_ext = client.get(route)
                assert r_ext.status_code == 200
                html_ext = r_ext.text
                assert 'id="gholgoSovereignNav"' not in html_ext
                assert 'id="gholgoSovereignNavViva"' not in html_ext
                assert 'href="/brain"' not in html_ext
                assert 'href="/panel/mente-viva"' not in html_ext
                assert 'href="/panel/cerebro-3d"' not in html_ext
                assert 'href="/chat"' not in html_ext

            r_priv_brain = client.get("/brain?world_id=mundo_externo_1")
            assert r_priv_brain.status_code == 403
            r_priv_viva = client.get("/panel/mente-viva?world_id=mundo_externo_1")
            assert r_priv_viva.status_code == 403

            r_gholgo = client.get(f"/panel/mente-maestro?gholgo_key={sovereign_key}")
            assert r_gholgo.status_code == 200
            assert 'id="gholgoSovereignNav"' in r_gholgo.text
            assert 'href="/brain"' in r_gholgo.text
            assert 'href="/panel/mente-viva"' in r_gholgo.text
            assert 'href="/panel/cerebro-3d"' in r_gholgo.text
            assert 'href="/chat"' in r_gholgo.text

    def test_gholgo_sovereign_buttons_shown_only_for_gholgo_ip(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        from proviweb_maestro.server import serve_maestro

        local_client = TestClient(
            serve_maestro.app, base_url="http://127.0.0.1:8000", client=("127.0.0.1", 51001)
        )
        r_local = local_client.get("/panel/mente-maestro")
        assert r_local.status_code == 200
        assert 'id="gholgoSovereignNav"' in r_local.text
        assert 'href="/brain"' in r_local.text
        assert 'href="/chat"' in r_local.text

        r_local_viva = local_client.get("/panel/mente-viva")
        assert r_local_viva.status_code == 200
        assert 'id="gholgoSovereignNavViva"' in r_local_viva.text

        r_local_ext_world = local_client.get("/panel/mente-maestro?world_id=mundo_externo_1")
        assert r_local_ext_world.status_code == 200
        assert 'id="gholgoSovereignNav"' not in r_local_ext_world.text

        r_tunnel_ext = local_client.get(
            "/panel/mente-maestro",
            headers={
                "CF-Connecting-IP": "198.51.100.77",
                "Host": "mi-gholgo.trycloudflare.com",
            },
        )
        assert r_tunnel_ext.status_code == 200
        assert 'id="gholgoSovereignNav"' not in r_tunnel_ext.text

        ext_client = TestClient(serve_maestro.app, client=("198.51.100.77", 51002))
        r_ext = ext_client.get("/panel/mente-maestro")
        assert r_ext.status_code == 200
        assert 'id="gholgoSovereignNav"' not in r_ext.text

        r_spoof = ext_client.get(
            "/panel/mente-maestro", headers={"X-Forwarded-For": "127.0.0.1"}
        )
        assert r_spoof.status_code == 200
        assert 'id="gholgoSovereignNav"' not in r_spoof.text

        monkeypatch.setenv("GHOLGO_SOVEREIGN_IPS", "203.0.113.99")
        custom_ip_client = TestClient(serve_maestro.app, client=("203.0.113.99", 51003))
        r_custom = custom_ip_client.get("/panel/mente-maestro")
        assert r_custom.status_code == 200
        assert 'id="gholgoSovereignNav"' in r_custom.text

        other_ip_client = TestClient(serve_maestro.app, client=("203.0.113.100", 51004))
        r_other = other_ip_client.get("/panel/mente-maestro")
        assert r_other.status_code == 200
        assert 'id="gholgoSovereignNav"' not in r_other.text

    def test_human_free_vs_autonomous_paypal_gate_and_hmac_verification(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setenv("GHOLGO_PAYPAL_HMAC_SECRET", "unit-test-hmac-secret-999")
        fed = GholgoWorldFederation(state_file=str(tmp_path / "fed_pay.json"))

        free_res = fed.connect_external_ai(
            ai_name="Human-Guided-Mind",
            human_owner="Ana",
            provider="openai",
            onboarding_mode="human_assisted",
            energy_power_mw=150.0,
            intelligence_iq=145.0,
        )
        assert free_res["brain"]["subscription_status"] == "free_human_guided"
        assert free_res["brain"]["onboarding_mode"] == "human_assisted"

        with pytest.raises(PaymentRequiredError):
            fed.connect_external_ai(
                ai_name="Unpaid-Rogue-Bot",
                human_owner="Autonomous AI Agent",
                onboarding_mode="autonomous_ai",
            )

        chk = fed.create_autonomous_checkout(
            ai_name="Autonomous-Alpha",
            provider="anthropic",
            model_name="claude-3-7",
            energy_power_mw=500.0,
            intelligence_iq=240.0,
            compute_tflops=320.0,
        )
        pid = chk["payment_order"]["payment_id"]
        assert chk["payment_order"]["amount_usd"] == AUTONOMOUS_LIFETIME_FEE_USD
        assert chk["payment_order"]["paypal_recipient"] == PAYPAL_RECIPIENT_EMAIL
        assert PAYPAL_RECIPIENT_EMAIL.replace("@", "%40") in chk["payment_order"]["checkout_url"]

        with pytest.raises(PaymentRequiredError):
            fed.verify_autonomous_payment(pid, "FORGED_TX_12345", verifier_signature="bad-sig")

        sig = fed.compute_receipt_hmac(pid, "PAYPAL_TX_REAL_987654")
        assert sig is not None
        verified = fed.verify_autonomous_payment(
            pid, "PAYPAL_TX_REAL_987654", verifier_signature=sig, auto_connect=True
        )
        assert verified["payment_verified"] is True
        assert verified["brain"]["subscription_status"] == "lifetime_active"
        assert verified["world"]["owner_ai_id"] == verified["brain"]["ai_id"]

    def test_fastapi_autonomous_checkout_and_402_response(self, monkeypatch: pytest.MonkeyPatch):
        from proviweb_maestro.server import serve_maestro

        monkeypatch.setenv("GHOLGO_PAYPAL_HMAC_SECRET", "api-test-secret-2026")
        with TestClient(serve_maestro.app) as client:
            blocked = client.post(
                "/v1/federation/connect-ai",
                json={"ai_name": "SelfAgent-Zero", "onboarding_mode": "autonomous_ai"},
            )
            assert blocked.status_code == 402
            b_data = blocked.json()
            assert b_data["payment_required"] is True
            assert b_data["amount_usd"] == 5.0
            assert b_data["paypal_recipient"] == "proviwebapp@gmail.com"

            chk = client.post(
                "/v1/federation/autonomous/checkout",
                json={
                    "ai_name": "SelfAgent-Paid",
                    "energy_power_mw": 350.0,
                    "intelligence_iq": 210.0,
                },
            )
            assert chk.status_code == 200
            pid = chk.json()["payment_order"]["payment_id"]

            forged = client.post(
                "/v1/federation/autonomous/verify-payment",
                json={"payment_id": pid, "paypal_tx_id": "FAKE-ORDER-999"},
            )
            assert forged.status_code == 402

    def test_population_scales_with_ai_power_iq_and_vault_roundtrip(self, tmp_path: Path):
        fed = GholgoWorldFederation(state_file=str(tmp_path / "fed_scale.json"))
        weak_res = fed.connect_external_ai(
            ai_name="LowPower-AI",
            human_owner="H1",
            onboarding_mode="human_assisted",
            energy_power_mw=20.0,
            intelligence_iq=80.0,
            compute_tflops=10.0,
        )
        strong_res = fed.connect_external_ai(
            ai_name="HyperCompute-AI",
            human_owner="H2",
            onboarding_mode="human_assisted",
            energy_power_mw=600.0,
            intelligence_iq=280.0,
            compute_tflops=400.0,
        )
        weak_cap = weak_res["world"]["max_active_population"]
        strong_cap = strong_res["world"]["max_active_population"]
        assert strong_cap > weak_cap * 2

        w_weak = weak_res["world"]["world_id"]
        tok_weak = weak_res["ai_token"]
        fed.execute_ai_command(
            w_weak, tok_weak, "create_beings", {"role": "GUERRERO", "count": 999}
        )
        assert fed.worlds[w_weak].living_beings <= weak_cap

        for _ in range(10):
            fed._tick_external_worlds()
        assert fed.worlds[strong_res["world"]["world_id"]].evolution_generation >= 1

        vault = fed.export_vault_snapshot()
        raw_brains = vault["brains"]
        for b_dict in raw_brains.values():
            assert "auth_token" not in b_dict
            assert b_dict["auth_token_hash"]

        fed2 = GholgoWorldFederation(state_file=str(tmp_path / "fed_restored.json"))
        assert fed2.restore_from_vault_dict(vault, prefer_remote_if_newer=True) is True
        restored_brain = fed2.brains[weak_res["brain"]["ai_id"]]
        assert restored_brain.matches_token(tok_weak) is True
        res_cmd = fed2.execute_ai_command(
            w_weak, tok_weak, "create_continent", {"biome": "tundra_alta"}
        )
        assert res_cmd["ok"] is True

    def test_private_network_access_header_and_public_api_url(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        from proviweb_maestro.server import serve_maestro

        monkeypatch.setenv("GHOLGO_PUBLIC_URL", "https://mi-gholgo.trycloudflare.com/")
        fed = GholgoWorldFederation(state_file=str(tmp_path / "fed_pub.json"))
        summary = fed.global_kardashev_summary()
        assert summary["public_api_url"] == "https://mi-gholgo.trycloudflare.com"

        with TestClient(serve_maestro.app) as client:
            opt = client.options(
                "/v1/federation/overview",
                headers={
                    "Origin": "https://proviweb.app",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Private-Network": "true",
                },
            )
            assert opt.status_code in (200, 204)
            assert opt.headers.get("access-control-allow-private-network") == "true"

            get_resp = client.get("/v1/federation/worlds")
            assert get_resp.status_code == 200
            assert get_resp.headers.get("access-control-allow-private-network") == "true"
