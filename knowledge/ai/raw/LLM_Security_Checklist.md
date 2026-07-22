# LLM AI Cybersecurity & Governance Checklist
**Source:** OWASP Top 10 for LLM Applications — Cybersecurity and Governance Checklist v1.1  
**Author:** Sandy Dunn & OWASP LLM Team | License: CC BY-SA 4.0

## Who Is This For?
Leaders across executive, tech, cybersecurity, privacy, compliance, and legal areas; DevSecOps, MLSecOps, and Cybersecurity teams and defenders. Intended for people striving to stay ahead in the fast-moving AI world, aiming to leverage AI for corporate success while protecting against risks of hasty or insecure AI implementations.

## Key LLM Challenges
- **Control/Data Plane Collapse**: Unlike traditional software, LLMs cannot strictly isolate the control and data planes. System prompts, user requests, and retrieved content are all processed as a unified token sequence.
- **Non-determinism**: LLMs yield different outcomes when prompted the same way. Semantic search rather than keyword search fundamentally changes reliability.
- **Hallucinations**: LLMs generate plausible-sounding but factually incorrect content due to training gaps.
- **Expanded Attack Surface**: LLM use increases the organizational attack surface. Familiar issues (SBOM, supply chain, DLP, access control) amplified alongside new AI-specific risks.
- **Adversarial LLM Use**: Attackers use LLMs to craft novel malware (potentially with zero-day vulnerabilities), sophisticated spear-phishing, convincing deepfakes (video/audio), and to accelerate intrusion development.

## Diagram: Pillars of Trustworthy AI
*The document includes a tree diagram showing Trustworthy AI branching into:*
- **Reliable**: Robust, Accountable, Monitored, Transparent, Explainable
- **Resilient**: Safe, Secure, Private, Effective
- **Responsible**: Fair, Ethical, Inclusive, Sustainable, Purposeful

## Diagram: LLM Threat Categories
*The document includes a web diagram illustrating the major AI threat categories.*

## Diagram: Deployment Strategy Options (Lowest to Highest Effort/Risk)
1. **Public Consumer Applications** (ChatGPT, Claude, Gemini) — lowest effort, least control
2. **Enterprise APIs** (OpenAI API, Anthropic API) — moderate effort, some control
3. **Fine-Tuned Models** — higher effort, domain-specific optimization
4. **Privately Hosted Open-Source Models** (Llama, Mistral) — high effort, full control
5. **Proprietary Custom Models** (trained from scratch) — highest effort/risk, maximum control

## Diagram: OWASP Top 10 for LLM Applications
*The document includes an infographic of all 10 LLM risks:*
1. LLM01 Prompt Injection
2. LLM02 Sensitive Information Disclosure
3. LLM03 Supply Chain Vulnerabilities
4. LLM04 Data and Model Poisoning
5. LLM05 Improper Output Handling
6. LLM06 Excessive Agency
7. LLM07 System Prompt Leakage
8. LLM08 Vector and Embedding Weaknesses
9. LLM09 Misinformation
10. LLM10 Unbounded Consumption

## The Shadow AI Problem
The most pressing non-adversarial LLM threat is "Shadow AI" — employees using unapproved online AI tools, unsafe browser plugins, and third-party applications that introduce LLM features without IT approval. Surveys indicate ~50% of employees use AI tools not sanctioned by their employer. IBM's Cost of a Data Breach Report confirms organizations with significant shadow AI face materially higher breach costs and longer detection times. Only 37% of organizations have policies to manage or detect Shadow AI.

## Full Checklist Summary

### Adversarial Risk
- Investigate how competitors invest in AI and what that means for market position.
- Investigate the impact of current controls (e.g., voice recognition password resets) which may no longer be sufficient against GenAI-enhanced attacks.
- Update Incident Response Plan and playbooks for GenAI-enhanced attacks and AI-specific incidents.

### Threat Modeling
- How will attackers accelerate exploit attacks? Anticipate hyper-personalized attacks at scale using GenAI.
- How could GenAI be used for attacks on customers through spoofing or AI-generated content?
- Can the business detect and neutralize harmful/malicious inputs or queries to LLM solutions?
- Secure connections with existing systems and databases at all LLM trust boundaries.
- Implement insider threat mitigation to prevent misuse by authorized users.
- Prevent unauthorized access to proprietary models or data (IP protection).
- Implement automated content filtering to prevent generation of harmful content.

