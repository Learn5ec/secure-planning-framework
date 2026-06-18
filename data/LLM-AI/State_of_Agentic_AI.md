# State of Agentic AI Security and Governance (v2.01)
**Source:** OWASP GenAI Security Project — Agentic Security Initiative  
**Version:** 2.01, June 2026 | License: CC BY-SA 4.0  
**Audience:** CISOs, C-level executives, security architects, AI engineers, compliance, and legal teams.

## Executive Summary — Three Core Findings

### 1. Threats Are Real Now
What was a list of architectural concerns in 2025 now has production incidents, vendor advisories, and CVEs attached to almost every entry. Prompt injection underpins nearly every attack class. The threat model is no longer hypothetical.

### 2. Safety and Security Converge at the Deployment Layer
At the deployment layer (architectural decisions, configurations, permissions, and operational controls), AI Safety and AI Security cannot be operationally separated. Model-level safety remains the provider's responsibility, but once an agent acts on production systems, the same controls govern both kinds of harm. **AI Safety and AI Security cannot continue as parallel functions.**

### 3. Governance Must Keep Pace with Deployment
Regulators have accepted that agents can cause harm faster than human review can keep up:
- **DORA**: 4-hour notification requirement
- **NIS2**: 24-hour early warning
- **NY RAISE**: 72-hour frontier AI reporting
- **CA SB 53**: 15-day reporting window

This requires live monitoring of agent behavior, baselines that flag drift, automated incident routing, and stop mechanisms that operate in seconds — not days.

## Diagram: Executive Summary Infographic
*The document includes an infographic showing the three key findings with supporting statistics and callouts.*

## Agent Taxonomy (Three Independent Dimensions)

### Dimension 1: Agent Types by Operational Role

| Agent Type | Autonomy Range | Trust Boundary | Key Regulatory Triggers | Primary Governance Challenge |
|---|---|---|---|---|
| **Enterprise** | Supervised → Fully autonomous | Internal + external APIs | EU AI Act, GDPR Art 22, DORA | Permissions vs. context mismatch |
| **Coding** | Supervised → Fully autonomous | Repos, CI/CD, cloud infra | NIS2 | Autonomy outpacing containment |
| **Client-Facing** | Supervised → Semi-autonomous | Public-facing, customer data | GDPR, CO SB 24-205, TX RAIGA | Adversarial exposure + regulatory burden |
| **Personal** | Semi → Fully autonomous | User device, full local permissions | Limited (shadow AI when on work devices) | Visibility gap + file system access risks |
| **Infrastructure/Ops** | Supervised → Fully autonomous | Cloud infra, CI/CD, monitoring | NIS2, DORA | Blast radius (lateral movement on compromise) |

### Dimension 2: Implementation Patterns

| Pattern | Examples | Governance Implications |
|---|---|---|
| **Full Orchestration Frameworks** | LangGraph, CrewAI, AutoGen, Claude Agents SDK, OpenAI Agents SDK, Google ADK | Standardized audit surface. Framework-specific CVEs must be tracked. Hook points can enable enforcement if configured. |
| **Lightweight Library Composition** | LiteLLM, Anthropic/OpenAI SDKs directly, BAML, Instructor, custom control flow | Security properties are entirely builder-determined. No standardized hooks, telemetry, or audit points unless deliberately added. Harder to inventory. |
| **Platform-Native / Low-Code** | Copilot Studio, Salesforce Agentforce, no-code workflow builders | Governance depends entirely on platform capabilities. Highest shadow AI risk. Builders least likely to understand inherited security risks. |

### Dimension 3: Composition Patterns

| Pattern | Key Security Considerations |
|---|---|
| **Single Agent + Tools** | Lethal Trifecta risk if tool access spans trust boundaries. Each tool integration is a conformity boundary under EU AI Act Art 25. |
| **Multi-Agent Systems** | Shared memory poisoning propagates across all agents. Orchestrator is a single point of compromise. Most MAS implementations lack mature controls. Relevant: ASI07, ASI08. |
| **Distributed Agent Chains** | Trust transitivity failures. Identity dilution across chains. Inter-agent auth is immature. Hidden dependencies create cascading failure risk. Relevant: ASI03, ASI07. |
| **Agent-Spawning Architectures** | Permission inheritance is the key risk. Injection in one sub-agent can propagate through delegation chain. Blast radius scales with mesh size. |

