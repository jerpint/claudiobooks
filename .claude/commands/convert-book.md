# Convert Book

Convert an ebook to text using Calibre for summarization.

## Usage

```
/convert-book <path-to-ebook>
```

Examples:
- `/convert-book ~/Downloads/some-book.mobi`
- `/convert-book ~/Downloads/another-book.epub`

## Supported formats

Calibre supports: mobi, epub, azw, azw3, pdf, and many others.

## What this does

1. Copies the ebook to `/tmp/book.<ext>` (avoids path issues)
2. Converts to plain text using Calibre's `ebook-convert`
3. Outputs to `/tmp/book.txt`
4. Reports word count and preview

## Instructions for Claude

When this skill is invoked:

1. Check Calibre is installed:
   ```bash
   ls /Applications/calibre.app/Contents/MacOS/ebook-convert
   ```
   If not found, tell user to install: `brew install --cask calibre`

2. Copy the file to /tmp to avoid path escaping issues:
   ```bash
   cp "<source_path>" /tmp/book.<extension>
   ```

3. Convert to text:
   ```bash
   /Applications/calibre.app/Contents/MacOS/ebook-convert /tmp/book.<ext> /tmp/book.txt
   ```

4. Report results:
   ```bash
   wc -w /tmp/book.txt  # word count
   head -100 /tmp/book.txt  # preview
   ```

5. The text is now ready at `/tmp/book.txt` for reading and summarizing.

## After conversion

To create a podcast summary:
1. Read the book text in chunks
2. Write a podcast-style summary (see `/add-audiobook` for style guide)
3. Generate audio: `cd pipeline && uv run tts.py <summary> /tmp/<output>.mp3 [voice]`

## Notes

- This is for personal/local use only
- Output stays in /tmp, not committed to repo
- For public domain books, use `/add-audiobook` instead
