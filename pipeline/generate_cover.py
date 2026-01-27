#!/usr/bin/env python3
"""Generate podcast cover artwork for Claudiobooks."""

import sys
from PIL import Image, ImageDraw, ImageFont

# Podcast cover requirements: 1400x1400 minimum, 3000x3000 maximum
SIZE = 3000
CENTER = SIZE // 2

# Colors (matching site branding)
PURPLE = (139, 92, 246)  # #8b5cf6
PURPLE_DARK = (109, 62, 216)  # darker shade for depth
WHITE = (255, 255, 255)
OFF_WHITE = (250, 249, 247)  # #faf9f7


def create_cover(output_path: str):
    """Create the podcast cover image."""
    # Create image with gradient-like background
    img = Image.new('RGB', (SIZE, SIZE), PURPLE)
    draw = ImageDraw.Draw(img)

    # Add subtle radial gradient effect (lighter in center)
    for i in range(SIZE // 2, 0, -10):
        alpha = int(255 * (i / (SIZE // 2)) * 0.15)
        color = (
            min(255, PURPLE[0] + alpha),
            min(255, PURPLE[1] + alpha),
            min(255, PURPLE[2] + alpha)
        )
        draw.ellipse(
            [CENTER - i, CENTER - i, CENTER + i, CENTER + i],
            fill=color
        )

    # Draw play button (triangle) - larger and centered upper area
    play_size = 600
    play_center_y = CENTER - 200

    # Play button triangle points
    triangle = [
        (CENTER - play_size // 2, play_center_y - play_size // 2),  # top left
        (CENTER - play_size // 2, play_center_y + play_size // 2),  # bottom left
        (CENTER + play_size // 2 + 100, play_center_y),  # right point
    ]
    draw.polygon(triangle, fill=WHITE)

    # Add "CLAUDIOBOOKS" text
    # Try to use a nice font, fall back to default
    font_size = 280
    try:
        # Try common fonts
        for font_name in ['Arial Bold', 'Helvetica Bold', 'DejaVuSans-Bold', 'FreeSans']:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except OSError:
                continue
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    text = "CLAUDIOBOOKS"
    text_y = CENTER + 450

    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (SIZE - text_width) // 2

    draw.text((text_x, text_y), text, fill=WHITE, font=font)

    # Add tagline
    tagline_size = 100
    try:
        for font_name in ['Arial', 'Helvetica', 'DejaVuSans', 'FreeSans']:
            try:
                tagline_font = ImageFont.truetype(font_name, tagline_size)
                break
            except OSError:
                continue
        else:
            tagline_font = ImageFont.load_default()
    except Exception:
        tagline_font = ImageFont.load_default()

    tagline = "Classic Literature, AI Narrated"
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (SIZE - tagline_width) // 2
    tagline_y = text_y + 320

    draw.text((tagline_x, tagline_y), tagline, fill=OFF_WHITE, font=tagline_font)

    # Save
    img.save(output_path, 'PNG', optimize=True)
    print(f"Created podcast cover: {output_path}")
    print(f"Size: {SIZE}x{SIZE} pixels")


if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else '../site/public/podcast-cover.png'
    create_cover(output)
