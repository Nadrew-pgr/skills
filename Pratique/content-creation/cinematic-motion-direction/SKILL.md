---
name: cinematic-motion-direction
description: Translate vague video, animation, and product-demo motion requests into precise cinematic direction for HyperFrames, Remotion, GSAP, or HTML video compositions. Use when the user wants a video, trailer, screen recording edit, build-in-public sequence, animated explanation, product reveal, transition, camera move, text reveal, or says an agent struggles to understand exact movement, pacing, choreography, easing, framing, or animation intent.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Cinematic Motion Direction

Purpose: turn motion taste into executable motion specs.

Use this skill before implementation when movement precision matters. It complements renderer/framework skills such as HyperFrames or Remotion; it does not replace them.

## Core Workflow

1. Identify output format: horizontal, vertical, square, duration, platform, fps if known.
2. Identify narrative beats: what viewer should feel/understand at each moment.
3. Search available context before asking the user. Use project files, docs, assets, prior conversation, screenshots, rendered frames, and tool output when available.
4. Ask only when the answer cannot be inferred or found. If the goal is still vague, route to `intake-and-grill`; if existing docs decide it, route to `grill-with-docs`; if current external facts matter, route to `grill-with-research`.
5. Lock the hero frame for each shot before animation.
6. Translate user wording into motion primitives: subject, path, anchor, depth, timing, easing, transition.
7. Use math primitives when language is ambiguous or geometry matters.
8. Produce a shot spec before coding complex animation.
9. If implementing, build static layout first, then animate from/to that layout.
10. Verify by screenshot/render at key timestamps, not only by reading code.

## Framework Split

This skill is framework-agnostic for motion direction.

Use framework-specific references only when implementing or choosing a renderer:

- HyperFrames: read `references/framework-hyperframes.md`.
- Remotion: read `references/framework-remotion.md`.

Do not mix their implementation contracts. HyperFrames is HTML/data-attributes/GSAP. Remotion is React/frame-based composition.

## When Using HyperFrames

Also use the native HyperFrames skill for file format, `data-*` attributes, tracks, media, timeline registration, and render workflow.

This skill decides what should move, how, why, and when. HyperFrames decides how to encode it.

Read `references/framework-hyperframes.md` and `references/hyperframes-bridge.md` before writing HyperFrames HTML.

## Required Motion Spec

For every important shot or transition, write:

- `intent`: emotional/product reason for the motion;
- `duration`: seconds or frame range;
- `hero_frame`: exact most-readable frame;
- `subject`: element/camera/background that moves;
- `start_state`: position, scale, opacity, crop, blur, depth;
- `end_state`: position, scale, opacity, crop, blur, depth;
- `path`: linear, arc, orbit, dolly, push, pull, reveal, morph;
- `easing`: chosen curve and reason;
- `sync`: relationship to audio, cursor, text, UI state, or beat;
- `exit`: how the shot clears without clutter;
- `risk`: overlap, motion sickness, unreadable text, fake depth, timing conflict;
- `verification`: timestamp(s) to inspect.
- `visual_evidence`: screenshot/render/frame/browser capture to review when possible.

## Rules

- No vague animation instructions such as "make it dynamic" without a spec.
- Do not ask the user for information that is already available in files, docs, assets, previous messages, screenshots, or tool output.
- If making an assumption from found context, state it briefly and continue.
- Distinguish camera motion from object motion from crop/pan motion.
- Do not simulate a camera move with random scale unless the desired effect is explicitly a graphic zoom.
- Express complex motion with coordinates, vectors, path functions, interpolation, contact points, and timing curves.
- Text readability wins over movement.
- Motion must support story, not decorate empty space.
- Use fewer, clearer movements instead of many simultaneous tweens.
- Avoid nausea: no abrupt camera rotations, jitter, or unmotivated whip moves.
- Maintain deterministic playback: no uncontrolled randomness.
- Prefer named timings and repeated motion tokens over one-off values.
- For product UI videos, prioritize cursor, focus state, panel reveal, and data flow clarity over cinematic excess.

## Visual QA

Technical tests are not enough for motion work.

When possible, verify visually using the best available channel:

- browser screenshot from the native/in-app browser;
- browser-use screenshot or inspection;
- rendered frame stills at key timestamps;
- local preview screenshot;
- exported MP4 spot-check;
- user-provided screenshot/video/visual feedback when agent tools cannot see the result.

Visual checks should answer:

- Does the hero frame match the shot spec?
- Does text fit and remain readable?
- Does movement direction match the intent?
- Does the transition handoff make sense?
- Is there accidental overlap, crop, flicker, jitter, or visual drift?
- Does final output differ from preview?

If browser/render tools are unavailable, ask the user for one targeted screenshot or timestamped feedback instead of guessing.

## Reference Loading

- Read `references/motion-language.md` when the user describes movement imprecisely.
- Read `references/math-primitives.md` when a movement needs geometry, impact/contact, parallax, camera/crop, curves, or precise timing.
- Read `references/shot-spec-template.md` when producing a storyboard or implementation brief.
- Read `references/framework-hyperframes.md` and `references/hyperframes-bridge.md` when implementing with HyperFrames.
- Read `references/framework-remotion.md` when implementing with Remotion.
- Read `references/objections-and-failure-modes.md` before choosing Remotion, HyperFrames, or heavy browser-rendered video architecture.
