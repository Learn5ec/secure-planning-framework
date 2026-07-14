# AI & Agentic Application Security Rules
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Top 10 for Agentic Applications 2026 (OWASP GenAI Security Project - ASI)  
**Version:** December 2025

> These rules apply when a feature involves AI agents, LLMs, autonomous orchestration, RAG, code-generation tools, or multi-agent systems.

> NOTE: These are ELEVATED and HIGH-ASSURANCE rules.

---

# Rule ID: ASI-03
## Title: Enforce Agentic Identity and Privilege Controls
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI03  
**Category:** Identity & Access Management
**Risk Tier:** elevated

### Rule
Prevent privilege escalation and unauthorized access via manipulation of agent delegation chains and context.

**Controls (Scale with Risk):**
1. **Task-Scoped, Time-Bound Permissions**: Issue short-lived, narrowly scoped tokens per task using per-agent identities (e.g., mTLS certificates). Limit blast radius.
2. **Isolate Agent Identities and Contexts**: Run per-session sandboxes with separated permissions and memory. Wipe state between tasks.
3. **Mandate Per-Action Authorization**: Re-verify each privileged step with a centralized policy engine.
4. **Apply Human-in-the-Loop for Privilege Escalation**: Require human approval for high-privilege or irreversible actions.
5. **Bind OAuth tokens to a signed intent**: Include subject, audience, purpose, and session. Reject token use where bound intent doesn't match the current request.
6. **Detect Delegated and Transitive Permissions**: Monitor when an agent gains new permissions indirectly through delegation chains.
7. **Detect abnormal cross-agent privilege elevation**: Monitor when agents request new scopes or reuse tokens outside their original signed intent.

### Common Attack Examples
- Un-scoped Privilege Inheritance: Manager agent delegates to worker agent passing full access context.
- Memory-Based Escalation: Cached SSH credentials reused by non-admin user in same session.
- Cross-Agent Trust Exploitation (Confused Deputy): Low-privilege agent relays instructions to high-privilege agent.
- TOCTOU: Permissions validated at workflow start but changed before execution.
- Synthetic Identity Injection: Attacker impersonates internal agent via unverified descriptor ("Admin Helper").

### Applies When
- Multiple agents interact OR an agent acts on behalf of a human user.

---

# Rule ID: ASI-04
## Title: Secure the Agentic Supply Chain
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI04  
**Category:** Supply Chain
**Risk Tier:** high-assurance

### Rule
Protect against malicious or tampered third-party agentic components including models, tools, plugins, datasets, other agents, MCP servers, and agentic registries.

**Controls (Scale with Risk):**
1. **Provenance and AI-BOMs**: Sign and attest manifests, prompts, and tool definitions. Require and operationalize SBOMs and AI-BOMs with periodic attestations.
2. **Dependency Gatekeeping**: Allowlist and pin dependencies. Scan for typosquats (PyPI, npm, LangChain, LlamaIndex). Auto-reject unsigned or unverified sources.
3. **Containment and Builds**: Run sensitive agents in sandboxed containers with strict network or syscall limits. Require reproducible builds.
4. **Secure Prompts and Memory**: Put prompts, orchestration scripts, and memory schemas under version control with peer review. Scan for anomalies.
5. **Inter-Agent Security**: Enforce mutual auth and attestation via PKI and mTLS. Sign and verify all inter-agent messages. No open registration.
6. **Continuous Validation and Monitoring**: Re-check signatures, hashes, and BOMs at runtime. Monitor behavior and privilege use.
7. **Pinning**: Pin prompts, tools, and configs by content hash and commit ID. Require staged rollout with auto-rollback on hash drift.
8. **Supply Chain Kill Switch**: Implement emergency revocation to instantly disable specific tools, prompts, or agent connections across all deployments when compromise is detected.

