# Common Security Considerations — Baseline Enforcement Rules

---

# Rule ID: COM-001
## Title: Prevent Storage of Sensitive Data in Local Storage

**Category:** Client-Side Security  

### Rule
Authentication tokens and sensitive user data MUST NOT be stored in browser localStorage or sessionStorage.

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

### Rule
All cookies MUST:
- Use HttpOnly flag
- Use Secure flag
- Set SameSite=Lax or Strict
- Have scoped domain and path

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
All state-changing requests MUST include CSRF protection mechanisms.

### Applies When
- POST/PUT/PATCH/DELETE endpoints

### Validation
- Attempt request without token

### Failure Impact
- Unauthorized actions

---

# Rule ID: COM-006
## Title: Restrict CORS Policy

**Category:** API Security  

### Rule
Access-Control-Allow-Origin MUST NOT be set to "*" for sensitive endpoints.

### Applies When
- APIs with cross-origin access

### Validation
- Inspect response headers

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
## Title: Enforce Strict Input Validation

**Category:** Input Validation  

### Rule
All inputs MUST follow strict validation rules based on expected data type and length.

### Applies When
- Any user input field

### Validation
- Inject invalid characters
- Test boundary values

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
## Title: Enforce Token Expiry and Invalidation

**Category:** Session Management  

### Rule
Session/Auth tokens MUST expire and MUST be invalidated on:
- Logout
- Password change
- Admin reset

### Applies When
- Authentication systems

### Validation
- Attempt reuse after logout/change

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
## Title: Prevent Long-Lived Tokens

**Category:** Session Security  

### Rule
Session and refresh tokens MUST have short lifetimes.

### Applies When
- Token-based auth

### Validation
- Inspect expiry times

### Failure Impact
- Persistent compromise

---

# Rule ID: COM-016
## Title: Enforce Differential Rate Limiting

**Category:** API Security  

### Rule
Rate limits MUST vary:
- Strict for unauthenticated
- Strict for payment/AI endpoints
- Moderate for others

### Applies When
- Public APIs

### Validation
- Load testing

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
Strong password policies MUST be enforced unless explicitly overridden.

### Applies When
- User authentication

### Validation
- Attempt weak passwords

### Failure Impact
- Account compromise

---

# Rule ID: COM-020
## Title: Verify User Identity at Registration

**Category:** Authentication  

### Rule
Primary login identifiers MUST be verified during registration.

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
## Title: Enforce Session Invalidation on Logout

**Category:** Session Security  

### Rule
Session MUST be invalidated and inaccessible after logout, including browser back navigation.

### Applies When
- Web apps

### Validation
- Use back button after logout

### Failure Impact
- Session reuse

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
## Title: Prevent Token Leakage via URL

**Category:** Session Security  

### Rule
Authentication tokens MUST NOT be passed in URL parameters.

### Applies When
- Auth flows

### Validation
- Inspect network requests

### Failure Impact
- Token leakage

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