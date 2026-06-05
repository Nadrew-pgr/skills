# HyperFrames Shot Spec Template

Use this before coding complex motion or a from-zero video.

```md
# STORYBOARD

Project:
- Type:
- Format:
- FPS:
- Duration:
- Source material:
- Viewer takeaway:

Design source:
- DESIGN.md / website capture / screenshot / user brief:

Timing table:
| Shot | Start | End | Purpose | Hero frame | Verify at |
|---|---:|---:|---|---|---:|
| 01 | 0.0 | 3.2 | Hook | title + subject readable | 1.6 |

## Shot 01 — Name

Intent:
- What should the viewer feel/understand?

HyperFrames:
- clip ids:
- `data-start`:
- `data-duration`:
- `data-track-index` plan:
- composition/subcomposition:

Hero frame:
- timestamp:
- static layout:
- required readable text:
- required visible product/object:

Layers:
- background:
- depth/3D world:
- subject:
- UI/text:
- foreground/transition:

Motion:
- subject start:
- subject path:
- subject end:
- camera/crop start:
- camera/crop path:
- camera/crop end:
- transition in:
- transition out:

3D / spatial plan, if relevant:
- technique: CSS 3D / Canvas 2D / SVG / WebGL / captured footage
- coordinate space:
- depth layers:
- parallax:
- camera vs object motion:

Timing:
- beat 1:
- beat 2:
- beat 3:

Easing:
- entrance:
- main move:
- settle:
- transition:

Risks:
- readability:
- overlap/crop:
- motion mismatch:
- render/performance:

Verification:
- `inspect --at` timestamp(s):
- screenshot/render required:
- acceptance criteria:
```

## Minimal Correction Spec

```md
Change:
- Problem:
- Evidence timestamp/screenshot:
- Element:
- Current:
- Expected:
- Scope:
- Technique:
- Verify at:
```
