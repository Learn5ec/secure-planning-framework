# LLM & AI Governance Security Rules
**Source:** OWASP Top 10 for LLM Applications — Cybersecurity & Governance Checklist (v1.1)  
**Audience:** Security teams, DevSecOps, MLSecOps, and engineering leads building or integrating LLM solutions.

> These rules apply when a feature builds on, integrates, or deploys a Large Language Model (LLM) or AI/ML system, whether custom-built or third-party (e.g., OpenAI, Anthropic, Google Gemini, open-source models).

---

# Rule ID: LLM-GOV-001
## Title: Perform Threat Modeling for LLM Trust Boundaries
**Source:** LLM Security Checklist — Threat Modeling  
**Category:** Threat Modeling
**Risk Tier:** baseline

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

# Rule ID: LLM-GOV-003
## Title: Enforce LLM Input and Output Security
**Source:** LLM Security Checklist — Using/Implementing LLM Solutions  
**Category:** Input Validation / Output Handling
**Risk Tier:** baseline

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

# Rule ID: LLM-GOV-007
## Title: Secure Retrieval-Augmented Generation (RAG) Implementation
**Source:** LLM Security Checklist — RAG: LLM Optimization  
**Category:** RAG Security
**Risk Tier:** baseline

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

# Rule ID: LLM-GOV-009
## Title: AI Security and Privacy Training Requirements
**Source:** LLM Security Checklist — AI Security & Privacy Training  
**Category:** Training & Awareness
**Risk Tier:** baseline

### Rule
All personnel involved in building, deploying, or operating AI systems must receive appropriate security and privacy training.

**Training Coverage (Scale with Risk):**
1. **All Users**: Ethics, responsibility, and legal issues (warranty, license, copyright). GenAI-related threats including voice cloning, image cloning, and spear-phishing.
2. **Developers and DevOps**: Secure AI deployment pipeline. AI safety and security assurances. How to incorporate LLM security with existing security controls (OWASP SAMM, ASVS, API Security).
3. **Security Teams**: LLM-specific attack vectors (prompt injection, model poisoning, jailbreaking). AI Red Teaming methodology. Mapping threats to MITRE ATT&CK and MITRE ATLAS.
4. **HR / Legal / Management**: EULA implications for AI tools. IP ownership of AI-generated content. Regulatory requirements for AI in hiring and employee management.
5. **Fair Use Policies**: Establish and communicate clear AI acceptable use policies with consequences for violations.

### Applies When
- Onboarding new team members to AI-enabled projects, or when introducing a new AI feature to an existing team.
