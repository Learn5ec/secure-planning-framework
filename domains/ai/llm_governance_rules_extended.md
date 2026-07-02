# LLM & AI Governance Security Rules
**Source:** OWASP Top 10 for LLM Applications — Cybersecurity & Governance Checklist (v1.1)  
**Audience:** Security teams, DevSecOps, MLSecOps, and engineering leads building or integrating LLM solutions.

> These rules apply when a feature builds on, integrates, or deploys a Large Language Model (LLM) or AI/ML system, whether custom-built or third-party (e.g., OpenAI, Anthropic, Google Gemini, open-source models).

> NOTE: These are ELEVATED and HIGH-ASSURANCE rules.

---

# Rule ID: LLM-GOV-001
## Title: Perform Threat Modeling for LLM Trust Boundaries
**Source:** LLM Security Checklist — Threat Modeling  
**Category:** Threat Modeling
**Risk Tier:** elevated

### Rule
Conduct dedicated threat modeling for ALL LLM components BEFORE integration or deployment. LLMs collapse the data and control planes into a single channel; conventional threat models do not capture this.

**Checks (Scale with Risk):**
1. How will attackers use GenAI to accelerate hyper-personalized spear-phishing attacks against employees, executives, or users? Plan defenses at scale.
2. Can the system detect and neutralize harmful or malicious inputs/queries to LLM solutions?
3. Are connections with existing systems and databases secured at ALL LLM trust boundaries?
4. Is there insider threat mitigation to prevent misuse by authorized users (including prompt manipulation to access unauthorized data)?
5. Can unauthorized access to proprietary models or training data be prevented (IP protection)?
6. Is automated content filtering in place to prevent generation of harmful or inappropriate content?
7. Model LLM components for: Prompt Injection, Sensitive Information Disclosure, Supply Chain Attacks, Data & Model Poisoning, Insecure Output Handling, Excessive Agency.

### Applies When
- Any feature integrates with an LLM API, hosts a model, or uses AI-generated content in workflows.

---

# Rule ID: LLM-GOV-002
## Title: Maintain an AI Asset Inventory (AI-BOM)
**Source:** LLM Security Checklist — AI Asset Inventory  
**Category:** Asset Management / Supply Chain
**Risk Tier:** elevated

### Rule
Catalog ALL AI/ML services and components used in the system, both internal and third-party.

**Controls (Scale with Risk):**
1. **Catalog** all existing AI services, tools, APIs, and their owners. Create a dedicated tag in asset management.
2. **Include AI components in the Software Bill of Materials (SBOM)**: All AI model dependencies, training data pipelines, and inference libraries must appear in the SBOM.
3. **Catalog AI data sources** and classify the sensitivity of data used (protected, confidential, public).
4. **Establish an AI onboarding process**: New AI services must go through security review before integration.
5. **Conduct pen testing or red teaming** of deployed AI solutions to determine the current attack surface risk.
6. **Shadow AI Detection**: Identify AI tools employees are using without IT approval. Only 37% of organizations have policies to manage or detect Shadow AI (Source: 2024 industry survey) — this is a critical gap.

### Applies When
- The feature introduces any new AI service, model API, or AI-generated content pipeline.

---

# Rule ID: LLM-GOV-003
## Title: Enforce LLM Input and Output Security
**Source:** LLM Security Checklist — Using/Implementing LLM Solutions  
**Category:** Input Validation / Output Handling
**Risk Tier:** elevated

### Rule
All inputs to and outputs from LLMs must be treated as untrusted and subjected to validation and sanitization.

**Controls (Scale with Risk):**
1. **Input Validation**: Evaluate and implement input validation methods. Validate all user inputs, retrieved content (RAG), and tool outputs before passing to the LLM.
2. **Output Filtering and Sanitization**: All LLM outputs must be filtered, sanitized, and approved before being used in downstream systems or presented to users.
3. **Access Control**: Implement least privilege access controls and defense-in-depth. LLM systems must only access data classified for the minimum access level of any user of the system.
4. **Training Pipeline Security**: Require rigorous control around training data governance, pipelines, models, and algorithms.
5. **Prompt Injection Safeguards**: Implement safeguards aligned with OWASP LLM01:2025 Prompt Injection Prevention Cheatsheet.
6. **Monitor for Injection Patterns**: Look into effects of prompt injection, release of sensitive information, and process manipulation. Log all such events.
7. **Investigate Model Attacks**: Identify the impact of model poisoning, improper data handling, supply chain attacks, and model theft on your threat model.

