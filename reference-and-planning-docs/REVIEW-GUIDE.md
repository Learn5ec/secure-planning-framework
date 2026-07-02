# Secure Planning Framework — Change Summary & Review Guide

> **NOTE: This guide reflects the initial v2.0 transition. It is superseded by `improvement-plan.md`.**
> A consolidated record of what was added/changed in this iteration, the system
> architecture, and a departmental split for review so the work can be validated
> quickly and consistently rather than by a single person.

---

## Part A — Change Summary

### 1. Cross-tool compatibility (made it a real, discoverable skill)

- Added **YAML frontmatter** (`name` + trigger-rich `description`) to `SKILL.md`.
- Moved `core/SKILL.md` → repo-root `SKILL.md` so its root-relative paths resolve.
- Registered for **Claude Code**: symlinked the repo into `~/.claude/skills/secure-planning-framework`.
- Built **delivery adapters** at each tool's canonical location:
  - **Cursor** — `.cursorrules` (fixed pointer)
  - **Windsurf** — `.windsurfrules` (new)
  - **VS Code / Copilot** — `.github/copilot-instructions.md` (new)
  - `delivery/` README + per-tool docs (claude, cursor, windsurf, vscode + planned mcp/npm/cli)

### 2. Filled the empty layers

- **Engine (`core/`)** — wrote `orchestration.md` (8-step lifecycle), `semantic_activation.md` (hybrid activation + scoring), `conflict_resolution.md` (most-restrictive + precedence + non-overridable list), `activation_logic.json`.
- **`meta/`** — `trigger_map.json`, `severity_map.json` (INFO→CRITICAL + escalation), `tag_index.json`, `version_manifest.json`.
- **`knowledge/`** — full **owasp** cheat-sheet + `ai` / `mobile` / `compliance` stubs (curated from `data/`).

> _Note: an `industries/` overlay layer was initially built but **removed in review**._

### 3. Reconciled SKILL.md edits into the engine

- **DPDP scoped to Indian data principals** (with fail-safe when jurisdiction unknown) across `semantic_activation.md` + `activation_logic.json`.
- **"Never assume — always ask"** mandate added to `orchestration.md` (questions via `INSUFFICIENT_INPUT`).

### 4. New baseline security rules (`COM-*`) from findings & guidance

**Crypto / transport / storage (non-negotiable):**

- `COM-032` Encryption at rest · `COM-033` TLS 1.3 + strict HTTPS · strengthened `COM-001` / `COM-002`
- `COM-038` Password/secret **hashing** (Argon2id) — and amended `COM-032` so passwords are hashed, not encrypted

**Input/output handling:**

- `COM-034` Type-specific field validation (generalized to *every* field, i18n-flexible)
- `COM-035` Context-aware output encoding
- `COM-036` Layered validation FE+Mobile+BE (server-side authoritative, non-overridable)
- `COM-037` Secure file-upload hardening

**16 checks distilled from 374 Jira vulnerabilities (`COM-039` → `COM-054`):**

| Theme | Rules |
|-------|-------|
| Session / token | 039 lifecycle, 040 JWT validation, 053 no-cache |
| Auth flows | 041 password reset, 042 enumeration, 043 lockout/bot, 048 OTP |
| Data exposure | 044 response minimization, 046 orphaned objects, 052 email auth |
| Access control | 045 access-state enforcement, 051 multi-tenant isolation |
| Business logic | 047 entitlements/pricing/quotas |
| Config / supply chain | 049 patch management, 050 disable non-prod surfaces, 054 IP-header trust |

- Strengthened `COM-020` (no auto-login before verification).

### 5. Generic design + planning-only activation gate (revised per review)

- **Removed the `industries/` layer** (finance, insurance, 10 stubs, template) — the skill is now **generic** and applies to all solution modules. Conflict-resolution precedence is now: Compliance → Common → Domain → CWE.
- **Added a planning-only Activation Gate** — the skill engages only when **both** (a) a feature is being planned/designed *before* implementation, and (b) the request carries an explicit security-planning trigger phrase (e.g. "secure plan", "threat model", "security requirements"). It stays dormant during coding, debugging, refactoring, and UI/UX-only work. Wired into `SKILL.md`, `core/semantic_activation.md` (Stage 0), `core/orchestration.md` (Step 0), `core/activation_logic.json` (`skill_activation_gate`), and all delivery adapters.
- _(See `joy-changelog.md` for full detail.)_

### 6. Engine policy: non-overridable controls

A hard-blocker class added to `conflict_resolution.md` + `orchestration.md` (cannot be waived by user override):

> `COM-001`, `COM-002`, `COM-032`, `COM-033`, `COM-036`, `COM-038`, `COM-040`, `COM-044`, `COM-045`, `COM-051`

### 7. Consistency / wiring

- All new rules indexed in `rule_index.json` + `tag_index.json`.
- Fixed 3 pre-existing **orphaned** rules (`COM-005`, `COM-023`, `COM-028`) that were never indexed.
- Full audit: no duplicates, no dangling refs, engine files agree, all JSON valid.

### Net state

