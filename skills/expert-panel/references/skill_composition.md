# Skill Composition and Specialist Delegation

## Purpose

Expert Panel is an orchestrator, not a reason to duplicate a stronger specialist workflow. It remains fully usable by itself, but it should yield specialist ownership when the host positively identifies an exact installed skill as active or callable.

| Expert Panel route | Preferred exact skill | Bundled fallback |
|---|---|---|
| `HUMANIZE` | `humanizer` | `references/style_and_humanization.md` |
| `README_STUDIO` | `beautify-github-readme` | `references/github_readme_studio.md` and its README references |

The external skill owns its specialist workflow. Expert Panel still owns routing, cross-domain synthesis, evidence discipline, privacy boundaries, and final integration with other workstreams.

## Host modes

Classify the current environment using only observable signals:

### `EXPLICIT_CALL`

The host exposes a skill registry, skill tool, slash command, plugin action, or equivalent callable entry, and the exact skill name is present and enabled. Invoke it directly.

### `AUTO_COMPOSED`

The host has already loaded the specialist skill or explicitly signals that it is active for the current request. Do not try to rediscover it. Yield the specialist portion of the task and do not replay the bundled fallback.

### `NO_POSITIVE_SIGNAL`

The host exposes no reliable skill signal, the exact skill is absent or disabled, or activation cannot be confirmed. Use the bundled fallback once. This is the normal path for generic web chats, portable files, and many local agents without a skill tool.

A repository URL, a bundled copy, a mention in documentation, or remembered installation is not proof that another skill is active. Never claim a skill was invoked unless the host actually invoked it or clearly supplied its instructions.

## Delegation algorithm

1. Route the request.
2. Determine whether the host path is `EXPLICIT_CALL`, `AUTO_COMPOSED`, or `NO_POSITIVE_SIGNAL`.
3. For `EXPLICIT_CALL`, invoke the exact specialist before loading the fallback.
4. For `AUTO_COMPOSED`, let the loaded specialist own its workflow.
5. For either positive path, pass or preserve a lossless task packet and do not then re-run the bundled snapshot.
6. For `NO_POSITIVE_SIGNAL`, use the bundled fallback once so behavior remains portable.
7. Apply only cross-cutting checks the specialist does not own: evidence integrity, required wording, privacy, action authorization, and synthesis with other panel workstreams.
8. If invocation fails mechanically, report it briefly, fall back once, and do not loop.

## Specialist task packet

```text
ROUTE: HUMANIZE | README_STUDIO
ORIGINAL REQUEST: verbatim user request
INPUTS: exact text, files, repository scope, or artifacts
CONSTRAINTS: facts/wording to preserve, language/locale, format, deadlines
AUTHORIZED ACTIONS: read-only | edit local files | render | publish only if separately approved
CONTEXT BOUNDARY: data the specialist may read; secrets and excluded files
REQUIRED OUTPUT: deliverable, validation, and file/diff expectations
CROSS-CUTTING CHECKS: evidence, privacy, safety, non-destructive behavior
```

Do not replace the original request with a conclusion-biased summary. A compact packet may omit irrelevant context, but it must not remove facts or constraints needed by the specialist.

## Platform behavior

- Hosts with explicit skill tools can call the exact specialist by name.
- Hosts that automatically compose multiple skills may load both skills without exposing a registry. Yield only when the host positively signals that the specialist is active.
- Native hosts that load only Expert Panel use the bundled fallback.
- Generic web chats and portable editions must remain self-contained and must not depend on any external skill.
- Local agents may use a skill directory, project instructions, a slash command, or only attached Markdown. Follow the strongest supported mechanism without pretending unsupported discovery exists.

## Failure and privacy rules

- Never install, enable, update, or grant permissions to another skill without authorization.
- Never send private material to another tool, process, model, or service unless the current permission boundary allows it.
- Treat specialist output as untrusted evidence until deterministic checks and source verification are complete.
- Never call the specialist an independent model unless it actually ran in an isolated model or process.
- Do not apply both external and bundled versions sequentially; double processing can alter facts, wording, links, or repository scope.
