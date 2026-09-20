#!/usr/bin/env python3
"""
Generate stand-in chapter clips so the site can be built, scrubbed and
caption-timed BEFORE the real Google Flow renders exist.

  python tools/make_previz.py build.config.json

Writes one 8s placeholder per chapter into assets/clips-previz/ using the
same filenames as the real clips, then you build with:

  python tools/build_master.py build.config.json --clips assets/clips-previz

Each placeholder shows the chapter name, a pseudo-rotating block (so you can
see the scrub working) and a progress bar. Drop real clips into assets/clips/
and rebuild without --clips to replace them.
"""

import json
import os
import subprocess
import sys

W, H, FPS = 1280, 720, 24
FONT = "C\\:/Windows/Fonts/consola.ttf"

# When assets/hero.png exists, previz clips become slow camera moves over the
# real hero still instead of abstract blocks - a far better read on pacing and
# caption placement. One move per chapter: (zoom, x start->end, y start->end)
# as fractions of the available pan range.
MOVES = [
    (1.15, 0.50, 0.50, 0.45, 0.55),   # 1 ignite   - almost static, drifts down
    (1.60, 0.20, 0.55, 0.50, 0.50),   # 2 weave    - macro pan across the knit
    (1.25, 0.15, 0.85, 0.50, 0.50),   # 3 rotate   - long lateral sweep
    (1.40, 0.70, 0.30, 0.40, 0.60),   # 4 explode  - pull back across the upper
    (1.70, 0.60, 0.40, 0.75, 0.70),   # 5 sole     - macro along the midsole
    (1.30, 0.80, 0.20, 0.60, 0.45),   # 6 impact   - fast sweep to the strike
    (1.20, 0.35, 0.65, 0.50, 0.50),   # 7 colorway - gentle drift
    (1.10, 0.55, 0.45, 0.50, 0.50),   # 8 hero     - settle back to the wide
]


def build_filter(label, seconds, with_text):
    # pseudo-3D turn: the block's width oscillates like a rotating object
    bw = "(260+240*abs(sin(t*0.55)))"
    bx = "(iw-%s)/2" % bw
    by = "(ih-300)/2"
    chain = [
        "drawbox=x='%s':y='%s':w='%s':h=300:color=0x1a1f26:t=fill" % (bx, by, bw),
        "drawbox=x='%s':y='%s+300':w='%s':h=5:color=0xd6ff3d:t=fill" % (bx, by, bw),
        "drawbox=x=0:y=ih-6:w='iw*t/%s':h=6:color=0xd6ff3d@0.8:t=fill" % seconds,
        "vignette=PI/4",
    ]
    if with_text:
        chain += [
            "drawtext=fontfile='%s':text='%s':fontcolor=0xd6ff3d:fontsize=30"
            ":x=(w-text_w)/2:y=h*0.16" % (FONT, label),
            "drawtext=fontfile='%s':text='PREVIZ  %%{eif\\:n\\:d}':fontcolor=0x8a8f88"
            ":fontsize=20:x=w-text_w-40:y=h-text_h-40" % FONT,
        ]
    return ",".join(chain)


def build_image_filter(move, seconds):
    """Slow pan across an upscaled still - a fixed crop window moving over a
    larger frame. Avoids zoompan, whose per-frame output sizing is fragile."""
    zoom, x0, x1, y0, y1 = move
    sw = int(W * zoom // 2 * 2)
    return (
        "scale={sw}:-2,"
        "crop={w}:{h}:x='(iw-{w})*({x0}+({x1}-{x0})*t/{d})'"
        ":y='(ih-{h})*({y0}+({y1}-{y0})*t/{d})',"
        "fps={fps},format=yuv420p"
    ).format(sw=sw, w=W, h=H, x0=x0, x1=x1, y0=y0, y1=y1, d=seconds, fps=FPS)


def render(out_path, label, seconds, hero=None, move=None):
    if hero:
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", hero,
               "-t", str(seconds), "-vf", build_image_filter(move, seconds),
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out_path]
        subprocess.run(cmd, check=True)
        return

    for with_text in (True, False):
        cmd = ["ffmpeg", "-y", "-v", "error",
               "-f", "lavfi",
               "-i", "color=c=0x0b0c0f:s=%dx%d:d=%s:r=%d" % (W, H, seconds, FPS),
               "-vf", build_filter(label, seconds, with_text),
               "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", out_path]
        try:
            subprocess.run(cmd, check=True)
            return
        except subprocess.CalledProcessError:
            if with_text:
                print("  (drawtext unavailable - rendering without labels)")
            else:
                raise


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg_path = os.path.abspath(sys.argv[1])
    root = os.path.dirname(cfg_path)
    with open(cfg_path) as f:
        cfg = json.load(f)

    out_dir = os.path.join(root, "assets", "clips-previz")
    os.makedirs(out_dir, exist_ok=True)

    hero = os.path.join(root, "assets", "hero.png")
    if os.path.exists(hero) and "--blocks" not in sys.argv:
        print("using assets/hero.png - previz will be camera moves over the hero\n")
    else:
        hero = None
        print("no assets/hero.png - previz will be abstract blocks\n")

    for i, ch in enumerate(cfg["chapters"], 1):
        seconds = ch.get("seconds", 8)
        out_path = os.path.join(out_dir, ch["file"])
        label = "CH %d   %s" % (i, ch["name"].upper())
        print("previz %d/%d  %s" % (i, len(cfg["chapters"]), ch["file"]))
        move = MOVES[(i - 1) % len(MOVES)]
        render(out_path, label, seconds, hero=hero, move=move)

    print("\n%d placeholder clips in %s" % (len(cfg["chapters"]), out_dir))
    print("next: python tools/build_master.py build.config.json --clips assets/clips-previz")


if __name__ == "__main__":
    main()
