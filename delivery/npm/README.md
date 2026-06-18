# Adapter — npm (PLANNED, not built)

**Status:** scaffold only. See `meta/version_manifest.json` -> compatibility.

## Intended design
Publish as an npm package bundling the rule packs + an orchestration module. Expose a
programmatic API (`planSecureFeature(description)`) and ship `SKILL.md` so installs
can drop the adapter files into a target repo. Version per `meta/version_manifest.json`.
