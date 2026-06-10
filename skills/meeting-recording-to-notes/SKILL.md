---
name: meeting-recording-to-notes
description: Turn a meeting recording into structured markdown meeting notes with a summary, key points, decisions, and action items. Use when the user says "transcribe my latest meeting", "turn this recording into notes", "process this meeting recording", or points at an audio/video file (or a folder of recordings) and wants notes out of it. Do NOT use for non-meeting media like lectures, podcasts, or YouTube videos.
---

# Meeting Recording → Notes

Take a meeting recording (local file, downloaded file, or the latest file in a
recordings folder) and produce a single structured markdown note the user can
act on — not a wall-of-text transcript.

## Configuration

Two locations drive this skill. Resolve them in this order: explicit user
instruction → environment variable → default.

| Setting | Env var | Default |
|---|---|---|
| Recordings folder | `MEETING_RECORDINGS_DIR` | `~/Movies/Meet Recordings` |
| Notes destination | `MEETING_NOTES_DIR` | `~/notes/meetings` |

If the user keeps recordings in a cloud-synced folder (Google Drive, Dropbox),
the synced local path works the same way.

## Workflow

### 1. Locate the recording

- If the user passed a file path or URL, use that. Download URLs to a temp
  directory first.
- If the user said "my latest meeting" (or gave no file), pick the most
  recently modified audio/video file in the recordings folder:
  `ls -t "$MEETING_RECORDINGS_DIR" | head -5` — confirm the pick with the user
  only if the top file is ambiguous (e.g. two files within a few minutes of
  each other).

### 2. Transcribe

Prefer whatever transcription tool is already on the machine, in this order:

1. A local `transcribe` CLI if one exists (`command -v transcribe`)
2. `whisper` / `mlx_whisper` (extract audio first if needed:
   `ffmpeg -i in.mp4 -vn -acodec libmp3lame out.mp3`)
3. If nothing is installed, ask before installing anything.

Keep the raw transcript in a temp file — do not paste it into the chat.

### 3. Write the note

One markdown file, named `YYYY-MM-DD <meeting topic>.md` (infer the topic from
the transcript, date from the file's timestamp). Structure:

```markdown
# <Meeting topic> — <date>

## Summary
2–4 sentences. What was this meeting and what came out of it.

## Key points
- The substance, grouped by theme — not a chronological play-by-play.

## Decisions
- Each decision on one line, with who made the call if identifiable.

## Action items
- [ ] <action> — owner: <name>, due: <date if mentioned>

## Open questions
- Anything raised but not resolved.

## Files & links mentioned
- Only if any came up; omit the section otherwise.
```

Rules:
- Action items must be checkboxes with an owner. If no owner was stated, mark
  it `owner: ?` rather than guessing.
- Omit empty sections entirely — a note full of "N/A" headers is noise.
- Keep speaker attribution only where it matters (decisions, disagreements).

### 4. Report back

Output the full path of the saved note and a one-line summary in the chat.
Nothing else — the note is the deliverable.

## Cleanup

Delete temp audio extractions and downloaded files when done. Never delete the
original recording.
