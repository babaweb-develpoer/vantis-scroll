# VANTIS 01 — scroll film site

**Live: <https://babaweb-develpoer.github.io/vantis-scroll/>**

An Apple-style scroll-driven product site for a fictional racing shoe. Scroll
position scrubs a frame sequence on a canvas (the AirPods technique), then the
page continues into a full brand homepage below the film.

VANTIS is an invented brand and the footage is AI-generated; nothing here is a
real product.

**It now runs on your real footage**: `assets/clips/float.mp4`, a 10-second
clip of a bone-white pair in a white studio, sliced into **240 WebP frames**
(24 fps, native, 6.7 MB).

The palette follows the film. It was originally near-black with a volt-yellow
accent, built for a dark single-shoe brief; white-studio footage on a near-black
page reads as a glowing rectangle with muddy letterbox bars, so the page is now
bone white (`#f3f1ee`) with charcoal ink and no accent colour. The engine reads
`--bg` from the page, so the canvas letterbox fill follows the theme
automatically — if you flip the palette again, the film follows.

Seven captions are timed to the film's real beats:

| Beat | Scroll | Caption |
|---|---|---|
| Title | 0.00 | VANTIS 01 |
| Angled float | 0.12–0.21 | Bone white, head to toe |
| Macro, upper | 0.23–0.31 | One thread. No seams. |
| Outsole | 0.33–0.44 | Every contact, mapped |
| Hanging by laces | 0.46–0.56 | One hundred and ninety grams |
| Macro, air unit | 0.70–0.81 | It gives it back |
| Final wide | 0.86–1.00 | VANTIS 01 + CTA |

`assets/clips-previz/` still holds the old placeholder clips; delete them
whenever you like.

## Run it

```bash
git clone https://github.com/babaweb-develpoer/vantis-scroll.git
```

```bash
python -m http.server 4173 -d vantis-scroll
```

Then open <http://localhost:4173>. Any static server works; there is no build
step and no dependencies. Rebuilding the film needs only **ffmpeg** (WebP is
encoded by libwebp inside ffmpeg, so there is no Pillow dependency) and
Python 3 for the scripts in `tools/`.

## The two prompt packs

- [PROMPTS.md](PROMPTS.md) — **Google Flow** video clips. ⚠ Its prompts still
  describe the original dark single-shoe brief; the file opens with the
  replacement anchor text to use instead.
- [IMAGES.md](IMAGES.md) — stills: **OpenArt** model picks and credit costs,
  **Canva**'s jobs, and where each file goes. The Canva route produced
  `assets/hero.png`, which belongs to the *dark* brief and is not used by the
  current light build.

## Adding more film

1. Render clips in Google Flow — see the note at the top of
   [PROMPTS.md](PROMPTS.md) about the changed brief.
2. Save them into `assets/clips/` and add them to `chapters` in
   `build.config.json`, in the order they should play.
3. Build:
   ```bash
   python tools/build_master.py build.config.json
   ```
   This crossfades the chapters into `assets/master.mp4`, slices WebP frames
   into `frames/`, writes `frames/frames.json`, and prints per-chapter scroll
   fractions.
4. Re-cut the brand-page stills from the new film (no extra renders needed):
   ```bash
   python tools/make_stills.py build.config.json
   ```
   If you'd rather use your own OpenArt/Canva stills for some slots, put them
   in `assets/incoming/` and run `python tools/import_images.py` **after** this
   step — it crops, converts and overwrites just the slots you supplied.
5. Reload. Adding chapters moves every fraction — paste the printed table to
   me and I'll re-time the captions, or edit the `data-in` / `data-hold` /
   `data-out` attributes in `index.html` yourself (each caption block is
   commented with the beat it belongs to). Raise `#track` height by roughly
   120vh per added chapter.

## Layout

```
index.html          film, captions, brand page, nav, footer — edit freely
main.js             the scrubber engine — rarely needs touching
build.config.json   chapter list, fps, width, quality, crossfade
frames/             built WebP sequence + frames.json
img/                brand-page stills (cut from the film)
assets/clips/       your Google Flow renders go here
assets/incoming/    your OpenArt / Canva stills go here
assets/clips-previz/ placeholder clips (delete once real ones land)
tools/build_master.py   clips  -> master film -> frames + caption fractions
tools/make_stills.py    master -> img/*.webp crops for the brand page
tools/import_images.py  assets/incoming -> cropped, converted img/*
tools/make_previz.py    regenerate the placeholders
```

## How the engine works

- `#track` is a 700vh div with a `position: sticky` full-viewport stage.
  Scroll progress = `scrollY / (track height − viewport height)`.
- Frames are fetched as compressed blobs up front; only a sliding window of
  ±120 decoded frames exists at a time, so phone RAM stays sane.
- Decoding prefers `createImageBitmap` and falls back to an `HTMLImageElement`
  — `createImageBitmap` throws in hidden tabs and some webviews, which would
  otherwise leave the canvas blank on a deployed site. Don't remove the
  fallback.
- A time-based lerp (`1 − exp(−dt·14)`) smooths the frame target, so fast
  flicks glide and throttled tabs still converge.
- Captions are absolutely positioned divs with `data-in` / `data-hold` /
  `data-out` scroll fractions; opacity is computed per frame. The opening title
  has a negative `data-in` so it's visible at scroll 0.
- Frames are drawn contain-fit with 4% overscan over a fill read from the
  page's `--bg`, so the letterbox matches the theme; `#vignette` feathers the
  edges and `#scrim` washes the flanks so captions stay legible over a
  near-white film.
- The frames manifest is fetched with `cache: "no-cache"`. It must revalidate —
  it keeps the same URL across rebuilds, and a cached copy leaves the engine
  scrubbing a frame count the film no longer has.

## Tuning

In `build.config.json`: `fps` 24 at `width` 1280 gives 240 frames for the
10-second clip — native frame rate, so nothing is dropped or duplicated, at
6.7 MB. Longer films want `fps` 12–16 to keep the download sane; the build
prints the total and warns past 30 MB. `xfade` is the crossfade between
chapters, only used once there is more than one.

## Brand

Bone white `#f3f1ee`, charcoal ink `#17181b`, no accent colour — the film is
monochrome, so the page is too. Tight-tracked display type, generous negative
space. Product copy, specs and stats are invented and tasteful — swap in real
ones if this becomes real.
