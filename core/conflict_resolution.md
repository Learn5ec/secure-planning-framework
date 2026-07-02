# Conflict Resolution Protocol

When two or more activated rules impose incompatible requirements on the same
control, the orchestrator MUST resolve the conflict deterministically using the
rules below. Conflicts are never resolved by picking the weaker option.

---

## Core Principle: Most Restrictive Control Wins
When rules conflict, apply the control that **reduces risk the most**, even if it
is more expensive or more inconvenient. Security defaults to the stricter side.

> **Availability Escape Hatch:** Most restrictive applies to controls that reduce risk WITHOUT trading off availability. Availability-affecting controls (lockout, rate limits, session lifetimes) pick the strictest value that does not create a self-DoS.

Examples:
- Rule A: "session expires in 24h", Rule B: "session expires in 30m" → **30m**.
- Rule A: "encrypt at rest recommended", Rule B: "encrypt at rest required" → **required**.
- Rule A: "validate input", Rule B: "validate + parameterize" → **validate + parameterize**.

---

## Precedence Order (tie-breaker when "most restrictive" is ambiguous)

When two rules are equally restrictive or the comparison is not on a numeric
scale, resolve by source precedence (highest wins):

1. **Compliance** (DPDP / regulatory) — legal obligations cannot be relaxed.
2. **Common Considerations** (`COM-*`) — non-negotiable baseline.
3. **Domain rules** (OWASP / MASVS / API / AI / MCP) for the activated domain.
4. **CWE mappings** — augment validation; never override the above.

A lower-precedence rule may only **add** strictness, never remove it.

---

## Non-Overridable Controls (no exception permitted)
The following baseline controls are **non-negotiable** and CANNOT be weakened by a
user override under any circumstances. If a user requests their relaxation, refuse
the downgrade, keep the control, and note the request as a rejected anti-pattern:

- **COM-032** — Encryption at rest (strong algorithms, managed keys).
- **COM-033** — Encryption in transit: TLS 1.3 + strict HTTPS (no plain HTTP, no legacy TLS).
- **COM-001** — No sensitive data/tokens in localStorage/sessionStorage.
- **COM-002** — Secure cookie attributes (HttpOnly, Secure, SameSite, scoped Domain/Path).
- **COM-036** — Server-side validation/sanitization must always be present; client-only validation is prohibited.
- **COM-038** — Passwords/secret verifiers must be hashed (Argon2id/bcrypt), never encrypted or plaintext.
- **COM-040** — JWT/token signatures must be verified; `alg:none`/algorithm-confusion rejected.
- **COM-044** — Secrets, hashes, OTPs, tokens, and trust-bearing flags must never be returned in API responses.
- **COM-045** — Revocation/suspension/deletion must be enforced server-side immediately across all access paths.
- **COM-051** — Multi-tenant/data-segregation isolation must be enforced server-side; cross-tenant access denied.

## User Override Exception
For controls **other than** the non-overridable list above, a user-approved
exception (see `orchestration.md` §7) is the **only** mechanism that allows a
control to be weakened, and even then:
- the stricter rule is still listed,
- the downgrade is recorded as a `user-approved exception` in `design_constraints`,
- the associated threat remains in `threat_model`,
- the weakened item is listed under `anti_patterns`.

The override is documented, never hidden.

---

## Resolution Algorithm
```
for each control with >1 applicable rule:
    if rules differ on a measurable scale (time, key length, factor count):
        choose the strictest value
    else:
        choose by precedence order above
    if a user-approved exception applies:
        record stricter rule + exception + threat (do NOT drop the rule)
```
