# Claudiobooks

Short-form audiobooks from the public domain, summarized and narrated by AI.

## Project Overview

This is an experiment in AI-assisted content creation. Claude Code is the primary developer and content creator. The human owner is intentionally hands-off - they orchestrate but rarely write code.

**Live site**: Deployed on Vercel (auto-deploys from `main`)

## Architecture

```
claudiobooks/
├── site/                 # Astro static site
│   ├── src/
│   │   ├── content/
│   │   │   └── audiobooks/   # Markdown files for each audiobook
│   │   ├── components/
│   │   ├── layouts/
│   │   └── pages/
│   └── public/
│       └── audio/            # MP3 files
├── pipeline/             # Python tools (use with `uv run`)
│   ├── fetch.py          # Fetch books from Project Gutenberg
│   └── tts.py            # Generate audio with OpenAI TTS
└── .github/workflows/    # CI runs on every PR
```

## Adding a New Audiobook

This is the main workflow. When asked to add an audiobook:

### 1. Fetch the book
```bash
cd pipeline && uv run fetch.py <gutenberg_id>
```
Find IDs at https://www.gutenberg.org - search for the book, ID is in the URL.

### 2. Write the summary
Read the book and write a podcast-friendly summary. Style guidelines:
- 2000-4000 words (roughly 10-20 minutes of audio)
- Narrative, engaging tone - like explaining to a curious friend
- Structure: hook → context → plot/themes → significance
- Use section breaks (---) for natural pauses
- Avoid academic jargon
- Include interesting quotes sparingly

Reference: See existing summaries in `site/src/content/audiobooks/` for tone.

### 3. Generate audio
```bash
cd pipeline && uv run tts.py <summary_file> ../site/public/audio/<slug>.mp3
```
Uses OpenAI TTS with the "onyx" voice (good for narration).

### 4. Get actual duration
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 site/public/audio/<slug>.mp3
```
Convert seconds to minutes (round to nearest minute) for the frontmatter.

### 5. Create the content file
Create `site/src/content/audiobooks/<slug>.md`:
```markdown
---
title: "Book Title"
author: "Author Name"
publishedYear: 1925
duration: "15 minutes"
audioFile: "book-title.mp3"
gutenbergId: 12345
description: "One-sentence hook for the card."
dateAdded: 2024-01-15
tags: ["fiction", "american literature"]
---

[Full summary text here - this appears on the audiobook page]
```

### 6. Create a PR
```bash
git checkout -b add/<slug>
git add site/src/content/audiobooks/<slug>.md site/public/audio/<slug>.mp3
git commit -m "Add <Book Title> audiobook"
git push -u origin add/<slug>
gh pr create --title "Add <Book Title>" --body "New audiobook: <description>"
```

The owner will review and merge via mobile. Vercel auto-deploys.

## Commands

```bash
# Build site locally
cd site && npm run build

# Dev server
cd site && npm run dev

# Fetch a book
cd pipeline && uv run fetch.py 76  # Tom Sawyer

# Generate audio
cd pipeline && uv run tts.py summary.txt output.mp3
```

## Environment

- `.env` in project root contains `OPENAI_API_KEY` (not committed)
- Audio files stored directly in git (no LFS - Vercel doesn't support it)
- Python deps managed with `uv` (see `pipeline/pyproject.toml`)
- Will migrate audio to HuggingFace when library grows large

## Conventions

- Branch naming: `add/<book-slug>` for new audiobooks
- Commit messages: imperative mood, concise
- Always create PRs rather than pushing directly to main
- Audio files: MP3 format, named `<slug>.mp3`
- Slugs: lowercase, hyphens, no special chars (e.g., `great-gatsby`)

## CI/CD

- GitHub Actions runs on every push and PR
- Vercel deploys automatically when PRs merge to `main`
- PR previews are generated automatically by Vercel

## Notes

- The owner prefers minimal interaction - be autonomous
- When in doubt, create a PR and let them review
- This project is about learning agents/subagents - experiment freely
