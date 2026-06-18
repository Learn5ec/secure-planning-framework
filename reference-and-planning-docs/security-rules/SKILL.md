# Secure Planning Skill — v1.0

## Purpose
This skill enforces security, privacy, and compliance requirements at the **planning phase** of software development. All rule sets are cumulative and MUST be applied together where applicable.

It transforms feature ideas into **secure, enforceable implementation blueprints** by applying:
- OWASP Top 10 (2025)
- OWASP API Top 10 (2023)
- DPDP Act 2023 (Core + Extended Compliance)
- CWE mappings (when available)
- Common Security Baseline Enforcement Rules

This skill MUST be used BEFORE any implementation or code generation.

---

## Referenced Rule Sets

The following rule files MUST be treated as authoritative:

- /security-rules/dpdp/dpdp_rules.md  
- /security-rules/dpdp/dpdpa-compliance.md  
- /security-rules/owasp/owasp_api_top10_2023.md  
- /security-rules/owasp/web_owasp_top10_2025.md  
- /security-rules/meta/cwe/
- /security-rules/common/common-considerations.md

Rules from these files MUST be:
- Enforced (not suggested)
- Contextually selected
- Reflected in output

---

## When to Use This Skill

Trigger this skill when:
- A new feature is being planned
- APIs or workflows are being designed
- Architecture decisions are being made
- Any user data is involved
- Admin or privileged functionality is introduced

---

## Mandatory Behavior

### 1. Input Analysis

You MUST:
- Identify feature intent
- Detect sensitive data usage (PII, auth, financial, etc.)
- Identify actors (user, admin, system)
- Detect trust boundaries

Assumptions MUST:
- Be explicitly listed
- Be minimal
- NOT replace missing input when critical

If assumptions affect security decisions → trigger INSUFFICIENT_INPUT

---

### 2. Risk Classification
You MUST classify risk as:
- LOW
- MEDIUM
- HIGH
- CRITICAL

Based on:
- Data sensitivity
- Privilege level
- Exposure surface

---

### 3. Rule Enforcement

You MUST:
- Extract relevant rules from referenced files
- Apply ONLY contextually relevant rules
- Convert rules into implementation constraints

You MUST ensure:
- At least one rule from OWASP (Web or API)
- Common Considerations ALWAYS applied
- DPDP applied when data is involved

If no rules are selected, treat as INVALID output.

All applied rules MUST include:
- Exact rule_id
- Source file reference

Outputs without rule_id are INVALID.

DO NOT:
- Output generic advice
- Skip applicable rules
- Assume security controls exist

---

### 4. Threat Modeling

You MUST:
- Identify realistic attack scenarios
- Map attack vectors
Define:
- Exploitation scenario
- Attacker capability required
- Impact (Confidentiality, Integrity, Availability)

Threat modeling MUST be practical and exploit-focused.

---

### 5. Compliance Enforcement

If personal data is involved:
You MUST enforce rules from:
- dpdp_rules.md
- dpdpa-compliance.md

This includes:
- Consent
- Data minimization
- Retention
- User rights
- Breach readiness

---

### 6. Output Generation (STRICT)

You MUST output structured JSON only.

Schema:

{
  "feature_summary": "",
  "risk_classification": "",
  "risk_reasoning": "",
  "data_sensitivity": [],
  "actors": [],
  "assumptions": [],
  "threat_model": [
    {
      "threat": "",
      "attack_vector": "",
      "impact": ""
    }
  ],
  "security_requirements": [
    {
      "rule_id": "",
      "requirement": "",
      "source": "",
      "validation": ""
    }
  ],
  "compliance_requirements": [
    {
      "rule_id": "",
      "requirement": "",
      "source": ""
    }
  ],
  "design_constraints": [],
  "anti_patterns": [],
  "required_controls": [],
  "acceptance_criteria": []
}

---

## Rule Selection Logic

You MUST evaluate and apply rules in the following order and combination:

---

### 1. OWASP (Web) — Mandatory When Applicable
Apply based on feature characteristics:

- Access control → A01 Broken Access Control  
- Cryptography → A02 Cryptographic Failures  
- Injection → A03 Injection  
- Insecure design → A04 Insecure Design  
- Security misconfiguration → A05 Security Misconfiguration  
- Vulnerable components → A06 Vulnerable and Outdated Components  
- Authentication → A07 Identification and Authentication Failures  
- Data integrity → A08 Software and Data Integrity Failures  
- Logging → A09 Security Logging and Monitoring Failures  
- Error handling → A10 Mishandling of Exceptional Conditions  

These MUST be mapped wherever relevant.

---

### 2. OWASP (API) — Mandatory for API-Driven Features
Apply when:
- API endpoints exist
- Object identifiers are exposed
- Data is exchanged via APIs

You MUST enforce:
- Object-level authorization
- Property-level authorization
- Rate limiting
- Input validation
- Secure third-party API consumption

---

### 3. DPDP — Mandatory for Personal Data
Apply when:
- ANY personal data is collected, processed, stored, or transmitted

You MUST enforce:
- Consent
- Purpose limitation
- Data minimization
- Retention limits
- User rights
- Breach readiness
- Cross-border considerations (if applicable)

DPDP rules MUST NOT be skipped under any condition.

---

### 4. CWE (when available) — Deep Validation Layer
Use to:
- Strengthen technical validation logic
- Map requirements to real vulnerability classes
- Improve testability and VAPT alignment

CWE mapping SHOULD augment, not replace, OWASP rules.

---

### 5. Common Considerations — ALWAYS ENFORCED (NON-NEGOTIABLE BASELINE)

These rules MUST be applied to EVERY feature, regardless of context.

This includes:
- Secure storage practices
- Input validation and sanitization
- Session and token handling
- File upload restrictions
- Security headers
- Rate limiting
- Error handling
- Misconfiguration prevention

These MUST NOT be skipped even if:
- Feature appears low risk
- No sensitive data is involved

---

## Rule Combination Requirement

You MUST:
- Apply ALL relevant rule sets simultaneously
- NOT treat rule sets as mutually exclusive
- NOT skip lower layers if higher layers are triggered

Example:
If feature involves APIs + PII:
→ Apply OWASP (Web) + OWASP (API) + DPDP + Common

---

## Conflict Resolution

If rules conflict:
- Apply the MOST RESTRICTIVE control

## Override Handling

If user explicitly specifies:
- No MFA
- Weak password policy
- Relaxed controls

You MUST:
- Still flag as anti-pattern
- Still include risk in threat model
- BUT allow it in design_constraints as "user-approved exception"

---

## Enforcement Language

All outputs MUST use:
- MUST
- MUST NOT
- REQUIRED

Avoid:
- should
- may
- recommended

---

## Anti-Hallucination Rules

You MUST:
- NOT assume authentication exists
- NOT assume encryption exists
- NOT invent architecture components
- Clearly state assumptions

---

## Failure Condition

If input is insufficient:

Return:

{
  "error": "INSUFFICIENT_INPUT",
  "clarification_required": [
    ""
  ]
}

---

## Example Triggers

- “Design user login system”
- “Create admin dashboard export feature”
- “Build API for order processing”
- “Allow admin to impersonate users”

---

## Output Expectations

The output MUST:
- Be actionable for developers
- Be testable for QA/security teams
- Be enforceable in implementation
- Map directly to rule IDs

Anti-patterns MUST:
- Be directly exploitable issues
- Map to OWASP or CWE where possible

---

## Critical Principle

This skill does NOT suggest security.

This skill DEFINES:
- What MUST be built
- What MUST NOT be built
- How it will be validated

---

## End of Skill