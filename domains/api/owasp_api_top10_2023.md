# OWASP API Top 10:2023 — Structured Security Rules

---

# Rule ID: API-001
## Title: Enforce Object-Level Authorization

**Source:** OWASP API Top 10:2023 - API1 Broken Object Level Authorization
**Category:** Object-Level Authorization
**Severity:** HIGH

### Rule
All API endpoints accessing objects MUST validate user authorization for each object reference.

### Applies When
- API uses object identifiers (IDs, UUIDs)

### Validation
- Modify object IDs and test access

### Failure Impact
- Unauthorized data access

---

# Rule ID: API-002
## Title: Secure Authentication in APIs

**Source:** OWASP API Top 10:2023 - API2 Broken Authentication
**Category:** Authentication
**Severity:** CRITICAL

### Rule
Authentication mechanisms MUST enforce secure token handling, MFA, and brute-force protection.

### Applies When
- API authentication implemented

### Validation
- Test token reuse, brute force

### Failure Impact
- Account takeover

---

# Rule ID: API-003
## Title: Enforce Property-Level Authorization

**Source:** OWASP API Top 10:2023 - API3 Broken Object Property Level Authorization
**Category:** API Data Exposure
**Severity:** HIGH

### Rule
APIs MUST restrict access to object properties and MUST NOT expose sensitive fields unnecessarily.

### Applies When
- API responses include object properties

### Validation
- Inspect responses for hidden/sensitive fields

### Failure Impact
- Data leakage

---

# Rule ID: API-004
## Title: Prevent Resource Exhaustion

**Source:** OWASP API Top 10:2023 - API4 Unrestricted Resource Consumption
**Category:** Availability
**Severity:** MEDIUM

### Rule
APIs MUST enforce rate limiting, quotas, and resource consumption limits.

### Applies When
- Public or high-traffic APIs

### Validation
- Perform DoS / high request testing

### Failure Impact
- Service disruption

---

# Rule ID: API-005
## Title: Enforce Function-Level Authorization (BFLA)

**Source:** OWASP API Top 10:2023 - API5 Broken Function Level Authorization
**Category:** Function-Level Authorization
**Severity:** HIGH

### Rule
APIs MUST enforce authorization at the function/endpoint level, not just at the object level. Admin and privileged endpoints MUST be inaccessible to regular users regardless of direct URL access. Verify that every endpoint enforces the correct role or permission — not just authentication.

### Applies When
- API has role-based or privileged endpoints (admin, moderator, internal)
- Different user roles exist with different permitted operations

### Validation
- As a regular user, call admin-only endpoints directly (e.g. DELETE /admin/users/{id}) — must return 403
- Attempt to access management or reporting endpoints with a non-privileged token
- Enumerate endpoints and test each with credentials below the required privilege level

### Failure Impact
- Privilege escalation — regular users can invoke admin or elevated functions
- Mass data deletion, account takeover, unauthorized configuration changes

---

# Rule ID: API-006
## Title: Protect Sensitive Business Flows from Automated Abuse

**Source:** OWASP API Top 10:2023 - API6 Unrestricted Access to Sensitive Business Flows
**Category:** Business Logic
**Severity:** HIGH

### Rule
APIs exposing sensitive business flows (checkout, payment, referral, inventory, voting, booking) MUST include protection against automated abuse, high-volume scripted requests, and bot exploitation. Controls MUST distinguish legitimate users from automation.

### Applies When
- API exposes workflows with real-world business value (purchases, rewards, reservations)
- Rate limits or quotas have financial or reputational impact if bypassed
- Workflows are repeatable and automatable (no natural human friction)

### Validation
- Script repeated automated requests against the flow — verify rate-limit or challenge is triggered
- Attempt to drain limited inventory or exhaust a promotion via automation
- Verify CAPTCHA, device fingerprinting, or behavioral analysis is applied to high-risk flows

### Failure Impact
- Scalping, reward/voucher abuse, inventory depletion, financial fraud
- Reputational damage and revenue loss

---

# Rule ID: API-007
## Title: Prevent SSRF in APIs

**Source:** OWASP API Top 10:2023 - API7 SSRF
**Category:** API Security
**Severity:** HIGH

### Rule
All user-supplied URLs MUST be validated and restricted to trusted destinations.

### Applies When
- APIs fetch external resources

### Validation
- Inject internal URLs (localhost, metadata)

### Failure Impact
- Internal network exposure

---

# Rule ID: API-008
## Title: Prevent API Security Misconfiguration

**Source:** OWASP API Top 10:2023 - API8 Security Misconfiguration
**Category:** Configuration
**Severity:** HIGH

### Rule
APIs MUST NOT be deployed with insecure default configurations, unnecessary HTTP methods, permissive CORS, verbose error messages, or missing security headers. All API-specific configuration MUST be hardened before production.

### Applies When
- Any API deployed to a production or shared environment
- APIs accessible from the public internet or cross-origin clients

### Validation
- Send OPTIONS request and verify only allowed HTTP methods are accepted
- Verify CORS policy does not allow arbitrary origins (cross-ref COM-006)
- Confirm error responses do not expose stack traces, internal paths, or server version strings
- Verify required security headers are present (cross-ref COM-003)
- Test that debug/diagnostic endpoints are not accessible in production (cross-ref COM-050)

### Failure Impact
- Information disclosure, CORS exploitation, unintended method execution
- Attack surface exposure leading to further compromise

### Cross-References
- COM-003 (security headers), COM-006 (CORS), COM-050 (non-prod surfaces), COM-004 (debug mode)

---

# Rule ID: API-009
## Title: Maintain API Inventory and Retire Deprecated Endpoints

**Source:** OWASP API Top 10:2023 - API9 Improper Inventory Management
**Category:** Configuration
**Severity:** MEDIUM

### Rule
All API versions, endpoints, and hosts MUST be inventoried. Deprecated, old-version, and non-production API endpoints MUST be decommissioned or explicitly access-controlled. Shadow APIs (undocumented, unmanaged endpoints) MUST NOT exist in production.

### Applies When
- API has multiple versions (v1, v2…) or multiple environments
- API has undergone versioning, migration, or deprecation

### Validation
- Enumerate all exposed API paths and compare against the official API inventory/documentation
- Confirm old API versions (e.g. /api/v1/ after /api/v2/ is live) are decommissioned or return 410 Gone
- Verify staging/debug/internal endpoints are not reachable in production (cross-ref COM-050)
- Confirm an up-to-date API inventory or SBOM-equivalent exists

### Failure Impact
- Attackers exploit unpatched or unmonitored legacy endpoints
- Sensitive functionality exposed via forgotten shadow APIs

### Cross-References
- COM-049 (dependency/patch management), COM-050 (non-prod surface removal)

---

# Rule ID: API-010
## Title: Secure Third-Party API Consumption

**Source:** OWASP API Top 10:2023 - API10 Unsafe Consumption of APIs
**Category:** Integration Security
**Severity:** HIGH

### Rule
All third-party API responses MUST be validated and treated as untrusted input.

### Applies When
- External APIs integrated

### Validation
- Inject malicious payloads via external services

### Failure Impact
- Injection, data leakage

---
