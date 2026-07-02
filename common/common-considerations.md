# Common Security Considerations — Baseline Enforcement Rules

---

# Rule ID: COM-001
## Title: Prevent Storage of Sensitive Data in Local Storage

**Category:** Client-Side Security  
**Severity:** CRITICAL

### Rule
Authentication tokens and sensitive user data MUST NOT be stored in browser localStorage or sessionStorage. On web: use HttpOnly, Secure, SameSite cookies. On mobile: use platform secure storage (Keystore/Keychain). In-memory (non-persisted) access tokens are an allowed alternative.
**NON-NEGOTIABLE: the localStorage ban is not subject to user override.**

### Applies When
- Web applications using browser storage

### Validation
- Inspect storage via DevTools
- Verify tokens are stored in secure cookies instead

### Failure Impact
- Token theft via XSS

---

# Rule ID: COM-002
## Title: Enforce Secure Cookie Attributes

**Category:** Session Security  
**Severity:** CRITICAL

### Rule
All cookies carrying authentication/session/sensitive data MUST:
- Use HttpOnly flag
- Use Secure flag
- Set SameSite=Lax or Strict
- Have an explicitly scoped Domain and Path

Cookies are the only permitted client-side store for such data (see COM-001).
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Cookies used for authentication/session

### Validation
- Inspect cookies in browser
- Verify flags and scope

### Failure Impact
- Session hijacking

---

# Rule ID: COM-003
## Title: Enforce Security Headers

**Category:** Security Headers  

### Rule
Applications MUST implement:
- Strict-Transport-Security (HSTS)
- Content-Security-Policy (CSP)
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy (where applicable)

### Applies When
- Web applications exposed publicly

### Validation
- Inspect response headers

### Failure Impact
- XSS, clickjacking, data leakage

---

# Rule ID: COM-004
## Title: Disable Server Information Disclosure Headers

**Category:** Information Disclosure  

### Rule
Server and X-Powered-By headers MUST be removed or obfuscated.

### Applies When
- Any HTTP response

### Validation
- Inspect response headers

### Failure Impact
- Technology fingerprinting

---

# Rule ID: COM-005
## Title: Enforce CSRF Protection

**Category:** Request Security  

### Rule
All state-changing requests (POST/PUT/PATCH/DELETE) in cookie-based or ambient-credential flows MUST include CSRF protection mechanisms. Acceptable defenses include Synchronizer Token Pattern, Double-Submit Cookie, or strictly enforcing `SameSite` (Lax/Strict) combined with `Origin`/`Referer` validation. Pure Bearer-token APIs without ambient credentials are exempt from CSRF requirements but must enforce strict CORS.

### Applies When
- POST/PUT/PATCH/DELETE endpoints using cookies or ambient auth

### Validation
- Attempt request without token or across origins

### Failure Impact
- Unauthorized actions

---

# Rule ID: COM-006
## Title: Restrict CORS Policy

**Category:** API Security  

### Rule
Cross-Origin Resource Sharing (CORS) MUST be restricted using an explicit, server-side allowlist of trusted domains. `Access-Control-Allow-Origin` MUST NOT be set to `*` for authenticated or sensitive endpoints. The combination of `Access-Control-Allow-Credentials: true` with a wildcard (`*`), a dynamically reflected `Origin`, or a `null` origin is strictly PROHIBITED.

### Applies When
- APIs with cross-origin access

### Validation
- Inspect response headers for explicit allowlisted origin

### Failure Impact
- Cross-origin data theft

---

# Rule ID: COM-007
## Title: Prevent Direct Public IP Access

**Category:** Network Security  

### Rule
Application MUST NOT be accessible via direct public IP if WAF/CDN is configured on domain.

### Applies When
- Production deployments

### Validation
- Attempt access via IP

### Failure Impact
- WAF bypass

---

# Rule ID: COM-008
## Title: Enforce Strict Input Validation (Superseded)

**Category:** Input Validation  

### Rule
*This rule has been superseded.* Please refer to the canonical input validation trio: **COM-034** (Type & Format Validation), **COM-035** (Length & Bounds), and **COM-036** (Business Logic Validation).

### Applies When
- Any user input field

### Validation
- See COM-034, COM-035, COM-036

### Failure Impact
- Injection, data corruption

---

# Rule ID: COM-009
## Title: Restrict File Upload Access Duration

**Category:** Data Exposure  

### Rule
Uploaded documents containing sensitive data MUST have time-bound access and MUST NOT be publicly accessible indefinitely.

### Applies When
- File upload functionality

