---
name: premium-hyperframes-video
description: "Produce professional HyperFrames videos end-to-end: website-to-video, product demos, launch videos, tutorials, build-in-public reels, 2D/3D motion sequences, kinetic typography, UI walkthroughs, and cinematic explainers. Use when the output should be a polished video built with HyperFrames HTML/GSAP, with strict storyboard, design, timing, motion-spec, visual QA, lint/inspect/preview gates, and no generic HTML page fallback."
license: MIT
author: Andrew (Nadrew-pgr)
---

# Premium HyperFrames Video

Purpose: create a real HyperFrames video, not a generic animated HTML page.

This skill is HyperFrames-first. It orchestrates native HyperFrames skills, visual direction, 3D/immersive motion constraints, timing, and verification. It should produce a one-shot attempt that is coherent enough that later feedback is refinement, not rescue.

## Non-Negotiable Outcome

The deliverable is a HyperFrames project or HyperFrames composition.

Do not produce:

- a generic webpage;
- a React/Next/Vue app;
- loose HTML without HyperFrames `data-*` timing;
- a motion concept with no rendered preview path;
- a video that only passes code checks but was not visually inspected.

If the user asks for a 3D, immersive, spatial, cinematic, product-in-space, camera, particles, depth, or world-like video, the implementation plan must include a real spatial technique: CSS 3D, Canvas 2D depth simulation, SVG/clip/mask depth, WebGL/Three.js when justified, or captured website/3D footage. A flat card animation is not acceptable unless explicitly justified.

## Required Native Skills

Load and obey native skills as needed:

- `hyperframes`: composition contract, HTML source, `data-*`, timelines, transitions, media, visual identity gate.
- `hyperframes-cli`: `init`, `lint`, `inspect`, `preview`, `render`, `doctor`, handoff URL.
- `website-to-hyperframes`: when a URL/site/app/page is the source material.
- `gsap`: when writing timeline choreography.
- `immersive-3d-scrollytelling`: when the video needs 3D, spatial camera logic, particle fields, depth, object morphing, or cinematic scene continuity.

This skill decides the production workflow and quality gates. Native HyperFrames decides exact framework syntax.

## Intake Rule

Search available context before asking. Use user brief, files, docs, assets, screenshots, transcripts, existing website, previous messages, and rendered output.

Ask only if a missing answer blocks production quality. If missing, ask at most three questions:

1. Target format/platform: `16:9`, `9:16`, `1:1`, duration.
2. Source material: URL, screenshots, app footage, assets, or pure generated visuals.
3. Desired mood/reference: premium, technical, cinematic, energetic, tutorial, launch, etc.

If these can be inferred, proceed and state assumptions.

## Production Workflow

Follow these gates in order. Do not skip gates for a from-zero video.

### Gate 1 — Source And Goal

Decide:

- video type: tutorial, product demo, launch trailer, build-in-public, explainer, social cut, website capture;
- output: dimensions, fps, duration, platform;
- source truth: website, app screen, script, article, screenshot, product UI, generated visual, recorded footage;
- viewer takeaway: one sentence.

If a website URL is involved, use `website-to-hyperframes`.

### Gate 2 — HyperFrames Project

Use HyperFrames project structure.

Preferred:

```bash
npx hyperframes init <project-name> --non-interactive
```

If an existing HyperFrames project exists, continue inside it. Do not create a separate hand-written HTML sandbox.

### Gate 3 — Visual Identity

Before composition HTML:

- read existing `DESIGN.md`, `visual-style.md`, brand docs, website capture, or screenshots;
- if absent, create a minimal `DESIGN.md`;
- define colors, type, spacing, motion tone, and anti-patterns.

No arbitrary default palette. No generic dark-gradient filler unless the brief asks for it.

### Gate 4 — Script And Timing

Create or derive:

- `SCRIPT.md` for narration/on-screen text, even if there is no voiceover;
- timing table in seconds;
- beat list with start/end times.

Scene durations should come from script/readability, not guessing.

### Gate 5 — Storyboard And Shot Specs

Create `STORYBOARD.md` with per-shot specs before coding complex animation.

Each shot must define:

- intent;
- hero frame timestamp;
- composition layers;
- static layout;
- motion path;
- timing/easing;
- transition in/out;
- visual risks;
- verification timestamps.

For 3D/spatial shots, include:

