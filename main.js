/* VANTIS 01 - scroll film engine
   Canvas image-sequence scrubber: scroll position drives frame index.
   Frames stay as compressed blobs; only a sliding window around the
   playhead is decoded, so RAM stays sane on phones. */

const canvas = document.getElementById("film");
const ctx = canvas.getContext("2d", { alpha: false });
const track = document.getElementById("track");
const loader = document.getElementById("loader");
const loadbar = document.getElementById("loadbar");
const scrollCue = document.getElementById("scroll-cue");
const captions = [...document.querySelectorAll(".caption")];

const KEEP = 120; // evict decoded frames further than this from the playhead
const AHEAD = 30; // decode this many frames ahead, weighted by scroll direction

// Letterbox fill, read from the page so the engine follows the theme instead
// of hard-coding a colour the frames have to match.
const BG =
  getComputedStyle(document.documentElement).getPropertyValue("--bg").trim() || "#07080a";

const state = {
  blobs: [],
  frames: new Map(), // index -> Frame
  count: 0,
  pattern: "",
  current: -1,
  target: 0,
  smooth: 0,
  dir: 1,
  ready: false,
  decoding: new Set(),
};

/* -- decoding -----------------------------------------------
   createImageBitmap is the fast path, but it throws "source image could
   not be decoded" in hidden/backgrounded tabs and some webviews, which
   silently leaves the canvas blank. Fall back to an HTMLImageElement;
   drawImage accepts both. */

async function decodeBlob(blob) {
  try {
    const bmp = await createImageBitmap(blob);
    return { src: bmp, release: () => bmp.close() };
  } catch {
    const url = URL.createObjectURL(blob);
    const img = new Image();
    img.decoding = "async";
    await new Promise((resolve, reject) => {
      img.onload = () => resolve();
      img.onerror = () => reject(new Error("img decode failed"));
      img.src = url;
    });
    return { src: img, release: () => URL.revokeObjectURL(url) };
  }
}

/* -- loading ------------------------------------------------ */

async function loadManifest() {
  // Must revalidate: the manifest keeps the same URL across rebuilds, so a
  // cached copy leaves the engine scrubbing a frame count the film no longer
  // has (requesting frames that 404). The file is a few bytes; the frames
  // themselves still cache normally.
  const res = await fetch("frames/frames.json", { cache: "no-cache" });
  if (!res.ok) throw new Error("no manifest");
  return res.json(); // { count, pattern }
}

function frameURL(i) {
  return state.pattern.replace("%04d", String(i + 1).padStart(4, "0"));
}

async function fetchBlob(i) {
  if (state.blobs[i]) return state.blobs[i];
  const res = await fetch(frameURL(i));
  state.blobs[i] = await res.blob();
  return state.blobs[i];
}

async function decode(i) {
  if (state.frames.has(i) || state.decoding.has(i) || !state.blobs[i]) return;
  state.decoding.add(i);
  try {
    state.frames.set(i, await decodeBlob(state.blobs[i]));
  } catch {
    /* transient - retried on a later tick */
  }
  state.decoding.delete(i);
}

function manageWindow(center) {
  for (let d = 0; d <= AHEAD; d++) {
    const fwd = center + d * state.dir;
    const back = center - Math.min(d, 8) * state.dir;
    if (fwd >= 0 && fwd < state.count) decode(fwd);
    if (back >= 0 && back < state.count) decode(back);
  }
  if (state.frames.size > KEEP * 2) {
    for (const [idx, f] of state.frames) {
      if (Math.abs(idx - center) > KEEP) {
        f.release();
        state.frames.delete(idx);
      }
    }
  }
}

async function preload() {
  const { count } = state;
  const EAGER = Math.min(Math.ceil(count * 0.15), 90);

  let done = 0;
  await Promise.all(
    Array.from({ length: EAGER }, (_, i) =>
      fetchBlob(i)
        .catch(() => {})
        .then(() => {
          done++;
          loadbar.style.transform = `scaleX(${done / EAGER})`;
        })
    )
  );
  await decode(0);
  state.ready = true;
  loader.classList.add("done");

  let next = EAGER;
  await Promise.all(
    Array.from({ length: 5 }, async () => {
      while (next < count) {
        const i = next++;
        try {
          await fetchBlob(i);
        } catch {
          /* refetched on demand */
        }
      }
    })
  );
}

/* -- drawing ------------------------------------------------ */

function resize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(canvas.clientWidth * dpr);
  canvas.height = Math.round(canvas.clientHeight * dpr);
  state.current = -1; // force redraw
}