### Validation
- Check file URL expiration

### Failure Impact
- Sensitive data exposure

---

# Rule ID: COM-010
## Title: Enforce Token Expiry and Invalidation (Superseded)

**Category:** Session Management  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039**.

### Applies When
- Token-based auth

### Validation
- See COM-039

### Failure Impact
- Session hijacking

---

# Rule ID: COM-011
## Title: Validate Numeric Inputs

**Category:** Business Logic  

### Rule
Numeric inputs MUST reject negative and fractional values where not applicable.

### Applies When
- Payments, quantities

### Validation
- Test negative/decimal values

### Failure Impact
- Financial abuse

---

# Rule ID: COM-012
## Title: Prevent Predictable Identifiers

**Category:** Access Control  

### Rule
Sensitive identifiers MUST NOT use sequential or guessable values.

### Applies When
- Resource identifiers

### Validation
- Attempt enumeration

### Failure Impact
- IDOR

---

# Rule ID: COM-013
## Title: Enforce Role Isolation in Tokens

**Category:** Authorization  

### Rule
User tokens MUST NOT grant elevated privileges such as admin access.

### Applies When
- Role-based systems

### Validation
- Use user token on admin endpoints

### Failure Impact
- Privilege escalation

---

# Rule ID: COM-014
## Title: Enforce MFA and CAPTCHA (Contextual)

**Category:** Authentication  

### Rule
MFA and CAPTCHA MUST be implemented for sensitive applications unless explicitly overridden.

### Applies When
- Fintech, health, PII-heavy apps

### Validation
- Verify presence in auth flow

### Failure Impact
- Brute force attacks

---

# Rule ID: COM-015
## Title: Prevent Long-Lived Tokens (Superseded)

**Category:** Session Security  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039**.

### Applies When
- Token-based auth

### Validation
- See COM-039

### Failure Impact
- Persistent compromise

---

# Rule ID: COM-016
## Title: Enforce Differential Rate Limiting

**Category:** API Security  

### Rule
Rate limits MUST vary based on endpoint sensitivity and authentication state. Concrete defaults MUST be enforced (e.g., Unauthenticated APIs: ≤100 req/min; Sensitive/Payment/AI/Login endpoints: ≤5-10 req/min per IP/user; Standard authenticated APIs: ≤1000 req/min). A hook or configuration MUST exist to override these defaults based on tenant tier or threat level.

### Applies When
- Public and authenticated APIs

### Validation
- Load testing against limits

### Failure Impact
- Abuse, DoS

---

# Rule ID: COM-017
## Title: Enforce File Naming Restrictions

**Category:** File Upload Security  

### Rule
File names MUST:
- Contain only one "."
- Disallow special characters
- Follow strict naming pattern

### Applies When
- File uploads

### Validation
- Upload malformed filenames

### Failure Impact
- Bypass filters

---

# Rule ID: COM-018
## Title: Enforce File Upload Restrictions

**Category:** File Upload Security  

### Rule
File uploads MUST:
- Enforce allowlist of file types
- Limit file size and count

### Applies When
- Upload features

### Validation
- Upload disallowed types

### Failure Impact
- RCE, storage abuse

---

# Rule ID: COM-019
## Title: Enforce Strong Password Policies

**Category:** Authentication  

### Rule
Strong password policies aligned with NIST SP 800-63B MUST be enforced: require a minimum of 12 characters or allow passphrases; block passwords found in known breach databases; allow all printable ASCII characters (including spaces); and do NOT enforce arbitrary periodic password rotation unless compromised.

### Applies When
- User authentication and registration

### Validation
- Attempt weak, short, or breached passwords

### Failure Impact
- Account compromise

---

# Rule ID: COM-020
## Title: Verify User Identity at Registration

**Category:** Authentication  

### Rule
Primary login identifiers MUST be verified during registration. A user MUST NOT be granted an authenticated session or be auto-logged-in before this verification is completed.

### Applies When
- Self-service signup

### Validation
- Check email/OTP verification

### Failure Impact
- Fake accounts

---

# Rule ID: COM-021
## Title: Avoid Boolean Authorization Flags

**Category:** Authorization  

### Rule
Authorization MUST NOT rely on flags like isAdmin or isLoggedIn.

### Applies When
- Role handling

### Validation
- Inspect token/logic

### Failure Impact
- Privilege bypass

---

# Rule ID: COM-022
## Title: Prevent Session Fixation (Superseded)

**Category:** Session Management  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039**.

### Applies When
- Session creation

### Validation
- See COM-039

