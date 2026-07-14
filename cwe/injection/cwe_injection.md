# CWE — Injection Weaknesses

---

## CWE-79 — Cross-Site Scripting (XSS)
Mapped OWASP: A05  
Enforcement:
- Output encoding
- Input sanitization  
Validation:
- Inject script payloads

---

## CWE-89 — SQL Injection
Mapped OWASP: A05  
Enforcement:
- Parameterized queries  
Validation:
- SQL payload testing

---

## CWE-77 — Command Injection
Mapped OWASP: A05  
Enforcement:
- Avoid shell execution  
Validation:
- Inject OS commands

---

## CWE-78 — OS Command Injection
Mapped OWASP: A05  
Enforcement:
- Strict input validation  
Validation:
- Command payload injection

---

## CWE-94 — Code Injection
Mapped OWASP: A05  
Enforcement:
- Avoid dynamic execution  
Validation:
- Inject code snippets

---

## CWE-918 — Server-Side Request Forgery (SSRF)
Mapped OWASP: A01 Broken Access Control (Cross-ref: API7)  
Enforcement:
- URL validation + allowlist  
Validation:
- Internal IP access

---
