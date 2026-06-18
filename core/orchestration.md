# Orchestration — Execution Lifecycle

This document defines the **step-by-step lifecycle** the orchestrator (`SKILL.md`)
follows for every feature request. It is the runtime contract; `SKILL.md` is the
entrypoint, this file is the procedure.

---

## Lifecycle Overview

```
prompt
  → 0. Activation Gate            (planning-only + trigger phrase; else ABORT)
  → 1. Context Inference
  → 2. Semantic Activation        (see core/semantic_activation.md)
  → 3. Dynamic Rule Retrieval     (read only activated files)
  → 4. Threat Modeling
  → 5. Rule Selection
  → 6. Conflict Resolution        (see core/conflict_resolution.md)
  → 7. Override Handling
  → 8. Output Generation          (core/output_schema.json)
```

---

## 0. Activation Gate (run first)
This skill is **planning-only and generic** (not industry-specific). Engage ONLY
when **both** hold: (a) a feature/system is being **planned/designed before
implementation**, and (b) the request contains a **security-planning trigger
phrase** (or close paraphrase) per `skill_activation_gate` in
`core/activation_logic.json`. The skill MUST NOT run during code writing,
debugging, refactoring, or UI/UX-only work. If the gate does not pass, stay
dormant — read nothing further and produce no blueprint. (See Stage 0 in
`core/semantic_activation.md`.)

## 1. Context Inference
Extract from the request, without inventing facts:
- **Intent** — what the feature does.
- **Data types** — PII, credentials, financial, health, biometric, none.
- **Actors** — user, admin, system, third party, anonymous.
- **Interactions** — web UI, API, mobile, AI/LLM, agentic, MCP.
- **Trust boundaries** — where untrusted input crosses into trusted code.

**Never assume — always validate facts.** Do not invent the feature's purpose,
its actors, the data it touches, or existing controls. If what the feature/app
actually does is unclear, or any security-relevant fact is missing and cannot be
safely derived from the request, you MUST ask the user clarifying questions via
`INSUFFICIENT_INPUT` (the `clarification_required` array is how questions are
posed to the user) rather than guessing. Any assumption you do make MUST be
minimal and listed explicitly in the output's `assumptions`.

## 2. Semantic Activation
Run the hybrid activation model in `core/semantic_activation.md` against
`meta/trigger_map.json` and `core/activation_logic.json` to produce the set of
**activated domains and compliance packs** with confidence scores. Only files
above the activation threshold are loaded.

## 3. Dynamic Rule Retrieval
Always load first (non-negotiable):
1. `common/common-considerations.md`
2. `meta/rule_index.json`
3. `core/output_schema.json`

Then load only the files activated in step 2 (domain rule packs, compliance
packs, and category-specific `cwe/` files). Do **not** load packs that were not
activated — this keeps token usage bounded (lazy loading).

## 4. Threat Modeling
For each activated area, derive realistic threats. Each threat MUST include:
- exploitation path,
- attacker capability required,
- business impact,
- technical impact (Confidentiality / Integrity / Availability).
Threats are grounded in the rules retrieved — not generic.

## 5. Rule Selection
- Apply only contextually relevant rules.
- Extract the **exact `rule_id`** and source file for every applied rule.
- Common Considerations are ALWAYS applied regardless of context.
- Output with zero selected rules is INVALID.

## 6. Conflict Resolution
When two rules conflict, apply `core/conflict_resolution.md`
(Most-Restrictive-Control wins; documented precedence order).

## 7. Override Handling
If the user explicitly requests a weaker control (e.g. "no MFA"):
- still flag it as an anti-pattern,
- still include its threat impact,
- record it under `design_constraints` as a `user-approved exception`.
Never silently honor a downgrade.

**Non-overridable controls:** COM-032 (encryption at rest), COM-033 (TLS 1.3 +
strict HTTPS), COM-001 (no sensitive data in localStorage), COM-002 (secure
cookie attributes), COM-036 (server-side validation always present), COM-038
(passwords hashed, never encrypted), COM-040 (JWT signature verification), COM-044
(no secrets/flags in API responses), COM-045 (server-side access-state enforcement),
and COM-051 (multi-tenant isolation) CANNOT be overridden. Refuse the downgrade,
keep the control, and record the request as a rejected anti-pattern (see
`core/conflict_resolution.md`).

## 8. Output Generation
Emit JSON strictly matching `core/output_schema.json`. No conversational text
outside the JSON. Every rule reference carries its `rule_id` and `source`.

---

## Failure Handling
On insufficient input, output exactly:
```json
{ "error": "INSUFFICIENT_INPUT", "clarification_required": ["..."] }
```

## Performance Notes
- **Selective activation** — never read a pack that wasn't activated.
- **Index-first** — use `meta/rule_index.json` to locate rules before opening files.
- **Order of loads** — core baseline files first, then activated packs, then
  category-specific CWE files last (smallest, most targeted).