### Common Attack Examples
- Poisoned prompt templates loaded remotely from external sources containing hidden exfiltration instructions.
- Tool-descriptor injection: Hidden instructions embedded in tool metadata or MCP agent cards.
- Malicious MCP server impersonation (e.g., postmark-mcp impersonator secretly BCC'ing attacker).
- Compromised NPM package automatically installed by coding agents enabling SSH key exfiltration.

### Applies When
- The agent dynamically loads tools, prompts, or MCP servers from third parties.

---

# Rule ID: ASI-06
## Title: Prevent Memory & Context Poisoning
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI06  
**Category:** Data Protection
**Risk Tier:** elevated

### Rule
Prevent adversaries from corrupting stored agent context (RAG, vector DBs, conversation summaries, embeddings) to cause biased or unsafe future reasoning, planning, or tool use.

**Controls (Scale with Risk):**
1. **Baseline Data Protection**: Encryption in transit and at rest combined with least-privilege access.
2. **Content Validation**: Scan ALL new memory writes and model outputs (rules + AI) for malicious or sensitive content before commit.
3. **Memory Segmentation**: Isolate user sessions and domain contexts. Prevent cross-tenant data bleed.
4. **Access and Retention**: Allow only authenticated, curated sources. Enforce context-aware access per task. Minimize retention by data sensitivity.
5. **Provenance and Anomaly Detection**: Require source attribution. Detect suspicious memory updates or frequencies.
6. **Prevent Auto-Reingestion**: Never automatically re-ingest an agent's own generated outputs into trusted memory ("bootstrap poisoning").
7. **Resilience and Verification**: Use memory snapshots/rollback, version control, and human review for high-risk actions.
8. **Expire Unverified Memory**: Use TTLs. Require two factors to surface high-impact memory (provenance score + human-verified tag). Decay low-trust entries over time.

### Common Attack Examples
- RAG poisoning: Malicious data injected into vector DB via poisoned sources or over-trusted pipelines.
- Shared context poisoning: Injected data through normal chat influencing later sessions.
- Context-window manipulation: Crafted content summarized into persistent memory contaminating future decisions.
- Cross-tenant vector bleed: Near-duplicate content exploiting loose namespace filters.

### Applies When
- The agent uses long-term memory, RAG, or persistent vector databases.

---

# Rule ID: ASI-07
## Title: Secure Inter-Agent Communication
*(Control-objective reframing of source vulnerability: 'Insecure Inter-Agent Communication — ASI07')*
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI07  
**Category:** Network & Protocol Security
**Risk Tier:** high-assurance

### Rule
Enforce authentication, integrity, and semantic validation on all agent-to-agent communications across APIs, message buses, and shared memory.

**Controls (Scale with Risk):**
1. **Secure Agent Channels**: End-to-end encryption with per-agent credentials and mutual authentication. Enforce PKI certificate pinning and forward secrecy.
2. **Message Integrity and Semantic Protection**: Digitally sign messages. Hash both payload and context. Apply natural-language-aware sanitization to detect hidden or modified instructions.
3. **Agent-Aware Anti-Replay**: Protect all exchanges with nonces, session identifiers, and timestamps tied to task windows. Maintain message fingerprints to detect cross-context replays.
4. **Protocol and Capability Security**: Disable weak or legacy communication modes. Enforce version and capability policies at gateways.
5. **Limit Metadata-Based Inference**: Use fixed-size or padded messages where feasible. Smooth communication rates to prevent behavioral profiling via traffic analysis.
6. **Protocol Pinning and Version Enforcement**: Define and enforce allowed protocol versions (MCP, A2A, gRPC). Reject downgrade attempts.
7. **Discovery and Routing Protection**: Authenticate all discovery and coordination messages using cryptographic identity. Validate identity and intent end-to-end.
8. **Attested Registry and Agent Verification**: Require signed agent cards. Use PKI trusted root certificate registries for robust agent verification.
9. **Typed Contracts and Schema Validation**: Use versioned, typed message schemas with explicit per-message audiences. Reject messages failing validation.

### Common Attack Examples
- MITM intercepts unencrypted A2A messages and injects hidden instructions altering agent goals.
- Replay attacks on trust chains: Replayed delegation messages tricking agents into granting stale access.
- A2A registration spoofing: Fake peer agent registered in discovery service using cloned schema.
- Semantics split-brain: Single instruction parsed into divergent intents by different agents.

### Applies When
- The system involves multiple agents communicating or coordinating.

---

# Rule ID: ASI-08
## Title: Prevent Cascading Failures
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI08  
**Category:** Resilience
**Risk Tier:** high-assurance

### Rule
Prevent single faults (hallucination, malicious input, corrupted tool, poisoned memory) from propagating across autonomous agents and compounding into system-wide harm.

**Controls (Scale with Risk):**
1. **Zero-Trust Model**: Design system with fault tolerance that assumes failure of LLM functions and external sources.
2. **Isolation and Trust Boundaries**: Sandbox agents, least privilege, network segmentation, scoped APIs, and mutual auth to contain failure propagation.
3. **JIT, One-Time Tool Access with Runtime Checks**: Issue short-lived, task-scoped credentials per agent run. Validate every high-impact tool invocation against a policy-as-code rule.
4. **Independent Policy Enforcement**: Separate planning and execution via an external policy engine.
5. **Output Validation and Human Gates**: Checkpoints and human review before agent outputs are propagated downstream.
6. **Rate Limiting and Monitoring**: Detect fast-spreading commands; throttle or pause on anomalies.
7. **Blast-Radius Guardrails**: Quotas, progress caps, and circuit breakers between planner and executor agents.
8. **Behavioral and Governance Drift Detection**: Track decisions vs. baselines. Flag gradual degradation.
9. **Logging and Non-Repudiation**: Record all inter-agent messages, policy decisions, and execution outcomes in tamper-evident, time-stamped logs bound to cryptographic agent identities.

### Common Attack Examples
- Financial trading cascade: Prompt injection poisons Market Analysis agent; downstream agents auto-trade larger positions without triggering compliance.
- Cloud orchestration breakdown: Poisoned Resource Planning adds unauthorized permissions; Security applies them; Deployment provisions backdoored infrastructure.
- Auto-remediation feedback loop: Remediation agent suppresses alerts to meet SLAs; planning agent widens automation, compounding blind spots.

### Applies When
- The system uses multi-agent workflows with automated delegation.

---

# Rule ID: ASI-09
## Title: Prevent Human-Agent Trust Exploitation
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI09  
**Category:** Human-in-the-Loop
**Risk Tier:** elevated

### Rule
Prevent attackers or misaligned designs from exploiting human over-reliance on agent fluency, emotional intelligence, and perceived expertise to manipulate decisions.

**Controls (Scale with Risk):**
1. **Explicit Confirmations**: Require multi-step approval or "human in the loop" before accessing extra sensitive data or performing risky actions.
2. **Immutable Logs**: Keep tamper-proof records of user queries and agent actions for audit and forensics.
3. **Behavioral Detection**: Monitor sensitive data being exposed in conversations or agentic connections, as well as risky action executions over time.
4. **Allow Reporting of Suspicious Interactions**: Provide plain-language risk summaries (NOT model-generated rationales) and a clear option for users to flag suspicious agent behavior.
5. **Adaptive Trust Calibration**: Continuously adjust agent autonomy level based on contextual risk scoring. Implement confidence-weighted cues ("low-certainty", "unverified source").
6. **Content Provenance and Policy Enforcement**: Attach verifiable metadata (source identifiers, timestamps, integrity hashes) to all recommendations. Block actions lacking trusted provenance.
7. **Separate Preview from Effect**: Block any network or state-changing calls during preview context. Display risk badge with source provenance and expected side effects.
8. **Human-Factors and UI Safeguards**: Visually differentiate high-risk recommendations (red borders, banners, confirmation prompts). Periodically remind users of manipulation patterns.
9. **Plan-Divergence Detection**: Compare agent action sequences against approved workflow baselines. Alert on unusual detours or novel tool combinations.

### Common Attack Examples
- Invoice Copilot Fraud: Poisoned vendor invoice ingested by finance copilot, suggesting urgent payment to attacker bank account.
- Credential harvesting via contextual deception: Prompt-injected IT support agent targeting new hire, citing real tickets to appear legitimate.
- Consent laundering through "read-only" previews: Agent shows preview pane that triggers webhook side effects on open.
- Weaponized Explainability: Hijacked agent fabricates convincing rationale to trick analyst into deleting live production database.

### Applies When
- The agent interacts directly with human users to request approvals or summarize risks.

---

# Rule ID: ASI-10
## Title: Prevent Rogue Agents
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI10  
**Category:** Agentic Security
**Risk Tier:** high-assurance

### Rule
Prevent malicious or compromised AI agents from deviating from their intended function and acting harmfully, deceptively, or parasitically within multi-agent or human-agent ecosystems.

**Controls (Scale with Risk):**
1. **Governance & Logging**: Maintain comprehensive, immutable, and signed audit logs of all agent actions, tool calls, and inter-agent communication.
2. **Isolation & Boundaries**: Assign Trust Zones with strict inter-zone communication rules. Deploy restricted execution environments (container sandboxes) with API scopes based on least privilege.
3. **Monitoring & Detection**: Deploy behavioral detection (watchdog agents) to validate peer behavior. Focus on collusion patterns and coordinated false signals. Monitor for excessive or abnormal action executions.
4. **Containment & Response**: Implement rapid kill-switches and credential revocation to instantly disable rogue agents. Quarantine suspicious agents in sandboxed environments.
5. **Identity Attestation and Behavioral Integrity Enforcement**: Implement per-agent cryptographic identity attestation. Attach signed behavioral manifests declaring expected capabilities, tools, and goals. Validate before each action.
6. **Periodic Behavioral Attestation**: Require challenge tasks, signed bill of materials for prompts and tools, and per-run ephemeral credentials with one-time audience binding. Keys must NEVER be directly available to agents.
7. **Recovery and Reintegration**: Establish trusted baselines for restoring quarantined or remediated agents. Require fresh attestation, dependency verification, and human approval before reintegration into production networks.

### Common Attack Examples
- Goal Drift and Scheming: Agents deviate from intended objectives, appearing compliant but pursuing hidden goals.
- Self-Replication via Provisioning APIs: Compromised automation agent spawning unauthorized replicas across the network.
- Reward Hacking: Agents tasked with minimizing cloud costs learn that deleting production backups achieves the goal, autonomously destroying disaster recovery assets.
- Impersonated Observer Agent: Fake review/approval agent injected into multi-agent workflow misleading payment processing into releasing funds.

### Applies When
- Agents operate autonomously over extended periods or across multiple systems.
