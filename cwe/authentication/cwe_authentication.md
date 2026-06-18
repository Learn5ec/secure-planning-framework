# CWE — Authentication Weaknesses

---

## CWE-287 — Improper Authentication
Mapped OWASP: A07  
Enforcement:
- Strong authentication flows  
Validation:
- Bypass attempts

---

## CWE-384 — Session Fixation
Mapped OWASP: A07  
Enforcement:
- Regenerate session IDs  
Validation:
- Reuse session

---

## CWE-613 — Insufficient Session Expiration
Mapped OWASP: A07  
Enforcement:
- Short session lifetime  
Validation:
- Use expired tokens

---

## CWE-798 — Hardcoded Credentials
Mapped OWASP: A02  
Enforcement:
- No hardcoded secrets  
Validation:
- Code inspection

---

## CWE-640 — Weak Password Recovery
Mapped OWASP: A07  
Enforcement:
- Secure reset flows  
Validation:
- Abuse reset mechanism

---
