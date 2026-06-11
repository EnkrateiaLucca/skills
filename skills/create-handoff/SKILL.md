---
name: create-handoff
description: Write a structured, timestamped handoff document that captures the current session's context (what was done, what changed, key learnings, next steps) so a fresh agent session can resume the work without replaying the prior conversation. Use when the user says "create a handoff", "save a handoff", "write a status.md", "end-of-session summary", "save session context", or wants to wrap up a working session so it can be picked up later.
---

# Create Handoff

Write a concise handoff document that captures the current session's context so another agent session can pick up where this one left off. Be thorough but compact — summarize without losing key details. The handoff file is the bridge across context windows: the next session reads it instead of replaying the entire prior conversation.

## Process

### 1. Gather metadata

Collect:
- Current date/time with timezone
- Git commit, branch, and repo name (if in a git repo)
- A filename-safe timestamp (`YYYY-MM-DD_HH-MM-SS`)

If the project has a `spec_metadata.sh` script (project root or `scripts/`), run it instead:

```bash
bash spec_metadata.sh
```

### 2. Create the handoff file

Save the file to `./handoffs/YYYY-MM-DD_HH-MM-SS_description.md` where:
- `YYYY-MM-DD_HH-MM-SS` is the current timestamp
- `description` is a brief kebab-case summary of the work

Example: `handoffs/2026-03-17_14-30-00_refactor-auth-middleware.md`

Create the `handoffs/` directory if it doesn't exist. Over time this folder becomes a dated trail of every working session the project has had.

### 3. Write the document

Use this template:

```markdown
---
date: [datetime with timezone]
git_commit: [commit hash, if available]
branch: [branch name, if available]
repository: [repo name, if available]
topic: "[Brief description of what you were working on]"
status: [complete | in-progress | blocked]
---

# Handoff: [concise description]

## What I Was Working On
{Describe the task(s) and the status of each: completed, in progress, or planned. If following a plan, note which phase you're on and reference the plan document.}

## What Changed
{List recent changes you made, using `path/to/file.ext:line` references.}

## Key Learnings
{Important discoveries: patterns, root causes of bugs, gotchas, or non-obvious behavior. Include file paths where relevant.}

## Artifacts Produced
{Exhaustive list of files you created or modified, as file paths or `file:line` references.}

## Next Steps
{What the next session should do to continue this work.}

## Additional Context
{Anything else useful: where relevant code lives, related docs, constraints, or things you tried that didn't work.}
```

### 4. Respond to the user

After creating the handoff, respond with:

```
Handoff created! Resume in a new session with the resume-handoff skill:

handoffs/[filename].md
```

## Guidelines

- **More information, not less.** The template is a minimum — add more if needed.
- **Be precise.** Include both high-level objectives and relevant low-level details.
- **Prefer file references over code snippets.** Use `path/to/file.ext:line` so the next session can read the live code itself instead of a stale copy. Only include snippets if essential (e.g. an error being debugged).
- **Record what didn't work.** Failed approaches are some of the highest-value content in a handoff — they save the next session from repeating them.
