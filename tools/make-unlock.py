#!/usr/bin/env python3
"""Rebuild unlock.png: the Omarchy wordmark in the Sorbet Noir pastel gradient.

    python3 tools/make-unlock.py [SOURCE_UNLOCK_PNG] [OUTPUT_PNG]

Takes any stock theme's unlock.png as the shape source, keeps its alpha mask
pixel-for-pixel, and repaints the glyphs with a left-to-right pastel sweep.
Defaults read a stock theme and write ./unlock.png.

Requires ImageMagick (`magick`). No Python dependencies.

Afterwards, regenerate the companion preview with Omarchy's own tool:

    omarchy plymouth preview 000000 a8f0dc unlock.png preview-unlock.png
"""
import subprocess, sys, os, tempfile

SRC = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/omarchy/themes/catppuccin/unlock.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "unlock.png"

def hx(s): return tuple(int(s[i:i+2], 16) for i in (1, 3, 5))

# The same ramp the focused-window border uses, extended through peach.
STOPS = [hx(c) for c in ("#a8f0dc", "#9ce8de", "#a2c4ff", "#dcaaff", "#ff9aa9", "#ffbd94")]

def ramp(t):
    t = min(max(t, 0.0), 1.0)
    n = len(STOPS) - 1
    i = min(int(t * n), n - 1)
    f = t * n - i
    a, b = STOPS[i], STOPS[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))

if not os.path.isfile(SRC):
    sys.exit(f"source not found: {SRC}")

W, H = map(int, subprocess.run(
    ["magick", "identify", "-format", "%w %h", SRC],
    capture_output=True, text=True, check=True).stdout.split())

with tempfile.TemporaryDirectory() as tmp:
    mask = os.path.join(tmp, "mask.png")
    plate = os.path.join(tmp, "plate.png")
    ppm = os.path.join(tmp, "plate.ppm")

    subprocess.run(["magick", SRC, "-alpha", "extract", mask], check=True)

    buf = bytearray(W * H * 3)
    for y in range(H):
        row = y * W * 3
        for x in range(W):
            c = ramp(x / W)
            i = row + x * 3
            buf[i], buf[i + 1], buf[i + 2] = c
    open(ppm, "wb").write(b"P6\n%d %d\n255\n" % (W, H) + bytes(buf))
    subprocess.run(["magick", ppm, plate], check=True)

    # Paint the gradient through the wordmark's own alpha, so the glyph shapes
    # and their antialiasing are preserved exactly.
    subprocess.run(["magick", plate, mask, "-alpha", "off",
                    "-compose", "copy_opacity", "-composite", OUT], check=True)

print(f"wrote {OUT}  ({W}x{H})")