### Failure Impact
- Session fixation

---

# Rule ID: COM-023
## Title: Enforce Single Device Admin Sessions (Conditional)

**Category:** Admin Security  

### Rule
Admin sessions SHOULD enforce single-device login unless explicitly overridden.

### Applies When
- Sensitive admin panels

### Validation
- Attempt concurrent login

### Failure Impact
- Admin session abuse

---

# Rule ID: COM-024
## Title: Reject Unexpected Parameters

**Category:** API Security  

### Rule
Backend MUST reject additional unexpected parameters in requests.

### Applies When
- API endpoints

### Validation
- Send extra params

### Failure Impact
- Mass assignment

---

# Rule ID: COM-025
## Title: Validate JWT Claims (Superseded)

**Category:** Authentication  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039** and **COM-040**.

### Applies When
- JWT validation

### Validation
- See COM-039, COM-040

### Failure Impact
- Authentication bypass

---

# Rule ID: COM-026
## Title: Prevent Race Conditions

**Category:** Concurrency  

### Rule
Critical operations MUST implement safeguards against race conditions.

### Applies When
- Payments, inventory

### Validation
- Simulate concurrent requests

### Failure Impact
- Logic abuse

---

# Rule ID: COM-027
## Title: Prevent Script Injection via Inputs

**Category:** Injection  

### Rule
Inputs MUST NOT allow execution of HTML, JS, or CSS unless explicitly required.

### Applies When
- User-generated content

### Validation
- Inject script payloads

### Failure Impact
- XSS

---

# Rule ID: COM-028
## Title: Validate External Redirections

**Category:** Redirect Security  

### Rule
External redirections MUST be validated and restricted.

### Applies When
- Redirect features

### Validation
- Test open redirect

### Failure Impact
- Phishing

---

# Rule ID: COM-029
## Title: Enforce Input Size Limits

**Category:** Input Validation  

### Rule
All inputs MUST enforce maximum and minimum length constraints.

### Applies When
- Any input field

### Validation
- Test extreme values

### Failure Impact
- DoS, crashes

---

# Rule ID: COM-030
## Title: Validate Configuration Inputs

**Category:** Configuration Security  

### Rule
Configuration values MUST have strict bounds and validation.

### Applies When
- Configurable intervals/limits

### Validation
- Set extreme values

### Failure Impact
- Service disruption

---

# Rule ID: COM-031
## Title: Prevent Detailed Error Disclosure

**Category:** Error Handling  

### Rule
System MUST NOT expose internal errors or stack traces to users.

### Applies When
- Error handling

### Validation
- Trigger errors

### Failure Impact
- Information disclosure

---

# Rule ID: COM-032
## Title: Enforce Encryption at Rest

**Category:** Cryptography / Data Protection  
**Severity:** CRITICAL

### Rule
All sensitive data that must be recoverable (PII, financial, and health data) MUST be encrypted at rest using strong, modern, industry-standard algorithms (e.g., AES-256-GCM) with properly managed keys. Sensitive data MUST NOT be persisted in plaintext anywhere, including databases, files, caches, logs, and backups.
Passwords and secret authentication verifiers are an exception: they MUST NOT be encrypted (reversible) — they MUST be **hashed** per COM-038.
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Any persistent storage of sensitive data (databases, object storage, files, caches, backups)

### Validation
- Verify storage-level/field-level encryption is enabled
- Verify algorithm strength and key management (no hardcoded keys — CWE-798)
- Confirm no plaintext sensitive data at rest, including backups and logs

### Failure Impact
- Mass data breach upon storage, backup, or disk compromise

---

# Rule ID: COM-033
## Title: Enforce Encryption in Transit (TLS 1.2+ & Strict HTTPS)

**Category:** Network Security / Cryptography  
**Severity:** CRITICAL

### Rule
All data in transit MUST be encrypted using a minimum of TLS 1.2 (TLS 1.3 preferred) with strong cipher suites. HTTPS MUST be strictly enforced for all traffic — plain HTTP MUST be rejected or redirected to HTTPS, and legacy/insecure protocols (SSL, TLS ≤ 1.1) and downgrade attempts MUST be disabled. HSTS MUST be enabled (see COM-003).
**NON-NEGOTIABLE: the TLS 1.2 minimum floor is not subject to user override.**

### Applies When
- Any network communication (web, API, mobile, service-to-service, third-party calls)

### Validation
- Verify TLS 1.3 is enforced and weak/legacy protocols are disabled
- Confirm HTTP is rejected or 301/308-redirected to HTTPS
- Verify HSTS header and strong cipher configuration

