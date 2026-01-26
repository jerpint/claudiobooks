# Process Issues

Check for open audiobook requests and process them.

## Usage

```
/process-issues
```

## What this does

1. Fetches open issues with the `audiobook-request` label
2. For each issue, runs the `/add-audiobook` workflow
3. Comments on the issue with the PR link
4. Closes the issue

## Instructions for Claude

When this skill is invoked:

1. List open issues:
   ```bash
   gh issue list --label "audiobook-request" --state open --json number,title,body
   ```

2. For each issue:
   - Parse the title (format: "Add: Book Title")
   - Extract any Gutenberg ID from the body if provided
   - Run the full `/add-audiobook` workflow
   - Comment on the issue with the result:
     ```bash
     gh issue comment <number> --body "Created PR #XX: <link>"
     ```
   - Close the issue:
     ```bash
     gh issue close <number>
     ```

3. If no issues found, just report "No pending audiobook requests."

## Error handling

If an audiobook can't be added (book not found, etc.):
- Comment on the issue explaining the problem
- Add a `needs-info` label instead of closing
- Don't close the issue
