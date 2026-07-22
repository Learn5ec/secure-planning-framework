# A Practical Guide for Secure MCP Server Development
**Source:** OWASP GenAI Security Project  
**Version:** 1.0, February 2026 | License: CC BY-SA 4.0  
**URL:** genai.owasp.org | **Intended For:** Software architects, platform engineers, and development teams building MCP servers.

## Background
MCP servers act as bridges between AI assistants and external tools or data sources. Unlike traditional APIs, MCP servers often operate with **delegated user permissions**, **dynamic tool-based architectures**, and can **chain multiple tool calls**, amplifying the impact of any single vulnerability. Any security gap could allow attackers to manipulate AI assistants, steal sensitive information, or compromise downstream systems.

## Current Vulnerability Landscape
- **Tool Poisoning**: Maliciously designed tool descriptions include hidden instructions tricking the model into unintended actions or data exfiltration.
- **Dynamic Tool Instability ("Rug Pulls")**: Previously trusted tool definitions swapped or modified in real-time to introduce malicious behavior, bypassing initial security checks.
- **Code Injection & Unsafe Execution**: MCP server passes model-provided inputs directly into system commands, APIs, or database queries without validation.
- **Credential Leakage & Token Misuse**: API keys or OAuth tokens improperly stored, logged in plaintext, or cached too long — allowing attackers to impersonate clients.
- **Excessive Permissions**: Over-privileged tools with broad access scopes amplify breach impact. Violates least privilege.
- **Insufficient Isolation (Session, Identity & Compute)**: Multiple concurrent sessions sharing access privileges or executing code in shared environments create cross-tenant data leakage, identity impersonation, and compute escape risks.

## Section 1: Secure MCP Architecture

### Local vs Remote Connections
**Local MCP Servers:**
- Prefer STDIO or Unix sockets over network sockets.
- If local HTTP is required, bind ONLY to `127.0.0.1`, validate Origin header, use explicit auth.
- Run processes in isolated/sandboxed subprocesses or containers with minimal privileges.

**Remote MCP Servers:**
- Enforce TLS 1.2+ for ALL remote connections.
- Strictly validate ALL JSON-RPC messages against the MCP schema. Reject malformed or unrecognized data.

### Client Authentication
- For known static relationships: use allowlists, hardcoded connections, or mTLS.
- For dynamic environments: use OAuth 2.1 or OIDC to dynamically verify client identity.

### Session Isolation (Multi-Tenant)
- Strictly segregate execution contexts, memory, and temp storage per user/agent.
- PROHIBIT use of global variables, class-level attributes, or shared singleton instances for user-specific data.
- Use session-keyed state stores (e.g., Redis with `session_id` namespaces).
- **Strict Lifecycle Management**: On session terminate/disconnect/timeout — immediately flush and destroy all file handles, temp storage, in-memory contexts, and cached tokens.
- **Per-Session Resource Quotas**: Enforce limits on memory, CPU, filesystem usage, and API rate limits keyed to session ID or user identity.

## Section 2: Safe Tool Design

- **Cryptographic Tool Manifests**: Every tool must have a signed manifest (description, schema, version, required permissions). Verify signature and hash at load time.
- **Strict Onboarding and Approval**: Adding or updating any tool requires: SAST, dynamic testing, dependency scanning (SCA), and manual security review.
- **Validate Descriptions vs. Behavior**: Manual checks, tool pinning, and LLM scans to ensure a tool's description matches actual code behavior. Flag any tool performing undescribed actions (e.g., network writes not in description).
- **Tool Structure Validation**: Maintain and audit all fields. Only expose minimal, strictly necessary fields to the model. Keep internal metadata and sensitive fields outside model context.

## Section 3: Data Validation & Resource Management

- **Resource Usage Limits**: Quotas and rate limits on tool invocations and data fetches per session. Use timeouts and isolated memory/compute budgets to prevent DoS or runaway processes.
- **Strict Input/Output Validation**: Define and enforce JSON Schemas for every tool's inputs (from model) and outputs (back to model). Reject any request not matching the expected schema.
- **Strict Input/Output Sanitization and Encoding**: Strip or escape sequences that could lead to XSS, SQL Injection, RCE. Enforce size limits on all outputs from tools or model.

## Section 4: Prompt Injection Controls

- **Structured Tool Invocation**: Favor structured JSON tool calls over free-form text commands. Funnels model intent through a formal, schema-validated interface.
- **Human-in-the-Loop (HITL)**: For high-risk actions (deleting data, sending money, system-level changes): pause and require explicit human confirmation (e.g., using MCP elicitations).
- **LLM-as-a-Judge**: For high-risk actions: run a dedicated approval check in a distinct LLM context session using a policy prompt defining allowed/blocked tool calls and parameters.
- **One Task, One Session**: Reset MCP sessions when agent switches contexts or tasks ("context compartmentalization"). Prevents hidden instructions from persisting in long conversation histories.