### Applies When
- Any feature passes user or external data to an LLM, or uses LLM output in business logic.

---

# Rule ID: LLM-GOV-004
## Title: AI Supply Chain Security
**Source:** LLM Security Checklist — Using/Implementing LLM Solutions  
**Category:** Supply Chain
**Risk Tier:** elevated

### Rule
Third-party AI models, APIs, and components are supply chain risks that must be actively managed.

**Controls (Scale with Risk):**
1. **Check for Existing Vulnerabilities**: Before integration, check for known vulnerabilities in the LLM model or supply chain (CVEs, security advisories).
2. **Third-Party Audits**: Request third-party audits, penetration testing, and code reviews for third-party AI providers — both initially and on an ongoing basis.
3. **Infrastructure Security**: Ask vendors how often they perform resilience testing and what their SLAs are for availability, scalability, and performance.
4. **Vendor EULA Review**: AI EULA agreements are fundamentally different — they govern user prompts, output rights, data privacy, compliance, and liability. Review carefully.
5. **Review AI-Assisted Code Development Tools**: A chatbot generating code may threaten the organization's ownership rights to its product. Assess IP ownership implications for all AI-generated code.

### Applies When
- The feature relies on any third-party AI model, API, or AI-powered tool (e.g., OpenAI API, GitHub Copilot, etc.).

---

# Rule ID: LLM-GOV-005
## Title: AI Governance and Accountability Framework
**Source:** LLM Security Checklist — Governance  
**Category:** Governance
**Risk Tier:** elevated

### Rule
Establish clear ownership, accountability, and policy for all AI systems.

**Controls (Scale with Risk):**
1. **Establish AI RACI Chart**: Define who is Responsible, Accountable, Consulted, and Informed for AI risk, assessments, and governance decisions.
2. **Data Management Policies**: Establish and technically enforce data classification and usage limitations. Models must only leverage data classified for the minimum access level of any user of the system. Data protection policy must explicitly prohibit inputting protected or confidential data into non-business-managed AI tools.
3. **Create an AI Policy**: Supported by established policies (standard of conduct, data protection, software use).
4. **Publish an Acceptable Use Matrix**: For all generative AI tools available to employees, defining permitted and prohibited uses.
5. **Document Data Sources**: Maintain documentation on all data sources and their management for any generative LLM models.
6. **Update Incident Response**: Update the Incident Response Plan and playbooks specifically for GenAI-enhanced attacks and AI-specific incidents.

### Applies When
- The team is deploying, managing, or integrating any AI/LLM feature into a product or internal tool.

---

# Rule ID: LLM-GOV-006
## Title: Continuous Testing, Evaluation, Verification, and Validation (TEVV)
**Source:** LLM Security Checklist — TEVV (NIST AI Framework)  
**Category:** Testing & Validation
**Risk Tier:** elevated

### Rule
Implement a continuous TEVV process across the AI system lifecycle, aligned with NIST AI Framework recommendations.

**Controls (Scale with Risk):**
1. **Continuous TEVV**: Establish continuous testing, evaluation, verification, and validation throughout the AI model lifecycle — not just at deployment.
2. **Include Application Testing, Source Code Review, Vulnerability Assessments, and Red Teaming** in the production release process for all AI features.
3. **Provide Regular Executive Metrics**: Track and report on AI Model functionality, security, reliability, and robustness.
4. **Recalibration and Monitoring**: Implement ongoing monitoring for model drift, behavioral changes, and security degradation over time.
5. **AI Red Teaming**: Conduct AI Red Team testing (adversarial attack simulation of the AI System) as a standard practice for AI models and applications. Required by NIST AI Framework and recommended by multiple regulatory bodies.
6. **Model Cards and Risk Cards**: Review model cards for all deployed models. Maintain and track model cards for any deployed model including models accessed through a third party. Establish a process to create and maintain risk cards documenting potential biases, privacy problems, and security vulnerabilities.

### Applies When
- Any AI model or LLM-based feature is deployed to production or significantly updated.

---

# Rule ID: LLM-GOV-007
## Title: Secure Retrieval-Augmented Generation (RAG) Implementation
**Source:** LLM Security Checklist — RAG: LLM Optimization  
**Category:** RAG Security
**Risk Tier:** elevated