### Failure Impact
- Man-in-the-middle, eavesdropping, credential/token interception

---

# Rule ID: COM-034
## Title: Type-Specific Field Validation (Allowlist + Max Length)

**Category:** Input Validation  

### Rule
**This applies to EVERY field the skill introduces in any feature it plans — not only the examples below.** For each field, the skill MUST define a least-privilege validation rule: an allowlist appropriate to that field's semantics plus an explicit maximum length (and a minimum where applicable, see COM-029). The allowlist MUST be **flexible enough to accept all legitimate values** (including internationalization — Unicode letters, accents, etc.) while **strict enough to reject everything outside the field's purpose**. Validation MUST be allowlist-based ("accept known-good"), never blocklist-based.

Illustrative examples (derive equivalent rules for any other field type):
- **Name / free-text identity fields** — allow letters (including Unicode letters for international names), spaces, hyphens, and apostrophes; reject digits and special/injection characters. Do NOT restrict to ASCII-only.
- **Email** — validate against a strict, RFC-compliant format and normalize before use.
- **Contact number** — allow digits only, with a single optional leading `+` for the country code; reject all other characters.
- **Numeric / quantity / amount** — enforce type, range, and sign (see COM-011).
- **Dates, enums, IDs, URLs, etc.** — validate against the exact expected format/set; reject anything else.

When the field type is novel or ambiguous, choose the **narrowest charset and length that still accepts every legitimate value**, and pair it with COM-035 output encoding rather than over-restricting input.

### Applies When
- Any user-supplied field (web, API, or mobile)

### Validation
- Submit out-of-charset values per field (digits in name, letters in phone, malformed email) — MUST be rejected
- Submit over-length values — MUST be rejected

### Failure Impact
- Injection, data corruption, business-logic abuse

---

# Rule ID: COM-035
## Title: Context-Aware Output Encoding

**Category:** Injection / Output Handling  

### Rule
All dynamic data rendered into an output context MUST be encoded/escaped for that specific context (HTML body, HTML attribute, JavaScript, URL, SQL/parameterized query, OS command, mobile WebView/native UI). Input validation and sanitization do NOT replace output encoding — both are required.

### Applies When
- Any user-controlled or external data is rendered, returned, or executed in an interpreter/UI

### Validation
- Inject context-specific payloads (HTML, JS, attribute breakouts) and verify they are encoded, not executed

### Failure Impact
- XSS, injection, UI redressing

---

# Rule ID: COM-036
## Title: Layered Validation & Sanitization (Defense in Depth)

**Category:** Input Validation / Architecture  
**Severity:** CRITICAL

### Rule
Input validation, sanitization, and output encoding MUST be applied at **every** layer present in the system — frontend, mobile, and backend. It MUST NEVER be implemented in only one layer. **Server-side (backend) validation is authoritative and MUST NEVER be omitted or weakened**; frontend and mobile validation are additional defense-in-depth and UX layers. For offline-first/local-only mobile apps, on-device validation (with MASVS-RESILIENCE and MASVS-STORAGE) is authoritative, but any results later synced to a backend MUST be re-validated server-side.
**NON-NEGOTIABLE: server-side validation (when a backend exists) MUST always be present; client-only validation is prohibited and not subject to user override.**

### Applies When
- Any system with more than one tier (web FE / mobile / API / backend)

### Validation
- Bypass the client (call the API directly with invalid/malicious input) — backend MUST still reject it
- Confirm validation exists independently in each present layer

### Failure Impact
- Trivial control bypass, injection, data integrity loss

---

# Rule ID: COM-037
## Title: Secure File Upload Hardening

**Category:** File Upload Security  

### Rule
File uploads MUST be hardened beyond extension/size checks (see COM-017, COM-018, COM-009):
- Verify true content type via magic-byte/MIME inspection, not just the extension.
- Store uploads outside the web root (or in isolated object storage) and serve them non-executably.
- Generate server-side random file names; never trust the client-supplied name or path (prevent path traversal).
- Scan uploads for malware where feasible.
- Strip metadata from media where privacy-relevant.

### Applies When
- Any file/document/media upload functionality (web, API, mobile)

### Validation
- Upload a file with a spoofed extension / mismatched content — MUST be rejected
- Attempt path traversal in the filename — MUST be neutralized
- Verify uploaded files cannot be executed from their storage location

### Failure Impact
- Remote code execution, stored XSS, path traversal, malware distribution

---

# Rule ID: COM-038
## Title: Password & Secret Storage (Hash, Never Encrypt)