### AI Asset Inventory
- Catalog AI services, tools, and owners with dedicated asset management tags.
- Include AI components in SBOM.
- Catalog AI data sources and their sensitivity classification.
- Establish pen testing or red teaming of deployed AI solutions.
- Create an AI solution onboarding process.

### AI Security and Privacy Training
- Train all users on ethics, responsibility, legal issues (warranty, license, copyright).
- Update security awareness to include GenAI threats (voice cloning, image cloning, spear-phishing).
- Training for DevOps and security teams on AI deployment pipeline safety.

### Governance
- Establish AI RACI chart (Responsible, Accountable, Consulted, Informed).
- Document and assign AI risk, risk assessments, and governance responsibility.
- Establish data management policies: Models should only leverage data classified for the minimum access level of any user.
- Create an AI Policy supported by established policy.
- Publish an acceptable use matrix for AI tools.
- Document sources and management of any generative LLM model data.

### Legal
- Confirm product warranties are clear for AI components.
- Review and update terms and conditions for GenAI considerations.
- Review AI EULA agreements (handle user prompts, output rights, data privacy, compliance, liability differently from standard software).
- Modify end-user agreements to prevent liabilities related to plagiarism, bias propagation, or IP infringement through AI-generated content.
- Review risks to IP from AI-generated code (chatbot-generated code may threaten ownership rights).
- Review contracts with indemnification provisions for AI use.
- Review liability for potential injury and property damage caused by AI systems.
- Review insurance coverage (traditional D&O and commercial general liability insurance may be insufficient).
- Ensure agreements for contractors covering appropriate use of AI.

### Regulatory
- Determine country/state/government-specific AI compliance requirements.
- Compliance requirements for electronic monitoring restrictions (Vermont, California, Maryland, New York, New Jersey).
- Compliance for facial recognition and AI video analysis (Illinois, Maryland, Washington, Vermont).
- Confirm vendor compliance with applicable AI laws and best practices.
- Document AI tool usage in hiring processes (training methodology, monitoring, corrections for bias).

### Using/Implementing LLM Solutions
- Threat model LLM components and architecture trust boundaries.
- Verify data classification and protection (personal and proprietary business data).
- Implement least privilege access controls and defense-in-depth.
- Require rigorous control around training data governance, pipelines, models, algorithms.
- Evaluate input validation methods and output filtering/sanitization/approval.
- Map workflows, monitoring, and responses for automation, logging, and auditing.
- Include application testing, source code review, vulnerability assessments, and red teaming in production release.
- Check for existing vulnerabilities in LLM model or supply chain.
- Investigate prompt injection, sensitive information release, and process manipulation impacts.
- Investigate model poisoning, improper data handling, supply chain attacks, and model theft impacts.
- Request third-party audits, penetration testing, and code reviews for third-party providers (initial and ongoing).
- Ask vendors about resilience testing frequency and SLAs.
- Update incident response playbooks and include LLM incidents in tabletop exercises.

### TEVV (Testing, Evaluation, Verification, Validation)
- Establish continuous TEVV throughout the AI model lifecycle (NIST AI Framework).
- Provide regular executive metrics on AI Model functionality, security, reliability, and robustness.

### Model Cards and Risk Cards
- Review a model's model card and risk card (if available) before deployment.
- Establish a process to track and maintain model cards for any deployed model.
- Key model card attributes: model details, architecture, training data/methodology, performance metrics, potential biases/limitations, responsible AI considerations.

### RAG (Retrieval-Augmented Generation)
- RAG provides efficient, transparent LLM optimization by retrieving pertinent data from up-to-date knowledge sources.
- Secure the embedding model deployment and indexing pipeline.
- Apply access controls, provenance tracking, and TTL to the vector database.

### AI Red Teaming
- Incorporate Red Team testing as a standard practice for AI Models and applications.
- Required by many regulatory and AI governing bodies including NIST.
- Red teaming alone is not comprehensive — combine with algorithmic impact assessments and external audits.

## Key Resources Referenced
- **MITRE ATT&CK**: Map LLM security threats to adversary tactics and techniques.
- **MITRE ATLAS**: Knowledge base of adversary tactics against ML systems.
- **OWASP SAMM**: Software Assurance Maturity Model for secure development lifecycle.
- **OWASP AI Security and Privacy Guide**: Comprehensive AI security and privacy considerations.
- **OWASP CycloneDX / AI-BOM**: Bill of Materials standard for AI supply chain transparency.
- **OWASP ASVS**: Application Security Verification Standard for web security requirements.
- **OWASP ML Security Top 10**: Security issues specific to ML systems.
