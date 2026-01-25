"""
Generate audio from text using OpenAI TTS.

Usage:
    uv run tts.py <input_file> <output_file>
    uv run tts.py summary.txt output.mp3
"""

import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")


def generate_audio(
    text: str,
    output_path: Path,
    voice: str = "onyx",  # Good for narration: alloy, echo, fable, onyx, nova, shimmer
    model: str = "tts-1-hd",  # tts-1 for speed, tts-1-hd for quality
) -> Path:
    """
    Generate audio from text using OpenAI TTS.

    For long texts, splits into chunks (max 4096 chars per request).
    """
    client = OpenAI()

    # OpenAI TTS has a 4096 character limit per request
    max_chars = 4096

    if len(text) <= max_chars:
        # Single request
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
        )
        response.stream_to_file(output_path)
    else:
        # Split into chunks at sentence boundaries
        chunks = split_into_chunks(text, max_chars)
        temp_files = []

        print(f"Generating {len(chunks)} audio chunks...")
        for i, chunk in enumerate(chunks):
            temp_path = output_path.parent / f"_temp_chunk_{i}.mp3"
            print(f"  Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")

            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=chunk,
            )
            response.stream_to_file(temp_path)
            temp_files.append(temp_path)

        # Concatenate chunks (requires ffmpeg)
        concat_audio_files(temp_files, output_path)

        # Cleanup temp files
        for temp_file in temp_files:
            temp_file.unlink()

    return output_path


def split_into_chunks(text: str, max_chars: int) -> list[str]:
    """Split text into chunks at sentence boundaries."""
    chunks = []
    current_chunk = ""

    # Split by sentences (roughly)
    sentences = text.replace('\n', ' ').split('. ')

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        test_chunk = current_chunk + (". " if current_chunk else "") + sentence

        if len(test_chunk) > max_chars:
            if current_chunk:
                chunks.append(current_chunk + ".")
            current_chunk = sentence
        else:
            current_chunk = test_chunk

    if current_chunk:
        chunks.append(current_chunk + "." if not current_chunk.endswith('.') else current_chunk)

    return chunks


def concat_audio_files(input_files: list[Path], output_path: Path):
    """Concatenate audio files using ffmpeg."""
    import subprocess

    # Create file list for ffmpeg
    list_file = output_path.parent / "_temp_filelist.txt"
    with open(list_file, 'w') as f:
        for path in input_files:
            f.write(f"file '{path.absolute()}'\n")

    # Run ffmpeg
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(list_file), '-c', 'copy', str(output_path)
    ], check=True, capture_output=True)

    list_file.unlink()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    text = input_path.read_text()
    print(f"Generating audio for {len(text)} characters...")

    generate_audio(text, output_path)
    print(f"Audio saved to: {output_path}")