function nearestDecoded(i) {
  if (state.frames.has(i)) return i;
  for (let d = 1; d < state.count; d++) {
    if (state.frames.has(i - d)) return i - d;
    if (state.frames.has(i + d)) return i + d;
  }
  return -1;
}

function drawFrame(i) {
  const j = nearestDecoded(i);
  if (j < 0) return;
  const src = state.frames.get(j).src;
  const cw = canvas.width;
  const ch = canvas.height;
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, cw, ch);
  // contain-fit with 4% overscan; the vignette hides the letterbox seam
  const s = Math.min(cw / src.width, ch / src.height) * 1.04;
  const w = src.width * s;
  const h = src.height * s;
  ctx.drawImage(src, (cw - w) / 2, (ch - h) / 2, w, h);
  state.current = j;
}

/* -- scroll mapping ----------------------------------------- */

function progress() {
  const max = track.offsetHeight - window.innerHeight;
  return max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
}

function transformBase(el) {
  if (el.classList.contains("cap-center")) return "translate(-50%, -50%)";
  if (el.classList.contains("cap-top") || el.classList.contains("cap-bottom"))
    return "translateX(-50%)";
  return "translateY(-50%)";
}

function updateCaptions(p) {
  for (const el of captions) {
    const tIn = +el.dataset.in;
    const tHold = +el.dataset.hold;
    const tOut = +el.dataset.out;
    const rise = Math.max((tHold - tIn) * 0.4, 0.008);
    const fall = Math.max((tOut - tHold) * 0.6, 0.008);
    let o = 0;
    if (p >= tIn && p <= tOut) {
      o = Math.min((p - tIn) / rise, 1) * Math.min((tOut - p) / fall, 1);
      o = Math.min(Math.max(o, 0), 1);
    }
    el.style.opacity = o.toFixed(3);
    el.style.visibility = o < 0.004 ? "hidden" : "visible";
    const drift = (p - tHold) * -40; // gentle parallax
    el.style.transform = `${transformBase(el)} translateY(${drift.toFixed(1)}px)`;
  }
  scrollCue.style.opacity = p < 0.015 ? 1 : 0;
}

/* -- main loop ---------------------------------------------- */

let lastT = performance.now();
function tick(now) {
  const dt = Math.min((now - lastT) / 1000, 0.5) || 0.016;
  lastT = now;
  if (state.ready) {
    const p = progress();
    const prevTarget = state.target;
    state.target = p * (state.count - 1);
    if (state.target !== prevTarget) state.dir = state.target >= prevTarget ? 1 : -1;
    // time-based lerp: fast flicks glide, throttled tabs still converge
    const k = 1 - Math.exp(-dt * 14);
    state.smooth += (state.target - state.smooth) * k;
    if (Math.abs(state.target - state.smooth) < 0.5) state.smooth = state.target;
    const i = Math.round(state.smooth);
    manageWindow(i);
    if (i !== state.current) drawFrame(i);
    updateCaptions(p);
  }
  requestAnimationFrame(tick);
}

/* -- boot --------------------------------------------------- */

function devPlaceholder(msg) {
  loader.classList.add("done");
  const draw = () => {
    const g = ctx.createLinearGradient(0, 0, 0, canvas.height);
    g.addColorStop(0, BG);
    g.addColorStop(1, BG);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    ctx.fillStyle = "rgba(214,255,61,0.85)";
    ctx.font = `${15 * dpr}px -apple-system, Segoe UI, sans-serif`;
    ctx.textAlign = "center";
    ctx.fillText(msg, canvas.width / 2, canvas.height / 2);
  };
  draw();
  window.addEventListener("resize", () => {
    resize();
    draw();
  });
  updateCaptions(progress());
  addEventListener("scroll", () => updateCaptions(progress()), { passive: true });
}

window.addEventListener("resize", resize);
resize();

// rAF gets throttled in backgrounded and low-power tabs, which can leave the
// captions a step behind the scroll. They are a pure function of progress, so
// keep them honest from the scroll event too (the frame draw stays in the tick).
addEventListener("scroll", () => {
  if (state.ready) updateCaptions(progress());
}, { passive: true });

loadManifest()
  .then((m) => {
    state.count = m.count;
    state.pattern = m.pattern;
    state.blobs = new Array(m.count).fill(null);
    requestAnimationFrame(tick);
    return preload();
  })
  .catch(() => devPlaceholder("frames not built yet - run tools/build_master.py"));
