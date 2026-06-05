# 3D Scrollytelling

Use one persistent WebGL scene to support the narrative, not a separate 3D demo per section.

## Spatial Rules

- X = horizontal, Y = vertical, Z = depth. Positive Z moves toward the viewer.
- Use camera or camera-rig movement for entering, backing away, diving, orbiting, or passing through.
- Do not use global object scale as a fake navigation zoom. Scale is valid for object breathing, morphing, staging, appearance, or emphasis.
- Choose FOV deliberately and keep it stable unless a vertigo/dolly-zoom effect is explicitly requested.
- Avoid sudden rotations, acceleration spikes, or excessive parallax that can cause motion sickness.

## Architecture

- Use one `<Canvas>` mounted across the entire immersive sequence.
- HTML sections declare the story beats. The WebGL layer listens to a typed `sceneState`.
- Use GSAP ScrollTrigger, a scroll store, or a central IntersectionObserver controller. Do not scatter scroll logic.
- Do not remount 3D components between sections. Animate existing refs, geometry attributes, uniforms, materials, and camera rigs.
- Keep text, forms, product UI, editors, and dashboards in HTML unless they specifically need 3D placement.
- For every adjacent scene pair, define how camera, objects, opacity, lines, and DOM overlays hand off. Avoid abrupt swaps unless intentional.

## Performance

- Never call React `setState` inside `useFrame`.
- Use refs, deltas, lerp, GSAP timelines, shader uniforms, `Float32Array`, `BufferGeometry`, and `InstancedMesh`.
- Cap DPR, simplify on weak/mobile devices, and support `prefers-reduced-motion`.
- Avoid heavy post-processing by default. Use fog for atmospheric depth, not as a real depth-of-field substitute.
- Avoid large GLB files, 4K textures, heavy realtime shadows, and many fullscreen blur layers in v1.

## Particles And Links

- Use `Points` for dense distant fields.
- Use `InstancedMesh` spheres when particles must read as tactile spheres.
- Use DOM cards for readable pre-ingestion fragments, then translate them into 3D particles/nodes at contact.
- For focus moments, keep the focused point stable when required and move the surrounding field around it.
- To isolate 5-10 active points, dim inactive particles via color/alpha/emissive ramps instead of hiding them.
- Animate line reveal through progress, opacity, dash offset, or segment growth. Do not show final lines too early.
- For local hover, compute pointer proximity/raycast hit and apply radial falloff to nearby vertices/instances only.

## Scene State Example

```ts
export type SceneState =
  | "hero"
  | "capture"
  | "enter"
  | "ask"
  | "read"
  | "reason"
  | "plan"
  | "execute"
  | "product"
  | "final";
```

## Verification

- Confirm the canvas remains mounted.
- Confirm each scene state produces a visible, distinct response.
- Verify desktop and mobile screenshots.
- Verify reduced motion.
- Check that canvas pointer behavior does not block HTML controls.
- Capture visual evidence when possible: browser screenshot, Playwright/browser-use screenshot, rendered frame, or exported video. If impossible, state that visual QA is blocked and ask for screenshot/timestamped feedback.
