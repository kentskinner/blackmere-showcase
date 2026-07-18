"""Self-check for assets/blackmere-technical-walkthrough.gif.

Checks existence, exact dimensions, frame count, total duration bounds,
and that the GIF loops. Run after make_technical_walkthrough.py:

    python verify_walkthrough.py
"""

import sys
from pathlib import Path

from PIL import Image

GIF = Path(__file__).resolve().parent.parent / "assets" / "blackmere-technical-walkthrough.gif"
EXPECTED_SIZE = (1280, 720)
MIN_DURATION_S = 60
MAX_DURATION_S = 90
MIN_FRAMES = 20


def main():
    errors = []

    if not GIF.exists():
        print(f"FAIL: {GIF} does not exist")
        sys.exit(1)

    im = Image.open(GIF)

    if im.size != EXPECTED_SIZE:
        errors.append(f"size {im.size} != expected {EXPECTED_SIZE}")

    loop = im.info.get("loop")
    if loop != 0:
        errors.append(f"loop={loop!r}, expected 0 (infinite loop)")

    frame_count = 0
    total_ms = 0
    try:
        while True:
            total_ms += im.info.get("duration", 0)
            frame_count += 1
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    total_s = total_ms / 1000

    if frame_count < MIN_FRAMES:
        errors.append(f"frame_count={frame_count} < minimum {MIN_FRAMES}")

    if not (MIN_DURATION_S <= total_s <= MAX_DURATION_S):
        errors.append(f"total_duration={total_s:.1f}s outside [{MIN_DURATION_S}, {MAX_DURATION_S}]s")

    size_bytes = GIF.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    print(f"path: {GIF}")
    print(f"dimensions: {im.size}")
    print(f"loop: {loop}")
    print(f"frames: {frame_count}")
    print(f"duration: {total_s:.1f}s")
    print(f"file size: {size_mb:.2f} MB")

    if errors:
        print("\nFAIL:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nOK: all checks passed")


if __name__ == "__main__":
    main()
