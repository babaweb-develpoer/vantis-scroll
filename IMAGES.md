# VANTIS 01 — image pack (OpenArt + Canva)

Companion to [PROMPTS.md](PROMPTS.md), which covers the eight Google Flow
video clips. This file covers every still: what to generate in OpenArt, what
to fix in Canva, and where each finished file goes.

## Status

- **`assets/hero.png` is done** — 1920x1080, unwatermarked, generated in
  **Canva** (`desktop_wallpaper`, which is natively 16:9). Side profile facing
  right with the bone-white midsole, which is what every clip prompt assumes.
  Upload this to Flow as the ingredient for chapters 3, 4, 6, 7 and 8.
- **OpenArt is on the Free plan**, so its output arrives with a large "OpenArt"
  watermark burned in. Two candidates are kept in `assets/` as composition
  references only (`hero-A-sideprofile-WATERMARKED.png`,
  `hero-B-threequarter-WATERMARKED.png`). The prompts below are proven — they
  worked first try — so a paid plan would produce the whole set cheaply at
  5 credits each (16:9 / low / 1K).
- **Canva is the working route** for stills. `generate-design` with
  `desktop_wallpaper` returns four 16:9 candidates, none watermarked and none
  carrying text. Use `create-design-from-candidate` then export PNG at
  1920x1080.
- Still to make: `studio-plate.png`, `exploded-flatlay.png`. The flat-lay
  failed once on Canva's side — worth another attempt.

## Who does what

| Asset | Made in | Why |
|---|---|---|
| `hero.png` | **OpenArt** | The anchor. Every Flow clip is generated from it. |
| `studio-plate.png` | OpenArt | First frame for Flow chapter 1. |
| `exploded-flatlay.png` | OpenArt | Chapter 4 Plan B + gallery image. |
| 7 brand-page stills | OpenArt *or* free from the film | See Part 2. |
| Logo removal, exact crops | **Canva** | Faster and more precise than re-rolling a prompt. |
| `og.png`, favicon | Canva | Needs real text, not generated text. |

**Generate the hero first and get it right before anything else.** Every clip
and most stills inherit from it. A weak hero costs you the whole set.

---

## OpenArt: model picks

Prices are credits for **one job at the config shown** — they change with
quality, resolution and output count, and are finalized at generation time.

| Job | Model | Cost | Why this one |
|---|---|---|---|
| Hero + product stills | **GPT Image 2** | 40 cr @ 2K / medium / 4:3 | Explicitly tuned for luxury product hero shots. |
| Maximum detail / 4K | **Nano Banana Pro** | 40 cr @ 1K / 1:1 | Native 4K, blends up to 14 references. |
| **Editing** — kill a fake logo, re-frame a crop | **Grok Imagine Image 2.0** | 33 cr @ 1K / low / image2image | Region-targeted edits, background removal, Smart Resize into any aspect ratio. |
| Cheap iteration while you're still exploring | **Nano Banana 2 Lite** | — | Fast 1K. Use it to find the composition, then re-roll the winner on GPT Image 2. |
| Anything with real text (og image) | **Nano Banana Pro** | — | The in-image text specialist. |

Two workflow notes that save a lot of credits:

- **Use image2image, not text2image, for everything after the hero.** Attach
  `hero.png` as the reference and describe the new angle. That's what keeps the
  same shoe across all seven stills. Fresh text2image rolls give you seven
  different shoes.
- **Don't re-generate to change shape.** Need the 4:3 hero as a 1:1 square?
  Grok Imagine's Smart Resize re-frames it for 33 credits instead of a fresh
  40-credit roll that comes back as a different shoe.

### Aspect ratio per asset — set this, don't crop later

| File | Ratio |
|---|---|
| `hero.png`, `studio-plate.png`, `exploded-flatlay.png` | **16:9** |
| `origin`, `knit-macro`, `sole-macro`, `gallery-4` | **16:10** |
| `gallery-1` | 4:3 |
| `gallery-2` | 4:5 (portrait) |
| `gallery-3` | 1:1 |
| `og` | 1200×630 |

The three film images **must** be 16:9 — Flow inherits the input's aspect, and
a mismatched clip gets pillarboxed in the scrubber.

---

## The shared anchor

Paste this block into every product prompt, word for word. It is the same
paragraph as the video pack, so stills and clips agree.