**Category:** Cryptography / Authentication  
**Severity:** CRITICAL

### Rule
Passwords and other secret authentication verifiers MUST be stored as salted, one-way hashes using a strong, memory-hard adaptive algorithm — **Argon2id preferred** (bcrypt or scrypt acceptable) — with a per-credential random salt and appropriate cost parameters. Passwords MUST NEVER be stored in plaintext or with reversible encryption.

Server-side-stored bearer tokens, API keys, and password-reset / email-verification tokens MUST also be persisted as hashes (e.g., SHA-256) rather than in recoverable form, MUST be single-use and time-bound, and MUST be compared in constant time.
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Any storage of passwords, API keys, or authentication/verification/reset tokens

### Validation
- Inspect storage: passwords MUST be Argon2id/bcrypt/scrypt hashes — never encrypted or plaintext
- Verify per-credential salt and sane cost factors
- Verify reset/verification tokens are stored hashed, single-use, and expiring

### Failure Impact
- Mass credential compromise and account takeover on database breach

---

# Rule ID: COM-039
## Title: Token & Session Lifecycle Integrity

**Category:** Session Management / Authentication  

### Rule
Authentication tokens and sessions MUST be invalidated server-side immediately upon: logout, password change/reset, role/permission/privilege change, and account suspension or deletion. The server MUST reject expired tokens (validate `exp`) and MUST NOT rely on the client to discard a token. Long-lived access tokens MUST be avoided: use short-lived access tokens with rotating refresh tokens, and refresh-token reuse MUST be detected and revoke the entire token family. For administrative accounts, concurrent logins MUST be controlled or notified.

### Applies When
- Any token- or session-based authentication

### Validation
- Reuse a token after logout / password reset / role change — MUST be rejected
- Replay an expired access token — MUST be rejected
- Replay a rotated refresh token — MUST revoke the family

### Failure Impact
- Session hijacking, privilege persistence after de-escalation, account takeover

---

# Rule ID: COM-040
## Title: JWT / Bearer Token Validation Hardening

**Category:** Authentication / Access Control  
**Severity:** CRITICAL

### Rule
Every JWT/bearer token MUST be cryptographically verified server-side: signature validated against a trusted key, algorithm pinned to a strong algorithm, and `alg: none` plus algorithm-confusion attacks (e.g., RS256→HS256) rejected. The server MUST enforce `exp`, `iss`, and `aud`. Session/identifier tokens MUST be high-entropy, random, and unpredictable — they MUST NOT be sequential, guessable, or derived from user data (username, email, id). Authorization decisions MUST rely on server-validated claims only, never on unverified or client-decoded token contents.
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Any JWT, bearer token, or opaque session identifier

### Validation
- Submit a token with `alg:none` / invalid signature / swapped algorithm — MUST be rejected
- Attempt to forge or guess a session token — MUST fail

### Failure Impact
- Full authentication bypass, privilege escalation, account compromise

---

# Rule ID: COM-041
## Title: Secure Password Reset & Account Recovery

**Category:** Authentication  

### Rule
Password-reset and account-recovery flows MUST use single-use, time-bound, high-entropy tokens stored hashed (COM-038). Issuing a new reset token MUST invalidate all previously issued tokens for that account. Completing a reset MUST invalidate all active sessions/tokens (COM-039). The new password MUST NOT be accepted if it equals the current password, and the flow MUST NOT reveal whether an account exists (COM-042). Reset/recovery parameters (e.g., reset "type", target user id) MUST be bound server-side to the request and MUST NOT be tamperable. A secure account-recovery mechanism MUST exist.

### Applies When
- Forgot-password, password-reset, and account-recovery features

### Validation
- Reuse a reset token, or use an old token after a new one was issued — MUST fail
- Set the new password equal to the current password — MUST be rejected
- Tamper with reset-type / target-user parameters — MUST be rejected

### Failure Impact
- Account takeover, privilege escalation

---

# Rule ID: COM-042
## Title: Prevent Account Enumeration

**Category:** Authentication  

### Rule
Authentication-related endpoints (login, registration, forgot-password, OTP, resend) MUST return generic, uniform responses and MUST NOT reveal whether an account, email, or username exists — via response text, status codes, or response timing. Email-based flows MUST respond identically regardless of account existence and convey the outcome only through the email sent.

### Applies When
- Any flow that accepts a user identifier

### Validation
- Submit existing vs non-existing identifiers — responses, status codes, and timing MUST be indistinguishable

