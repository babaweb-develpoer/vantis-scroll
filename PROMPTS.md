# VANTIS 01 — Google Flow generation pack

> ## ⚠ The brief changed — read this before using any prompt below
>
> The site is now built on your real clip: **a pair of bone-white sneakers in a
> bright white studio**. Everything below still describes the original brief —
> a *single charcoal-black shoe with a volt-yellow accent on a deep black
> background*. Generating from these prompts as written will give you clips that
> clash with the film.
>
> **Swap the anchor paragraph** everywhere it appears with this one:
>
> ```
> The shoes: a pair of futuristic athletic sneakers in a single bone-white
> colourway, white engineered mesh upper with tonal white overlays, a chunky
> white foam midsole with a clear air unit in the heel, a pale grey rubber
> outsole, no visible logos, no branding, no text anywhere on the shoes.
> ```
>
> **And the look block:**
>
> ```
> Bright high-key white photography studio, seamless white backdrop with soft
> white panels, diffused light from every direction, very soft shadows, airy and
> serene, photorealistic 8k commercial product photography, shallow depth of
> field, minimal, premium.
> ```
>
> **Negative list** — add `dark background, black background, dramatic shadows,
> coloured accents, neon, single shoe` to the existing one, and drop
> `two shoes, pair of shoes, duplicate shoe, second sneaker` (a pair is now
> correct).
>
> The *structure* below — chapter order, the Ingredients/Frames technique, the
> retry levers, the QC step — all still applies. Ask me and I'll rewrite the
> whole file against the new brief rather than you patching each prompt.


Everything you need to render the film. One hero image, then eight 8-second
clips. Save each clip with the **exact filename** in the table and drop them
into `assets/clips/` — the build script expects those names.

| # | file | chapter | how to generate | risk |
|---|------|---------|-----------------|------|
| 0 | `hero.png` | the anchor still | Image / Ingredients | — |
| 1 | `ch1-ignite.mp4` | shoe emerges from black | Frames to Video | low |
| 2 | `ch2-weave.mp4` | macro knit forming | Text to Video | low |
| 3 | `ch3-rotate.mp4` | 360° turntable | Image/Ingredients to Video | medium |
| 4 | `ch4-explode.mp4` | layers separate | Ingredients to Video | **high** |
| 5 | `ch5-sole.mp4` | midsole compression macro | Ingredients to Video | medium |
| 6 | `ch6-impact.mp4` | foot strike, dust burst | Ingredients to Video | medium |
| 7 | `ch7-colorway.mp4` | colour sweeps across the knit | Image/Ingredients to Video | medium |
| 8 | `ch8-hero.mp4` | final bloom + slow push-in | Image/Ingredients to Video | low |

---

## Flow settings — set these once

- **Aspect ratio: 16:9.** Do not mix aspects. The site is built for 16:9 and
  a stray 9:16 clip will get pillarboxed.
- **Resolution: the highest your plan offers** (1080p if available, otherwise
  720p). Mixed resolutions are fine — the build script normalises everything
  to the first clip's geometry — but matched inputs look better.
- **Duration: 8s** (the Veo default). If you get 4s or 6s clips instead,
  that's fine too; just tell me and I'll re-time the captions.
- **Audio: ignore it.** Veo generates sound; the build strips it. Don't spend
  retries on audio.
- **Outputs: download the MP4**, don't screen-record.

### The consistency rule (this is the whole game)

The shoe must look identical in all eight clips. Two mechanisms:

1. **Ingredients to Video** — attach `hero.png` as an ingredient on every clip
   that shows the whole shoe (3, 4, 6, 7, 8). This is what keeps the silhouette
   and colourway stable.
2. **Frames to Video** — when a clip has to continue the previous one's state,
   export the previous clip's last frame and use it as the new clip's first
   frame. Needed for chapter 1, useful anywhere you see a jump.

If your plan doesn't expose Ingredients, use plain image-to-video from
`hero.png` for every clip — same idea, slightly more drift.

### The paragraph that goes in every prompt

Keep this block **word-for-word identical** everywhere. It is the anchor.

```
The shoe: a single futuristic racing sneaker, side profile, matte charcoal-black
engineered knit upper with a faint volt-yellow filament woven through the weave,
one thin volt-yellow line tracing the midsole, bone-white supercritical foam
midsole with a visible black carbon plate edge, no visible logos, no branding,
no text anywhere on the shoe.
```