### Rule
When using RAG to augment LLM capabilities, apply strict security controls to the retrieval pipeline and knowledge base.

**Controls (Scale with Risk):**
1. **Validate and sanitize all data** entering the RAG knowledge base. Treat all ingested content as potentially adversarial.
2. **Access Control on Retrieval**: Enforce context-aware access per task. Users should only retrieve documents they are authorized to access.
3. **Provenance Tracking**: Require source attribution for all retrieved content. Surface provenance to the model and to human reviewers.
4. **Prevent Bootstrap Poisoning**: Never automatically re-ingest the model's own generated outputs into the RAG knowledge base as authoritative data.
5. **Memory TTL and Decay**: Implement Time-To-Live (TTL) on stored vector embeddings. Expire and re-verify stale or low-trust entries.
6. **Namespace Isolation**: Use per-tenant or per-session namespaces in vector databases to prevent cross-tenant data bleed.
7. **Content Filtering on Retrieval Output**: Scan all retrieved chunks for sensitive or malicious content before passing to the LLM context.

### Applies When
- The feature uses Retrieval-Augmented Generation (RAG), vector databases, or semantic search to augment LLM responses.

---

# Rule ID: LLM-GOV-008
## Title: AI Regulatory Compliance Awareness
**Source:** LLM Security Checklist — Regulatory  
**Category:** Compliance
**Risk Tier:** elevated

### Rule
Evaluate and comply with applicable AI regulations based on jurisdiction and use case.

**Key Regulatory Instruments to Assess:**
- **EU AI Act**: First comprehensive AI law (applies from 2026). Risk-based classification (unacceptable, high, limited, minimal risk). Requires conformity assessments, transparency, and human oversight for high-risk AI systems.
- **GDPR (EU)**: Covers data collection, data security, fairness, transparency, accuracy, and accountability for AI systems processing personal data.
- > **INFORMATIONAL:** DORA sets phased notification windows for major incidents (e.g., initial notification by end of business day), not a flat 4-hour rule.
- **NIS2 (EU)**: 24-hour early warning requirement for significant incidents.
- **US State Laws (10 states, in effect by end of 2025)**: Include restrictions on electronic monitoring, employment-related automated decision systems (Vermont, CA, MD, NY, NJ), facial recognition, and AI video analysis (Illinois, MD, WA, VT).
- **NY RAISE**: 72-hour frontier AI reporting.
- **CA SB 53**: 15-day incident reporting window.

**Mandatory Compliance Checks:**
1. Determine country, state, or government-specific AI compliance requirements for your deployment context.
2. Determine compliance requirements for restricting electronic monitoring of employees and employment-related automated decision systems.
3. Confirm vendor compliance with applicable AI laws and best practices.
4. Review AI tools used for employee hiring or management for potential disparate treatment or disparate impact claims.
5. Ensure AI solutions do not collect or share sensitive information without proper consent or authorization.

### Applies When
- The feature uses AI for any user-facing decisions, employee management, hiring, or data processing involving personal data.

---

# Rule ID: LLM-GOV-009
## Title: AI Security and Privacy Training Requirements
**Source:** LLM Security Checklist — AI Security & Privacy Training  
**Category:** Training & Awareness
**Risk Tier:** elevated

### Rule
All personnel involved in building, deploying, or operating AI systems must receive appropriate security and privacy training.

**Mandatory Training Coverage:**
1. **All Users**: Ethics, responsibility, and legal issues (warranty, license, copyright). GenAI-related threats including voice cloning, image cloning, and spear-phishing.
2. **Developers and DevOps**: Secure AI deployment pipeline. AI safety and security assurances. How to incorporate LLM security with existing security controls (OWASP SAMM, ASVS, API Security).
3. **Security Teams**: LLM-specific attack vectors (prompt injection, model poisoning, jailbreaking). AI Red Teaming methodology. Mapping threats to MITRE ATT&CK and MITRE ATLAS.
4. **HR / Legal / Management**: EULA implications for AI tools. IP ownership of AI-generated content. Regulatory requirements for AI in hiring and employee management.
5. **Fair Use Policies**: Establish and communicate clear AI acceptable use policies with consequences for violations.

### Applies When
- Onboarding new team members to AI-enabled projects, or when introducing a new AI feature to an existing team.
