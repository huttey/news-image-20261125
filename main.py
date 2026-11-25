#!/usr/bin/env python3
"""Copy the news front page image to the output directory.

The entry is the image file beside this program. Before copying,
the gate is checked: the data must be a whole PNG or a whole JPEG,
at most 1048576 bytes, and a PNG must be at most 1024x1024 pixels.
On a gate failure the program prints why and exits non-zero.
"""
import os
import struct
import sys

MAX_BYTES = 1048576
MAX_PNG_SIDE = 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


def is_whole_png(data):
    """True if data is a complete PNG within the pixel limit."""
    if not data.startswith(PNG_MAGIC):
        return False
    # Walk the chunks; a whole PNG ends with an IEND chunk.
    pos = len(PNG_MAGIC)
    seen_ihdr = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            return False
        if ctype == b"IHDR":
            if length != 13:
                return False
            width, height = struct.unpack(">II", data[pos + 8:pos + 16])
            if width > MAX_PNG_SIDE or height > MAX_PNG_SIDE:
                return False
            seen_ihdr = True
        if ctype == b"IEND":
            return seen_ihdr
        pos = end
    return False


def is_whole_jpeg(data):
    """True if data starts with SOI and ends with EOI."""
    return data.startswith(JPEG_SOI) and data.endswith(JPEG_EOI)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("gate fail: image over 1048576 bytes", file=sys.stderr)
        return 1
    if not (is_whole_png(data) or is_whole_jpeg(data)):
        print("gate fail: not a whole PNG or JPEG", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
