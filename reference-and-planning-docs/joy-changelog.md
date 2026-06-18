# Joy — Review Changelog

Changes made in response to Joy's review comments. Date: 2026-06-18.

---

## [1] Skill too large — remove `.git`, `.docker`, and other cloned-repo cruft

**Done.** Removed VCS/CI/editor/build scaffolding left over from the cloned OWASP
repos under `data/`:

- Directories: nested `.git`, `.github`, `.vscode`, `.devcontainer`, `tools/`
- Files: `.gitignore`, `.gitattributes`, `.dockerignore`, `.gitbook.yaml`,
  `book.json`, `.markdownlint*`, `.markdownlinkcheck.json`, `CHANGELOG.md`,
  `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `PULL_REQUEST_TEMPLATE.md`,
  `release.yml`, `LANGUAGE-METADATA`, `FUNDING.yml`

Preserved: `License.md` files (attribution), and the root `.github/copilot-instructions.md` (our VS Code adapter — not cruft).

> **Important note for the team:** the cruft was small. The skill's real weight is
> `data/` itself — **~72 MB of 73 MB** — almost entirely `data/mastg/` (60 MB
> MASTG gitbook) and `data/LLM-AI/` (9 MB of PDFs). `data/` is a **temporary
> authoring staging area** (raw OWASP sources awaiting conversion); it should be
> **excluded from the distributed/loaded skill**. Per the owner's instruction it
> is **not deleted here** — it will be removed manually. Recommended: delete or
> move `data/` out of the skill root before distribution, which takes the skill
> from ~72 MB to well under 1 MB.

## [2] Make it generic, not industry-specific

**Done.** Removed the entire industry layer; the skill is now generic and applies
to all solution modules.

- Deleted the `industries/` directory (finance + insurance full overlays, the
  10 stubs, and `_TEMPLATE.md`).
- De-wired all references:
  - `core/activation_logic.json` — removed the `industries` block.
  - `meta/trigger_map.json` — removed the `industries` triggers.
  - `meta/version_manifest.json` — removed the `industry_overlays` block.
  - `core/conflict_resolution.md` — removed the `IND-*` precedence tier and the
    "Industry Overlay Rule" section (precedence is now Compliance → Common →
    Domain → CWE).
  - `core/semantic_activation.md` — removed industry inference + example.
  - `core/orchestration.md` — removed "industry overlays" from steps 2 and 3.
  - `delivery/mcp/README.md` — removed `industries/` from the load list.

The generic rule packs are unchanged and remain the core: `common/` (always-on
baseline), `domains/`, `compliance/`, `cwe/`.

## [3] Planning-only + explicit trigger phrases (avoid firing on every plan)

**Done.** Added a two-condition **Activation Gate** so the skill stays dormant
unless explicitly invoked for security planning.

- **Planning-only:** the skill MUST NOT run during code writing, debugging,
  refactoring, or UI/UX-only work — only when a feature/system is being
  planned/designed *before* implementation.
- **Explicit trigger phrases:** it engages only when the request contains a
  security-planning phrase (or close paraphrase) such as: `secure plan`,
  `security plan`, `plan securely`, `secure design`, `threat model`,
  `security requirements`, `security blueprint`, `secure planning framework`.
- **Both conditions required**; otherwise the skill reads no rule packs and emits
  no blueprint (keeps execution time + token usage low).

Wired in:
- `core/activation_logic.json` — new `skill_activation_gate` object
  (`phase: planning_only`, `trigger_phrases`, `must_not_run_during`, `require_both`).
- `core/semantic_activation.md` — new **Stage 0 — Skill Activation Gate** (runs
  before keyword/semantic stages, can abort).
- `core/orchestration.md` — new **Step 0 — Activation Gate** in the lifecycle.
- `SKILL.md` — tightened the frontmatter `description` (planning-only + trigger
  phrases + explicit "do NOT use during coding") and added an **Activation Gate**
  section at the top of the body.
- Delivery adapters (`.cursorrules`, `.windsurfrules`,
  `.github/copilot-instructions.md`) — updated so each tool only routes to the
  skill on an explicit security-planning request, not on every plan/design.

---

## Validation after changes
- `industries/` removed; **no residual** `IND-*` / industry-overlay references
  anywhere (outside `data/` and this docs folder).
- Activation gate present in `SKILL.md`, `orchestration.md`,
  `semantic_activation.md`, and `activation_logic.json`.
- All JSON files valid.

## Note on REVIEW-GUIDE.md
`REVIEW-GUIDE.md` was written before these changes and still depicts the
`industries/` layer in its architecture/summary. It is retained as a
point-in-time review artifact; this changelog supersedes it on points [1]–[3].