| Dimension | Before | After |
|-----------|--------|-------|
| COM baseline | 31 rules | **54 rules** |
| Scope | (was industry-specific) | **generic — no industry layer** |
| Activation | fires on any plan | **planning-only + trigger-gated** |
| Engine + meta | empty | **fully populated** |
| Adapters | Cursor-only | **Claude Code + Cursor + Windsurf + VS Code** |
| Non-overridable controls | 0 | **10** |

_...and much more._

---

## Part B — Architecture (for reviewers)

It's a **prompt-driven, file-based "dynamic skill."** There is no runtime binary —
the model (Claude Code / Cursor / etc.) reads `SKILL.md`, then selectively reads
rule files based on the feature being planned, and emits a structured security
blueprint. Think of it as layers:

```text
Layer 0  DELIVERY ADAPTERS    .cursorrules · .windsurfrules · .github/copilot-instructions.md
         (how each tool        ~/.claude/skills symlink · delivery/ docs
          discovers the skill)
                │
Layer 1  ORCHESTRATOR         SKILL.md (root, YAML frontmatter)  ← entrypoint + persona
                │
Layer 2  ENGINE  (core/)      orchestration.md        (8-step lifecycle)
                              semantic_activation.md  (hybrid keyword+semantic, scoring)
                              conflict_resolution.md  (most-restrictive + non-overridable)
                              output_schema.json      (strict JSON contract)
                │
Layer 3  ROUTING META (meta/) activation_logic.json · trigger_map.json
                              rule_index.json · tag_index.json · severity_map.json
                │
Layer 4  RULE PACKS           common/      (54 COM-* always-on baseline)
                              domains/     (web, api, mobile, ai, mcp)
                              compliance/  (dpdp)   cwe/ (curated)
                │
Layer 5  REFERENCE            knowledge/ (cheat-sheets)  ·  data/ (raw sources)
```

**Execution flow:**

```text
prompt
  → activation gate (planning-only + trigger phrase; else ABORT — stay dormant)
  → context inference
  → semantic activation (which packs?)
  → dynamic retrieval (always-load common/ + activated packs via rule_index)
  → threat model
  → conflict resolution (non-overridable controls win)
  → emit output_schema.json blueprint for review
```

**Invariants reviewers should keep in mind:**

1. The skill is **planning-only** and **gated** — it does nothing unless a security plan/design is explicitly requested before implementation.
2. `common/` is **always** applied when the skill runs.
3. Lower-precedence rules may only **strengthen**, never weaken — and 10 controls are flat-out **non-overridable**.

---

## Part C — Who Reviews What

> A single-person review of the whole skill is hard. Splitting by departmental
> expertise is faster and more consistent.

| Reviewer | Primary area | Files / focus | Why them |
|----------|--------------|---------------|----------|
| **Tech Lead** — *Aiyaj* | Architecture & glue | `core/orchestration.md`, `activation_logic.json` (incl. `skill_activation_gate`), `conflict_resolution.md`, `meta/*`, `delivery/`, `version_manifest.json`, cross-tool compatibility | Owns coherence: do the lifecycle, the planning-only gate, routing, precedence, and packaging hang together and scale? |
| **AI team member** — *Harnish* | AI/LLM packs + the "dynamic skill" design | `domains/ai/agentic_ai_rules.md`, `domains/ai/llm_governance_rules.md`, `domains/mcp/`, `knowledge/ai/`, `semantic_activation.md`, `SKILL.md` persona/prompt quality | The activation engine *is* model inference; AI rules + prompt design are their wheelhouse. |
| **Senior Fullstack #1** — *Joy* | Web + API rule correctness | `domains/web/`, `domains/api/`, `knowledge/owasp/`, web/session COM rules (cookies, headers, CORS, CSRF, caching) | Validates the rules match real FE/BE practice and aren't over/under-strict. |
| **Senior Python dev** — *Maulik* | Backend + data integrity | `output_schema.json` + all `meta/*.json` (structural/index correctness, no dangling refs), injection/crypto/hashing rules (`COM-032`/`COM-038`), API auth rules; future engine tooling/scripts | Strong on schema validity, backend auth/crypto, and the JSON wiring everything depends on. |
| **Senior Fullstack + Security** ⭐ — *Vicky* | Security content authority | `common/common-considerations.md` (all 54 COM rules), the Jira-derived `COM-039`→`COM-054`, `conflict_resolution.md` non-overridable list, `severity_map.json`, `cwe/`, threat-modeling logic | The adversarial/correctness reviewer — is the security advice actually sound, complete, and well-prioritized? |
| **Flutter member** — *Viraj* | Mobile pack | `domains/mobile/owasp_masvs.md`, `knowledge/mobile/`, mobile specifics (keystore, deep links, cert pinning, minSDK, backup flag), how `COM-036` layered validation applies on-device | Only person who can judge mobile/MASVS accuracy and Flutter applicability. |

### Shared / needs a second set of eyes

- **`compliance/dpdp/`** → *Vicky* reviews the technical controls, but **flag for legal/DPO validation** — DPDP wording and the Indian-data scoping are legal calls, not engineering ones.
- **`common/` baseline** → because it's always-on, **both fullstack reviewers** (*Joy* + *Vicky*) should sanity-check it doesn't impose impractical constraints on their stacks.


