"""Self-check for assets/blackmere-technical-walkthrough.gif.

Checks existence, exact dimensions, frame count, total duration bounds,
looping, and the reviewed decoded frame/timing digest. Run after
make_technical_walkthrough.py:

    python verify_walkthrough.py
"""

import hashlib
import struct
import sys
from pathlib import Path

from PIL import Image

GIF = Path(__file__).resolve().parent.parent / "assets" / "blackmere-technical-walkthrough.gif"
EXPECTED_SIZE = (1280, 720)
MIN_DURATION_S = 60
MAX_DURATION_S = 90
MIN_FRAMES = 20
EXPECTED_DECODED_SHA256 = "1aa1a8664cdbd065970dbeba3000169f6a9256354bbec78e195b4a30bbcad8dc"


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
    decoded_digest = hashlib.sha256()
    try:
        while True:
            duration_ms = im.info.get("duration", 0)
            total_ms += duration_ms
            decoded_digest.update(struct.pack("<I", duration_ms))
            decoded_digest.update(im.convert("RGBA").tobytes())
            frame_count += 1
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    total_s = total_ms / 1000

    if frame_count < MIN_FRAMES:
        errors.append(f"frame_count={frame_count} < minimum {MIN_FRAMES}")

    if not (MIN_DURATION_S <= total_s <= MAX_DURATION_S):
        errors.append(f"total_duration={total_s:.1f}s outside [{MIN_DURATION_S}, {MAX_DURATION_S}]s")

    decoded_sha256 = decoded_digest.hexdigest()
    if decoded_sha256 != EXPECTED_DECODED_SHA256:
        errors.append(
            "decoded frame/timing digest changed: "
            f"{decoded_sha256} != {EXPECTED_DECODED_SHA256}"
        )

    size_bytes = GIF.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    print(f"path: {GIF}")
    print(f"dimensions: {im.size}")
    print(f"loop: {loop}")
    print(f"frames: {frame_count}")
    print(f"duration: {total_s:.1f}s")
    print(f"decoded SHA-256: {decoded_sha256}")
    print(f"file size: {size_mb:.2f} MB")

    if errors:
        print("\nFAIL:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nOK: all checks passed")


if __name__ == "__main__":
    main()
