# WearImpact

WearImpact is a sustainable-fashion web application that helps users reduce textile waste by making eco-friendly choices easier to discover, understand, and act on. It combines a map-based eco-shop navigator, an AI sustainability advisor, a privacy-first digital wardrobe, and a brand sustainability search tool into a single Vue 3 experience.

---

## Project Goals

- Help users find nearby second-hand, donation, and recycling destinations.
- Provide AI-driven guidance on extending garment life and making greener purchasing decisions.
- Let users build a personal digital wardrobe from photos, with automatic clothing recognition.
- Surface sustainability ratings and certifications for fashion brands.

---

## Feature Overview

### Local Eco-Shop Navigator
A Mapbox-powered map that searches second-hand shops, donation points, and recycling centres near the user's location. Results are sorted by straight-line (Haversine) distance, with detail panels showing address, opening hours, phone, and website. Place details are cached in Redis to reduce upstream Google Places traffic.

### Digital Wardrobe + AI Advisor
- **Digital Wardrobe** — users upload garment photos; a CLIP + rembg + human-parser pipeline classifies each item into a main category (upper body / lower body / footwear) and a subcategory. Wardrobe data is stored entirely in the browser (IndexedDB via Dexie), so no account or backend storage is required.
- **AI Sustainability Advisor** — a chat assistant that answers fabric-care, repair, and eco-impact questions, with response caching on the backend.

### Brand Sustainability Search
Search a curated brand index and view sustainability ratings, certifications, and recommended alternatives.

### Knowledge Hub & Home
A redesigned content surface that introduces users to fast-fashion impact, circular-fashion concepts, and the project's tools.

---

## Architecture

```
┌──────────────── Browser (Vue 3 + Vite + Tailwind) ────────────────┐
│   Home · Knowledge Hub · Eco-Shop Map · Wardrobe · Advisor · Brand │
└───────┬───────────────────────┬───────────────────────┬────────────┘
        │ REST                  │ REST (multipart)      │ REST
        ▼                       ▼                       ▼
  FastAPI backend       HuggingFace Space        FastAPI backend
  (locations API)       Flask + CLIP + rembg     (advisor + brands)
        │                                               │
        ▼                                               ▼
  Google Places API                                Redis cache
  Redis cache
```

- **Frontend** — Vue 3, Vue Router, Tailwind CSS v4, Mapbox GL, GSAP, Dexie (IndexedDB).
- **Backend** — Python 3.11 + FastAPI, Redis (cache), Google Places API.
- **Model service** — separate Flask app deployed to a HuggingFace Space (Docker SDK, CPU). Kept independent of the FastAPI backend because the PyTorch / CLIP / rembg dependency footprint (~1.5 GB) would otherwise bloat the API deploy.

---

## Repository Layout

```
.
├── frontend/        Vue 3 single-page app (Vite)
├── backend/         FastAPI service (locations, advisor, brands)
└── README.md
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | Vue 3, Vite, Vue Router, Tailwind CSS v4, Mapbox GL, GSAP, Dexie, Iconify, Lucide |
| Backend | Python 3.11, FastAPI, Pydantic, Redis (async), httpx |
| AI / Vision | CLIP (`openai/clip-vit-base-patch32`), rembg, FASHN human parser, Flask, gunicorn |
| Hosting | Vercel (frontend), Railway (backend + Redis), HuggingFace Spaces (model service) |

---

## Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- Redis (optional locally; backend gracefully runs without it)

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check: `GET http://localhost:8000/health`.

### Model service
The clothing-classification service (Flask + CLIP + rembg) is maintained separately and deployed to a HuggingFace Space. The frontend talks to it directly, so no local setup is required for normal development. Source lives in [FIT5120-Classification-Mod/](FIT5120-Classification-Mod/).

---

## Environment variables checklist

The repo does not ship secret values. Ask the project owner for the actual values, or generate your own where applicable. **Names only** — set these in your local `.env*` files (which are gitignored).

### Frontend (`frontend/.env.local`)
| Variable | Purpose |
|---|---|
| `VITE_GOOGLE_MAPS_API_KEY` | Google Maps / Places — required for Eco-Shop map |
| `VITE_MAPBOX_ACCESS_TOKEN` | Mapbox GL public token — required for the map renderer |
| `VITE_MODEL_SERVICE_URL` | HF Space URL for image classification (defaults to public Space) |
| `VITE_HF_TOKEN` | HuggingFace token — only needed if the Space is private |

### Backend (`backend/.env`)
| Variable | Purpose |
|---|---|
| `GOOGLE_MAPS_API_KEY` | Server-side Google Places API key |
| `ANTHROPIC_API_KEY` | Claude API key for the wardrobe advisor (Epic 3) |
| `ANTHROPIC_MODEL` | Optional override; defaults to `claude-haiku-4-5-20251001` |
| `REDIS_URL` | Optional; defaults to `redis://localhost:6379` |
| `DATABASE_URL` | PostgreSQL URL for Epic 4 brand search (asyncpg driver) |
| `CORS_ORIGINS` | Comma-separated allowed origins; only enforced when `CORS_STRICT=1` |
| `CORS_STRICT` | Set to `1` to enable the CORS whitelist; unset = open (current default) |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Wardrobe upload hangs 30–60 s on first try | HuggingFace Space cold start (CLIP + rembg loading ~1.5 GB into RAM) | Wait — subsequent calls run in 1–10 s. Free-tier Spaces sleep after ~48 h idle. |
| Advisor `/api/wardrobe/audit` returns 503 | `ANTHROPIC_API_KEY` missing or quota exhausted | Check backend logs; set the env var; restart `uvicorn`. |
| Map shows but markers don't load | Missing `VITE_MAPBOX_ACCESS_TOKEN` or `VITE_GOOGLE_MAPS_API_KEY` | Add the missing env var to `frontend/.env.local` and restart `npm run dev`. |
| Backend logs `Redis unavailable — caching is disabled` | Local Redis not running | Optional — app still works uncached. Run `docker run -p 6379:6379 redis:7` to enable caching. |
| Model-service `POST /extract-items` returns 413 | Upload >10 MB total | Pre-resize images to ≤1024 px client-side (see `browser-image-compression` use in the frontend). |

---

## API Highlights

- `GET /api/locations/nearby?lat=&lng=&radius_km=` — nearby eco-shops, sorted by distance.
- `GET /api/locations/details/{place_id}` — place detail (cached 24 h).
- `POST /api/advisor/chat` — sustainability Q&A.
- `GET /api/brands/search?q=` — brand sustainability lookup.
- `POST /extract-items` (model service) — multipart image upload returning category, subcategory, and a transparent preview image.

---

## Privacy

- The digital wardrobe never leaves the browser. Images are processed transiently by the classification service and the resulting preview/metadata are persisted only in IndexedDB.
- No login or user accounts are required.
- Clearing browser storage clears the wardrobe.
