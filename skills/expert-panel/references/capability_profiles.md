# Capability profiles and adaptive installation

Expert Panel separates the skill payload from host capabilities. Installation should choose the least powerful path that preserves the requested behavior.

## Profiles

| Profile | Host capability | Installation | Runtime behavior |
|---|---|---|---|
| `PLUGIN` | Verified client plugin API plus agent/subagent support | Plugin definition, canonical skill, and subagent manifests | Plugin owns discovery; subagents receive isolated scoped tasks when the client actually exposes them |
| `AGENTS` | Agent skill directory plus verified subagent directory, no plugin API | Canonical skill and subagent manifests directly | The host loads the skill; subagents are callable only if the host confirms that directory and format |
| `SOLO` | Skill/custom-instruction support only | Canonical skill payload without subagents | One model uses bounded sequential lens passes; it must not pretend to be independent agents |
| `WEB` | File attachment or native web skill import | `web-skill`, `universal-zip`, or `universal-text` | A single model follows the portable host profile |

## Selection algorithm

1. Detect actual host capabilities, not vendor names or documentation claims.
2. Prefer `PLUGIN` only after the client confirms its plugin manifest and agent registration format.
3. Otherwise choose `AGENTS` only when the host exposes a supported subagent directory and invocation mechanism.
4. Otherwise install `SOLO`; do not fail a useful skill install merely because optional delegation is unavailable.
5. Record the selected profile, paths, installer version, and hashes in the marker.
6. Never silently overwrite an existing skill, plugin, or agent file. Require a clean destination or an explicit verified migration path.

The installer can copy files, but it cannot grant a host a capability it does not expose. A copied JSON manifest is not proof that a subagent is active.
