# Provenance

Copied from https://github.com/brockmartin/roblox-game-skill at commit
`3f38c3f6cce34d325b7e504bb7f39f41051d4c47` (2026-03-04) after a security review.
This is a reviewed snapshot: don't replace it with a newer upstream version without
reviewing that version too.

## Left out

- `README.md`, `.gitignore`, `docs/plans/` — upstream design notes, not used by the skill.

## Changed

- `SKILL.md` — added **Safety Rules**: approval before any change to the Studio place, no
  Creator Store/Toolbox assets, no remote code loading, pinned dependencies, no new MCP
  servers or plugins.
- `references/mcp-orchestration.md` — removed Creator Store search/insert from the toolset
  and the autonomous build; added approval steps to the build, debug, and bulk-edit
  patterns; dropped the preference for the third-party community server; added a
  **Third-Party Assets** section with a backdoor audit script.
- `workflows/new-game.md`, `workflows/debug-loop.md`, `templates/game-scaffold.md` — point
  to the Safety Rules where they run code in Studio.
- `references/tooling-ecosystem.md` — example Rojo project sets `HttpEnabled` to false.
- `references/combat-systems.md` — WCS install pinned to an exact version, no Toolbox copy.
