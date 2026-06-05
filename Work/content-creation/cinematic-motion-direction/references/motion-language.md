# Motion Language

Use this reference to translate user wording into implementation-ready movement.

## Translation Table

| User says | Clarify as | Useful implementation primitives |
|---|---|---|
| "enter inside" | camera/viewer crosses a boundary | dolly/push, foreground threshold, parallax layers, fog/depth, scale only for breathing |
| "zoom" | camera move, crop, or graphic scale? | dolly for spatial, crop for screen recording, scale for graphic emphasis |
| "smooth" | no discontinuity, readable easing | `power2.out`, `power3.inOut`, long settle, no bounce unless playful |
| "premium" | restrained, intentional, quiet confidence | fewer tweens, longer easing, subtle depth, precise spacing |
| "energetic" | fast but still legible | shorter beats, snap easing, strong cuts, controlled overshoot |
| "liquid" | deformation, flow, delayed follow-through | masks, SVG/filter displacement, staggered points, ease-in-out waves |
| "magnetic" | objects attracted to a point | accelerating path, slight overshoot, orbital settle |
| "builds in direct" | construction should be visible over time | staged reveal, layer assembly, cursor/agent action, progress beats |
| "not AI slop" | remove generic decoration | product-relevant objects, specific labels, coherent art direction |
| "scroll/story" | sequence of transformations | state machine, one visual object changing roles, continuity across shots |
| "horizontal scroll feel" | viewer progresses through space | lateral camera track, parallax, pinned panels, timeline rail |
| "impact" | physical contact moment | contact timing, squash/deform at point, no ripple unless echo is intended |

## Motion Primitives

- `dolly in/out`: camera/view moves through space.
- `truck left/right`: camera/view tracks horizontally.
- `pan/tilt`: camera rotates, use sparingly.
- `orbit`: camera moves around subject; slow only for premium/product.
- `parallax`: layers move at different speeds to imply depth.
- `morph`: same element changes topology/form.
- `reveal`: mask, clip, opacity, or slide exposes content.
- `handoff`: moving object becomes next scene's object.
- `settle`: final small movement that communicates completion.

## Easing Defaults

- Premium reveal: `power3.out`, `power2.inOut`.
- Technical snap: `power2.out`, short duration, no bounce.
- Organic flow: sine-like in/out, staggered delays, mild overshoot only if tasteful.
- Impact/contact: fast approach, short compression, slower recovery.
- Exit: `power2.in` or `power3.in`, shorter than entrance.

## Red Flags

- Multiple focal points moving at the same time.
- Text moving while user must read it.
- Camera rotates while UI changes.
- Objects pop without cause.
- Movement direction changes between shots without handoff.
- "Zoom" used when viewer should feel spatial entry.
