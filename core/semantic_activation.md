# Semantic Activation Engine

The activation engine decides **whether to run at all**, and if so **which rule
packs and compliance packs to load** for a given request. It uses a hybrid model:
a fast keyword bootstrap followed by semantic refinement. Backing data lives in
`meta/trigger_map.json` and `core/activation_logic.json`.

---

## Hybrid Activation Model

### Stage 0 — Skill Activation Gate (run first; may abort)
Before any other work, decide whether this skill should engage at all. This skill
is for **security planning/design only** and is **generic** — it is not tied to
any industry. Engage ONLY when **both** are true:

1. **Planning intent** — a feature/system is being planned or designed *before*
   implementation (not while writing, fixing, or refactoring code).
2. **A security-planning trigger phrase is present** (or a close paraphrase) — see
   `skill_activation_gate.trigger_phrases` in `core/activation_logic.json`
   (e.g. "secure plan", "plan it securely", "threat model", "security
   requirements", "secure design").

If either is missing — for example UI/UX-only work, bug fixes, code generation, or
a plain "plan the layout" with no security-planning phrase — the skill MUST stay
**dormant**: do not read rule packs and do not emit a blueprint. This prevents the
skill from firing (and burning tokens) on every plan that merely mentions a
security-adjacent word.

### Stage 1 — Keyword Bootstrap
Once the gate passes, scan the request for trigger keywords defined in
`meta/trigger_map.json`. Each match contributes to a domain/compliance candidate
set. This is cheap and catches explicit signals ("API", "login", "Flutter", "RAG").

### Stage 2 — Semantic Refinement
Interpret intent beyond literal keywords. A request can activate a pack with no
keyword match:
- "let users reset their password by email" → authentication + email + tokens,
  even though "auth" never appears.
- "store the user's Aadhaar number" → PII + DPDP, even without the word "consent".
- "an assistant that books flights for the user" → agentic AI + LLM governance.

Semantic refinement may **add** activations the keyword stage missed; it should
not silently remove a keyword-triggered activation (err toward inclusion).

---

## Confidence Scoring
Each candidate gets a score in `[0,1]`:

```
score = (0.5 * keyword_signal) + (0.5 * semantic_signal)
```

- `keyword_signal` — normalized count/strength of trigger matches.
- `semantic_signal` — model judgement that the pack is relevant to intent.

A pack is **activated** when `score >= activation_threshold` (default `0.4`,
see `core/activation_logic.json`).

---

## Always-On Activations (ignore scoring)
These load for every request regardless of score:
- `common/common-considerations.md`
- `meta/rule_index.json`
- `core/output_schema.json`

DPDP compliance is force-activated whenever personal data of **Indian data
principals (users in India)** is — or may be — involved, even at low confidence.
When residency/jurisdiction is unknown, **fail safe**: still activate DPDP and
record the residency assumption under `assumptions` (per the never-assume rule).
Do not silently skip DPDP just because jurisdiction was not stated.

---

## What Gets Inferred
The engine infers, per request:
- **Domains** — web, api, mobile, ai_agentic, ai_llm, mcp.
- **Compliance** — dpdp (extensible: gdpr, hipaa, pci_dss, soc2, iso27001).
- **Risk posture** — drives `risk_classification` in the output.

---

## Output of Activation
A resolved activation set, e.g.:
```json
{
  "domains": ["web", "api"],
  "compliance": ["dpdp"],
  "cwe_categories": ["access_control", "authentication"],
  "files_to_load": [
    "domains/web/web_owasp_top10_2025.md",
    "domains/api/owasp_api_top10_2023.md",
    "compliance/dpdp/dpdp_rules.md"
  ]
}
```
This set is handed to `orchestration.md` step 3 (Dynamic Rule Retrieval).
