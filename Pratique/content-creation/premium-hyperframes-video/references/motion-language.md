# Motion Language

Use this to translate vague video feedback into executable HyperFrames motion.

## Translation Table

| User says | Clarify as | Useful primitives |
|---|---|---|
| "make a video" | HyperFrames composition, not a webpage | project init, clips, storyboard, preview |
| "use my site" | website-to-HyperFrames workflow | capture, DESIGN.md, SCRIPT.md, storyboard |
| "3D immersive" | spatial implementation required | CSS 3D, Canvas particles, SVG depth, WebGL if justified |
| "enter inside" | camera/crop crosses boundary | dolly/push, parallax, foreground threshold |
| "zoom" | camera/crop move or graphic scale? | wrapper transform, crop camera, object scale only if object grows |
| "smooth" | no discontinuity | eased paths, handoff, no abrupt scene jump |
| "premium" | restrained, intentional | fewer focal motions, exact spacing, strong typography |
| "energetic" | fast but legible | shorter beats, stronger contrast, no unreadable text |
| "liquid" | flow/deformation | masks, SVG paths, canvas displacement, staggered particles |
| "magnetic" | attraction to target | Bezier path, acceleration, overshoot, settle |
| "builds live" | visible construction | staged assembly, cursor/agent action, progress beats |
| "not generic" | source-specific visual proof | product UI, real assets, concrete labels, no filler cards |
| "transition bad" | handoff mismatch | outgoing frame, transition layer, incoming entrance |
| "motion wrong" | path/anchor/timing mismatch | specify subject, anchor, start/end, easing, verify timestamp |

## Video-Specific Red Flags

- It looks like a responsive webpage screenshot, not a video composition.
- It has no designed hero frame.
- Text is web-size instead of video-size.
- Motion starts before viewer understands the object.
- 3D request became flat UI.
- Scene cuts happen without transition.
- Agent cannot point to timestamped visual evidence.

## Motion Defaults

- Hook: strong readable frame by `0.4s..1.2s`.
- Product proof: keep UI/object stable long enough to inspect.
- Tutorial: cursor/focus state leads the eye.
- Build-in-public: screen, timeline, and transformation should be legible.
- Launch trailer: one signature motion per beat.

## Easing Defaults

- Premium reveal: `power3.out`, `power2.inOut`.
- Product UI: `power2.out`, short but readable.
- Spatial camera/crop: `power3.inOut`, avoid jitter.
- Organic flow: sine-like, staggered, mild overshoot.
- Impact/contact: fast approach, delayed compression, slower recovery.

## Handoff Rule

Every scene should hand something to the next scene:

- object becomes UI;
- line becomes transition;
- cursor action becomes next panel;
- particle field becomes product proof;
- text phrase becomes final CTA.

If there is no handoff, use a deliberate transition layer.
