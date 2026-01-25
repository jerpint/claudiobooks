"""
Fetch books from Project Gutenberg.

Usage:
    uv run fetch.py <gutenberg_id>
    uv run fetch.py 76  # Adventures of Tom Sawyer
    uv run fetch.py 84  # Frankenstein
"""

import sys
import requests
from pathlib import Path


def fetch_gutenberg_text(book_id: int) -> tuple[str, dict]:
    """
    Fetch a book's plain text from Project Gutenberg.
    Returns (text_content, metadata).
    """
    # Try different URL patterns (Gutenberg has various formats)
    urls = [
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
    ]

    text = None
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                text = response.text
                break
        except requests.RequestException:
            continue

    if text is None:
        raise ValueError(f"Could not fetch book {book_id} from Project Gutenberg")

    # Extract basic metadata from the text header
    metadata = {
        "gutenberg_id": book_id,
        "source_url": f"https://www.gutenberg.org/ebooks/{book_id}",
    }

    # Try to extract title and author from the header
    lines = text[:3000].split('\n')
    for line in lines:
        line_lower = line.lower()
        if 'title:' in line_lower:
            metadata['title'] = line.split(':', 1)[1].strip()
        elif 'author:' in line_lower:
            metadata['author'] = line.split(':', 1)[1].strip()

    return text, metadata


def save_book(book_id: int, output_dir: Path = None) -> Path:
    """Fetch and save a book to the output directory."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "books"

    output_dir.mkdir(exist_ok=True)

    print(f"Fetching book {book_id} from Project Gutenberg...")
    text, metadata = fetch_gutenberg_text(book_id)

    # Create filename from metadata or ID
    title = metadata.get('title', f'book-{book_id}')
    safe_title = "".join(c if c.isalnum() or c in ' -' else '' for c in title)
    safe_title = safe_title.strip().replace(' ', '-').lower()[:50]

    output_path = output_dir / f"{safe_title}-{book_id}.txt"
    output_path.write_text(text)

    print(f"Saved to: {output_path}")
    print(f"Title: {metadata.get('title', 'Unknown')}")
    print(f"Author: {metadata.get('author', 'Unknown')}")

    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    book_id = int(sys.argv[1])
    save_book(book_id)
