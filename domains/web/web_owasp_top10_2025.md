# OWASP Top 10:2025 — Structured Security Rules

---

# Rule ID: OWASP-A01-001
## Title: Enforce Server-Side Access Control

**Source:** OWASP Top 10:2025 - A01 Broken Access Control  
**Category:** Access Control  

### Rule
All access control checks MUST be enforced on the server side and MUST NOT rely on client-controlled data.

### Applies When
- Any authenticated or unauthenticated endpoint exists
- APIs or web applications expose resources

### Validation
- Attempt IDOR / parameter tampering
- Modify JWT/session tokens and verify enforcement
- Access restricted endpoints without authorization

### Failure Impact
- Unauthorized data access
- Privilege escalation  

---

# Rule ID: OWASP-A01-002
## Title: Enforce Least Privilege Access

**Source:** OWASP Top 10:2025 - A01 Broken Access Control  
**Category:** Access Control  

### Rule
Access MUST be denied by default and granted only based on explicit role or ownership validation.

### Applies When
- Role-based or user-based systems exist

### Validation
- Attempt horizontal/vertical privilege escalation
- Verify default deny behavior

### Failure Impact
- Full system compromise  

---

# Rule ID: OWASP-A02-001
## Title: Secure Configuration Management

**Source:** OWASP Top 10:2025 - A02 Security Misconfiguration  
**Category:** Configuration  

### Rule
All environments MUST enforce hardened configurations with no default credentials, debug modes, or exposed sensitive configs.

### Applies When
- Any deployment environment exists

### Validation
- Check for debug endpoints
- Inspect config files and headers

### Failure Impact
- System exposure  

---

# Rule ID: OWASP-A03-001
## Title: Enforce Secure Software Supply Chain

**Source:** OWASP Top 10:2025 - A03 Software Supply Chain Failures  
**Category:** Dependency Security  

### Rule
All dependencies MUST be tracked, verified, and scanned for vulnerabilities before deployment.

### Applies When
- Third-party libraries/components used

### Validation
- SBOM generation
- Dependency vulnerability scan

### Failure Impact
- Remote code execution  

---

# Rule ID: OWASP-A04-001
## Title: Enforce Strong Cryptography

**Source:** OWASP Top 10:2025 - A04 Cryptographic Failures  
**Category:** Cryptography  

### Rule
Sensitive data MUST be encrypted using strong, modern cryptographic algorithms both in transit and at rest.

### Applies When
- Handling PII, credentials, financial data

### Validation
- Check TLS enforcement
- Verify encryption algorithms and key management

### Failure Impact
- Data exposure  

---

# Rule ID: OWASP-A05-001
## Title: Prevent Injection Attacks

**Source:** OWASP Top 10:2025 - A05 Injection  
**Category:** Input Validation  

### Rule
All user inputs MUST be validated, sanitized, and parameterized before being processed by interpreters.

### Applies When
- User input is used in queries, commands, templates

### Validation
- Test SQLi, XSS, command injection payloads

### Failure Impact
- Arbitrary code execution  

---

# Rule ID: OWASP-A06-001
## Title: Enforce Secure Design Practices

**Source:** OWASP Top 10:2025 - A06 Insecure Design  
**Category:** Design  

### Rule
All critical application flows MUST undergo threat modeling and secure design validation before implementation.

### Applies When
- New feature planning phase

### Validation
- Threat model existence
- Abuse case coverage

### Failure Impact
- Systemic vulnerabilities  

---

# Rule ID: OWASP-A07-001
## Title: Secure Authentication Mechanisms

**Source:** OWASP Top 10:2025 - A07 Authentication Failures  
**Category:** Authentication  

### Rule
Authentication mechanisms MUST use industry standards and MUST enforce MFA where applicable.

### Applies When
- Login/auth flows exist

### Validation
- Test brute force
- Validate token security

### Failure Impact
- Account takeover  

---

# Rule ID: OWASP-A08-001
## Title: Ensure Data Integrity Validation

**Source:** OWASP Top 10:2025 - A08 Software and Data Integrity Failures  
**Category:** Integrity  

### Rule
All software updates, data inputs, and code artifacts MUST be verified for integrity before execution.

### Applies When
- CI/CD, updates, external inputs

### Validation
- Signature verification checks

### Failure Impact
- Supply chain compromise  

---

# Rule ID: OWASP-A09-001
## Title: Enforce Logging and Alerting

**Source:** OWASP Top 10:2025 - A09 Security Logging & Alerting Failures  
**Category:** Monitoring  

### Rule
All critical events MUST be logged and MUST trigger alerts for suspicious activities.

### Applies When
- Any production system

### Validation
- Trigger failed login attempts
- Check alert generation

### Failure Impact
- Undetected breaches  

---

# Rule ID: OWASP-A10-001
## Title: Handle Exceptions Securely

**Source:** OWASP Top 10:2025 - A10 Mishandling of Exceptional Conditions  
**Category:** Error Handling  

### Rule
All exceptions MUST be handled securely without exposing internal system details.

### Applies When
- Error handling implemented

### Validation
- Trigger errors and inspect responses

### Failure Impact
- Information disclosure  

---
