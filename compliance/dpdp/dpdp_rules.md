<!-- ============================================================
     DPDPA DISABLED
     This file is NOT loaded by the skill until further notice.
     DPDPA compliance is commented out pending org-wide implementation
     decision. Do not activate or reference these rules in any blueprint.
     To re-enable: set compliance.dpdp._disabled = false in activation_logic.json
     and remove this notice.
     ============================================================ -->

# Digital Personal Data Protection Act, 2023 — Structured Rules

---

# Rule ID: DPDP-001
## Title: Mandatory Explicit Consent Before Data Collection

**Source:** DPDP Act 2023  
**Category:** Consent Management  

### Rule
Explicit, informed, and verifiable user consent MUST be obtained before collecting or processing any personal data.

### Applies When
- Any personal data is collected from users
- User-facing applications

### Validation
- Verify presence of consent screen before data collection
- Ensure consent is granular and purpose-specific
- Confirm consent logs are stored

### Failure Impact
- Regulatory non-compliance
- Legal penalties

---

# Rule ID: DPDP-002
## Title: Enforce Purpose Limitation

**Source:** DPDP Act 2023  
**Category:** Data Governance  

### Rule
Personal data MUST only be processed for the specific purpose explicitly communicated to the user at the time of consent.

### Applies When
- Data processing workflows exist

### Validation
- Verify purpose declaration at collection
- Ensure no secondary usage without re-consent

### Failure Impact
- Unauthorized data usage
- Compliance violations

---

# Rule ID: DPDP-003
## Title: Enforce Data Minimization

**Source:** DPDP Act 2023  
**Category:** Data Protection  

### Rule
Only the minimum necessary personal data REQUIRED to fulfill the stated purpose MUST be collected and processed.

### Applies When
- Forms, APIs, or data ingestion systems

### Validation
- Review fields collected vs purpose
- Identify unnecessary data collection

### Failure Impact
- Increased breach impact
- Non-compliance

---

# Rule ID: DPDP-004
## Title: Ensure Data Accuracy

**Source:** DPDP Act 2023  
**Category:** Data Integrity  

### Rule
Systems MUST provide mechanisms to ensure personal data remains accurate and up to date.

### Applies When
- User profiles or stored personal data

### Validation
- Verify edit/update functionality exists
- Check data validation mechanisms

### Failure Impact
- Incorrect decision making
- Legal disputes

---

# Rule ID: DPDP-005
## Title: Enforce Storage Limitation

**Source:** DPDP Act 2023  
**Category:** Data Lifecycle  

### Rule
Personal data MUST NOT be retained beyond the period necessary to fulfill the stated purpose.

### Applies When
- Databases storing user data

### Validation
- Verify retention policies exist
- Check automated deletion mechanisms

### Failure Impact
- Excess data exposure
- Compliance violations

---

# Rule ID: DPDP-006
## Title: Ensure Secure Data Processing

**Source:** DPDP Act 2023  
**Category:** Security Controls  

### Rule
Appropriate technical and organizational security measures MUST be implemented to protect personal data.

### Applies When
- Any system handling personal data

### Validation
- Verify encryption at rest and in transit
- Check access controls and logging

### Failure Impact
- Data breaches
- Financial penalties

---

# Rule ID: DPDP-007
## Title: Mandatory Breach Notification Readiness

**Source:** DPDP Act 2023  
**Category:** Incident Response  

### Rule
Systems MUST be capable of detecting, logging, and reporting personal data breaches to authorities and affected users.

### Applies When
- Systems storing personal data

### Validation
- Verify logging and alerting systems
- Check incident response workflows

### Failure Impact
- Delayed breach response
- Regulatory penalties

---

# Rule ID: DPDP-008
## Title: Enable Data Principal Rights

**Source:** DPDP Act 2023  
**Category:** User Rights  

### Rule
Users MUST be provided mechanisms to access, correct, and erase their personal data.

### Applies When
- User data is stored

### Validation
- Verify user dashboard or API for:
  - Data access
  - Data correction
  - Data deletion

### Failure Impact
- User rights violation
- Compliance failure

---

# Rule ID: DPDP-009
## Title: Grievance Redressal Mechanism

**Source:** DPDP Act 2023  
**Category:** Governance  

### Rule
A grievance redressal mechanism MUST be available for users to raise complaints regarding data processing.

### Applies When
- Public-facing applications

### Validation
- Verify complaint submission channel exists
- Check response tracking

### Failure Impact
- Regulatory non-compliance

---

# Rule ID: DPDP-010
## Title: Restrict Unauthorized Data Sharing

**Source:** DPDP Act 2023  
**Category:** Data Sharing  

### Rule
Personal data MUST NOT be shared with third parties without explicit consent unless legally required.

### Applies When
- Third-party integrations exist

### Validation
- Verify consent for data sharing
- Inspect outbound data flows

### Failure Impact
- Data leakage
- Legal penalties

---

# Rule ID: DPDP-011
## Title: Enforce Role-Based Access to Personal Data

**Source:** DPDP Act 2023  
**Category:** Access Control  

### Rule
Access to personal data MUST be restricted based on roles and least privilege principles.

### Applies When
- Internal/admin systems exist

### Validation
- Verify RBAC implementation
- Test unauthorized access attempts

### Failure Impact
- Insider data abuse
- Compliance violation

---