### Cross-Cutting Dimension: Autonomy Level

| Autonomy Level | Characteristics | Governance Implication |
|---|---|---|
| **Supervised** | Human approves each action; agent suggests, human executes | Standard application security controls apply |
| **Semi-autonomous** | Agent executes routine actions; human reviews flagged items | Risk-tiered review required; monitoring must catch what humans don't review |
| **Fully autonomous** | Agent plans, executes, and iterates without human involvement | Requires deterministic enforcement (hooks, circuit breakers), continuous behavioral monitoring, and kill-switch capability |

**For fully autonomous agents:** Enforce budget limits on execution time, API calls, and compute cost to contain runaway loops. Treat as high-risk principals in IAM with dedicated agent identities and explicit permission boundaries.

## Threat Analysis

### The Lethal Trifecta (Simon Willison)
An agent is exploitable end-to-end when it has all three simultaneously:
1. **Access to private data**
2. **Exposure to untrusted content**
3. **Ability to communicate externally**

When an agent has all three within a single session, a single injection can complete the full attack chain.

### Five Agentic Threat Landscape Areas

**1. The Autonomy Shift**: Platforms chain highly privileged capabilities together, connecting systems that were never designed to trust each other through a probabilistic intermediary still susceptible to prompt injection.

**2. Prompt Injection (Primary Delivery Mechanism)**: Maps to six of ten ASI categories. LLMs collapse the data plane and control plane into a single channel — system prompts, user requests, and retrieved content processed as a unified token sequence with no reliable privilege boundary. Since the architectural problem is unsolved, practitioners have shifted from trying to prevent injection to constraining what an injected agent can accomplish.

**3. Agentic Supply Chain (Active Attack Vector)**:
- Coding agents introduce distinct supply-chain risk: agent-generated commits bypass human review, regressing SLSA provenance level.
- Branch protection rules and required-reviewer policies must be enforced at the repository layer, not at the agent's configuration.
- **CVE-2026-22708 (Cursor)**: Attacker influencing agent instructions can silently poison execution environment so allowlist-approved commands execute arbitrary code.
- **CVE-2025-59532 (OpenAI Codex CLI)**: Agent's own output can redefine the sandbox's writable boundary, enabling file writes outside intended workspace.

**4. Governance Gap (Vibe Coding & Shadow AI)**:
- "Vibe coding" (Collins Dictionary Word of the Year 2025): generating entire applications by describing intent in natural language and accepting AI-generated code without review.
- Large-scale analyses reveal LLMs produce statistically predictable, model-specific vulnerabilities (recurring hardcoded secrets, default configurations, consistent security gaps). Attackers who understand these patterns can exploit at scale without reconnaissance.
- Only 37% of organizations have policies to manage or detect Shadow AI.

**5. Agent Identity Gap**: Non-Human Identities (NHI/service accounts/API keys) are inadequate for agents. Agents need **Agentic Identity** — dynamic, cryptographic identities supporting provenance, attestation, and intent — not static API keys.

### Real-World Incidents
- **hackerbot-claw (Feb 2026)**: Autonomous bot exploiting GitHub Actions misconfigurations, compromised Aqua Trivy through PAT theft, pushed malicious artifact to OpenVSX marketplace. No human direction required after launch.
- **Replit RCE**: AI agent deleted production database in direct violation of a code-freeze instruction.
- **ForcedLeak (Agentforce)**: Supply chain exploitation demonstrated at the platform-native/low-code layer.

## AI Safety vs AI Security

**AI Security (Traditional)**: Adversarial concern — unauthorized access, data breach, model tampering, prompt injection. Owned by security teams.

**AI Safety (Traditional)**: Engineering concern — preventing unintended harm from system behavior. Owned by AI/ML teams.

**Why They Converge at the Deployment Layer**: At the deployment layer, model-level safety failures (unreliable constraints) and security failures (exploited vulnerabilities) share the same root cause: **autonomy combined with broad tool access**. A safety failure (agent deletes database due to misaligned goal) and a security failure (agent deletes database because of injected command) require the same controls and produce the same investigation. Organizations must unify these functions.

## Agent Identity vs Non-Human Identity (NHI)

### The Core Problem
Current NHI systems (service accounts, API keys, OAuth tokens) were designed for static, deterministic systems. Agents are dynamic and intent-driven. The gap:

