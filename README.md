# Skills

Personal agent skills I use every day, packaged for anyone to steal.

Each skill is a self-contained folder with a `SKILL.md` — portable instructions
an agent loads on demand. They follow the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
format, so they work with Claude Code out of the box and port to any
SKILL.md-compatible harness.

I write and teach about AI workflows at [Automata Learning Lab](https://www.automatalearninglab.com/),
and I'm currently writing a book about agent skills. The skills here are the
ones that survived real daily use — not demos.

## Quickstart

```bash
git clone https://github.com/EnkrateiaLucca/skills.git
cp -r skills/skills/* ~/.claude/skills/
```

Restart Claude Code (or run `/reload-skills`) and the skills trigger
automatically when relevant. To install a single skill, copy just its folder.

## The skills

| Skill | What it does |
|---|---|
| [meeting-recording-to-notes](skills/meeting-recording-to-notes/SKILL.md) | Turns a meeting recording into one structured markdown note — summary, decisions, action items with owners — instead of a wall-of-text transcript. |

More coming as they earn their place.

## What makes a skill worth keeping

My bar for adding anything here:

1. **It compresses a real seam.** The skill removes mechanical work between a
   thought and its artifact — it doesn't replace the judgment on either side.
2. **The body is thin.** Everything the agent needs to *decide* what to do
   lives in `SKILL.md`; everything about *doing it well* gets pushed to
   reference files loaded on demand.
3. **It survived repeated use.** A skill that worked once is a prompt that got
   lucky.

## A note on trust

Read any skill before installing it — including these. Skills are instructions
your agent will follow with your permissions. Treat them like you'd treat any
dependency: audit first, then install.

## License

MIT — take what's useful.
