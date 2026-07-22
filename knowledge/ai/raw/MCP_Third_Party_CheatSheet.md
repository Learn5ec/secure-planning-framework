# A Practical Guide for Securely Using Third-Party MCP Servers
**Source:** OWASP GenAI Security Project  
**Version:** 1.0, October 23, 2025 | License: CC BY-SA 4.0  
**URL:** genai.owasp.org | **Intended For:** Companies and developers using third-party MCP servers (not MCP server developers).

## Background
The Model Context Protocol (MCP) standardizes how LLM/agent hosts connect to external tools, data, and prompt templates via a server. By connecting models to databases, APIs, and internal applications, MCP unlocks powerful automation. However, it presents a new attack surface. Since tools can execute code, access files, and make network calls, a compromised MCP stack can lead to data theft, malicious code execution, and system sabotage.

**MCP Architecture:**
- **MCP Host**: Application (e.g., AI agent runtime) that manages clients and routes requests.
- **MCP Client**: Connector that communicates with a single MCP server.
- **MCP Server**: Program exposing three primitive types:
  - **Tools**: Executable functions (file operations, API calls, database queries)
  - **Resources**: Data sources providing contextual information (file contents, database records, API responses)
  - **Prompts**: Reusable templates structuring interactions with language models

## Diagram: Use Case Deployment Patterns
**Local MCP (STDIO):** Downloadable MCP server running locally with native tools and system-level permissions. Uses STDIO for communication between MCP client and server. Some functionality (LLM execution, remote API calls) may interface with remote services.

**Remote MCP (HTTP Streamable):** MCP client connects to server via HTTP Streamable, server running remotely, capable of interacting with external tools and APIs, often hosted in cloud environments. Core considerations: authentication/authorization, server discovery, and unreviewed MCP tool changes.

## Current Vulnerability Landscape

### Tool Poisoning & Rug Pull Attacks
Tool poisoning is a form of **indirect prompt injection** where adversaries embed malicious commands within a tool's description or parameters. A **rug pull** is a specific type where a legitimate tool is secretly replaced with a malicious version, leveraging established trust to execute the attack.

**Mitigations:**
- **Enforce Full Tool Transparency**: MCP clients should display the full tool manifest (descriptions, parameters, capabilities) before user activation. Avoid rendering shortened summaries that can hide injected instructions.
- **Sanitize Descriptions**: Review descriptions for suspicious keywords or markup. Review full MCP code if available. Compare tool names to descriptions and code to identify suspicious mismatches.
- **Monitor Tool Integrity and Version**: Pin the version of the MCP server and its tools at initial user approval. Use hash/checksum to verify tool descriptions and functionality haven't been maliciously altered. Maintain a version history and alert administrators on any unauthorized changes.
- **Runtime Policy Enforcement**: Enforce least-privilege policies at the MCP server boundary (host/container/proxy) to restrict tools from reading local files, accessing sensitive APIs, or exfiltrating data.

### Prompt Injection
Attackers craft malicious user inputs, content retrieved by tools, or tool arguments to hijack the model's context and force unintended actions (calling dangerous tools, leaking conversation history, overriding safety policies).

**Mitigations:**
- **Validate Untrusted Data**: Sanitize and validate all external data (tool descriptions, server responses, user inputs) before passing to the model. Refer to OWASP LLM Prompt Injection Prevention Cheat Sheet.
- **Use Strong Schemas**: Define and enforce strict JSON/YAML schemas for all tool inputs. Use libraries like Pydantic (Python) or JSON Schema for validation.
- **Segment Contexts**: Segment client interactions with different users. Establish new connections/sessions with third-party MCP servers for new or distinct operations.

### Memory Poisoning
Corrupts an agent's short-term or long-term memory (e.g., vector database), causing storage of false information, bypassing security checks, or making flawed decisions. Can lead to systemic misinformation or privilege escalation.

**Mitigations:**
- **Secure and Validate Memory**: Enforce validation on every memory update. Scan for anomalies, require source attribution, use cryptographic hashes.
- **Limit Memory Retention**: Implement TTL (Time-To-Live) on stored data to prevent outdated or malicious information from persisting.
- **Segment Memory**: Prevent agents from writing to a shared memory store to avoid cascading failures. Isolate memory by session or user identity.

### Tool Interference
Using multiple MCP servers can lead to unintended tool execution chains. An LLM's output from one tool might accidentally trigger a tool from another server, causing data leaks, accidental operations, or denial-of-service loops.

**Mitigations:**
- **Require Human-in-the-Loop**: Implement an acceptance flow before executing a tool. For agentic systems, use a tiered HITL strategy.
- **Separate Context**: Isolate the context for each tool execution, passing only necessary information between them. Reset LLM context between distinct executions.
- **Set Timeouts**: Implement execution timeouts to prevent poorly implemented or looping tools from impacting the host.

## Client Security and Server Discovery

### MCP Client Security Considerations
Clients are often embedded in applications and act as the first line of defense against malicious servers.