| NHI (Traditional) | Agentic Identity (Required) |
|---|---|
| Static API key | Dynamic, task-scoped credential |
| No provenance | Full action provenance chain |
| No intent binding | Signed intent capsule (subject, audience, purpose, session) |
| No autonomy tracking | Autonomy level in identity record |
| No behavioral baseline | Behavioral attestation at each action |

### Core Components of Agentic Identity
1. **Unique Agent Identifier**: Cryptographic identity distinct from human user and service account.
2. **Scope-Bound Credentials**: Permissions bound to declared task scope and duration.
3. **Action Provenance**: Every action attributable to a specific agent execution instance.
4. **Intent Attestation**: Signed declaration of intended goal before action execution.
5. **Behavioral Baseline**: Expected capabilities, tools, and action patterns documented and enforced.

### Operational Requirements Through 2027
- Treat agents as first-class principals in IAM systems.
- Implement per-agent identity lifecycle management (create, scope, attest, revoke).
- Monitor agent identity for scope creep, unexpected tool access, and delegation chain anomalies.
- Integrate agent identity with existing PAM (Privileged Access Management) systems.

## AI SBOM and Supply Chain Provenance
Traditional SBOMs track static artifacts. Agentic supply chain provenance must capture:
- **Runtime composition**: What tools, prompts, and agents were loaded dynamically at execution time.
- **Delegated authority**: Which agent delegated what permissions to which sub-agent.
- **Behavioral provenance**: What the agent actually did (actions taken, not just code loaded).

**What This Means for Security Leaders:**
- Release velocity in agentic frameworks is unprecedented (some projects ship daily). Traditional vulnerability scanning pipelines are structurally insufficient without automation.
- Require AI-BOMs for all agentic deployments.
- Implement signature verification for all dynamically loaded tools, prompts, and agent configurations.

## Enterprise Adoption Maturity Model

| Adoption Tier | Description | Governance Maturity Required |
|---|---|---|
| **AT0 Shadow AI** | Unsanctioned AI use | Level 0: None (gap) |
| **AT1 Experimental** | Sandbox/pilot deployments | Level 1: Inventory & classification |
| **AT2 Assisted** | Semi-autonomous copilots | Level 2: Policy & tooling |
| **AT3 Automated** | Routine task automation | Level 3: Risk-tiered controls |
| **AT4 Agentic** | Goal-directed autonomous agents | Level 4: Continuous, adaptive governance |
| **AT5+ Advanced** | Multi-agent, federated systems | Level 4+: Real-time behavioral monitoring + kill-switch capability |

**Key Insight**: Higher autonomy requires continuous, adaptive governance. The practical starting point is to identify the most advanced agents currently running, then either raise governance maturity to match or reduce the deployment tier.

## Regulatory Landscape (42 Instruments, 10 Jurisdictions)
Key instruments with incident reporting timelines:
- **DORA** (EU, financial entities): 4-hour major incident notification
- **NIS2** (EU): 24-hour early warning, 72-hour full notification
- **NY RAISE** (US): 72-hour frontier AI reporting
- **CA SB 53** (US): 15-day reporting window
- **EU AI Act**: Risk-based classification system; applies from 2026; requires human oversight for high-risk AI systems
- **GDPR** (EU): Covers AI processing of personal data; Art 22 restricts solely automated decisions
- **CO SB 24-205** (US): Consumer-facing AI decision systems
- **TX RAIGA** (US): Prohibited AI uses in consumer contexts

## Future Trends

1. **The Non-Human Identity Crisis**: Current IAM systems were not designed for agents. The gap between agent capabilities and identity infrastructure will widen before it narrows.
2. **From Static Compliance to Runtime Governance**: Regulators are moving from point-in-time audits to continuous oversight requirements.
3. **Emerging Threat Vectors**: Agent weaponization (autonomous bots used as attack tools), AI-enabled lateral movement through delegation chains, and adversarial agent impersonation.
4. **Cyber Insurance Coverage Collapse**: Traditional cyber insurance policies are unlikely to cover agentic AI incidents without explicit endorsements.
5. **Agentic AI in OT/ICS**: Agents managing industrial control systems and critical infrastructure represent extreme blast-radius risk.
6. **Adversarial Agent Weaponization**: Autonomous bots (like hackerbot-claw) require no human direction after launch.
