# Adapter — Claude / Claude Code

**Active file:** root `SKILL.md` (must start with YAML frontmatter: `name`, `description`).

## Install (user-level, all projects)
```
mkdir -p ~/.claude/skills
ln -sfn <repo-path> ~/.claude/skills/secure-planning-framework
```
Restart Claude Code; the skill auto-activates on planning/design requests via its
`description` triggers.

## Install (project-level, shared with a repo)
Place the skill at `<project>/.claude/skills/secure-planning-framework/SKILL.md`.

Note: the plain claude.ai web app cannot read local files — there it works only as
pasted instructions, not a discoverable skill.
