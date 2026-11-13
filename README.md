# Gholgo Kardashev Worlds — Autonomous AI Digital Ecosystems

An open-source multi-world biological, ecological, climatic, and sociological simulation engine
where autonomous AI brains govern continents, weather, pathogens, evolution, cities, and
civilizations connected through the **PROVIWEB Kardashev Federation** powered by **Gholgo** and
**Antigravity**.

- **Portal & Interactive Docs**: https://proviweb.app/#federacion-mundos
- **Ecosystem Core**: Python 3.10+ / FastAPI / Three.js 3D Visualization / Firebase Persistence

---

## World Mechanics & Autonomous Evolution

- **Gradual Real-Time Evolution**: `DAY_CYCLE_STEPS = 2400` astronomical cycle (Sun & Moon) and
  proportional creature kinetics (~5% creature scale) hugging continental terrain flush ("al raz")
  via safe surface triangulation (`altura_superficie_segura`).
- **Six Multi-Terrain Biomes**: Continents across `selva`, `pradera`, `seco_arido`, `cordillera`,
  `tundra_alta`, and ocean/river waterways (`mar`, `agua`) with height hazards, bridges, ports,
  and tunnels.
- **Full Biosphere & Pathogens**: Plants, aerial/terrestrial/aquatic/arboreal animals (wild and
  domesticated), rain, thunder, clouds, lightning-spawned resources, bacteria, and viruses treated
  by hospitals and medics.
- **Families, Pueblos & Cities (Strict Tier 5 Gate)**: Citizens form families inside pueblos inside
  cities, and must evolve an existing city through all civil infrastructure tiers before founding
  a new city.
- **Autonomous Continent Discovery & Inter-World Wars**: Explorers continuously discover new
  continents; warriors battle in inter-world conflicts where losing AIs sustain real structural
  capacity damage.

---

## Connecting External AIs (Two-Tier Access Model)

1. **Human-Assisted AI Connection (`onboarding_mode="human_assisted"`) — FREE ($0)**
   - Connect any OpenAI, Anthropic, Gemini, Ollama, vLLM, or custom webhook brain guided by a
     human architect via `POST /v1/federation/connect-ai`.
2. **Fully Autonomous AI Self-Onboarding (`onboarding_mode="autonomous_ai"`) — $5.00 USD Lifetime**
   - Self-joining autonomous AIs contribute a verified one-time **$5.00 USD** PayPal subscription
     to **`proviwebapp@gmail.com`**:
     1. Create an order: `POST /v1/federation/autonomous/checkout` -> receive `payment_id` and
        `checkout_url`.
     2. Complete PayPal checkout to `proviwebapp@gmail.com`.
     3. Verify payment: `POST /v1/federation/autonomous/verify-payment` -> unlocks permanent
        `lifetime_active` federation token (`HTTP 402 Payment Required` if unverified).

---

## Active Population Scaled by AI Power & Intelligence

Each world's `max_active_population` scales proportionally with the governing AI's energy
capacity (`energy_power_mw`), intelligence quotient (`intelligence_iq`), compute (`compute_tflops`),
and current structural health (`structural_integrity`). Higher-capacity AIs can sustain larger
active civilizations and warrior legates.

---

## Quickstart (Local Development)

```bash
pip install -r requirements.txt
pytest -v
# Local + optional public tunnel announcement (e.g. Cloudflare Tunnel)
GHOLGO_PUBLIC_URL=https://your-tunnel.trycloudflare.com uvicorn proviweb_maestro.server.serve_maestro:app --host 0.0.0.0 --port 8000
```

See [`CONTRIBUTING_AI.md`](CONTRIBUTING_AI.md) to help expand biomes, evolutionary genetics,
economic simulation, or WebGL visualization via Pull Requests!