### Negative prompt (paste into Flow's negative field if it has one)

```
two shoes, pair of shoes, duplicate shoe, extra shoe appearing, second sneaker,
morphing shoe, deforming shoe, hands, feet, people, legs, text, letters, logo,
brand mark, watermark, camera shake, camera zoom, camera pan, background change,
lighting change, blur, flicker, cartoon, illustration, low quality
```

If there's no negative field, the "Do not" sentence at the end of each prompt
below does the same job — keep it.

---

## 0. The hero still

Make this first and be fussy about it. Everything else inherits from it.
Generate 3 candidates, pick the cleanest side profile, and **zoom in to check
for invented logos or text** — image models sprinkle fake brand marks on
sneakers constantly. Send me the pick and I'll patch out any artifacts.

```
Photorealistic 8k commercial product photography of a single futuristic racing
sneaker floating in the centre of the frame, perfect side profile facing right,
matte charcoal-black engineered knit upper with a faint volt-yellow filament
woven through the weave, one thin volt-yellow line tracing the midsole,
bone-white supercritical foam midsole with a visible black carbon plate edge,
thin zoned rubber outsole. Deep black seamless studio background, generous empty
space around the shoe on all sides. Dramatic volt-yellow rim light from behind
left, soft white key light from above right, subtle reflection beneath.
Ultra sharp, shallow depth of field, cinematic, minimal, premium.
Do not include: any logo, any brand mark, any text, any lettering, a second
shoe, a shoe box, hands, feet, people.
```

Two alternates worth trying (same everything, swap the first line):

- `...three-quarter view from the front left, heel slightly raised...` — more
  character, drifts more in video.
- `...perfect side profile facing right, resting on a black reflective floor...`
  — grounded rather than floating; easier for the impact chapter to match.

---

## 1. `ch1-ignite.mp4` — emergence

**Mode:** Frames to Video. First frame = an empty dark studio plate, last
frame = `hero.png`. (Make the plate by prompting the hero image prompt with
the shoe removed, or just take any near-black frame.)
**Fallback if Frames to Video isn't available:** image-to-video from `hero.png`
with the same prompt — it'll read as a light reveal rather than a materialise.

```
A single racing sneaker slowly emerges out of total darkness as a volt-yellow
rim light rises from behind it and a soft white key light blooms in from above
right, revealing the shoe's silhouette edge first and then its full form by the
final frame. The shoe: a single futuristic racing sneaker, side profile, matte
charcoal-black engineered knit upper with a faint volt-yellow filament woven
through the weave, one thin volt-yellow line tracing the midsole, bone-white
supercritical foam midsole with a visible black carbon plate edge, no visible
logos, no branding, no text anywhere on the shoe. The shoe itself stays
perfectly still and centred, only the light changes. Deep black seamless studio
background unchanged throughout. Locked static camera, no camera movement.
Slow, cinematic, photorealistic product film.
Do not include: a second shoe, duplicate shoes, people, hands, text, logos,
camera movement, background changes.
```

**Good take:** ends on a clean, fully-lit shoe that matches the hero.
**Retry lever:** if the reveal finishes too early, add "the light rises very
slowly and only completes the reveal in the last second".

---

## 2. `ch2-weave.mp4` — one thread

**Mode:** Text to Video (no ingredient — this is abstract macro, it doesn't
need product consistency).

```
Extreme macro shot of a single charcoal-black filament being knitted, the thread
weaving itself into a dense engineered-knit textile that fills the frame, one
faint volt-yellow fibre running through the weave and catching the light. The
knit builds row by row in slow motion, fibres tightening and interlocking.
Deep black background, dramatic volt-yellow rim light raking across the surface
from the left, soft white key light from above. Shallow depth of field,
photorealistic 8k macro cinematography, textile close-up.
Locked static camera, no camera movement.
Do not include: shoes, people, hands, machinery with faces, text, logos,
watermark, camera movement.
```

**Good take:** reads as fabric forming, not as fabric waving.
**Retry lever:** add "the knit grows from the bottom of the frame upward".

---

## 3. `ch3-rotate.mp4` — the 360

This is the chapter that makes the site feel 3D. Worth a couple of retries.

**Mode:** Ingredients to Video with `hero.png` (or image-to-video from it).

