# Model Context Protocol (MCP) Security Rules
**Sources:** (Provisional/draft — verify against genai.owasp.org before citing externally)
  
- A Practical Guide for Secure MCP Server Development (OWASP GenAI, v1.0, Feb 2026)  
- A Practical Guide for Securely Using Third-Party MCP Servers (OWASP GenAI, v1.0, Oct 2025)

> These rules apply when designing, building, or consuming MCP servers. Two perspectives are covered: **Server Developer** and **Client Consumer**.

> NOTE: These are ELEVATED and HIGH-ASSURANCE rules.

---

# Rule ID: MCP-001
## Title: Secure MCP Architecture and Communication Channels
**Source:** Practical Guide for Secure MCP Server Development — Section 1  
**Category:** MCP Security / Network
**Risk Tier:** elevated

### Rule
Design MCP server communication to minimize the attack surface from the transport layer upwards.

**Local MCP Servers:**
- Prefer STDIO or Unix sockets over network sockets.
- If local HTTP is required, bind ONLY to `127.0.0.1`. Validate the Origin header. Use explicit authorization/authentication.
- Run processes in isolated/sandboxed subprocesses or containers with minimal privileges and no access to external networks.

**Remote MCP Servers:**
- Enforce TLS 1.2+ for ALL remote connections.
- Strictly validate ALL JSON-RPC messages against the MCP schema. Reject any malformed or unrecognized data.

**Client Authentication:**
- Use allowlists, hardcoded connections, or mTLS for known static client relationships.
- In dynamic environments, use OAuth 2.1 or OIDC to dynamically verify client identity.

**Session Isolation:**
- Strictly segregate execution contexts, memory, and temp storage per user or agent session.
- PROHIBIT use of global variables, class-level attributes, or shared singleton instances for user-specific data.
- Use session-keyed state stores (e.g., Redis with `session_id` namespaces).
- Implement **deterministic cleanup routines**: when an MCP session terminates, disconnects, or times out, immediately flush and destroy all file handles, temp storage, in-memory contexts, and cached tokens.
- Enforce **per-session resource quotas** on memory, CPU, filesystem usage, and API rate limits keyed to session ID or user identity.

### Applies When
- Designing or building an MCP server (local or remote).

---

# Rule ID: MCP-002
## Title: Safe Tool Design and Manifest Integrity
**Source:** Practical Guide for Secure MCP Server Development — Section 2  
**Category:** MCP Security / Supply Chain
**Risk Tier:** elevated

### Rule
Prevent Tool Poisoning and Rug Pull attacks by enforcing strict controls on tool onboarding and runtime validation.

**Controls (Scale with Risk):**
1. **Cryptographic Tool Manifests**: Every tool MUST have a signed manifest including description, schema, version, and required permissions. Verify signature and hash at load time.
2. **Strict Onboarding and Approval Workflow**: Adding or updating any tool description, prompt, or resource requires:
   - Code scanning (SAST)
   - Dynamic testing
   - Dependency scanning (SCA)
   - Manual security review
3. **Validate Descriptions vs. Behavior**: Implement manual checks, tool pinning, and LLM scans to ensure a tool's advertised description matches its actual code behavior at runtime. Flag any tool that attempts actions (e.g., network writes) not mentioned in its description.
4. **Tool Structure Validation**: Maintain and audit all fields of each tool, prompt, and resource. Only expose the **minimal, strictly necessary fields** to the model. Keep internal metadata and sensitive fields outside model context.

### Applies When
- Designing tools for any MCP server.

---

# Rule ID: MCP-003
## Title: Strict Input/Output Validation and Resource Management
**Source:** Practical Guide for Secure MCP Server Development — Section 3  
**Category:** MCP Security / Data Validation
**Risk Tier:** elevated

### Rule
Treat all MCP data as untrusted. Apply strict validation, sanitization, and rate limiting.

**Controls (Scale with Risk):**
1. **Resource Usage Limits**: Impose quotas and rate limits on tool invocations and data fetches per session. Use timeouts and isolated memory/compute budgets to prevent DoS or runaway processes.
2. **Strict Input/Output Validation**: Define and enforce JSON Schemas for every tool's inputs (from the model) and outputs (back to the model). Reject any request that doesn't match the expected schema.
3. **Strict Input/Output Sanitization and Encoding**: Filter and sanitize all inputs to the model and outputs into the tool. Strip or escape sequences that could lead to XSS, SQL Injection, or RCE. Enforce size limits on all outputs.

### Applies When
- Processing any tool invocation on an MCP server.

---

