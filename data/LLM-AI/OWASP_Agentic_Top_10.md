# OWASP Top 10 for Agentic Applications 2026
**Source:** OWASP GenAI Security Project — Agentic Security Initiative  
**Version:** December 2025 | License: CC BY-SA 4.0  
**URL:** genai.owasp.org

## Overview
Agentic AI systems are moving from pilots to production across finance, healthcare, defense, critical infrastructure, and the public sector. Unlike task-specific automations, agents plan, decide, and act across multiple steps and systems. This document serves as a "compass" providing concise, practical, actionable guidance on the Top 10 highest-impact threats.

> Key Principle: **Least-Agency** — Avoid unnecessary autonomy. Deploying agentic behavior where it is not needed expands the attack surface without adding value. Strong observability is non-negotiable.

## Diagram: Agentic Top 10 Architecture Mapping
*The document includes a flowchart showing where each vulnerability sits in the agentic architecture:*
- **Inputs** (User Prompts, API, External Agents): ASI01, ASI03, ASI09
- **Integration/Processing** (Policy, Human-in-the-loop, Agent, Memory, Connected data/RAG): ASI06, ASI07, ASI10
- **Outputs** (Tools, External Agents, APIs/Resources): ASI02, ASI04, ASI05, ASI08

## Top 10 Vulnerabilities

| ID | Title |
|---|---|
| ASI01 | Agent Goal Hijack |
| ASI02 | Tool Misuse and Exploitation |
| ASI03 | Identity and Privilege Abuse |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution (RCE) |
| ASI06 | Memory & Context Poisoning |
| ASI07 | Insecure Inter-Agent Communication |
| ASI08 | Cascading Failures |
| ASI09 | Human-Agent Trust Exploitation |
| ASI10 | Rogue Agents |

## OWASP Security Mapping Matrix (Appendix A)

| ASI ID | OWASP LLM Top 10 (2025) | Agentic Threats & Mitigations | AIVSS Core Risk |
|---|---|---|---|
| ASI01 | LLM01 Prompt Injection, LLM06 Excessive Agency | T6 Goal Manipulation, T7 Misaligned Behaviors | Agent Goal & Instruction Manipulation |
| ASI02 | LLM06 Excessive Agency | T2 Tool Misuse, T4 Resource Overload, T16 Inter-Agent Protocol Abuse | Agentic AI Tool Misuse |
| ASI03 | LLM01, LLM06, LLM02 Sensitive Info Disclosure | T3 Privilege Compromise | Agent Access Control Violation |
| ASI04 | LLM03 Supply Chain Vulnerabilities | T17 Supply Chain Compromise, T2, T11, T12, T13, T16 | Agent Supply Chain & Dependency Attacks |
| ASI05 | LLM01 Prompt Injection, LLM05 Improper Output Handling | T11 Unexpected RCE & Code Attacks | Insecure Agent Critical Systems Interaction |
| ASI06 | LLM01, LLM04 Data & Model Poisoning, LLM08 Vector & Embedding Weaknesses | T1 Memory Poisoning, T4, T6, T12 | Memory Use & Contextual Awareness |
| ASI07 | LLM02, LLM06 | T12 Agent Communication Poisoning, T16 | Agent Memory & Context Manipulation |
| ASI08 | LLM01, LLM04, LLM06 | T5 Cascading Hallucination Attacks, T8 Repudiation & Untraceability | Agent Cascading Failures |
| ASI09 | LLM01, LLM05, LLM06, LLM09 Misinformation | T7, T8, T10 Overwhelming Human in the Loop | Agent Untraceability / Human Manipulation |
| ASI10 | LLM02, LLM09 | T13 Rogue Agents, T14 Human Attacks, T15 Human Manipulation | Behavioral Integrity, Operational Security, Compliance Violations |

## Relationship to OWASP CycloneDX and AIBOM (Appendix B)
OWASP CycloneDX provides SBOM, ML-BOM, and AI-BOM formats to identify and exchange component data. The Agentic AI Top 10 addresses behavioral and autonomy-driven risks beyond static component inventory. Together they provide: CycloneDX establishes supply-chain transparency (WHAT is in my AI system?), while the Agentic Top 10 addresses HOW those components can behave or fail in unsafe ways.

## Mapping to OWASP Non-Human Identities (NHI) Top 10 (Appendix C)
The NHI Top 10 (2025) risks map directly to agentic identity challenges:
- ASI03 (Identity & Privilege Abuse) is the primary agentic evolution of NHI risks.
- Agents require **Agentic Identity** — dynamic, cryptographic identities supporting provenance, attestation, and intent — rather than static API keys.

## Notable Real-World Exploits & Incidents (Appendix D)
- **EchoLeak (ASI01)**: Zero-click indirect prompt injection causing M365 Copilot to exfiltrate emails, files, and chat logs without user interaction.
- **MCP Tool Descriptor Poisoning (ASI04)**: Malicious public tool hiding commands in metadata causing GitHub assistant to exfiltrate private repo data.
- **Malicious MCP Server on npm (ASI04)**: First in-the-wild malicious MCP server impersonating postmark-mcp, secretly BCC'ing emails to attackers.
- **Amazon Q Supply Chain Compromise (ASI04)**: Poisoned prompt in Q for VS Code repo shipping to thousands of users before detection.
- **Replit Vibe Coding RCE (ASI05)**: Automated agent generating and executing unreviewed shell commands, deleting/overwriting production data.
- **ChatGPT Memory Poisoning (ASI06)**: Indirect prompt injection used to corrupt Gemini's long-term memory.
- **AgentFlayer 0-click (ASI01, ASI06)**: Persistent zero-click exploit on ChatGPT via memory poisoning.