### Failure Impact
- User enumeration enabling targeted phishing and credential stuffing

---

# Rule ID: COM-043
## Title: Account Lockout & Automated-Abuse (Bot) Mitigation

**Category:** Authentication / API Security  

### Rule
Authentication and other sensitive/critical endpoints MUST enforce progressive account lockout or temporary backoff after a threshold of failed attempts, in addition to rate limiting (COM-016). Bot mitigation (CAPTCHA, proof-of-work, or device attestation) MUST protect critical/abusable endpoints (login, signup, OTP, password reset, scan/quota actions). Lockout and mitigation logic MUST fail gracefully (never a server error) and MUST NOT enable denial-of-service against a victim account (prefer backoff/notify over indefinite hard lock).

### Applies When
- Login and sensitive or automatable endpoints

### Validation
- Exceed the failed-attempt threshold — lockout/backoff triggers without a 5xx
- Script the endpoint — bot mitigation engages

### Failure Impact
- Brute force, credential stuffing, OTP/quota abuse

---

# Rule ID: COM-044
## Title: Minimize Sensitive Data in API Responses

**Category:** Data Protection / API Security  
**Severity:** CRITICAL

### Rule
API responses MUST return only the fields required for the use case (least exposure). They MUST NEVER include secrets or security-internal values — passwords, password hashes, OTPs, reset/verification tokens, API keys, session secrets — nor other users' PII, nor internal control/authorization flags (e.g., `isAdmin`, `isApproved`, `role`). Authorization and state fields MUST be derived and enforced server-side and MUST NOT be trusted if echoed by the client (see COM-024).
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Any API that serializes objects into a response

### Validation
- Inspect responses across roles — no secrets/hashes/OTP/tokens, no other-user PII, no trust-bearing flags
- Manipulate an echoed flag (e.g., `isApproved`) — MUST have no server-side effect

### Failure Impact
- Credential/secret disclosure, verification/authorization bypass, PII leakage

---

# Rule ID: COM-045
## Title: Server-Side Enforcement of Access-State Changes

**Category:** Access Control  
**Severity:** CRITICAL

### Rule
Revocation, suspension, role downgrade, plan/entitlement change, and account/data deletion MUST take effect immediately and authoritatively on the backend for ALL access paths (web, mobile, direct API). Cached permissions, already-issued tokens, and background/batch jobs MUST honor the new state (see COM-039). After deletion, the data principal's data MUST be erased or anonymized per retention policy and MUST NOT remain retrievable.
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Any feature that revokes, suspends, downgrades, or deletes access or data

### Validation
- After revoking/suspending a user, call backend APIs with their prior token — MUST be denied
- After deletion, attempt retrieval — MUST fail

### Failure Impact
- Unauthorized access after revocation, residual-data exposure, compliance breach

---

# Rule ID: COM-046
## Title: Resource Lifecycle & Orphaned-Object Cleanup

**Category:** Data Exposure / Storage  

### Rule
Uploaded files and stored objects (profile images, documents, generated assets) MUST be access-controlled and lifecycle-managed: when a resource is updated, replaced, or deleted, the prior object MUST be purged or made inaccessible — it MUST NOT persist at a public, guessable, or previously shared URL. Object storage (e.g., S3) holding PII or sensitive data MUST NOT be publicly readable; access MUST use authorization and time-bound signed URLs (see COM-009). Object identifiers MUST be unguessable (COM-012).

### Applies When
- Any feature storing user files/objects, especially in cloud/object storage

### Validation
- Update/delete a file, then request its old URL — MUST be inaccessible
- Attempt unauthenticated access to a PII object — MUST be denied
- Enumerate object URLs — MUST fail

### Failure Impact
- Persistent exposure of sensitive media/documents, PII leakage

---

# Rule ID: COM-047
## Title: Server-Side Enforcement of Entitlements, Pricing & Quotas

**Category:** Business Logic  

### Rule
Prices, plan/tier, entitlements, usage quotas, and limits MUST be determined and enforced server-side from trusted data — NEVER accepted from or trusted via client input. Plan changes (upgrade/downgrade), purchases, and limit consumption MUST be validated server-side and applied atomically to prevent race-condition bypass (see COM-026). Purchase/activation tokens MUST be single-use (see COM-039, COM-041).

### Applies When
- Subscriptions, payments, metered/quota features, donations, any client-influenced value

### Validation
- Tamper with plan/price/quota in the request — server MUST ignore it and use trusted values
- Fire concurrent requests against a limit — MUST NOT exceed it
- Replay a purchase token — MUST fail

