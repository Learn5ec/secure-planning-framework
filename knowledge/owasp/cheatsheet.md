# Knowledge Cheat-Sheet — OWASP (Web + API)

> **Purpose:** Token-efficient quick reference distilled from the raw sources in
> `knowledge/ai/raw/` and the authoritative rule packs in `knowledge/`. This is a *reference*,
> not an authoritative rule pack — when enforcing, cite the `rule_id` from
> `knowledge/owasp/web_owasp_top10_2025.md` or `knowledge/api-top10/owasp_api_top10_2023.md`.

---

## OWASP Top 10:2025 (Web) — at a glance

| Code | Risk | One-line control | Rule ID |
|------|------|------------------|---------|
| A01 | Broken Access Control | Server-side checks, default-deny, least privilege | OWASP-A01-001/002 |
| A02 | Security Misconfiguration | Hardened config, no defaults/debug, secure headers | OWASP-A02-001 |
| A03 | Software Supply Chain Failures | Track + scan + verify dependencies (SBOM) | OWASP-A03-001 |
| A04 | Cryptographic Failures | Strong crypto in transit & at rest, key mgmt | OWASP-A04-001 |
| A05 | Injection | Validate + sanitize + parameterize all input | OWASP-A05-001 |
| A06 | Insecure Design | Threat model critical flows before build | OWASP-A06-001 |
| A07 | Authentication Failures | Standards-based auth, MFA, brute-force protection | OWASP-A07-001 |
| A08 | Software & Data Integrity | Verify updates/artifacts/inputs (signatures) | OWASP-A08-001 |
| A09 | Logging & Alerting Failures | Log critical events, alert on anomalies | OWASP-A09-001 |
| A10 | Mishandling Exceptional Conditions | Fail closed, no internal detail leakage | OWASP-A10-001 |

## OWASP API Top 10:2023 — at a glance

| Code | Risk | One-line control | Rule ID |
|------|------|------------------|---------|
| API1 | Broken Object Level Authz (BOLA/IDOR) | Authorize every object reference | API-001 |
| API2 | Broken Authentication | Secure tokens, MFA, brute-force protection | API-002 |
| API3 | Broken Object Property Level Authz | Restrict fields; never over-expose | API-003 |
| API4 | Unrestricted Resource Consumption | Rate limits, quotas, payload caps | API-004 |
| API5 | Broken Function Level Authz (BFLA) | Enforce role/permission on every endpoint | API-005 |
| API6 | Unrestricted Access to Sensitive Business Flows | Bot/abuse protection on high-value flows | API-006 |
| API7 | SSRF | Validate & allowlist outbound URLs | API-007 |
| API8 | Security Misconfiguration | Harden config, disable debug, restrict methods | API-008 |
| API9 | Improper Inventory Management | Inventory all versions; retire deprecated endpoints | API-009 |
| API10 | Unsafe Consumption of APIs | Treat 3rd-party responses as untrusted | API-010 |

---

## Fast decision hooks
- **Any object accessed by ID?** → BOLA/IDOR check (API-001, OWASP-A01-001, CWE-639).
- **Any user input into a query/command/template?** → injection (OWASP-A05-001, CWE-79/89/78).
- **Any login/session?** → auth + session (OWASP-A07-001, CWE-287/384/613).
- **Any outbound fetch of a user-supplied URL?** → SSRF (API-007, CWE-918).
- **Any sensitive data stored/sent?** → crypto + data protection (OWASP-A04-001, CWE-200/522).

## Cross-references
- Common baseline: `instructions/common_considerations.md` (always applied).
- CWE depth: `knowledge/cwe/<category>.md`.
- Compliance: DPDPA is currently disabled pending org decision; do not reference `mappings/compliance/dpdp/`.
