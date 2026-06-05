# HyperFrames Bridge

Use this with the native HyperFrames skill.

## Responsibility Split

This skill:

- defines shots;
- chooses movement;
- defines pacing/easing;
- prevents vague animation;
- keeps choreography coherent.

HyperFrames skill:

- defines composition HTML;
- handles `data-*` timing attributes;
- defines track rules;
- registers GSAP timelines;
- renders and verifies output.

## Implementation Rules

- Build the hero frame as static HTML/CSS first.
- Animate from/to the static layout.
- Use `data-duration` for clip duration.
- Register timelines synchronously in `window.__timelines`.
- Do not use infinite repeats; compute finite repeat count.
- Keep media playback controlled by HyperFrames.
- Use deterministic values; seeded randomness only if needed.

## Motion Spec To GSAP Mapping

| Spec field | GSAP/HTML mapping |
|---|---|
| subject | selector or wrapper element |
| start_state | `gsap.from()` values |
| end_state | CSS hero frame or `gsap.to()` values |
| path | translate/rotate/clip/mask/camera-wrapper transform |
| easing | `ease` value |
| sync | timeline position labels |
| exit | `gsap.to()` out transition |

## Verification

Render or inspect at:

- first readable frame;
- hero frame;
- peak motion/contact frame;
- transition handoff frame;
- final frame.

Do not accept a video only because timeline code "looks right".
