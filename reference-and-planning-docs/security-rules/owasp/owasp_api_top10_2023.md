# OWASP API Top 10:2023 — Structured Security Rules

---

# Rule ID: API-001
## Title: Enforce Object-Level Authorization

**Source:** OWASP API Top 10:2023 - API1 Broken Object Level Authorization  
**Category:** API Access Control  

### Rule
All API endpoints accessing objects MUST validate user authorization for each object reference.

### Applies When
- API uses object identifiers (IDs, UUIDs)

### Validation
- Modify object IDs and test access

### Failure Impact
- Unauthorized data access  
:contentReference[oaicite:11]{index=11}

---

# Rule ID: API-002
## Title: Secure Authentication in APIs

**Source:** OWASP API Top 10:2023 - API2 Broken Authentication  
**Category:** Authentication  

### Rule
Authentication mechanisms MUST enforce secure token handling, MFA, and brute-force protection.

### Applies When
- API authentication implemented

### Validation
- Test token reuse, brute force

### Failure Impact
- Account takeover  
:contentReference[oaicite:12]{index=12}

---

# Rule ID: API-003
## Title: Enforce Property-Level Authorization

**Source:** OWASP API Top 10:2023 - API3 Broken Object Property Level Authorization  
**Category:** API Data Exposure  

### Rule
APIs MUST restrict access to object properties and MUST NOT expose sensitive fields unnecessarily.

### Applies When
- API responses include object properties

### Validation
- Inspect responses for hidden/sensitive fields

### Failure Impact
- Data leakage  
:contentReference[oaicite:13]{index=13}

---

# Rule ID: API-004
## Title: Prevent Resource Exhaustion

**Source:** OWASP API Top 10:2023 - API4 Unrestricted Resource Consumption  
**Category:** Availability  

### Rule
APIs MUST enforce rate limiting, quotas, and resource consumption limits.

### Applies When
- Public or high-traffic APIs

### Validation
- Perform DoS / high request testing

### Failure Impact
- Service disruption  
:contentReference[oaicite:14]{index=14}

---

# Rule ID: API-005
## Title: Validate Business Logic Abuse

**Source:** OWASP API Top 10:2023  
**Category:** Business Logic  

### Rule
Critical business flows MUST include abuse protection mechanisms.

### Applies When
- Financial / transactional APIs

### Validation
- Simulate automation abuse scenarios

### Failure Impact
- Financial loss  
:contentReference[oaicite:15]{index=15}

---

# Rule ID: API-007
## Title: Prevent SSRF in APIs

**Source:** OWASP API Top 10:2023 - API7 SSRF  
**Category:** API Security  

### Rule
All user-supplied URLs MUST be validated and restricted to trusted destinations.

### Applies When
- APIs fetch external resources

### Validation
- Inject internal URLs (localhost, metadata)

### Failure Impact
- Internal network exposure  
:contentReference[oaicite:16]{index=16}

---

# Rule ID: API-010
## Title: Secure Third-Party API Consumption

**Source:** OWASP API Top 10:2023 - API10 Unsafe Consumption of APIs  
**Category:** Integration Security  

### Rule
All third-party API responses MUST be validated and treated as untrusted input.

### Applies When
- External APIs integrated

### Validation
- Inject malicious payloads via external services

### Failure Impact
- Injection, data leakage  
:contentReference[oaicite:17]{index=17}

---