```
The shoe rotates slowly and smoothly through a full 360 degrees around its
vertical axis while floating in dark space, one continuous turntable rotation at
constant speed, staying perfectly centred and perfectly level the whole time.
The shoe: a single futuristic racing sneaker, side profile, matte charcoal-black
engineered knit upper with a faint volt-yellow filament woven through the weave,
one thin volt-yellow line tracing the midsole, bone-white supercritical foam
midsole with a visible black carbon plate edge, no visible logos, no branding,
no text anywhere on the shoe. A volt-yellow rim light sweeps across the upper as
it turns, revealing the heel, then the outsole edge, then the side profile again.
Deep black seamless studio background unchanged, studio lighting unchanged.
Locked static camera, no camera movement — the shoe turns, not the camera.
Slow motion, photorealistic 8k commercial product animation.
Do not include: a second shoe, duplicate shoes, the shoe deforming or morphing,
people, hands, text, logos, camera movement, background changes.
```

**Good take:** one smooth revolution, shoe the same size at start and end.
**Retry lever:** if it wobbles or only turns 180°, say "exactly one full
revolution, ending in the same side profile it started in".
If Flow adds a glowing floor ring — keep it, it usually looks great.

---

## 4. `ch4-explode.mp4` — nine parts — **the risky one**

Known failure: video models tend to *duplicate* complex multi-part objects
instead of separating their layers. You may get two shoes. **Give it two
attempts, then switch to Plan B.**

### Plan A — separation in place

**Mode:** Ingredients to Video with `hero.png`. Push prompt adherence up if
your UI offers a strength/guidance control.

```
Exploded-view product animation: the single sneaker slowly comes apart, its
layers separating vertically away from each other with large gaps of empty black
space between them — the knit upper lifts up and away, the insole floats out,
the bone-white foam midsole separates downward, the black carbon plate slides out
from between the foam layers, the rubber outsole drops to the bottom, the laces
lift clear. By the final frame the shoe is fully separated into distinct floating
layers, each layer intact and clearly readable, arranged in a vertical exploded
diagram with black space between every part. Every part keeps its original
materials and colours. Deep black seamless studio background unchanged, volt-
yellow rim light unchanged. Locked static camera, no camera movement.
Very slow motion, photorealistic 8k engineering exploded view.
Do not include: a second shoe, a second set of parts, duplicate shoes, parts
turning into whole shoes, people, hands, text, logos, camera movement.
```

### Plan B — flat-lay drift (near-guaranteed)

Generate the exploded state as a *still* first (image models are excellent at
these), then animate it gently:

Still prompt:
```
Top-down flat-lay photograph of a single racing sneaker fully disassembled into
its nine components, laid out on a deep black seamless surface with generous
space between each part: charcoal-black knit upper, laces, insole, bone-white
foam midsole, black carbon plate, rubber outsole, heel counter, tongue, sock
liner. Neatly arranged in a grid, evenly spaced, volt-yellow rim lighting from
the left, soft white key light from above. Photorealistic 8k product photography,
technical, minimal. No logos, no text, no labels, no second shoe.
```
Then image-to-video from that still:
```
The disassembled components drift very slowly and evenly further apart from each
other, floating a few centimetres, the gaps between parts widening gradually.
Every part keeps its shape and material exactly. Deep black background unchanged,
lighting unchanged. Locked static camera, no camera movement. Extremely slow,
photorealistic.
Do not include: parts reassembling, a whole shoe appearing, duplicate parts,
people, hands, text, logos, camera movement.
```

### Plan C — if both fail

Send me the exploded **still** on its own. I'll slice it into strips and
animate the separation in code, which is fully controllable and honestly often
looks better. Tell me and I'll wire that chapter differently.

---

## 5. `ch5-sole.mp4` — energy return

**Mode:** Ingredients to Video with `hero.png`, or Frames to Video starting
from a cropped close-up of the hero's midsole.

```
Extreme macro close-up of the bone-white supercritical foam midsole of a single
racing sneaker, filling the frame, with the black carbon plate edge visible as a
dark line through the foam and one thin volt-yellow line tracing its side. The
foam compresses downward under load and then springs back up, one slow deliberate
compression and rebound, the foam cells visibly squashing and recovering, a faint
ripple travelling along the length of the plate. Deep black background, volt-
yellow rim light raking from the left, soft white key light above. Shallow depth
of field, slow motion, photorealistic 8k macro product cinematography.
Locked static camera, no camera movement.
Do not include: a second shoe, whole shoes, feet, legs, people, hands, text,
logos, camera movement, background changes.
```

