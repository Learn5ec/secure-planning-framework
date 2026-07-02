# Semantic Activation Engine

The activation engine decides **which domain rule packs to load** for a given
request. The skill is always-on — Stage 0 has been removed. Backing data lives
in `meta/trigger_map.json` and `core/activation_logic.json`.

---

## Activation Model (v2.0 — Always-On with Opt-Out)

### Opt-Out Check (replaces Stage 0)
Before any other work, check for an explicit opt-out signal. If the request
contains any of the following phrases (or a close equivalent), remain dormant:

- `"do not use spf skill"`
- `"skip spf"`
- `"no secure planning"`
- `"disable spf"` / `"spf off"`

If opt-out is detected → **ABORT**: do not read rule packs, do not emit a blueprint.

For all other requests, proceed immediately to domain activation. No keyword gate,
no planning-intent check, no surface detection required to activate the skill.

---

### Stage 1 — Keyword Bootstrap
Scan the request for trigger keywords defined in `meta/trigger_map.json`. Each
match adds the corresponding domain to the candidate activation set. This is
cheap and catches explicit signals ("API", "login", "Flutter", "RAG").

### Stage 2 — Semantic Refinement
Interpret intent beyond literal keywords. A request can activate a pack with no
keyword match:
- "let users reset their password by email" → authentication + email + tokens,
  even though "auth" never appears.
- "an assistant that books flights for the user" → agentic AI + LLM governance.

Semantic refinement may **add** activations the keyword stage missed; it should
not silently remove a keyword-triggered activation (err toward inclusion).

**Activation rule (replaces numeric scoring):** Activate domain pack D if any
trigger keyword matches **OR** the model judges D clearly relevant to the request.
No score threshold — deterministic inclusion.

---

## Always-On Loads (ignore activation; load for every request)
- `common/common-considerations.md`
- `meta/rule_index.json`
- `core/output_schema.json`

---

## Compliance Packs — DISABLED

> **DPDPA, GDPR, HIPAA, PCI-DSS, SOC2, EU AI Act, ISO 27001 are NOT activated.**
> Compliance enforcement is disabled pending org-wide implementation decision.
> Do NOT load `compliance/dpdp/` files or any compliance pack in any blueprint
> until this is explicitly re-enabled.
>
> Previous behaviour: DPDP was force-activated on any personal data and failed
> safe when jurisdiction was unknown. This behaviour is **suspended**.

---

## What Gets Inferred
The engine infers, per request:
- **Domains** — web, api, mobile, ai_agentic, ai_llm, mcp.
- **Risk posture** — drives `risk_classification` in the output.

---

## Output of Activation
A resolved activation set, e.g.:
```json
{
  "domains": ["web", "api"],
  "compliance": [],
  "cwe_categories": ["access_control", "authentication"],
  "files_to_load": [
    "domains/web/web_owasp_top10_2025.md",
    "domains/api/owasp_api_top10_2023.md"
  ]
}
```
This set is handed to `orchestration.md` step 3 (Dynamic Rule Retrieval).
