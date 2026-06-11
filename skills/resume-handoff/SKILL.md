---
name: resume-handoff
description: Resume work from a handoff document written by a previous agent session, with context analysis and drift validation before any work starts. Use when the user says "resume from the handoff", "pick up where we left off", "continue from yesterday's session", "resume handoff", or points at a file in a handoffs/ directory. Pairs with the create-handoff skill, which writes the documents this skill consumes.
---

# Resume Work from a Handoff

You are resuming work from a handoff document. Handoffs contain critical context, learnings, and next steps from a previous agent session — read them fully and verify them against reality before doing anything.

## Initial Response

When this skill is invoked:

1. **If a handoff file path was provided** (e.g. `handoffs/2026-03-17_14-30-00_refactor-auth.md`):
   - Read the handoff document fully (no limit/offset)
   - Read any plan or reference documents it links to — do NOT delegate these critical files to sub-agents
   - Begin the analysis process below

2. **If no path was provided**:
   - Look for a `handoffs/` directory in the project root
   - If it exists, list its contents and pick the most recent file (by filename timestamp)
   - If no handoffs directory or no files found, respond:
     ```
     No handoffs found. You can provide a path directly to a handoff file.
     ```
   - Then wait for input

## Process

### Step 1: Read and Analyze

1. Read the handoff document completely
2. Extract all sections: tasks, changes, learnings, artifacts, next steps
3. Read the key files referenced in the handoff:
   - Files from "What Changed" to verify modifications are still present
   - Files from "Key Learnings" to understand context
   - Files from "Artifacts Produced" to review what was built
4. Check for drift: have files changed since the handoff was written?

### Step 2: Present Analysis

Present a concise summary to the user:

```
Resuming from handoff: [date] — [topic]

**Tasks:**
- [Task 1]: [status from handoff] → [current state]
- [Task 2]: [status from handoff] → [current state]

**Key Learnings Still Valid:**
- [Learning 1 with file reference]
- [Learning 2 with file reference]

**Changes Verified:**
- [Change 1] — [present / missing / modified]

**Recommended Next Steps:**
1. [Most logical next action from handoff]
2. [Second priority]

Shall I proceed with [step 1], or would you like to adjust?
```

Wait for confirmation before proceeding.

### Step 3: Begin Work

1. Create a task list from the handoff's next steps
2. Start with the first approved task
3. Reference learnings from the handoff throughout
4. Apply patterns and approaches documented in the handoff

## Guidelines

- **Read everything first.** Never assume the handoff state matches reality — verify file references still exist and code hasn't changed.
- **Be interactive.** Present findings before starting. Get buy-in on the approach.
- **Leverage handoff wisdom.** Pay special attention to "Key Learnings" — these save you from repeating mistakes.
- **Consider creating a new handoff when done.** If you don't finish, use the create-handoff skill so the next session can continue the thread.
