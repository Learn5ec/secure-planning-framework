# Model Context Protocol (MCP) Security Rules
**Sources:** (Provisional/draft — verify against genai.owasp.org before citing externally)
- A Practical Guide for Secure MCP Server Development (OWASP GenAI, v1.0, Feb 2026)  
- A Practical Guide for Securely Using Third-Party MCP Servers (OWASP GenAI, v1.0, Oct 2025)

> These rules apply when designing, building, or consuming MCP servers. Two perspectives are covered: **Server Developer** and **Client Consumer**.

---

# Rule ID: MCP-001
## Title: Secure MCP Architecture and Communication Channels
**Source:** Practical Guide for Secure MCP Server Development — Section 1  
**Category:** MCP Security / Network
**Risk Tier:** baseline

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

# Rule ID: MCP-003
## Title: Strict Input/Output Validation and Resource Management
**Source:** Practical Guide for Secure MCP Server Development — Section 3  
**Category:** MCP Security / Data Validation
**Risk Tier:** baseline

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
**Risk Tier:** baseline

### Rule
Minimize prompt injection attack surface in MCP server design.

**Controls (Scale with Risk):**
1. **Structured Tool Invocation**: Favor structured JSON tool calls over free-form text commands. This funnels the model's intent through a formal, schema-validated interface.
2. **Human-in-the-Loop (HITL)**: For high-risk actions (deleting data, sending money, system-level changes), implement an approval checkpoint. Pause and require explicit human confirmation (e.g., using MCP elicitations) before proceeding.
3. **LLM-as-a-Judge**: For high-risk actions, run a dedicated approval check in a distinct LLM context session using a policy prompt that defines which tool calls and parameters are allowed or blocked.
4. **One Task, One Session**: Reset MCP sessions when an agent switches contexts or tasks (context compartmentalization). This prevents hidden instructions from persisting in long conversation histories.

### Applies When
- The MCP server handles tool calls that could be influenced by user or external input.
