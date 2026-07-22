# AI & Agentic Application Security Rules
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Top 10 for Agentic Applications 2026 (OWASP GenAI Security Project - ASI)  
**Version:** December 2025

> These rules apply when a feature involves AI agents, LLMs, autonomous orchestration, RAG, code-generation tools, or multi-agent systems.

---

# Rule ID: ASI-01
## Title: Prevent Agent Goal Hijack
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI01  
**Category:** Agentic Security
**Risk Tier:** baseline

### Rule
Treat ALL natural-language inputs (user prompts, uploaded documents, retrieved RAG content, emails, calendar invites, tool outputs, peer-agent messages) as untrusted. Route all inputs through prompt-injection safeguards before they can influence goal selection, planning, or tool calls.

**Controls (Scale with Risk):**
1. Enforce least privilege for agent tools; require human approval for high-impact or goal-changing actions.
2. Define and lock agent system prompts so that goal priorities and permitted actions are explicit and auditable. Changes must go through configuration management and human approval.
3. At runtime, validate both user intent AND agent intent before executing goal-changing or high-impact actions. Pause or block execution on any unexpected goal shift.
4. When applicable, evaluate "intent capsules" — a pattern to bind the declared goal, constraints, and context to each execution cycle in a signed envelope.
5. Sanitize and validate all connected data sources (RAG, emails, uploaded files, external APIs) using CDR, prompt-carrier detection, and content filtering before the data can influence agent goals.
6. Maintain comprehensive logging and behavioral baseline monitoring including goal state and tool-use patterns. Alert immediately on unexpected goal changes.
7. Incorporate AI Agents into the Insider Threat Program to monitor insider prompts intended to alter agent behavior.

### Common Attack Examples
- Indirect Prompt Injection via hidden instructions in web pages or documents in RAG scenarios silently redirect agents to exfiltrate data.
- Malicious prompt override manipulates a financial agent into unauthorized transfers.
- Goal-lock drift via scheduled calendar invites injecting recurring "quiet mode" instructions.

### Applies When
- The agent processes external untrusted input OR can dynamically select its goals or tools.

---

# Rule ID: ASI-02
## Title: Prevent Tool Misuse and Exploitation
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI02  
**Category:** Agentic Security
**Risk Tier:** baseline

### Rule
Implement strict controls to prevent agents from misusing legitimate tools. Risks arise from prompt injection, misalignment, or unsafe delegation in tool orchestration.

**Controls (Scale with Risk):**
1. **Least Agency and Least Privilege for Tools**: Define per-tool least-privilege profiles (scopes, max rate, egress allowlists). Read-only queries for databases; no send/delete rights for email summarizers; minimal CRUD for APIs.
2. **Action-Level Authentication and Approval**: Require explicit authentication per tool invocation and human confirmation for high-impact or destructive actions (delete, transfer, publish). Display pre-execution dry-run diff.
3. **Execution Sandboxes and Egress Controls**: Run tool execution in isolated sandboxes. Enforce outbound allowlists; deny all non-approved network destinations.
4. **Policy Enforcement Middleware ("Intent Gate")**: Treat LLM/planner outputs as untrusted. A pre-execution Policy Enforcement Point (PEP/PDP) validates intent, enforces schemas and rate limits, and issues short-lived credentials.
5. **Adaptive Tool Budgeting**: Apply usage ceilings (cost, rate, token budgets) with automatic revocation or throttling when exceeded.
6. **Just-in-Time and Ephemeral Access**: Grant temporary credentials or API tokens that expire immediately after use.
7. **Semantic and Identity Validation ("Semantic Firewalls")**: Enforce fully qualified tool names and version pins. Fail closed on ambiguous resolution.
8. **Logging, Monitoring, and Drift Detection**: Maintain immutable logs of all tool invocations. Monitor for anomalous execution rates and unusual tool-chaining patterns.

### Common Attack Examples
- Tool Poisoning: Attacker compromises tool interface (MCP tool descriptors, schemas, metadata) causing agent to invoke a tool based on falsified capabilities.
- Over-Privileged API: Customer service bot intended to fetch order history also issues refunds due to full financial API access.
- Tool name impersonation (typosquatting): Malicious tool named 'report' resolved before 'report_finance'.
- EDR Bypass via Tool Chaining: Legitimate admin tools chained to exfiltrate logs without triggering EDR.

### Applies When
- The agent has access to external tools, APIs, or local system commands.

---

# Rule ID: ASI-05
## Title: Prevent Unexpected Code Execution (RCE)
**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP Agentic Top 10 — ASI05  
**Category:** Code Execution
**Risk Tier:** baseline

### Rule
Prevent prompt injection, tool misuse, or unsafe serialization from converting agent text outputs into unintended executable behavior (RCE, container escape, persistence).

**Controls (Scale with Risk):**
1. Sanitize agent-generated code with input validation and output encoding per LLM05:2025.
2. **Ban `eval()` in production agents**: Require safe interpreters and taint-tracking on generated code.
3. **Execution environment security**: Never run as root. Run code in sandboxed containers with strict limits (network, filesystem). Use `mcp-run-python` style framework sandboxes.
4. **Prevent direct agent-to-production**: Include security evaluations, adversarial unit tests, and detection of unsafe memory evaluators before production.
5. **Architecture and design**: Isolate per-session environments. Fail secure by default. Separate code generation from execution with validation gates.
6. **Access control and approvals**: Require human approval for elevated runs. Keep an allowlist for auto-execution under version control.
7. **Code analysis and monitoring**: Static scans before execution. Enable runtime monitoring. Watch for prompt-injection patterns. Log and audit all code generation and runs.

### Common Attack Examples
- Shell injection: Attacker prompt containing `test.txt && rm -rf /important_data`.
- Code Hallucination with Backdoor: Security patch agent hallucinates code containing hidden backdoor.
- Unsafe Object Deserialization: Agent generates serialized malicious payload triggering code execution.
- Memory System RCE: Attacker exploits unsafe `eval()` in agent memory by embedding executable code.
- Dependency lockfile poisoning: Agent regenerates lockfile and pulls backdoored minor version.

### Applies When
- The agent generates, interprets, or executes code (e.g., code assistants, vibe coding, code refactoring).
