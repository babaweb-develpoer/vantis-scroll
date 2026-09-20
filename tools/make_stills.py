#!/usr/bin/env python3
"""
Cut the brand-page stills out of the finished master film - crops of frames
you already paid for, so the page below the film costs zero extra renders.

  python tools/make_stills.py build.config.json

Writes img/*.webp. Edit STILLS below: (output name, position in the film
0-1, aspect ratio, zoom, vertical bias -1..1).
Zoom 1.0 = widest centred crop at that aspect; 2.0 = punched in twice as far.
"""

import json
import os
import subprocess
import sys

OUT_WIDTH = 1400
QUALITY = 82

STILLS = [
    # name          at     aspect  zoom  y-bias   beat in the film
    ("origin",     0.060, 16 / 10, 1.00,  0.00),  # the pair, floating wide
    ("knit-macro", 0.290, 16 / 10, 1.25, -0.10),  # macro, the upper mesh
    ("sole-macro", 0.375, 16 / 10, 1.00,  0.00),  # outsole from below
    ("gallery-1",  0.500, 4 / 3,   1.00,  0.00),  # hanging by the laces
    ("gallery-2",  0.625, 4 / 5,   1.10,  0.00),  # floating, three-quarter
    ("gallery-3",  0.750, 1 / 1,   1.10,  0.00),  # macro, the air unit
    ("gallery-4",  0.930, 16 / 10, 1.00,  0.00),  # final wide
]


def probe(path, entries, stream=False):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", "v", "-show_entries", "stream=" + entries]
    else:
        cmd += ["-show_entries", "format=" + entries]
    cmd += ["-of", "csv=p=0", path]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return out.stdout.strip().split("\n")[0]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg_path = os.path.abspath(sys.argv[1])
    root = os.path.dirname(cfg_path)
    with open(cfg_path) as f:
        cfg = json.load(f)

    master = cfg.get("master", "assets/master.mp4")
    master = master if os.path.isabs(master) else os.path.join(root, master)
    if not os.path.exists(master):
        sys.exit("no master film yet - run tools/build_master.py first")

    out_dir = os.path.join(root, "img")
    os.makedirs(out_dir, exist_ok=True)

    total = float(probe(master, "duration"))
    sw, sh = (int(v) for v in probe(master, "width,height", stream=True).split(",")[:2])

    for name, at, aspect, zoom, bias in STILLS:
        # widest crop of this aspect that fits the frame, then zoom in
        if sw / sh > aspect:
            cw, chh = sh * aspect, float(sh)
        else:
            cw, chh = float(sw), sw / aspect
        cw, chh = cw / zoom, chh / zoom
        cw, chh = int(cw // 2 * 2), int(chh // 2 * 2)
        x = int((sw - cw) / 2)
        y = int((sh - chh) / 2 * (1 + bias))
        y = max(0, min(y, sh - chh))
        out = os.path.join(out_dir, name + ".webp")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % (at * total), "-i", master,
             "-frames:v", "1",
             "-vf", "crop=%d:%d:%d:%d,scale=%d:-2" % (cw, chh, x, y, OUT_WIDTH),
             "-c:v", "libwebp", "-quality", str(QUALITY), "-compression_level", "5", out],
            check=True)
        print("  img/%s.webp   at %.3f  %dx%d crop" % (name, at, cw, chh))

    print("\n%d stills written to img/" % len(STILLS))


if __name__ == "__main__":
    main()