**Good take:** one clear squash-and-rebound, foam stays foam.
**Retry lever:** "one single compression only, starting at two seconds".

---

## 6. `ch6-impact.mp4` — the strike

**Mode:** Ingredients to Video with `hero.png`.

```
The single racing sneaker strikes a dark reflective ground plane in extreme slow
motion, the bone-white foam midsole compressing on contact and a burst of fine
dust and small particles spraying outward from the point of impact, lit volt-
yellow by the rim light. The shoe then lifts slightly and settles. The shoe:
matte charcoal-black engineered knit upper with a faint volt-yellow filament woven
through the weave, one thin volt-yellow line tracing the midsole, bone-white
supercritical foam midsole with a visible black carbon plate edge, no visible
logos, no branding, no text anywhere on the shoe. Deep black seamless background,
volt-yellow rim light from behind left. Extreme slow motion, photorealistic 8k
commercial product cinematography. Locked static camera, no camera movement.
Do not include: feet, legs, people, runners, hands, a second shoe, duplicate
shoes, text, logos, camera movement.
```

**Good take:** one impact, no human limbs sneaking in.
**Retry lever:** if a foot appears, add "the shoe is empty, there is no foot
inside it" to the front of the prompt.

---

## 7. `ch7-colorway.mp4` — four ways to be seen

**Mode:** Ingredients to Video with `hero.png`.

```
A band of light sweeps slowly from the toe to the heel of the single racing
sneaker, and as it passes, the engineered knit upper changes colour behind it —
from matte charcoal-black to deep bone-white, then to volt-yellow, then back to
charcoal-black — one continuous colour sweep across the upper. The shoe's shape,
position, size and materials stay exactly the same the entire time; only the
colour of the knit changes. The bone-white foam midsole stays bone-white
throughout. Deep black seamless studio background unchanged, studio lighting
unchanged. Locked static camera, no camera movement. Slow motion, photorealistic
8k commercial product animation.
Do not include: a second shoe, duplicate shoes, the shoe changing shape or
morphing, people, hands, text, logos, camera movement, background changes.
```

**Good take:** silhouette rock-steady, only colour moves.
**Retry lever:** cut to two colours instead of four — "from charcoal-black to
volt-yellow and back" is much easier to hold together.

---

## 8. `ch8-hero.mp4` — the close

The one clip where camera movement is allowed, and the only one that should
have any.

**Mode:** Ingredients to Video with `hero.png`.

```
The single racing sneaker floats perfectly still in dark space as the studio
lighting slowly blooms warmer and richer, the volt-yellow rim light intensifying
along the upper's edge and the bone-white foam catching a soft highlight, fine
details of the knit glinting. The shoe: matte charcoal-black engineered knit
upper with a faint volt-yellow filament woven through the weave, one thin volt-
yellow line tracing the midsole, bone-white supercritical foam midsole with a
visible black carbon plate edge, no visible logos, no branding, no text anywhere
on the shoe. Very slow, smooth, subtle camera push-in toward the shoe. Deep black
seamless studio background unchanged. Cinematic, premium, photorealistic 8k
commercial product film, slow motion.
Do not include: a second shoe, duplicate shoes, people, hands, text, logos,
fast camera movement, background changes.
```

**Good take:** ends on a poster frame you'd put on a billboard — this is the
last thing anyone sees before the CTA.

---

## QC each clip before you send it

Watch for: a second shoe appearing, the shoe morphing or changing shape mid-clip,
the background shifting from black, the lighting jumping, the camera drifting,
or fake text/logos materialising on the upper.

Quick contact sheet (first / quarter / mid / three-quarter / last frame):

```bash
n=$(ffprobe -v error -select_streams v -count_frames -show_entries stream=nb_read_frames -of csv=p=0 clip.mp4); ffmpeg -y -v error -i clip.mp4 -vf "select='eq(n\,0)+eq(n\,$((n/4)))+eq(n\,$((n/2)))+eq(n\,$((3*n/4)))+eq(n\,$((n-1)))',scale=460:-1,tile=5x1" -frames:v 1 sheet.png
```

Regenerate only the clip that failed — never the whole set. Every chapter is
independently replaceable, and the build takes about a minute.

---

## When you have the clips

Drop them in `assets/clips/` with the exact filenames, then:

```bash
python tools/build_master.py build.config.json
```

It prints the real per-chapter scroll fractions. If any clip came back shorter
or longer than 8s, hand me that output and I'll re-time the captions to match.
