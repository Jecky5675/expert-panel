# Portable usage

Portable editions are for AI chats that do not have a native Skill loader.

## Recommended choice

Start with:

```text
EXPERT_PANEL_BALANCED.md
```

It includes the general workflow and the most useful specialist methods without the size of the complete edition.

## Other choices

| File | Use it when |
| --- | --- |
| `EXPERT_PANEL_LITE.md` | The context window is small or the task is narrow. |
| `EXPERT_PANEL_COMPLETE.md` | The model can handle a large attachment and the project may need every module. |
| `*_STANDALONE.md` | You need only Prompt Engineer, Security Review, Humanizer, README Studio, or Upstream Maintenance. |

## How to use a portable file

1. Attach one portable file to the chat.
2. Attach the project files or text needed for the task.
3. Send a short instruction and the task.

Example:

```text
Read the attached Expert Panel workflow and use it for this task.
Use only the tools and files available in this chat, and answer in my language.

My task: Compare these two project architectures and recommend one.
```

You do not need to attach every edition. Doing so wastes context and can make the instructions harder to follow.

## External skills

Portable files already contain their own fallback methods. They work without separate `humanizer` or `beautify-github-readme` installations. A web host may combine skills on its own, but the portable file does not assume that this happened.

## Large projects

For a large repository, provide a scoped archive or the most relevant directories. Tell the model which paths are important and which paths should be excluded. A review based on selected files should say that it is scoped rather than repository-wide.

## When Python is unavailable

The AI can still follow the Markdown workflow. Automated validators, packaging checks, and SVG rendering simply remain unavailable. Manual review should be described as manual rather than reported as a passed script.

## Updating

Replace the portable file with the matching file from a newer release. Avoid combining different Expert Panel versions in the same chat.