```
The shoe: a single futuristic racing sneaker, matte charcoal-black engineered
knit upper with a faint volt-yellow filament woven through the weave, one thin
volt-yellow line tracing the midsole, bone-white supercritical foam midsole with
a visible black carbon plate edge, no visible logos, no branding, no text
anywhere on the shoe.
```

And this look block:

```
Deep black seamless studio background, generous empty space around the subject.
Dramatic volt-yellow rim light from behind left, soft white key light from above
right. Photorealistic 8k commercial product photography, shallow depth of field,
cinematic, minimal, premium.
```

End every prompt with:

```
Do not include: any logo, any brand mark, any text, any lettering, a second
shoe, a pair of shoes, a shoe box, hands, feet, people, watermark.
```

---

# Part 1 — the three images the film needs

## 1. `hero.png` — 16:9 — the anchor

Roll 3–4 candidates. Pick the cleanest, most symmetrical side profile.

```
Photorealistic 8k commercial product photography of a single futuristic racing
sneaker floating in the centre of the frame, perfect side profile facing right.
The shoe: a single futuristic racing sneaker, matte charcoal-black engineered
knit upper with a faint volt-yellow filament woven through the weave, one thin
volt-yellow line tracing the midsole, bone-white supercritical foam midsole with
a visible black carbon plate edge, thin zoned rubber outsole, no visible logos,
no branding, no text anywhere on the shoe.
Deep black seamless studio background, generous empty space around the subject on
all sides. Dramatic volt-yellow rim light from behind left, soft white key light
from above right, subtle reflection beneath the shoe. Shallow depth of field,
ultra sharp, cinematic, minimal, premium.
Do not include: any logo, any brand mark, any text, any lettering, a second shoe,
a pair of shoes, a shoe box, hands, feet, people, watermark.
```

**Before you use it:** zoom to 200% on the heel, the tongue and the side panel.
Image models invent Nike-ish swooshes and fake wordmarks constantly. If you find
one, fix it in Canva (below) or with Grok Imagine — do **not** proceed to video
with a fake logo, because all eight clips will inherit it.

## 2. `studio-plate.png` — 16:9 — the empty stage

The first frame for chapter 1's Frames-to-Video reveal.

```
Photorealistic 8k photograph of a completely empty dark product photography
studio: a deep black seamless backdrop with a subtle reflective black floor,
lit only by a faint volt-yellow rim light from behind left and a very soft white
key light from above right. Almost entirely dark, moody, empty, no subject in
frame, generous empty space, cinematic, minimal.
Do not include: any object, any product, any shoe, any person, text, logos,
watermark.
```

## 3. `exploded-flatlay.png` — 16:9 — nine parts

Chapter 4's fallback, and it doubles as a gallery image. Worth making even if
Flow's Plan A works — it's the most "engineered" image in the set.

```
Top-down flat-lay photograph of a single racing sneaker fully disassembled into
its nine components, laid out on a deep black seamless surface with generous even
space between every part: charcoal-black engineered knit upper, laces, insole,
bone-white supercritical foam midsole, black carbon fibre plate, black rubber
outsole, heel counter, tongue, sock liner. Neatly arranged, evenly spaced,
technical exploded parts diagram.
Dramatic volt-yellow rim light from the left, soft white key light from above.
Photorealistic 8k commercial product photography, minimal, premium.
Do not include: any logo, any brand mark, any text, any labels, any lettering,
a second shoe, a whole assembled shoe, hands, people, watermark.
```

---

# Part 2 — the seven brand-page stills

**These are optional.** `tools/make_stills.py` already cuts all seven out of the
finished film for free, and crops of your own footage look deliberate. Generate
these only if you want the brand page sharper than a 1280px film frame allows.

For every one: **image2image with `hero.png` attached as the reference**, plus
the anchor + look blocks and the "Do not include" line.

### 4. `origin` — 16:10 — the wide establishing shot

```
The same sneaker resting on a dark reflective studio floor, three-quarter view
from the front left, photographed wide with a lot of empty dark space around it
and a soft reflection below.
```

### 5. `knit-macro` — 16:10 — the upper

```
Extreme macro close-up of the engineered knit upper of the same sneaker, filling
the frame, individual charcoal-black fibres and one faint volt-yellow filament
clearly visible in the weave, raking side light picking out the texture.
```

### 6. `sole-macro` — 16:10 — the plate

