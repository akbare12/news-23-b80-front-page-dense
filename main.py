#!/usr/bin/env python3
"""news-23 b80 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

SRC_NAME = "entry.png"
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(src):
        return fail("missing " + src)

    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))

    # Parse the PNG header by hand (struct): signature, IHDR size, CRC, IDAT, IEND.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    pos = 8
    width = height = None
    seen_idat = False
    seen_iend = False
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        chunk_end = pos + 8 + length + 4
        if chunk_end > len(data):
            return fail("truncated chunk " + repr(ctype))
        body = data[pos + 8:pos + 8 + length]
        crc_stored, = struct.unpack(">I", data[pos + 8 + length:chunk_end])
        crc_calc = binascii.crc32(ctype + body) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            return fail("CRC mismatch in chunk " + repr(ctype))
        if ctype == b"IHDR":
            width, height, depth, ctype_code = struct.unpack(">IIBB", body[:10])
            if (width, height) != (1024, 1024):
                return fail("IHDR is %dx%d, expected 1024x1024" % (width, height))
            if depth != 8 or ctype_code not in (2, 6):
                return fail("unexpected IHDR bit depth / colour type")
        elif ctype == b"IDAT":
            seen_idat = True
            if length == 0:
                return fail("empty IDAT chunk")
        elif ctype == b"IEND":
            if length != 0:
                return fail("IEND must be empty")
            seen_iend = True
            break
        pos = chunk_end
    if not seen_idat:
        return fail("no IDAT chunk found")
    if not seen_iend:
        return fail("no well-formed IEND trailer found")

    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        return fail("output differs from source")
    print("entry.png %d bytes sha256 %s" % (len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