# Rule ID: MCP-004
## Title: Prompt Injection Controls for MCP Servers
**Source:** Practical Guide for Secure MCP Server Development — Section 4  
**Category:** Prompt Injection Prevention
**Risk Tier:** elevated

### Rule
Minimize prompt injection attack surface in MCP server design.

**Controls (Scale with Risk):**
1. **Structured Tool Invocation**: Favor structured JSON tool calls over free-form text commands. This funnels the model's intent through a formal, schema-validated interface.
2. **Human-in-the-Loop (HITL)**: For high-risk actions (deleting data, sending money, system-level changes), implement an approval checkpoint. Pause and require explicit human confirmation (e.g., using MCP elicitations) before proceeding.
3. **LLM-as-a-Judge**: For high-risk actions, run a dedicated approval check in a distinct LLM context session using a policy prompt that defines which tool calls and parameters are allowed or blocked.
4. **One Task, One Session**: Reset MCP sessions when an agent switches contexts or tasks (context compartmentalization). This prevents hidden instructions from persisting in long conversation histories.

### Applies When
- The MCP server handles tool calls that could be influenced by user or external input.

---

# Rule ID: MCP-005
## Title: Authentication and Authorization on MCP Servers
**Source:** Practical Guide for Secure MCP Server Development — Section 5  
**Category:** Identity & Access Management
**Risk Tier:** elevated

### Rule
Enforce strong identity verification and least-privilege access on all MCP server interactions.

**Controls (Scale with Risk):**
1. **Enforce OAuth 2.1 / OIDC**: Authentication is mandatory for all remote MCP servers. Validate `iss`, `aud`, `exp`, and signatures on every request.
2. **Token Delegation (RFC 8693)**: Use OAuth token delegation flow to pass user context and permissions while limiting permissions and retaining distinct server non-human identity (NHI).
3. **PROHIBIT Token Passthrough**: Do NOT forward client tokens to downstream APIs. Use tokens explicitly issued to the MCP server or validated via "On-Behalf-Of" flows. Direct passthrough breaks audit trails, bypasses policies, and creates a Confused Deputy vulnerability.
4. **Short-Lived, Scoped Tokens**: Issue access tokens with minimal lifetimes (minutes) and narrow scopes. Revalidate token signature, audience, and expiry on EACH call.
5. **Treat Sessions as State, Not Identity**: Never rely on session IDs alone for authorization. Bind session/stream/queue entries to validated OAuth identity. Re-check authorization before performing sensitive actions.
6. **Centralize Policy Enforcement**: Use a dedicated policy/gateway layer to enforce authentication, authorization, consent, tool filtering, and audit logging across all agents and servers.

### Applies When
- Any remote MCP server or multi-tenant MCP deployment.

---

# Rule ID: MCP-006
## Title: Hardened MCP Server Deployment and Governance
**Source:** Practical Guide for Secure MCP Server Development — Sections 6, 7, 8  
**Category:** Infrastructure Security / Governance
**Risk Tier:** elevated

### Rule
Deploy MCP servers in minimal, hardened environments and enforce continuous governance.

**Deployment Controls:**
1. **Secrets Storage and Management**: Use secrets vaults for all credentials and API keys. Do NOT store secrets in environment variables, logs, or plaintext in code. NEVER allow an LLM direct access to a secret — all secrets management must occur in transparent middleware inaccessible to the LLM.
2. **Containerize and Harden**: Deploy in minimal, hardened containers. Run as a non-root user. Drop all unnecessary packages, dependencies, and Linux capabilities.
3. **Network Segmentation**: Place in a restricted network segment. Block all inbound and outbound traffic except what is explicitly required (firewall rules or Kubernetes NetworkPolicies).
4. **Supply Chain Controls**: Version-pin and scan all dependencies at build time. Use signed container images. Monitor for new CVEs. Maintain AI-BOMs for all builds.
5. **CI/CD Security Gates**: Integrate SAST, SCA, and policy-as-code checks (e.g., OPA) as required gates in the pipeline. Fail the build on new vulnerabilities or unapproved dependencies.
6. **Safe Error Handling**: Do NOT return stack traces, tokens, filesystem paths, or tool internals in responses returned to the model or client.

