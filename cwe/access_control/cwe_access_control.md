# CWE — Access Control Weaknesses

---

## CWE-284 — Improper Access Control
Mapped OWASP: A01  
Enforcement:
- Enforce server-side authorization
- Deny by default  
Validation:
- IDOR testing

---

## CWE-285 — Improper Authorization
Mapped OWASP: A01  
Enforcement:
- Role-based access checks
Validation:
- Privilege escalation attempts

---

## CWE-639 — Authorization Bypass Through User-Controlled Key
Mapped OWASP: A01  
Enforcement:
- Validate ownership of resources  
Validation:
- Modify object IDs

---

## CWE-200 — Exposure of Sensitive Information
Mapped OWASP: A02  
Enforcement:
- Restrict sensitive data exposure  
Validation:
- Inspect responses

---

## CWE-522 — Insufficiently Protected Credentials
Mapped OWASP: A07  
Enforcement:
- Secure credential storage  
Validation:
- Check storage mechanisms

---

## CWE-306 — Missing Authentication for Critical Function
Mapped OWASP: A07  
Enforcement:
- Enforce authentication  
Validation:
- Access endpoints unauthenticated

---

## CWE-862 — Missing Authorization
Mapped OWASP: A01  
Enforcement:
- Authorization checks everywhere  
Validation:
- Access restricted endpoints

---

## CWE-863 — Incorrect Authorization
Mapped OWASP: A01  
Enforcement:
- Correct logic validation  
Validation:
- Role manipulation

---