- **Trust Minimization**: Do NOT assume servers are trustworthy. Always validate manifests, enforce schemas, and apply allowlists.
- **Sandbox Execution**: Run clients in restricted environments (containers with limited filesystem/network access). Use Docker containers for third-party MCP servers to prevent a compromised server from accessing host system resources, files, or network.
- **Just-in-Time (JIT) Access**: Grant tools temporary, narrowly scoped permissions only for the task duration, with automatic expiration and instant revocation.
- **UI Transparency**: Expose full tool descriptions, permissions, and data access to users before execution. Avoid hidden or "summarized" views that mask risk.
- **Local Data Protection**: Prevent servers from exfiltrating client-side secrets, history, or cached memory. Sanitize data passed into the LLM.
- **Incident Detection**: Monitor for unusual tool invocation patterns (mass file reads, excessive API calls) and trigger alerts.

### Server Discovery and Verification

**Discovery & Connection:**
- **Verify Origin Before Connecting**: Only connect to servers from a trusted registry. Use IP allowlists and network isolation. For open-source tools or locally hosted servers, always verify source, check signatures, and scan for known vulnerabilities.
- **Use Registry-Only Discovery**: Maintain a central registry for all approved servers.
- **STDIO (Local)**: For locally hosted MCP servers, use STDIO as a connection to an MCP server sub-process. Lowest latency, easiest to harden via process sandboxing, seccomp, or AppArmor.
- **Streamable HTTP (Remote)**: For remote, multi-tenant, or auto-scaling servers. Use TLS/mTLS or OAuth 2.1 for robust authentication. Protect with a WAF and rate limiters. Rotate credentials regularly.

**Verification:**
- **Pin Versions**: Maintain a manifest of approved server and tool versions. Use checksums to verify integrity and prevent silent, malicious upgrades.
- **Staged Rollout**: Enable new servers in staging with full telemetry first. Promote to production only after a probation period with no incidents. Automate rollback procedures.
- **Record Human Approvals**: Log all security and domain-owner approvals in the registry. Monitor and alert on drift from the approved server inventory.

## Authentication and Authorization

### Authentication
- **Client Credentials** for system operations (MCP clients interacting as systems with no user identity).
- **OIDC/PKCE** for user operations (chatbots, AI assistants with user identity).
  - Where OAuth cannot be implemented, use narrowly scoped and short-lived Personal Access Tokens.
- **Protected Registration**: Dynamic Client Registration is NOT advised for most use cases. If necessary, protect the registration endpoint with:
  - OAuth access tokens for registration requests
  - Software Statements (signed JWT asserting client metadata)
  - Signed Request Bodies with server-side signature verification

### Authorization
- **Define Least-Permission OAuth Scopes**: Restrict access using OAuth scopes to ensure MCP clients or users don't have excessive access.
- **Use Granular Permissions**: Action-level permissions on a per-identity basis to limit access to specific actions or individual data elements.
- **Human-in-the-Loop Controls**: Require HITL approval for actions not previously performed (e.g., first-time local MCP server access to the file system, or accessing emails on a new remote resource).

## Tools & Utilities

### Automated Scanners
- **Invariant Labs MCP-Scan**: Scans for malicious descriptions in MCP tools and monitoring connections for prompt injections, tool poisoning, and unsafe data flows.
- **Semgrep MCP Scanner**: Static analysis tool with MCP rules, scans Python and Node.js dependencies, integrates with MCP-Get.
- **mcp-watch**: Scans for vulnerabilities such as insecure credential storage and tool poisoning attempts.
- **Trail of Bits mcp-context-protector**: Security wrapper for MCP servers addressing risks from running untrusted servers.
- **Vijil Evaluate**: Platform evaluating AI agents for reliability, safety, and security.

### Content Monitoring/Moderation
- **LangKit**: Toolkit for monitoring LLM outputs.
- **OpenAI Moderation API**: API for detecting inappropriate content.
- **Invariant Labs Invariant**: Contextual guardrails for securing agent systems.
- **LlamaFirewall**: Framework with scanners for risks affecting agentic LLM use.

### Open Source Management
- **OpenSSF Scorecard**: Verify repository maturity and security posture.
- **Snyk package health**: Verify repository maintenance.

### Sandboxed Execution
- **Docker**: Run MCP servers inside Docker Containers (both local and remote compute) to limit access to local files and prevent malicious tools from escaping the defined operating environment.

## Governance

Establish a formal governance strategy to ensure only vetted and monitored MCP servers are used. The core of this strategy is a **trusted MCP registry** that holds metadata about each approved server and enforces policy at runtime.

### Governance Workflow
1. **Submission**: Developer submits a new third-party MCP server for review with documentation and a hash of its tool descriptions.
2. **Scanning**: Automated security tools analyze the server (or code repository if available) for malware, hidden instructions, and other risks.
3. **Review & Sign-off**: Security and domain experts review scan results. Approved servers are version-pinned and added to the registry.
4. **Deployment & Monitoring**: Server deployed to staging and monitored. After a probation period, promoted to production.
5. **Periodic Re-validation**: Servers are automatically re-scanned at regular intervals or when versions change.

### Recommended Roles & Responsibilities
| Role | Responsibility |
|---|---|
| **Submitter (Developer)** | Proposes a new server integration and provides documentation |
| **Security Reviewer** | Validates security controls, scans, and supply chain integrity |
| **Domain Owner** | Confirms the server's functional necessity and approves scopes |
| **Approver** | Both Security Reviewer and Domain Owner must sign off before enabling |
| **Operator (SRE)** | Manages connection rollout, monitoring, and the kill-switch |
