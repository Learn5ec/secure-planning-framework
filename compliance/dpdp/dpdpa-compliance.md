<!-- ============================================================
     DPDPA DISABLED
     This file is NOT loaded by the skill until further notice.
     DPDPA compliance is commented out pending org-wide implementation
     decision. Do not activate or reference these rules in any blueprint.
     To re-enable: set compliance.dpdp._disabled = false in activation_logic.json
     and remove this notice.
     ============================================================ -->

# Digital Personal Data Protection Act, 2023 — Extended Compliance Rules

---

# Rule ID: DPDP-012
## Title: Lawful Processing Basis Enforcement

**Source:** DPDP Act 2023  
**Category:** Legal Basis  

### Rule
Personal data MUST only be processed based on a valid lawful basis, primarily explicit consent or legitimate uses defined under the Act.

### Applies When
- Any personal data processing activity

### Validation
- Verify documented lawful basis for each processing activity
- Ensure consent or legitimate use is recorded

### Failure Impact
- Illegal data processing
- Regulatory penalties

---

# Rule ID: DPDP-013
## Title: Notice Requirement Before Consent

**Source:** DPDP Act 2023  
**Category:** Transparency  

### Rule
A clear and accessible notice MUST be provided to the user before obtaining consent, specifying:
- Data being collected
- Purpose of processing
- User rights

### Applies When
- Consent flows exist

### Validation
- Verify notice visibility before consent
- Ensure language is clear and accessible

### Failure Impact
- Invalid consent
- Legal non-compliance

---

# Rule ID: DPDP-014
## Title: Withdrawal of Consent Mechanism

**Source:** DPDP Act 2023  
**Category:** User Rights  

### Rule
Users MUST be able to withdraw consent as easily as it was given.

### Applies When
- Consent-based processing exists

### Validation
- Verify withdrawal option exists
- Ensure withdrawal triggers cessation of processing

### Failure Impact
- Continued unlawful processing

---

# Rule ID: DPDP-015
## Title: Cease Processing Upon Consent Withdrawal

**Source:** DPDP Act 2023  
**Category:** Data Lifecycle  

### Rule
All data processing activities MUST cease immediately upon withdrawal of consent unless legally required otherwise.

### Applies When
- Consent withdrawn

### Validation
- Trigger withdrawal and verify system behavior
- Ensure downstream systems also stop processing

### Failure Impact
- Unauthorized data usage

---

# Rule ID: DPDP-016
## Title: Special Handling for Children's Data

**Source:** DPDP Act 2023  
**Category:** Sensitive Data  

### Rule
Processing personal data of children MUST require verifiable parental consent and MUST NOT involve tracking, behavioral monitoring, or targeted advertising.

### Applies When
- Users under defined age threshold

### Validation
- Verify age-gating mechanism
- Validate parental consent workflow

### Failure Impact
- Severe regulatory penalties

---

# Rule ID: DPDP-017
## Title: Significant Data Fiduciary Obligations

**Source:** DPDP Act 2023  
**Category:** Governance  

### Rule
Entities classified as Significant Data Fiduciaries MUST:
- Appoint a Data Protection Officer (DPO)
- Conduct Data Protection Impact Assessments (DPIA)
- Implement periodic audits

### Applies When
- Large-scale or high-risk data processing

### Validation
- Verify DPO appointment
- Check DPIA documentation

### Failure Impact
- Non-compliance with enhanced obligations

---

# Rule ID: DPDP-018
## Title: Data Protection Impact Assessment (DPIA)

**Source:** DPDP Act 2023  
**Category:** Risk Management  

### Rule
High-risk data processing activities MUST undergo a Data Protection Impact Assessment before implementation.

### Applies When
- Processing sensitive or large-scale personal data

### Validation
- Verify DPIA existence
- Check risk mitigation measures

### Failure Impact
- Unidentified high-risk vulnerabilities

---

