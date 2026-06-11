---
name: decision-deck-html
description: Generate a single-file swipeable HTML "decision deck" for iterating over a set of options/ideas/candidates and curating them down to a shortlist. Each card shows one option; the user swipes through with arrow keys or buttons, marks each as Keep or Delete, and selections persist in localStorage and can be exported as JSON or Markdown. Use this skill whenever the user has a list of things they want to triage one-by-one — brainstormed ideas, candidate names, paper titles, feature proposals, recipe options, job postings, design directions, prompt variants, etc. — and asks for a swipeable, card-based, deck-style, or "Tinder-for-X" UI to pick favorites. Trigger even when the user doesn't say "deck" explicitly: phrases like "let me swipe through them", "I want to pick the ones I like", "show them to me one by one so I can keep/delete", "shortlist these", or "help me decide between these options interactively" all qualify.
---

# decision-deck-html

This skill produces a **single self-contained HTML file** that lets the user swipe through a set of options and curate them. No build step, no dependencies, no server — just `open file.html`.

## When to use

Use this skill whenever the user has a *set of discrete options* and wants to *triage them interactively* rather than read them as a flat list. Common signals:

- "show me 20 ideas in a deck I can swipe through"
- "let me keep the ones I like and delete the rest"
- "I want a Tinder-style UI for these candidates"
- "make me a slide deck where I can pick favorites"
- "help me shortlist these"

The skill is also a good fit when *you* (Claude) have just generated a list of N options and the user needs a way to react to them quickly. In that case, proactively suggest the deck format.

## What the skill produces

A single `.html` file containing:

1. A **fullscreen card** showing one option at a time, with: a tag, title, "why this matters" line, body description, and 1–2 metadata fields.
2. **Keyboard + button navigation**: ← / → to move, `K` to keep, `D` to delete, `S` to toggle a summary panel. Keep/Delete auto-advance.
3. **localStorage persistence** so the user can close the file and come back later without losing picks.
4. A **summary panel** that lists kept/deleted/undecided items as pills, with **Download kept.json** and **Download kept.md** buttons and a Reset link.
5. Visual feedback: kept cards get a green border, deleted cards get a red border + dimmed.

## How to build one

1. **Read the template** at `references/deck-template.html`. It is a working deck with a placeholder `SLIDES` array and generic field names.
2. **Decide on the field set**. The template uses these generic fields per slide:
   - `tag` — short category label (1–2 words, shown as a pill)
   - `title` — the option's name (≤8 words ideally)
   - `why` — one sentence on why this option matters / the trade-off it represents
   - `body` — the meat: 2–4 sentences describing the option
   - `meta1` and `meta2` — two short metadata fields shown at the bottom (e.g. "Cost", "Effort", "Deliverable", "Risk"). Rename their **labels** in the render function to fit the domain — but keep the field *names* as `meta1`/`meta2` so the template stays generic.
3. **Fill in the `SLIDES` array** with the user's options. Aim for 10–25 cards; fewer feels thin, more becomes a chore.
4. **Customize the meta labels** in the `render()` function (the two `<b>...</b>` labels inside `.meta`) to fit the domain. If the domain only needs one meta field, delete the second `<span>`. If it needs three, add one — but more than three crowds the card.
5. **Save the file** to a sensible location (the user's working directory by default; ask if unclear) and **open it** with `open <file>.html` on macOS so the user can start swiping immediately.
6. **Tell the user the controls** in your reply: arrow keys to navigate, K/D to keep/delete, S for summary, and that the summary panel has download buttons. Mention that selections persist in localStorage.

## Field naming guidance

Don't rename the per-slide field names (`tag`, `title`, `why`, `body`, `meta1`, `meta2`) even if they feel awkward for the domain. The template's `render()` function references them directly, and keeping them stable means future edits are predictable. If a field genuinely doesn't apply to the domain (e.g. there's no meaningful "why"), leave it as an empty string rather than removing it — the template tolerates empty values.

## A note on the localStorage key

The template stores selections under a key derived from the deck title. If you make multiple decks for the same user, give each one a distinct `STORAGE` key (top of the `<script>` block) so they don't collide. A good default is `deck_<short-slug>_v1`.

## A note on slide reordering

Selections are keyed by **slide index**, not slide content. This means: if the user asks you to add or reorder slides later, the kept/deleted marks will follow the wrong cards. If you anticipate reordering, switch the storage key from `i` to `s.title` in the `mark()` and `render()` functions. Mention this trade-off to the user only if it's likely to come up.

## Output expectations

After running the skill, you should:

- Have written one `.html` file to disk.
- Have opened it (on macOS, via `open`).
- Have told the user the keyboard controls and how to export their picks.
- Optionally, list the slide titles inline so the user can see what's in the deck without opening the file.

## Why this format works

The deck format compresses a decision into a sequence of small, bounded judgments — one card, one binary choice, no scrolling. That matches how humans actually triage. The export step makes the output durable: the kept items become a Markdown shortlist or a JSON file the user can feed into the next step of their workflow. Keep that pipeline in mind: the deck is a *means*, not the end.
