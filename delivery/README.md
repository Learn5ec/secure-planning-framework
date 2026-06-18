# Delivery Adapters

Each AI coding assistant discovers project instructions through its own convention.
The single source of truth for behavior is the root **`SKILL.md`**; every live
adapter is a thin pointer that routes the assistant to it. Keep adapters in sync
when you change the orchestration entrypoint.

| Assistant            | File the tool auto-reads (live location)          | Status |
|----------------------|---------------------------------------------------|--------|
| Claude / Claude Code | `SKILL.md` (root) + frontmatter; symlinked into `~/.claude/skills/secure-planning-framework` | live |
| Cursor               | `.cursorrules` (root)                             | live |
| Windsurf             | `.windsurfrules` (root)                           | live |
| VS Code (Copilot)    | `.github/copilot-instructions.md`                 | live |
| MCP server           | `delivery/mcp/`                                   | planned |
| npm package          | `delivery/npm/`                                   | planned |
| CLI                  | `delivery/cli/`                                   | planned |

> The per-tool folders below document install/build steps. The *active* files
> live at the canonical locations above (that is where each tool actually reads).
