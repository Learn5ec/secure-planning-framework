# Adapter — cli (PLANNED, not built)

**Status:** scaffold only. See `meta/version_manifest.json` -> compatibility.

## Intended design
A local CLI (`spf plan "<feature>"`) that runs the same activation + orchestration
lifecycle (`core/orchestration.md`) and prints/saves the JSON blueprint. Useful for
CI gating before implementation.