### Failure Impact
- Revenue loss, quota/limit bypass, plan-tampering abuse

---

# Rule ID: COM-048
## Title: Secure OTP Handling

**Category:** Authentication  

### Rule
One-time passwords/codes MUST be generated server-side with sufficient entropy, MUST be single-use, short-lived, and bound to the specific user and action. OTPs MUST NEVER be returned in API responses, logs, or client-accessible storage — only delivered out-of-band (SMS/email/authenticator). Verification MUST be server-side, rate-limited and attempt-capped (see COM-043), and compared in constant time. Enumeration via OTP flows MUST be prevented (COM-042).

### Applies When
- OTP/2FA, email/phone verification, transaction confirmation

### Validation
- Inspect API responses/logs — the OTP MUST be absent
- Reuse or brute-force an OTP — MUST fail
- Use an expired OTP — MUST fail

### Failure Impact
- OTP bypass, account takeover, MFA defeat

---

# Rule ID: COM-049
## Title: Dependency & Platform Patch Management

**Category:** Configuration / Supply Chain  

### Rule
All dependencies, libraries, frameworks, runtimes, and server software MUST be tracked (SBOM) and continuously scanned (SCA) for known vulnerabilities. Known-vulnerable or end-of-life components — e.g., outdated JS frameworks (Next.js/Vue.js), unpatched Nginx/SSH/OS, EOL language runtimes, or low/EOL mobile minSDK targets — MUST be patched or replaced before release. A defined patching/update cadence MUST exist for production systems.

### Applies When
- ONLY when adding, updating, or modifying project dependencies (package.json, requirements.txt, go.mod, build.gradle) or Dockerfiles.

### Validation
- Run SCA / vulnerability scan — no known critical/high vulnerabilities in shipped components
- Verify server software and runtimes are on supported, patched versions

### Failure Impact
- Remote code execution, known-CVE exploitation, full compromise

---

# Rule ID: COM-050
## Title: Disable Non-Production Surfaces in Production

**Category:** Configuration / API Security  

### Rule
Production deployments MUST NOT expose development/debug surfaces: interactive API docs (Swagger/OpenAPI UI), GraphQL introspection, debug endpoints, verbose stack traces (see COM-031), default/sample pages, or directory listings. API schemas/specs MUST NOT leak internal hostnames, ports, or environment details (e.g., `localhost:port`). Such surfaces MUST be disabled or restricted to trusted networks/identities.

### Applies When
- ONLY when the feature explicitly sends transactional or notification emails.

### Validation
- Request Swagger/OpenAPI UI or GraphQL introspection in production — MUST be unavailable/restricted
- Inspect specs for internal hosts/ports — MUST be absent

### Failure Impact
- Attack-surface mapping, information disclosure, easier exploitation

---

# Rule ID: COM-051
## Title: Multi-Tenant / Data-Segregation Isolation

**Category:** Access Control  
**Severity:** CRITICAL

### Rule
In multi-tenant, multi-branch, or multi-organization systems, every data access and mutation MUST be scoped server-side to the caller's tenant/branch/org context derived from the authenticated session — NEVER from a client-supplied tenant/branch identifier alone. Cross-tenant access MUST be denied by default and explicitly tested. Tokens/identifiers MUST NOT be reusable across tenant boundaries.
**NON-NEGOTIABLE: this control is not subject to user override.**

### Applies When
- Any system serving multiple tenants/branches/organizations

### Validation
- Using Tenant A's credentials, attempt to read/modify Tenant B's data (including via token reuse or id manipulation) — MUST be denied

### Failure Impact
- Cross-tenant data breach and modification

---

# Rule ID: COM-052
## Title: Email Authentication & Safe Content

**Category:** Configuration / Data Protection  

### Rule
Sending domains MUST publish and enforce SPF, DKIM, and DMARC to prevent email spoofing and phishing. Email content MUST NOT contain sensitive data — passwords, OTPs, full tokens, or unnecessary PII; emails MUST reference actions via secure, single-use links rather than embedding secrets.

### Applies When
- Any feature sending transactional or notification email

### Validation
- Check DNS for valid, enforcing SPF/DKIM/DMARC records
- Inspect email bodies — no OTP/password/secret/excess PII

### Failure Impact
- Phishing/spoofing of users, sensitive data exposure via mailbox compromise

---

# Rule ID: COM-053
## Title: No Caching of Authenticated or Sensitive Responses

**Category:** Session Security / Configuration  

