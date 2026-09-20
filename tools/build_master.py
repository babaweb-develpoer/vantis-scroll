#!/usr/bin/env python3
"""
Crossfade-concat the chapter clips into one master film, slice it into WebP
scrub frames, write frames/frames.json, and print the scroll fractions you
need to calibrate the captions in index.html.

  python tools/build_master.py build.config.json
  python tools/build_master.py build.config.json --clips assets/clips-previz

Only ffmpeg is required (WebP is encoded by libwebp inside ffmpeg, so there
is no Pillow dependency). Paths in the config are relative to the config file.

Config:
{
  "clips_dir": "assets/clips",
  "frames_dir": "frames",
  "master": "assets/master.mp4",
  "fps": 12, "width": 1280, "quality": 78, "xfade": 0.5,
  "chapters": [ {"name": "ignite", "file": "ch1-ignite.mp4"},
                {"name": "assembly", "file": "ch4-explode.mp4", "reverse": true} ]
}

A chapter with "reverse": true is played backwards (cached as <file>-rev.mp4).
"""

import json
import os
import shutil
import subprocess
import sys


def run(cmd):
    print("+ ffmpeg", " ".join(str(c) for c in cmd[1:6]), "...")
    subprocess.run(cmd, check=True)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def dimensions(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True)
    w, h = out.stdout.strip().split("\n")[0].split(",")[:2]
    return int(w), int(h)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found on PATH")

    cfg_path = os.path.abspath(sys.argv[1])
    root = os.path.dirname(cfg_path)
    with open(cfg_path) as f:
        cfg = json.load(f)

    def rel(p):
        return p if os.path.isabs(p) else os.path.join(root, p)

    clips_dir = rel(cfg.get("clips_dir", "assets/clips"))
    if "--clips" in sys.argv:
        clips_dir = rel(sys.argv[sys.argv.index("--clips") + 1])
    frames_dir = rel(cfg.get("frames_dir", "frames"))
    master = rel(cfg.get("master", "assets/master.mp4"))
    fps = cfg.get("fps", 12)
    width = cfg.get("width", 1280)
    quality = cfg.get("quality", 78)
    xfade = cfg.get("xfade", 0.5)

    inputs = []
    missing = []
    for ch in cfg["chapters"]:
        src = os.path.join(clips_dir, ch["file"])
        if not os.path.exists(src):
            missing.append(ch["file"])
            continue
        if ch.get("reverse"):
            revd = src.rsplit(".", 1)[0] + "-rev.mp4"
            if not os.path.exists(revd) or os.path.getmtime(revd) < os.path.getmtime(src):
                run(["ffmpeg", "-y", "-v", "error", "-i", src,
                     "-vf", "reverse", "-an", "-crf", "16", revd])
            src = revd
        inputs.append((ch["name"], src, duration(src)))

    if missing:
        print("missing clips in " + clips_dir + ":")
        for m in missing:
            print("   - " + m)
        if not inputs:
            sys.exit("nothing to build")
        print("building with the " + str(len(inputs)) + " clip(s) present\n")

    args = ["ffmpeg", "-y", "-v", "error"]
    for _, src, _ in inputs:
        args += ["-i", src]

    # xfade needs identical geometry/fps on every input; Flow renders can
    # differ (1080p vs 720p, 24 vs 30fps), so normalise to the first clip.
    W, H = dimensions(inputs[0][1])
    filters = []
    for i in range(len(inputs)):
        filters.append(
            "[{0}:v]scale={1}:{2}:force_original_aspect_ratio=decrease,"
            "pad={1}:{2}:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p,setsar=1[n{0}]"
            .format(i, W, H))

    meta = [{"name": inputs[0][0], "start": 0.0}]
    prev, prev_end = "[n0]", inputs[0][2]
    for i in range(1, len(inputs)):
        name, _, dur = inputs[i]
        offset = prev_end - xfade
        out = "[v%d]" % i
        filters.append(
            "{0}[n{1}]xfade=transition=fade:duration={2}:offset={3:.4f}{4}"
            .format(prev, i, xfade, offset, out))
        meta.append({"name": name, "start": offset})
        prev, prev_end = out, offset + dur
    total = prev_end

    os.makedirs(os.path.dirname(master) or ".", exist_ok=True)
    if len(inputs) == 1:
        args += ["-filter_complex", ";".join(filters), "-map", "[n0]"]
    else:
        args += ["-filter_complex", ";".join(filters), "-map", prev]
    args += ["-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", master]
    run(args)

    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        if f.endswith(".webp"):
            os.remove(os.path.join(frames_dir, f))
    run(["ffmpeg", "-y", "-v", "error", "-i", master,
         "-vf", "fps={0},scale={1}:-2".format(fps, width),
         "-c:v", "libwebp", "-lossless", "0", "-quality", str(quality),
         "-compression_level", "5", "-preset", "picture",
         os.path.join(frames_dir, "frame_%04d.webp")])

    webps = sorted(f for f in os.listdir(frames_dir) if f.endswith(".webp"))
    if not webps:
        sys.exit("no frames were written - check the ffmpeg output above")

    with open(os.path.join(frames_dir, "frames.json"), "w") as f:
        json.dump({"count": len(webps), "pattern": "frames/frame_%04d.webp"}, f)

    size = sum(os.path.getsize(os.path.join(frames_dir, f))
               for f in os.listdir(frames_dir)) / 1e6
    print("\nmaster: {0:.1f}s  ->  {1} frames @ {2}px, {3:.1f} MB total"
          .format(total, len(webps), width, size))
    if size > 30:
        print("  (over ~30 MB: drop fps to 10 or quality to 70)")

    print("\ncaption calibration - paste these into index.html:")
    print("  {0:<12} {1:>8}  {2:>8} {3:>8} {4:>8}"
          .format("chapter", "starts", "data-in", "hold", "out"))
    for idx, m in enumerate(meta):
        start = m["start"] / total
        end = (meta[idx + 1]["start"] / total) if idx + 1 < len(meta) else 1.0
        span = end - start
        print("  {0:<12} {1:>8.3f}  {2:>8.3f} {3:>8.3f} {4:>8.3f}".format(
            m["name"], start,
            start + span * 0.11, start + span * 0.48, start + span * 0.90))


if __name__ == "__main__":
    main()
