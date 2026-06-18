# Adapter — mcp (PLANNED, not built)

**Status:** scaffold only. See `meta/version_manifest.json` -> compatibility.

## Intended design
Expose the framework as an MCP server with a `plan_secure_feature` tool that takes a
feature description and returns the `core/output_schema.json` blueprint. The server
loads rule packs from `domains/`, `compliance/`, `common/` per
`core/activation_logic.json`.