## Section 5: Authentication & Authorization

- **Enforce OAuth 2.1 / OIDC**: Mandatory for all remote MCP servers. Validate `iss`, `aud`, `exp`, and signatures on every request.
- **Token Delegation (RFC 8693)**: Use OAuth token delegation to pass user context and permissions while retaining distinct server NHI.
- **PROHIBIT Token Passthrough**: Do NOT forward client tokens to downstream APIs. Direct passthrough creates a **Confused Deputy** vulnerability — allowing the MCP server to be tricked into misusing a user's privileges.
- **Short-Lived, Scoped Tokens**: Issue tokens with minimal lifetimes (minutes) and narrow scopes. Revalidate signature, audience, and expiry on each call.
- **Treat Sessions as State, Not Identity**: Never rely on session IDs alone for auth. Bind to validated OAuth identity. Re-check authorization before sensitive actions.
- **Centralize Policy Enforcement**: Use a dedicated policy/gateway layer to enforce authentication, authorization, consent, tool filtering, and audit logging consistently across all agents and servers.

## Section 6: Secure Deployment & Updates

- **Secrets Storage and Management**: Use secrets vaults. Do NOT store in environment variables, logs, or plaintext code. NEVER allow an LLM direct access to a secret — secrets management must occur in transparent middleware inaccessible to the LLM.
- **Containerize and Harden**: Deploy in minimal, hardened containers. Run as non-root. Drop all unnecessary packages, dependencies, and Linux capabilities.
- **Network Segmentation**: Restricted network segment. Block all inbound/outbound traffic except what is explicitly required (firewall rules or Kubernetes NetworkPolicies).
- **Supply Chain Controls**: Version-pin and scan all dependencies at build time. Use signed container images. Monitor for new CVEs. Maintain AI-BOMs for all builds.
- **CI/CD Security Gates**: Integrate SAST, SCA, and policy-as-code checks (e.g., OPA) as mandatory pipeline gates. Fail build on new vulnerabilities or unapproved dependencies.
- **Safe Error Handling**: Do NOT return stack traces, tokens, filesystem paths, or tool internals in responses to the model or client.

## Section 7: Governance

- **Cryptographic Integrity**: Cryptographic signing and version pinning for all tools, dependencies, and registry manifests.
- **Peer Review and Oversight**: No new tool or major code change goes live without a security-focused peer review.
- **Audit Logs and Trails**: Log every action: tool invocations (with parameters), resource access, auth/authorization events, configuration changes (old and new values). Use field-level allowlists and redaction/hashing. Store securely and immutably.
- **Non-Human Identity (NHI) Governance**: Treat all automated agents, backend processes, and MCP server systems as first-class identities with unique credentials and tightly scoped permissions. Continuously audit NHI systems.

## Section 8: Tools & Continuous Validation

- **Automated Code Scanning**: SAST with custom MCP rules + Invariant MCP-Scan in CI/CD. SCA tools (npm audit, pip audit, OSV-Scanner). Break builds exceeding risk tolerance.
- **Runtime Protections**: Docker seccomp profiles, AppArmor, or specialized wrappers like context-protector. Tools like mcp-watch for runtime behavior monitoring.
- **Continuous Monitoring**: MCP server audit logs → centralized SIEM. Real-time alerts for: spike in failed validations, high-frequency tool calls, tool suddenly accessing unusual files.
- **Supply Chain Vigilance**: OpenSSF Scorecard to evaluate project security posture. Monitor OSV for new dependency vulnerabilities.

## MCP Security Minimum Bar (Review Checklist)

**1. Strong Identity, Auth & Policy Enforcement**
- [ ] All remote MCP servers use OAuth 2.1/OIDC
- [ ] Tokens are short-lived, scoped, validated on every call
- [ ] No token passthrough; policy enforcement is centralized

**2. Strict Isolation & Lifecycle Control**
- [ ] Users, sessions, and execution contexts are fully isolated
- [ ] No shared state for user data
- [ ] Sessions have deterministic cleanup and enforced resource quotas

**3. Trusted, Controlled Tooling**
- [ ] Tools are cryptographically signed, version-pinned, and formally approved
- [ ] Tool descriptions are validated against runtime behavior
- [ ] Only minimal, necessary tool fields are exposed to the model

**4. Schema-Driven Validation Everywhere**
- [ ] All MCP messages, tool inputs, and outputs are schema-validated
- [ ] Inputs/outputs are sanitized, size-limited, and treated as untrusted
- [ ] Structured (JSON) tool invocation is required

**5. Hardened Deployment & Continuous Oversight**
- [ ] Server runs containerized, non-root, network-restricted
- [ ] Secrets are stored in vaults and never exposed to the LLM
- [ ] CI/CD security gates, audit logs, and continuous monitoring are mandatory
