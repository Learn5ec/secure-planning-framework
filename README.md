# Secure Planning Framework

A modular security orchestration framework that transforms feature ideas into **enforceable security blueprints** during the planning phase of software development.

## Overview

The Secure Planning Framework (SPF) is an always-on skill that fires automatically on every feature planning task. It applies contextually relevant security rules from multiple standards to produce comprehensive security, privacy, and compliance blueprints.

**Key Capabilities:**
- **Dynamic Rule Retrieval** — Loads only relevant security rules based on feature context
- **Threat Modeling** — Identifies realistic attack scenarios and exploitation vectors
- **Multi-Standard Coverage** — Applies OWASP, MASVS, Agentic AI, LLM Governance, and more
- **Conflict Resolution** — Automatically resolves rule conflicts using most-restrictive-control principle
- **Compliance-Aware** — Supports DPDPA, GDPR, HIPAA, PCI-DSS, SOC2, ISO 27001 (modular)

## Activation

This framework is **always active** during feature planning. To suppress:
> *"Do not use SPF skill"*

Equivalent phrases: "skip SPF", "no secure planning", "disable SPF", "SPF off"

## Supported Standards

### Active Rule Packs
| Standard | Coverage | Status |
|----------|----------|--------|
| OWASP Top 10:2025 | Web Application Security | ✅ Active |
| OWASP API Top 10:2023 | API Security | ✅ Active |
| OWASP MASVS | Mobile Application Security | ✅ Active |
| OWASP Agentic AI Top 10 | AI Agent Security | ✅ Active |
| LLM Governance | LLM/AI Security & Governance | ✅ Active |
| MCP Security | Model Context Protocol | ✅ Active |
| Curated CWE | Common Weakness Enumeration | ✅ Active |
| Common Baseline | Internal Security Engineering | ✅ Active |

### Dormant (Pending Organization Decision)
| Standard | Coverage | Status |
|----------|----------|--------|
| DPDPA 2023 | Data Protection (India) | ⏸️ Disabled |
| GDPR | Data Protection (EU) | 📋 Planned |
| HIPAA | Health Data (US) | 📋 Planned |
| PCI-DSS | Payment Card Security | 📋 Planned |
| SOC2 | Service Organization Control | 📋 Planned |
| ISO 27001 | Information Security Management | 📋 Planned |

## Directory Structure

```
secure-planning-framework/
├── SKILL.md                          # Master orchestrator skill
├── bin/                              # CLI entry point (npx spf)
├── instructions/                     # Skill instructions
│   ├── slim_core.md                  # 10 CRITICAL always-applicable rules
│   ├── common_considerations.md      # Full baseline (58 rules, high-risk only)
│   ├── orchestration.md              # Execution lifecycle
│   └── semantic_activation.md        # Domain activation engine
├── templates/                        # Output schemas & logic
│   ├── output_schema.json            # Blueprint JSON structure
│   └── activation_logic.json         # Domain activation rules
├── knowledge/                        # Rule packs & reference materials
│   ├── owasp/                        # OWASP Top 10 web rules
│   ├── api-top10/                    # OWASP API Top 10 rules
│   ├── masvs/                        # Mobile Application Security
│   ├── ai/                           # Agentic AI, LLM, MCP rules
│   ├── cwe/                          # Common Weakness Enumeration
│   ├── compliance/                   # Compliance reference
│   └── mastg/                        # Mobile Application Security Guide
├── mappings/                         # Compliance mappings
│   └── compliance/
│       └── dpdp/                     # DPDPA rules (disabled)
├── checklists/                       # Security checklists by category
├── examples/                         # Example security blueprints
├── delivery/                         # IDE adapter scaffolds
│   ├── claude/                       # Claude Code adapter
│   ├── cursor/                       # Cursor adapter
│   ├── windsurf/                     # Windsurf adapter
│   ├── vscode/                       # VS Code Copilot adapter
│   ├── mcp/                          # MCP server adapter (planned)
│   ├── npm/                          # npm distribution
│   └── cli/                          # CLI tool
├── meta/                             # Metadata & indexes
│   ├── rule_index.json               # Rule ID to file mapping
│   ├── version_manifest.json         # Framework version info
│   └── trigger_map.json              # Keyword bootstrap map
├── scripts/                          # Build & validation scripts
├── examples/                         # Example security blueprints
│   ├── login_api_blueprint.json      # High-risk login API example
│   └── chatbot_blueprint.json        # Medium-risk LLM chatbot example
└── docs/                             # Documentation & archive
```