```
Extreme macro close-up of the midsole of the same sneaker seen from the side,
the bone-white supercritical foam filling the frame with the black carbon plate
edge running through it as a sharp dark line and one thin volt-yellow line
tracing the foam.
```

### 7. `gallery-1` — 4:3 — the beauty shot

```
The same sneaker floating, three-quarter view from the front right, toe angled
slightly toward the camera, heel raised, lit for a magazine cover.
```

### 8. `gallery-2` — 4:5 portrait — the heel

```
Vertical close-up of the heel and collar of the same sneaker seen from behind,
the heel counter and the volt-yellow line catching the rim light, tall narrow
composition with dark space above and below.
```

### 9. `gallery-3` — 1:1 — the outsole

```
The same sneaker seen from directly underneath, showing the zoned black rubber
outsole pattern flat to the camera, centred in a square frame on deep black.
```

### 10. `gallery-4` — 16:10 — motion

```
The same sneaker captured mid-air in extreme slow motion just after leaving a
dark reflective ground plane, a fine burst of dust and small particles frozen
beneath it, lit volt-yellow from behind.
```

---

# Part 3 — Canva's jobs

Canva is better than a re-roll for all of these.

### 1. Kill invented logos (the important one)

Generated sneakers almost always sprout a fake swoosh or wordmark. In Canva:
**Magic Eraser** over the mark, or clone a clean patch of the surrounding
material over it. Match the surrounding brightness — a patch that's too flat
reads as a smudge. Zoom to 200% to check before exporting.

If Magic Eraser leaves a smear, Grok Imagine Image 2.0 does region-targeted
removal for 33 credits: attach the image and prompt
`remove the logo from the side panel, replace it with the same knit texture,
change nothing else`.

### 2. Exact crops

Set a custom size to the target ratio, drop the image in, position, export. This
is free and beats asking a model to re-compose. (Or let `tools/import_images.py`
centre-crop for you — see below.)

### 3. `og.png` — 1200×630 — the link preview

The one asset that genuinely needs real, legible text. Build it in Canva:
`hero.png` on the left two-thirds, near-black `#07080a` background, and on the
right:

- **VANTIS 01** — heavy sans, tight letter-spacing, `#f2f4f0`
- **Run lighter.** — smaller, `#d6ff3d`

Export PNG. If you'd rather generate it, Nano Banana Pro is the in-image text
specialist — but check every letter, text models still drop characters.

### 4. Favicon

32×32 PNG: solid `#07080a` background, a single volt-yellow `V` or a thick
volt hairline. Export as `favicon.png`.

### 5. Export settings

PNG, highest quality, **no Canva watermark** (check the free-element warning on
export). Don't export JPG — the dark gradients band badly. The import script
converts to WebP for you.

---

# Getting everything into the site

Drop your finished files into `assets/incoming/`, named after their slot, then:

```bash
python tools/import_images.py
```

It centre-crops each file to its slot's ratio, scales it, converts to WebP and
writes it into `img/`. Any extension works (`.png`, `.jpg`, `.webp`).

| Put this in `assets/incoming/` | Becomes |
|---|---|
| `origin.png` | `img/origin.webp` |
| `knit-macro.png` | `img/knit-macro.webp` |
| `sole-macro.png` | `img/sole-macro.webp` |
| `gallery-1.png` … `gallery-4.png` | `img/gallery-1.webp` … |
| `og.png` | `img/og.png` (1200×630, stays PNG) |
| `favicon.png` | `img/favicon.png` (32×32) |

The three film images are different — they go to **Flow**, not into `img/`:
keep `hero.png`, `studio-plate.png` and `exploded-flatlay.png` in `assets/`
and upload them to Flow as ingredients / frames.

**Order of operations:** `make_stills.py` overwrites `img/` from the film, so
run it *first* and `import_images.py` *after*, or your hand-made stills will be
replaced by film crops.

---

# QC before you ship an image

- Zoom to 200% and hunt for invented logos and text — the number one failure.
- One shoe, not two. Models love adding the other foot.
- Background actually black, not dark grey — it has to match `#07080a` or the
  image will sit in a visible rectangle on the page.
- Same shoe as the hero: check the midsole line, the foam colour, the plate.
- No cast shadow running off the edge of the frame — the page masks image edges
  with a radial fade, and a hard shadow fights it.
