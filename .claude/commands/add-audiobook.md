# Add Audiobook

Add a new audiobook to Claudiobooks from Project Gutenberg.

## Usage

```
/add-audiobook <book title or Gutenberg ID>
```

Examples:
- `/add-audiobook The Great Gatsby`
- `/add-audiobook 64317` (Gutenberg ID)

## What this does

1. **Find the book** on Project Gutenberg (search if title given, fetch if ID)
2. **Download and read** the full text
3. **Write a summary** (2000-4000 words, podcast-friendly style)
4. **Choose a voice** appropriate for the book's tone
5. **Generate audio** using OpenAI TTS
6. **Create content file** with proper frontmatter
7. **Create a PR** for review

## Voice Selection

Pick a voice that matches the book's character:

| Voice | Best for |
|-------|----------|
| onyx | Serious literature, philosophy, history |
| alloy | General purpose, balanced |
| echo | Warm stories, memoirs, conversations |
| fable | British literature, fantasy, whimsical |
| nova | Upbeat, adventure, young adult |
| shimmer | Poetry, gentle stories, romance |

## Instructions for Claude

When this skill is invoked:

1. If given a title, search Project Gutenberg to find the book ID
2. Fetch the book using: `cd pipeline && uv run fetch.py <id>`
3. Read the downloaded book file thoroughly
4. Write a podcast-style summary following the style in existing audiobooks:
   - 2000-4000 words
   - Narrative, engaging tone
   - Structure: hook → context → story/themes → significance
   - Use section breaks (---) and ### headers
   - Avoid academic jargon
5. Save the summary to a temp file
6. Generate audio: `cd pipeline && uv run tts.py <summary> ../site/public/audio/<slug>.mp3`
7. **Get actual duration** from the generated audio file:
   ```bash
   ffprobe -v error -show_entries format=duration -of csv=p=0 <audio_file>
   ```
   Convert seconds to human-readable format (e.g., "12 minutes")
8. Create the markdown file in `site/src/content/audiobooks/<slug>.md` with frontmatter
   - Use the actual duration from step 7 in the `duration` field
9. Create a feature branch: `git checkout -b add/<slug>`
10. Commit and push: `git add . && git commit -m "Add <title> audiobook" && git push -u origin add/<slug>`
11. Create PR: `gh pr create --title "Add <title>" --body "..."`

## Summary Style Guide

See `site/src/content/audiobooks/adventures-of-huckleberry-finn.md` for reference.

Key points:
- Open with a hook that captures the book's essence
- Tell the story, don't just describe it
- Include key quotes sparingly
- End with why it matters today
- Close with "This has been [Book Title] by [Author]."
