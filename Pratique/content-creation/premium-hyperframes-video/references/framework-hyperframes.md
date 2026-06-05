# Framework Notes: HyperFrames

Use this when implementing. Also load native `hyperframes`, `hyperframes-cli`, and `gsap` skills.

## What HyperFrames Is

HyperFrames is not a website builder.

It is a video composition system where HTML is the source, clips are timed with `data-*`, GSAP timelines drive motion, and the CLI validates/previews/renders the result.

## Fit

Good fit:

- product demo, website promo, launch trailer, tutorial, build-in-public edit;
- graphic + UI + text + data + screenshots + video footage;
- deterministic HTML/CSS/GSAP -> MP4;
- AI agent needs inspectable source and visual QA.

Poor fit:

- open-ended interactive website;
- realtime app logic;
- uncontrolled browser randomness;
- render-time network dependency;
- huge WebGL/postprocessing scene with no fallback.

## Mandatory Project Contract

- Use a HyperFrames project when building from zero.
- Prefer `npx hyperframes init <name> --non-interactive`.
- Main entry is a HyperFrames composition, not a generic page.
- Standalone root has `data-composition-id`, `data-width`, `data-height`.
- Timed elements use `id`, `data-start`, `data-duration`, `data-track-index`.
- GSAP timelines register synchronously in `window.__timelines`.
- Use `data-track-index` for temporal tracks, CSS `z-index` for visual layers.
- Use muted `<video>` plus separate `<audio>` when audio is needed.

## Visual Identity Gate

Before HTML:

1. Read `DESIGN.md`, `visual-style.md`, website capture, screenshots, brand docs.
2. If none exist, create a minimal `DESIGN.md`.
3. Use explicit colors, typography, spacing, and anti-patterns.

Never use arbitrary default colors because they “look fine”.

## Layout Before Animation

For each scene:

1. Identify the hero frame.
2. Build static layout at that frame.
3. Verify text size, spacing, and crop.
4. Add `gsap.from()` entrances.
5. Add transitions.

Do not position elements at animated start states and hope the final frame lands correctly.

## Scene Rules

- Multi-scene videos need transitions.
- Every scene needs entrance motion.
- No scene should simply appear fully formed.
- Avoid exit animations before transition; transition handles exit.
- Final scene may fade out.
- If two scenes share the same area, their hero frames must be independently readable.

## 3D And Immersive In HyperFrames

If the brief asks for 3D/immersive:

- Use CSS 3D for lightweight UI/product depth.
- Use Canvas 2D for particles, fields, waves, trails, and generative motion.
- Use SVG masks/paths for line drawing, morphing, liquid-ish reveals.
- Use Three.js/WebGL only when real camera/geometry is required.
- If using WebGL, keep it deterministic and bounded; include fallback visual.

Never downgrade “3D immersive” into plain flat cards without explicitly explaining why.

## CLI Gate

Run:

```bash
npx hyperframes lint
npx hyperframes inspect --samples 15
npx hyperframes preview --port <port>
```

Use `inspect --at <times>` for storyboard hero frames.

Render only when requested or final:

```bash
npx hyperframes render --quality standard
```

## Common Agent Failures

- Writes generic `index.html` without HyperFrames attrs.
- Uses React/Next because it is familiar.
- Forgets `window.__timelines`.
- Uses `repeat: -1`.
- Uses jump cuts instead of transitions.
- Makes text too small for video.
- Animates every element at once.
- Creates flat UI when user asked for spatial/3D.
- Ships after lint only, without visual inspect.

## Prevention

- Start from `DESIGN.md`, `SCRIPT.md`, `STORYBOARD.md`.
- Lock hero frames before GSAP.
- Use storyboard timestamps in `inspect --at`.
- Keep motion deterministic.
- Use one clear focal motion per beat.
- Treat visual QA as mandatory, not optional.