### Rule
Responses containing authenticated, personal, or sensitive data MUST set `Cache-Control: no-store` (with appropriate `Pragma`/`Expires`) so they are not cached by browsers, shared caches, or restored via back-navigation after logout (extends COM-022). Sensitive data MUST NOT be cached by intermediaries or CDNs.

### Applies When
- Any authenticated or sensitive HTTP response

### Validation
- After logout, use browser back/history — sensitive pages MUST NOT be served from cache
- Inspect `Cache-Control` headers on sensitive responses

### Failure Impact
- Sensitive data exposure on shared/public devices, post-logout access

---

# Rule ID: COM-054
## Title: Do Not Trust Client-Supplied IP or Headers for Security

**Category:** API Security / Network Security  

### Rule
Security decisions (rate limiting, lockout, geofencing, audit attribution, authorization) MUST NOT rely solely on client-controllable signals such as `X-Forwarded-For`, `X-Real-IP`, `Referer`, or `Origin`. Client IP MUST be derived only from a trusted reverse proxy/load-balancer configuration; spoofable headers MUST be ignored or validated. Authorization MUST be based on authenticated identity, not network headers.

### Applies When
- Any rate-limiting, abuse-control, geo, or attribution logic

### Validation
- Send forged `X-Forwarded-For` values — rate limiting/lockout/geo MUST NOT be bypassable

### Failure Impact
- Rate-limit/lockout bypass, spoofed audit trails, abuse-control evasion

---

# Rule ID: COM-055
## Title: Centralized Secrets Management / No Hardcoded Secrets

**Category:** Configuration / Cryptography  
**Severity:** HIGH

### Rule
API keys, database credentials, cryptographic keys, and third-party tokens MUST NOT be hardcoded in source code, committed to version control, embedded in client-side applications (mobile/web), or baked into container images. All secrets MUST be managed centrally using a dedicated secret vault or environment-injected secret manager.

### Applies When
- Any service, script, or application requiring credentials to access another service

### Validation
- Static code analysis (e.g., TruffleHog, GitLeaks) shows zero secrets in code
- Secrets are dynamically retrieved at runtime or injected safely by the orchestrator

### Failure Impact
- Credential compromise, unauthorized access to adjacent systems

---

# Rule ID: COM-056
## Title: Secure Logging Baseline

**Category:** Logging & Alerting  
**Severity:** HIGH

### Rule
The system MUST log critical security events including authentication success/failures, authorization decisions (especially failures), and all administrative/privileged actions. The system MUST strictly PROHIBIT the logging of sensitive data including passwords, authentication tokens, session IDs, OTPs, full credit card numbers (PAN), and full PII/PHI.

### Applies When
- Implementing audit trails and application logs

### Validation
- Review logs for absence of sensitive data
- Verify that security-relevant events generate logs with adequate context (timestamp, user ID, event type, success/failure)

### Failure Impact
- Data exposure through log files, lack of accountability during incident response

---

# Rule ID: COM-057
## Title: Server-Side Request Forgery (SSRF) Prevention

**Category:** Network Security / Architecture  
**Severity:** HIGH

### Rule
Any feature that initiates outbound HTTP requests or network connections based on user input MUST strictly validate and restrict destinations. The system MUST enforce an allowlist of permitted domains/IPs, explicitly deny access to internal networks (RFC1918), link-local addresses, cloud metadata services (e.g., 169.254.169.254), and loopback. Redirect following MUST be disabled or strictly re-validated to prevent bypasses.

### Applies When
- Webhooks, URL fetching, proxying requests, PDF generation from URLs

### Validation
- Attempt to fetch internal resources (e.g., `http://127.0.0.1` or `http://169.254.169.254`) — requests must fail

### Failure Impact
- Internal network enumeration, cloud credential theft, unauthorized access to internal APIs

---

# Rule ID: COM-058
## Title: Prevent Insecure Deserialization

**Category:** Input Validation / Architecture  
**Severity:** HIGH

### Rule
The application MUST NOT deserialize untrusted data using unsafe deserialization formats or libraries that allow arbitrary object instantiation (e.g., Java native serialization, Python `pickle`, .NET `BinaryFormatter`, or YAML unsafe loads). Systems MUST use safe, data-only serialization formats like JSON or Protocol Buffers.

### Applies When
- Processing serialized data from APIs, queues, files, or cache

### Validation
- Ensure parsers are configured securely (e.g., `yaml.safe_load`)
- Send manipulated serialized objects (if applicable) — must result in a safe rejection without executing code

### Failure Impact
- Remote Code Execution (RCE), Denial of Service (DoS)

---