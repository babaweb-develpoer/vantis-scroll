#!/usr/bin/env python3
"""
Import hand-made stills (OpenArt renders, Canva exports) into the site.

  python tools/import_images.py

Drop files into assets/incoming/ named after their slot - origin.png,
gallery-2.jpg, og.png - and this centre-crops each to its slot's aspect ratio,
scales it, converts to WebP and writes img/<slot>.webp.

og and favicon stay PNG (link previews and browser tabs want PNG).

Run this AFTER tools/make_stills.py, not before: make_stills overwrites img/
with crops cut from the film.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_DIR = os.path.join(ROOT, "assets", "incoming")
OUT_DIR = os.path.join(ROOT, "img")
QUALITY = 82

# slot -> (aspect ratio, output width, format)
SLOTS = {
    "origin":     (16 / 10, 1400, "webp"),
    "knit-macro": (16 / 10, 1400, "webp"),
    "sole-macro": (16 / 10, 1400, "webp"),
    "gallery-1":  (4 / 3,   1400, "webp"),
    "gallery-2":  (4 / 5,   1100, "webp"),
    "gallery-3":  (1 / 1,   1200, "webp"),
    "gallery-4":  (16 / 10, 1400, "webp"),
    "og":         (1200 / 630, 1200, "png"),
    "favicon":    (1 / 1,     32, "png"),
}

EXTS = (".png", ".jpg", ".jpeg", ".webp", ".avif")


def main():
    if not os.path.isdir(IN_DIR):
        os.makedirs(IN_DIR, exist_ok=True)
        sys.exit("created " + IN_DIR + " - put your images there and re-run")

    os.makedirs(OUT_DIR, exist_ok=True)
    found = {}
    unknown = []
    for f in sorted(os.listdir(IN_DIR)):
        stem, ext = os.path.splitext(f)
        if ext.lower() not in EXTS:
            continue
        if stem in SLOTS:
            found[stem] = os.path.join(IN_DIR, f)
        else:
            unknown.append(f)

    if unknown:
        print("skipped (name doesn't match a slot):")
        for f in unknown:
            print("   - " + f)
        print("   valid slots: " + ", ".join(SLOTS) + "\n")

    if not found:
        sys.exit("nothing to import from " + IN_DIR)

    for slot, src in found.items():
        aspect, width, fmt = SLOTS[slot]
        out = os.path.join(OUT_DIR, slot + "." + fmt)
        # centre-crop to the slot's aspect, then scale; trunc keeps dims even
        vf = ("crop=w='trunc(min(iw,ih*{a})/2)*2':h='trunc(min(ih,iw/{a})/2)*2',"
              "scale={w}:-2").format(a=aspect, w=width)
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-frames:v", "1"]
        if fmt == "webp":
            cmd += ["-c:v", "libwebp", "-quality", str(QUALITY), "-compression_level", "5"]
        cmd.append(out)
        subprocess.run(cmd, check=True)
        kb = os.path.getsize(out) / 1024
        print("  {0:<12} -> img/{1}.{2}  ({3:.0f} KB)".format(
            os.path.basename(src), slot, fmt, kb))

    print("\n{0} image(s) imported to img/".format(len(found)))
    missing = [s for s in SLOTS if s not in found and s not in ("og", "favicon")]
    if missing:
        print("still coming from the film (make_stills.py): " + ", ".join(missing))


if __name__ == "__main__":
    main()
