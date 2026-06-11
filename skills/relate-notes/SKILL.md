---
name: relate-notes
description: Relate a main note (outline, draft, bites file) to one or more source notes in an Obsidian vault by finding the blocks in the sources that genuinely support specific bullets in the main note, planting block anchors (^id) on them, and adding Obsidian block-reference links back into the main note. Use when the user says "relate this note to", "link my notes on X into this outline", "find supporting material in my vault for", "connect this draft to my older notes", or names a main note plus sources (or a search description) and wants them linked.
---

# Relate Notes

Given a **main note** (usually an outline or bites file) and **one or more source notes** (notes with material to mine), find the bullets/paragraphs in the source(s) that genuinely support specific bullets in the main note. Add Obsidian block-anchors (`^id`) to those blocks in each source, then add linked-bullet references in the main note that point at those exact blocks.

The result is the institutional-memory move: the main note ends up standing on everything the vault already knows, with links like `[[Meeting Notes - Expert Call - 2026-04-21#^47c6a0 | frankenstein skill]]` that Cmd-click jumps straight to in Obsidian.

## Configuration

| Setting | Env var | Default |
|---|---|---|
| Vault location | `OBSIDIAN_VAULT_DIR` | `~/notes` |

Resolve in this order: explicit user instruction → environment variable → default. All note paths are relative to the vault unless an absolute path is given.

## Inputs to extract from the user's request

1. **Main note** — the outline/bites file that gets new bullets added (required, single file).
2. **Source(s)** — can take three forms (required):
   - A single note path (e.g. `Licklider - Man-Computer Symbiosis.md`).
   - A comma- or newline-separated list of note paths.
   - A **search description** instead of paths — e.g. *"any note about agents and learning"*, *"all my notes on context engineering"*. In this case, discover candidates yourself (see Discovery below).
3. **Connection kind** — what kind of relationships to look for (optional). Examples: *"anything about scoping"*, *"only the rubric/litmus-test angle"*. If absent, decide based on the topics in the main note.
4. **Count** — total number of block links to produce across all sources (optional, default **3**). Distribute across sources by signal strength, not evenly.
5. **Max sources** — cap on how many distinct source notes to draw from when a search description is given (optional, default **5**). Keeps the result reviewable.

If the main note is missing or ambiguous, ask the user. Don't guess paths — verify with `ls` if unsure.

## Discovery (only when source is a search description, not paths)

1. **Translate the description into search terms.** *"Agents and learning"* → keywords like `agent`, `agents`, `learning`, `expertise`, `skill acquisition`. Aim for 3–8 terms covering the concept.
2. **Find candidate files.** Glob `*.md` in the vault and grep (case-insensitive) the terms to assemble a candidate set. Filter out the main note itself and obviously unrelated hits.
3. **Triage candidates.** Read titles + first ~30 lines of each candidate. Score each on relevance to (a) the search description and (b) the topics actually in the main note. Reject candidates that don't clear both bars.
4. **Cap at `max sources`.** Pick the top `max sources` by relevance score.
5. **Show the user the shortlist before mining.** Print the candidate list (filename + 1-line "why this matched") and proceed unless the user interrupts. If a candidate looks borderline, say so honestly — don't pad the shortlist.

Skip Discovery entirely when explicit source paths were given.

## Steps

1. **Read the main note and every selected source note in full.** Don't skim. The whole point is judgment about which blocks genuinely support which bullets.

2. **Identify candidate connections, ranked.**
   - For each section/bullet in the main note, scan every source for blocks that *substantively support or sharpen this exact claim*.
   - Build a single ranked list across all sources, scored by how load-bearing the connection is.
   - Apply the connection-kind filter if one was given.
   - Take the top `count` (default 3) from the ranked list. **It is fine — and often correct — for some sources to contribute zero links and one source to contribute multiple.** Distribution follows signal, not fairness.

3. **Plant block anchors in each source note that contributed.**
   - At the end of each selected block, append a space and `^<short-kebab-id>`. Examples: `^prompt-loader-insight`, `^85-percent`, `^artifact-as-scope`.
   - IDs must be short, meaningful, and unique *within their source note*. Read each source first and check existing anchors before adding new ones.
   - For tables, code blocks, or anything that can't take an inline anchor, put `^id` on its own line directly after the block (blank line separator).

4. **Add linked bullets to the main note.**
   - Use Obsidian syntax: `[[<source basename without .md>#^<id> | <display text>]]`.
   - Display text is a tight one-liner that carries the argument *before* the reader clicks. Match the voice of the surrounding bullets.
   - Place each link **where it belongs argumentatively** — as a sub-bullet under the existing bullet it supports, or as a sibling bullet in the matching section. Placement is the argument; don't dump links at the bottom.
   - If two sources support the same main-note bullet, stack them as adjacent sub-bullets so the reader sees the convergence.

5. **Report back** with a small table:

   | Main note location | Source → anchor | Why this placement |

   When sources came from a search description, also list which candidates were considered and rejected (and why) so the user can redirect on the next run.

## Style rules

- **Don't over-anchor.** Three high-signal links beats ten thematic ones. If the chosen sources only genuinely support two of the requested `count`, return two and explain.
- **Don't invent connections.** If no source has material that supports a specific main-note bullet, skip it.
- **Don't paraphrase the source.** The display text on the link is your gloss; the anchor target is the source's own words.
- **Don't add YAML frontmatter or tags** to either note. Touch only the lines you're modifying.
- **Don't bidirectionalize unless asked.** This skill adds links from main → sources, not the reverse.
- **Don't open MOC/index notes as sources unless explicitly listed.** Catch-all inbox and index notes are usually not what the user wants to mine.

## When to ask vs. decide

- **Ask** if the main note is missing or ambiguous, or if a search description is so vague that the candidate set would be >20 notes.
- **Decide** the connection kind silently if not specified — but mention in the report what kind of connections you ended up prioritizing, so the user can redirect on the next run.
- **Decide** which subset of discovered candidates to actually mine when sources came from a search description, capped at `max sources` and filtered by signal — but show the shortlist before mining so the user can interrupt if a wrong note made the cut.
