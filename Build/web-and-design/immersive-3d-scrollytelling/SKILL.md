---
name: immersive-3d-scrollytelling
description: Build performant immersive WebGL scrollytelling experiences with React Three Fiber, GSAP or scroll-driven state, DOM overlays, dynamic narrative content, and strict camera, layering, accessibility, and performance constraints. Use when Codex needs to implement or review a one-canvas 3D landing page, scroll narrative, procedural particle scene, camera transition, DOM/WebGL hybrid layout, or R3F animation architecture.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Immersive 3D Scrollytelling

## Description

Use this skill for the technical engine of immersive DOM + WebGL experiences. It does not define the brand style; it enforces spatial logic, one-canvas architecture, predictable scroll state, and WebGL performance.

## Working Model

Before coding, write or infer:

- spatial thesis: what the user moves through, toward, around, or inside
- scene states: the named story beats the 3D scene must represent
- control model: which parts are scroll-driven, hover-driven, click-driven, and passive
- fallback model: how the page remains understandable without WebGL or with reduced motion

For each non-trivial scene, maintain a compact scene spec:

- entry condition and previous-state continuity
- main visual action
- exit condition and next-state handoff
- camera target/path
- object primitive choice (`Points`, `InstancedMesh` spheres, meshes, sprites, DOM cards)
- DOM overlay responsibility
- proof required to call the scene done

Also maintain an object lifecycle matrix for important scene objects: cards, shell particles, inactive particles, active spheres, focus labels, connection lines, timeline points, UI anchors, and camera. Track appearance, movement, transform, hide/exit, and data source.

## Camera And Space

Treat camera movement and object staging as different tools.

- Use WebGL axes consistently: X is horizontal, Y is vertical, Z is depth. Positive Z moves toward the viewer.
- To simulate moving forward, entering, backing away, or passing through a scene, animate the camera position or a camera rig in space.
- Do not use global object `scale` as a fake navigation zoom. Reserve scale for object breathing, appearance, staging, morphing, or local emphasis.
- Choose the camera FOV as a direction-art choice and keep it stable. Do not animate FOV to fake navigation unless the brief explicitly asks for a vertigo/dolly-zoom effect.
- Avoid sudden camera acceleration, rotation flips, or parallax that can cause motion sickness.

## Canvas Layering

Use one persistent WebGL canvas.

- Create a single global `<Canvas>` for the immersive scene.
- Keep the canvas mounted across sections and scene states.
- Put the canvas in a controlled background layer such as `fixed inset-0 z-0`.
- Put HTML content above it with a higher z-index.
- Ensure the canvas does not accidentally block HTML controls. Use `pointer-events` deliberately: default to non-blocking overlays, then explicitly enable WebGL hit areas only where needed.
- Render text, forms, editors, dashboards, and product UI in HTML, not inside WebGL, unless there is a specific 3D reason.

## Scroll Engine

Drive the narrative from one source of truth.

- HTML sections declare story beats; the WebGL scene listens to the current `sceneState`.
- Use a robust controller such as GSAP ScrollTrigger, a scroll store, or a central IntersectionObserver controller. Do not scatter scroll logic across many components.
- Keep scene states named, typed, and finite.
- Do not remount 3D components to transition between story beats. Animate existing refs, materials, vertices, uniforms, camera rigs, and geometry data.
- Scroll defines the base narrative. Hover and click add temporary offsets or controlled branches; they should not replace the story state machine.
- Every adjacent scene pair needs a transition plan. Avoid instant visibility swaps unless the brief explicitly wants a hard cut.
- When lines or links appear, animate their draw/progress/opacity intentionally. Do not show final graph lines from frame one unless requested.
- Do not replace scroll/state choreography with CSS-only infinite loops for narrative objects. Loops are only for ambient breathing/drift.

Example state shape:

```ts
type SceneState =
  | "hero"
  | "capture"
  | "enter"
  | "read"
  | "reason"
  | "plan"
  | "execute"
  | "product"
  | "final";
```

## WebGL Performance

Use zero-tolerance rules for frame loops.

