<!--
WearImpact PR template — keep it short, copy CLAUDE.md commit conventions.
Use Conventional Commits style scope in the PR title (feat/fix/chore/docs/refactor/test).
-->

## Scope

<!-- One line: which layer(s)? frontend / backend / model-service / docs / infra -->

## Why

<!-- The problem this PR solves, or the user-visible improvement. Link the issue if applicable. -->

## What changed

<!-- 3–5 bullet points. File-level granularity is fine; no need to repeat the diff. -->

-
-
-

## Test plan

<!-- How a reviewer can verify. Include the exact commands or steps. -->

- [ ] Local: `cd frontend && npm run dev` — feature works end-to-end in browser
- [ ] Local: `cd backend && pytest` — existing tests still pass
- [ ] Manual: <add your scenario>

## Deploy risk

<!-- Pick ONE and explain in one sentence if non-zero. -->

- [ ] **No deploy impact** — pure docs/tests/dev tooling
- [ ] **Behaviour-preserving** — production behaviour byte-equivalent to current
- [ ] **Behaviour change** — describe what changes for end users, how to roll back

## Checklist

- [ ] No `.env` / secrets staged
- [ ] No `Co-Authored-By: Claude` trailer (per CLAUDE.md)
- [ ] Branch is `develop` (or explicitly named by the owner)