# Rule ID: DPDP-019
## Title: Cross-Border Data Transfer Restrictions

**Source:** DPDP Act 2023  
**Category:** Data Transfer  

### Rule
Personal data MUST only be transferred to jurisdictions approved by the government.

### Applies When
- Data stored or processed outside India

### Validation
- Verify data storage locations
- Check approved country list compliance

### Failure Impact
- Illegal data transfer

---

# Rule ID: DPDP-020
## Title: Data Processor Accountability

**Source:** DPDP Act 2023  
**Category:** Third-Party Management  

### Rule
Data fiduciaries MUST ensure that data processors adhere to the same data protection obligations.

### Applies When
- Third-party processors used

### Validation
- Review contracts and DPAs
- Verify processor security controls

### Failure Impact
- Indirect data breaches

---

# Rule ID: DPDP-021
## Title: Data Breach Notification to Users

**Source:** DPDP Act 2023  
**Category:** Incident Response  

### Rule
Affected users MUST be notified of a data breach in a timely and clear manner.

### Applies When
- Data breach occurs

### Validation
- Simulate breach and verify notification workflow

### Failure Impact
- User harm
- Legal penalties

---

# Rule ID: DPDP-022
## Title: Maintain Processing Records

**Source:** DPDP Act 2023  
**Category:** Accountability  

### Rule
Organizations MUST maintain records of:
- Data processing activities
- Consent logs
- Data sharing events

### Applies When
- Any data processing system

### Validation
- Verify audit logs
- Inspect processing records

### Failure Impact
- Lack of auditability

---

# Rule ID: DPDP-023
## Title: Data Retention Policy Disclosure

**Source:** DPDP Act 2023  
**Category:** Transparency  

### Rule
Users MUST be informed about how long their data will be retained.

### Applies When
- Data collection occurs

### Validation
- Check privacy notice
- Verify retention policy visibility

### Failure Impact
- Lack of transparency

---

# Rule ID: DPDP-024
## Title: Restrict Automated Decision-Making Impact

**Source:** DPDP Act 2023  
**Category:** Fair Processing  

### Rule
Automated decision-making systems MUST ensure fairness and MUST NOT negatively impact user rights without recourse.

### Applies When
- AI/automated systems process user data

### Validation
- Review decision logic
- Verify appeal mechanisms

### Failure Impact
- Unfair user impact

---

# Rule ID: DPDP-025
## Title: Data Erasure Upon Purpose Completion

**Source:** DPDP Act 2023  
**Category:** Data Lifecycle  

### Rule
Personal data MUST be erased once the purpose of processing is fulfilled.

### Applies When
- Purpose achieved

### Validation
- Verify deletion workflows
- Check archival systems

### Failure Impact
- Excess data retention

---

# Rule ID: DPDP-026
## Title: Secure Data Storage Localization Awareness

**Source:** DPDP Act 2023  
**Category:** Infrastructure  

### Rule
Systems MUST maintain awareness of where personal data is stored and processed at all times.

### Applies When
- Distributed/cloud systems

### Validation
- Verify data mapping
- Inspect infrastructure logs

### Failure Impact
- Loss of control over data

---

# Rule ID: DPDP-027
## Title: Prevent Dark Patterns in Consent

**Source:** DPDP Act 2023  
**Category:** UX Compliance  

### Rule
Consent mechanisms MUST NOT use deceptive patterns to manipulate user decisions.

### Applies When
- UI/UX for consent

### Validation
- Review UI flows
- Check for pre-ticked boxes or misleading wording

### Failure Impact
- Invalid consent

---

# Rule ID: DPDP-028
## Title: Grievance Officer Accessibility

**Source:** DPDP Act 2023  
**Category:** Governance  

### Rule
Details of the grievance officer MUST be clearly accessible to users.

### Applies When
- Public-facing systems

### Validation
- Verify visibility of contact details

### Failure Impact
- Compliance violation

---
