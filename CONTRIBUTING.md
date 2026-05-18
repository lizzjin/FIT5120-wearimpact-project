# Contributing to WearImpact

Welcome. This guide is the short version — the authoritative project conventions live in [CLAUDE.md](CLAUDE.md). Read that first; this file just adds the human-friendly contributor entry points.

## Project layout (TL;DR)

| Layer | Path | Stack | Deploy target |
|---|---|---|---|
| Frontend | [frontend/](frontend/) | Vue 3 + Vite + Tailwind v4 | Vercel |
| Backend (Epic 1/3/4 APIs) | [backend/](backend/) | FastAPI + Redis | Railway |
| Model service (image classification) | [FIT5120-Classification-Mod/](FIT5120-Classification-Mod/) | Flask + CLIP + rembg | HuggingFace Space |

The three layers are independent deployments — see [CLAUDE.md](CLAUDE.md#e31-architecture-overview) for the architectural rationale.

## Running locally

### Frontend
```bash
cd frontend
npm install
npm run dev          # http://localhost:5173
npm run build        # production bundle
```

Requires a `frontend/.env.local` with the env vars listed in the root [README.md](README.md#environment-variables-checklist). Ask the project owner if you don't have one — these are not in the repo for security reasons.

### Backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # PowerShell on Windows
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
uvicorn app.main:app --reload     # http://localhost:8000
pytest                            # run the test suite
```

Redis is optional locally — the backend gracefully runs without it (cache disabled, advisor/place-details work uncached).

### Model service
The HuggingFace Space deployment at `https://lizzjin-wearimpact-classifier.hf.space` is the canonical instance. **You do not need to run it locally** for normal frontend work. If you must, see [FIT5120-Classification-Mod/](FIT5120-Classification-Mod/) and run with `gunicorn -w 1 --threads 4 app:app` (single worker is intentional, see [CLAUDE.md](CLAUDE.md#e34-operational-notes--known-behaviors)).

## Branch & commit policy

- **Default branch:** `develop`. Never push to `main` directly.
- **Commit style:** Conventional Commits with scope, e.g. `feat(ui): add wardrobe filter`, `fix(map): correct radius clamp`. Subject ≤ 70 chars.
- **No AI co-author trailers.** Do not add `Co-Authored-By: Claude ...` or mention the assistant in commit bodies. See [CLAUDE.md](CLAUDE.md#co-author-trailer).
- **Staging:** prefer `git add <explicit paths>` over `git add -A` so accidental docs/secrets don't sneak in.

## Pull requests

Open PRs against `develop`. The [PR template](.github/PULL_REQUEST_TEMPLATE.md) walks you through:

1. **Scope** — which layer(s) does this touch
2. **Why** — the problem solved
3. **What changed** — short bullet list
4. **Test plan** — exact verification steps
5. **Deploy risk** — pick one of three categories

PRs are auto-routed to the owner via [CODEOWNERS](.github/CODEOWNERS). All reviews are async.

## Code quality

This project does not yet enforce linters in CI, but local tooling is provided:

- **Frontend:** `npm run lint` (ESLint) / `npm run format` (Prettier). Warnings only — not blocking.
- **Backend:** `ruff check .` and `ruff format .` (configured in [backend/pyproject.toml](backend/pyproject.toml)).
- **Pre-commit hooks** (optional, opt-in):
  - **Backend**: `pip install pre-commit && pre-commit install` — installs ruff + small safety checks from [`.pre-commit-config.yaml`](.pre-commit-config.yaml).
  - **Frontend**: `cd frontend && npm install && npm run hooks:enable` — installs husky deps and points git's `core.hooksPath` at `frontend/.husky/`. Run once per clone; disable later with `git config --local --unset core.hooksPath`.
  - Neither hook runs in CI (Vercel / GitHub Actions); they are purely local sanity gates.

Tests:
- Backend: `cd backend && pytest` — Epic 3 advisor, wardrobe audit, security, and Epic 1 location endpoints are covered.
- Frontend / model service: manual smoke tests for now (see [`FIT5120-Classification-Mod/test.html`](FIT5120-Classification-Mod/test.html)).

## Reporting bugs / requesting features

Open a GitHub issue describing:
- Steps to reproduce
- Expected vs actual behaviour
- Which layer(s) are involved
- Browser / OS / device (for frontend issues)

## What NOT to commit

- `.env`, `.env.local`, or any file containing secrets, tokens, or API keys
- `node_modules/`, `dist/`, `__pycache__/`, build artefacts
- Large binaries (videos, model weights, PDFs) — link from issues/PRs instead
- AI-assistant working notes (`claude.md`, `DESIGN.md`, `openspec/`, etc.)

See [.gitignore](.gitignore) for the full exclusion list.