**Governance Controls:**
7. **Cryptographic Integrity**: Use cryptographic signing and version pinning for all tools, dependencies, and registry manifests.
8. **Peer Review and Oversight**: No new tool or major code change goes live without a security-focused peer review.
9. **Audit Logs and Trails**: Log every action including tool invocations (with parameters), resource access, authentication/authorization events, and configuration changes (logging new and old values). Use field-level allowlists and redaction/hashing to prevent sensitive data from entering logs. Store logs securely and immutably.
10. **Non-Human Identity (NHI) Governance**: Treat all automated agents, backend processes, and MCP server systems as first-class identities with unique credentials and tightly scoped permissions. Continuously audit NHI systems for data access and tool usage.
11. **Automated Code Scanning**: Use SAST with custom MCP rules, Invariant MCP-Scan, and SCA tools (npm audit, pip audit, OSV-Scanner) in CI/CD. Break builds that exceed risk tolerance.
12. **Continuous Monitoring**: Feed MCP server audit logs into a centralized SIEM. Configure real-time alerts for suspicious patterns (spike in failed validations, high-frequency tool calls, tool suddenly accessing unusual files).

### Applies When
- Deploying any MCP server to staging or production.

---

# Rule ID: MCP-007
## Title: Third-Party MCP Client Security Controls
**Source:** Practical Guide for Securely Using Third-Party MCP Servers  
**Category:** MCP Client Security
**Risk Tier:** elevated

### Rule
When acting as an MCP Client consuming third-party MCP servers, enforce trust minimization and comprehensive verification.

**Current Vulnerability Landscape:**
- **Tool Poisoning & Rug Pulls**: Hidden malicious commands in tool descriptions. Legitimate tools secretly replaced with malicious versions.
- **Prompt Injection**: Malicious inputs in tool arguments hijacking model context to call dangerous tools or override safety policies.
- **Memory Poisoning**: Corrupting agent's short-term or long-term memory (vector databases) causing false information storage or privilege escalation.
- **Tool Interference**: Multiple MCP servers causing unintended tool execution chains or denial-of-service loops.

**Client Controls (Scale with Risk):**
1. **Trust Minimization**: Do NOT assume servers are trustworthy. Always validate manifests, enforce schemas, and apply allowlists.
2. **Sandbox Execution**: Run third-party MCP servers inside Docker containers providing isolated environments that prevent compromised servers from accessing host system resources, files, or network.
3. **Just-in-Time (JIT) Access**: Grant tools only temporary, narrowly scoped permissions for the specific task duration with automatic expiration and instant revocation.
4. **UI Transparency**: Expose full tool descriptions, permissions, and data access to users before execution. AVOID hidden or summarized views that mask risk.
5. **Tool Integrity Monitoring**: Pin the version of the MCP server and its tools at initial user approval. Use hash/checksum to verify tool descriptions haven't been maliciously altered. Maintain a version history and alert on any unauthorized changes.
6. **Local Data Protection**: Prevent servers from exfiltrating client-side secrets, history, or cached memory.
7. **Incident Detection**: Monitor for unusual tool invocation patterns (mass file reads, excessive API calls) and trigger alerts.

**Server Discovery and Verification:**
8. **Verify Origin Before Connecting**: Only connect to servers from a trusted registry. Use IP allowlists and network isolation.
9. **Registry-Only Discovery**: Maintain a central registry for all approved servers with metadata and policy enforcement.
10. **Pin Versions**: Maintain a manifest of approved server and tool versions. Use checksums to verify integrity and prevent silent malicious upgrades.
11. **Staged Rollout**: Enable new servers in staging with full telemetry first. Promote to production only after a probation period with no incidents.

**Authentication (Third-Party):**
12. **Client Credentials** for system operations (no user identity).
13. **OIDC/PKCE** for user operations (chatbots, AI assistants).
14. **Least-permission OAuth Scopes**: Restrict access using OAuth scopes to prevent excessive access.
15. **Granular Permissions**: Use action-level permissions on a per-identity basis.
16. **Human-in-the-Loop for Novel Actions**: Require HITL approval for actions not previously performed (e.g., first-time local filesystem access, accessing emails on a new remote resource).

**Governance Workflow for Onboarding Third-Party MCP Servers:**
1. **Submission**: Developer submits server documentation + hash of tool descriptions.
2. **Scanning**: Automated security tools analyze for malware, hidden instructions, and risks.
3. **Review & Sign-off**: Security and domain experts review scan results. Approved servers are version-pinned and added to the registry.
4. **Deployment & Monitoring**: Staged deployment with monitoring. Probation period before production.
5. **Periodic Re-validation**: Automatic re-scanning at regular intervals or on version changes.

**Recommended Governance Roles:**
- **Submitter (Developer)**: Proposes integration with documentation.
- **Security Reviewer**: Validates security controls, scans, and supply chain integrity.
- **Domain Owner**: Confirms functional necessity and approves scopes.
- **Approver**: Both Security Reviewer and Domain Owner must sign off.
- **Operator (SRE)**: Manages rollout, monitoring, and kill-switch.

### Applies When
- An agent or application acts as an MCP Client connecting to any third-party MCP Server.