- coordinate space: CSS pixels, normalized, world units, or composition pixels;
- camera/crop/object distinction;
- depth layers and parallax factors;
- path: line, Bezier, orbit, dolly, truck, reveal, morph;
- contact/impact rules when relevant.

### Gate 6 — Static Hero Frames First

Build each scene at its most readable hero frame before GSAP.

Rules:

- content container fills the composition;
- use padding/flex/grid for layout;
- reserve absolute positioning for decorative or spatial layers;
- text must fit at the target resolution;
- product UI must be readable as video, not web-size tiny.

### Gate 7 — Animate With HyperFrames Contract

Use native HyperFrames rules:

- timed clips need `id`, `data-start`, `data-duration`, `data-track-index`;
- composition root needs `data-composition-id`, `data-width`, `data-height`;
- standalone `index.html` must not hide content in `<template>`;
- timelines use `window.__timelines`;
- GSAP timelines are synchronous and paused;
- no uncontrolled randomness;
- no `repeat: -1`;
- no generic scene jump cuts;
- transition handles scene exit except final scene;
- use `data-track-index` for timing, CSS `z-index` for layers.

### Gate 8 — 3D/Immersive Execution

When 3D is requested:

- never replace it with flat cards without saying why;
- choose the simplest adequate technique:
  - CSS 3D for panels, depth stacks, UI flythroughs;
  - Canvas 2D for particles, fields, trails, procedural shapes;
  - SVG masks/paths for draw-on, morphing, liquid, orbital lines;
  - Three.js/WebGL only when real 3D geometry/camera is necessary;
  - captured site/app footage when the product itself is the visual proof.
- build the hero frame first, then animate camera/object/crop separately;
- keep motion deterministic with seeded values;
- verify that 3D is visible, framed, and not blocking text.

If using WebGL inside HyperFrames, keep it bounded and render-safe:

- one canvas per composition unless justified;
- no expensive post-processing by default;
- no network asset dependency at render time;
- static fallback frame if WebGL fails.

### Gate 9 — Verification

Prefer an independent review over autoreview. If the agent has access to subagents or an equivalent independent reviewer, delegate the review pass to one before declaring completion. The reviewer should compare the HyperFrames project against the brief, DESIGN.md, SCRIPT.md, STORYBOARD.md, skill rules, acceptance criteria, and visual output. If no subagent/reviewer capability is available, perform an explicit autoreview and label it as such.

Run before handoff:

```bash
npx hyperframes lint
npx hyperframes inspect --samples 15
npx hyperframes preview --port <available-port>
```

Inspect key timestamps from the storyboard. If possible, capture stills or screenshots.

Render MP4 only when requested or when final delivery requires it:

```bash
npx hyperframes render --quality standard
```

Use `draft` for iteration, `standard` for review, `high` only for final.

## Acceptance Checklist

Before saying done:

- It is a HyperFrames project/composition, not generic HTML.
- Native HyperFrames skill rules were followed.
- Visual identity is defined and used.
- Script/timing/storyboard exist or are embedded in the production notes.
- Every scene has a readable hero frame.
- Every scene has entrance motion.
- Multi-scene video has transitions.
- 3D/immersive requests use a real spatial technique.
- Text is readable at target format.
- No accidental overlap/crop/flicker/jitter.
- `lint` passes.
- `inspect` passes or findings are documented.
- Preview URL is provided.
- Visual evidence was checked or the exact missing visual QA is disclosed.
- Review provenance is explicit: subagent/independent review when available; otherwise labeled autoreview.
- “Done” is only used for completed work. If partial, say `Prototype`, `Foundation`, or `Partial`, and explain why it is not done.

## Reference Loading

Read references only when needed:

- `references/motion-language.md`: user describes movement imprecisely.
- `references/math-primitives.md`: geometry, camera/crop, 3D, particles, contact, parallax, timing curves.
- `references/hyperframes-bridge.md`: mapping storyboards to HyperFrames/GSAP.
- `references/framework-hyperframes.md`: HyperFrames-specific reminders and failure modes.
- `references/shot-spec-template.md`: when writing storyboard or correction plan.
- `references/objections-and-failure-modes.md`: before large implementation or when a prior attempt missed the brief.

## Response Style

For build work, report:

- what was created;
- preview URL;
- commands run;
- visual QA evidence;
- remaining risks.

Do not dump long code unless asked.