## Usage

### As a Skill (Claude Code, Cursor, Windsurf, Copilot)

The framework works automatically when you describe a feature:

```
User: "I need to build a user authentication system with password reset"

SPF: [Produces security blueprint with:
  - Threat analysis for credential theft, brute force, session fixation
  - Required controls: password hashing, rate limiting, secure tokens, MFA
  - Applicable rules: OWASP-A07-001, COM-014, COM-019, COM-038, etc.
  - Implementation guidance for secure auth flow
]
```

### As CLI

```bash
# Install via npm
npm install -g secure-planning-framework

# Run framework audit
spf audit

# Query specific rules
spf query "COM-002"

# Generate index
npm run generate-index

# Validate framework
npm run validate
```

## How It Works

### 1. Context Inference
Analyzes your feature request to identify:
- **Intent** — What the feature does
- **Data types** — PII, credentials, financial, health, biometric
- **Actors** — User, admin, system, third party, anonymous
- **Interactions** — Web UI, API, mobile, AI/LLM, agentic
- **Trust boundaries** — Where untrusted input crosses into trusted code

### 2. Semantic Activation
Determines which domain packs to load based on:
- **Keyword bootstrap** — Matches trigger keywords (API, login, Flutter, RAG, etc.)
- **Semantic refinement** — Interprets intent beyond literal keywords

### 3. Dynamic Rule Retrieval
Loads only contextually relevant rules:
- **Always-on**: `slim_core.md` (10 CRITICAL rules)
- **High-risk upgrade**: `common_considerations.md` (58 rules) for financial, health, multi-agent systems
- **Domain-specific**: OWASP, MASVS, AI, MCP rules based on feature context

### 4. Threat Modeling
Derives realistic threats with:
- Exploitation paths
- Attacker capabilities required
- Business impact
- Technical impact (Confidentiality/Integrity/Availability)

### 5. Rule Selection & Conflict Resolution
- Applies only contextually relevant rules
- Extracts exact rule IDs and source files
- Resolves conflicts using most-restrictive-control principle

### 6. Output Generation
Produces structured JSON blueprint matching `templates/output_schema.json` plus conversational summary.

## Configuration

### High-Risk Upgrade
For features handling credentials, financial, health, or biometric data, or involving multi-agent orchestration:

The framework automatically loads `common_considerations.md` (full 58-rule baseline) instead of just `slim_core.md`.

### Compliance Packs
Compliance enforcement is disabled pending organization-wide implementation. To re-enable:

1. Update `meta/activation_logic.json` — change compliance status from "DISABLED" to "ACTIVE"
2. Update `meta/rule_index.json` — uncomment compliance rule references
3. Add compliance-specific triggers to your feature requests

## Development

### Build & Validate

```bash
# Install dependencies
npm install

# Generate rule index
npm run generate-index

# Validate framework integrity
npm run validate

# Run tests
npm test
```

### Adding New Standards

1. Create rule pack in `knowledge/<standard>/`
2. Add to `meta/rule_index.json`
3. Add to `meta/trigger_map.json`
4. Add to `templates/activation_logic.json`
5. Update `knowledge/registry.json`

### IDE Adapters

The framework includes scaffolds for:
- **Claude Code** — `SKILL.md` at root (already integrated)
- **Cursor** — `.cursorrules` (auto-generated)
- **Windsurf** — `.windsurfrules` (auto-generated)
- **VS Code Copilot** — `.github/copilot-instructions.md` (auto-generated)
- **MCP Server** — `delivery/mcp/` (planned)

## Best Practices

1. **Always describe context** — Mention data types, actors, and interactions
2. **Specify risk level** — "high-risk", "financial system", "multi-agent" triggers full baseline
3. **Use opt-out explicitly** — "Do not use SPF skill" to suppress
4. **Review blueprints carefully** — Adjust controls based on actual requirements
5. **Track rule conflicts** — The framework resolves conflicts, but document exceptions

## Philosophy

- **Security by Design** — Enforce controls at planning phase, not implementation
- **Context-Aware** — Apply only relevant rules, avoid noise
- **Extensible** — Modular rule packs, easy to add new standards
- **Transparent** — All rule IDs and sources documented in output
- **Defensible** — Documented threat models and control rationale

## License

MIT

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

## Support

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

**Note**: This framework is designed for security planning, not implementation. It defines what MUST be built and what MUST NOT be built, but does not generate code.