- Never call React `setState` inside `useFrame` or high-frequency pointer events.
- Mutate refs in `useFrame`; use deltas, lerp, easing, and GSAP timelines for smooth changes.
- Use `Float32Array`, `BufferGeometry`, `InstancedMesh`, and shader uniforms for particles or repeated objects.
- Cap DPR for heavy scenes and simplify on weak devices.
- Avoid heavy post-processing by default. Prefer native `<fog>` for atmospheric depth, not as a true depth-of-field substitute.
- Avoid large GLB files, 4K textures, heavy real-time shadows, and many transparent full-screen layers unless the brief explicitly justifies them.
- Dispose or reuse generated geometries/materials when needed.

## Particle And Focus Systems

Do not treat all particles as generic glowing points.

- Pick the primitive deliberately: `Points` for very large fields, `InstancedMesh` spheres for tactile visible particles, sprites for soft glows, DOM cards for readable pre-ingestion fragments.
- If the user says particles should be spheres, use instanced sphere geometry or a shader impostor that reads as spherical.
- For focus states, keep the focused point stable when requested while surrounding particles orbit, breathe, or drift around it.
- For “dim everything except active points,” reduce color/alpha/emissive value of the inactive particles; do not hide them unless the brief asks for disappearance.
- When following reasoning, move attention along the emerging relationship between active objects. If the brief asks for point-to-point focus, use a stable camera rig or projected labels; avoid uncontrolled rollercoaster motion.
- For local hover reaction, use pointer/raycast proximity with radial falloff. Apply attract/repel/normal displacement locally, not to the entire object.
- Add individual noise/drift in addition to global object movement when the material should feel organic.

## Content And i18n

Make the narrative data-driven.

- Do not hardcode visible user-facing text in React or R3F components.
- Source visible labels, node names, floating words, section copy, and scenario content from project dictionaries or config files.
- If the 3D scene connects conceptual objects, derive their count, labels, colors, and relationships from data.
- Keep scenario data decoupled from WebGL implementation so the story can change without rewriting geometry code.

## Motion Quality

Make movement legible.

- Use easing that matches the project mood. Premium or calm projects usually need slow, continuous, low-jitter motion.
- Make transitions explain state changes: chaos to structure, exterior to interior, scattered inputs to connected graph, graph to plan.
- Avoid decorative movement that competes with reading.
- Respect `prefers-reduced-motion`; provide a static or simplified sequence.
- Translate user metaphors into math before coding: camera path, morph targets, force fields, falloff curves, opacity ramps, primitive type, easing and duration.

## Validation

Prefer an independent review over autoreview. If the agent has access to subagents or an equivalent independent reviewer, delegate the review pass to one before declaring completion. The reviewer should compare the scene/state implementation against the spec, PRD, skill rules, object lifecycle matrix, acceptance criteria, and visual output. If no subagent/reviewer capability is available, perform an explicit autoreview and label it as such.

Before handing off, verify:

- one canvas remains mounted throughout the narrative
- scroll changes `sceneState` predictably
- no React frame-loop state updates were introduced
- WebGL does not block HTML controls
- desktop and mobile remain readable
- reduced-motion users get a usable path
- typecheck/build pass
- visual verification confirms the canvas is nonblank and key scene states render. Prefer native browser screenshot, browser-use/Playwright screenshot, rendered frames, or exported video. If no visual tool is available, ask for a screenshot or timestamped user feedback and clearly state the gap.
- review the implementation against the spec/PRD/skill before saying done; list any missing acceptance criteria
- review provenance is explicit: subagent/independent review when available; otherwise labeled autoreview
- verify the object lifecycle matrix against code and preview so cards, active spheres, labels, lines, and camera do not disappear or duplicate unexpectedly.

## Completion Honesty

Do not mark an issue or scene as done unless all acceptance criteria are implemented and visually verified when possible. If partial, use `Prototype`, `Partial`, or `Foundation`, and justify exactly what is missing and what evidence supports the current status. Do not downgrade to a softer label to avoid finishing work; use it only when scope, time, tooling, or unresolved design approval makes completion genuinely impossible.
