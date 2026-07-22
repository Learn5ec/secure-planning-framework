# Orchestration — Execution Lifecycle

This document defines the **step-by-step lifecycle** the orchestrator (`SKILL.md`)
follows for every feature request. It is the runtime contract; `SKILL.md` is the
entrypoint, this file is the procedure.

---

## Lifecycle Overview

```
prompt
  → 0. Opt-Out Check               (ABORT only if user says "Do not use SPF skill")
  → 1. Context Inference
  → 2. Semantic Activation        (see instructions/semantic_activation.md)
  → 3. Dynamic Rule Retrieval     (read only activated files)
  → 4. Threat Modeling
  → 5. Rule Selection
  → 6. Conflict Resolution        (see instructions/conflict_resolution.md)
  → 7. Override Handling
  → 8. Output Generation          (templates/output_schema.json)
```

---

## 0. Opt-Out Check (run first)
This skill is **always-on** — it fires by default on every planning and
development task. The **only** reason to abort is an explicit opt-out from the
user. If the request contains any of the following phrases (or a close
equivalent), stay dormant — read nothing further and produce no blueprint:
- `"do not use spf skill"` / `"skip spf"` / `"no secure planning"` / `"spf off"`

For all other requests, proceed immediately to step 1.

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
Run the hybrid activation model in `instructions/semantic_activation.md` against
`meta/trigger_map.json` and `templates/activation_logic.json` to produce the set of
**activated domains and compliance packs** with confidence scores. Only files
above the activation threshold are loaded.

## 3. Dynamic Rule Retrieval
Always load first (non-negotiable):
1. `instructions/slim_core.md` — the 10 CRITICAL always-applicable baseline rules.
2. `meta/rule_index.json`
3. `templates/output_schema.json`

**High-risk upgrade:** If the feature meets ANY criterion in `templates/activation_logic.json high_risk_criteria` (credentials/financial/health/biometric data, multi-agent, admin paths, payment/banking/healthcare systems), ALSO load `instructions/common_considerations.md` (full 58-rule baseline) and the `_extended` variant of each activated AI/MCP pack.

For all other requests, `instructions/slim_core.md` is sufficient — do NOT load `instructions/common_considerations.md` to keep token usage bounded.

Then load only the domain files activated in step 2. Do **not** load packs that were not
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
When two rules conflict, apply `instructions/conflict_resolution.md`
(Most-Restrictive-Control wins; documented precedence order).

## 7. Override Handling
If the user explicitly requests a weaker control (e.g. "no MFA"):
- still flag it as an anti-pattern,
- still include its threat impact,
- record it under `design_constraints` as a `user-approved exception`.
Never silently honor a downgrade.

**Non-overridable controls:** COM-032 (encryption at rest), COM-033 (TLS 1.2 minimum
floor + strict HTTPS — no plain HTTP, no SSL/TLS≤1.1), COM-001 (no sensitive data in
localStorage), COM-002 (secure cookie attributes), COM-036 (server-side validation always
present when a backend exists), COM-038 (passwords hashed, never encrypted), COM-040
(JWT signature verification), COM-044 (no secrets/flags in API responses), COM-045
(server-side access-state enforcement), and COM-051 (multi-tenant isolation) CANNOT be
overridden. Refuse the downgrade, keep the control, and record the request as a rejected
anti-pattern (see `core/conflict_resolution.md`).

## 8. Output Generation
Emit structured markdown containing the JSON blueprint (matching `templates/output_schema.json`)
within a ` ```json ``` ` code block, followed by a short conversational summary for the
developer. Every rule reference carries its `rule_id` and `source` file.

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
