# Motion Glossary

Translate user metaphors into implementable 3D/motion decisions.

## Common Translations

- “Enter the sphere”: move camera/camera rig along Z through a membrane threshold; do not just scale the sphere.
- “Liquid surface”: vertex displacement, normal-based local deformation, shader noise, slow organic easing.
- “Drop hitting water”: local surface depression/rebound at contact point; avoid full ripple rings unless the user asks for an echo/wave.
- “Particles become structure”: morph `BufferGeometry` positions from scattered points to graph/timeline/grid targets.
- “Particles are spheres”: use `InstancedMesh` sphere geometry or shader impostors that read as 3D balls; do not use flat `PointsMaterial` if tactility matters.
- “One dot stays focused”: pin the focus particle position; animate other particles, camera orbit, or lines around it.
- “Everything darkens except a few”: lower inactive particle opacity/color/emissive while preserving their positions; active 5-10 points stay bright/white.
- “Lines draw in”: animate line progress, opacity, or dash offset from source to target; avoid instant final networks.
- “Hover attracts/repels matter”: pointer raycast/proximity -> radial falloff -> local displacement or velocity impulse.
- “Follow the line being formed”: keep a stable camera rig, focus one active sphere, draw the line segment toward the next sphere, then shift focus to the next sphere with low acceleration.
- “Label anchored to visual object”: when a label explains a visual object, project the object position to screen space and anchor an HTML label/card near it, or use Drei `<Html>` with occlusion/depth constraints. Do not force anchored labels when the brief wants separate editorial copy.
- “Primary interaction surface is cinematic/display-only”: remove fake submit affordance or make the control trigger the next narrative state; do not leave dead buttons or inputs that look actionable but do nothing.
- “Venom/organic shell”: dark membrane, irregular edge/noise, subtle specular veins; avoid cartoon slime unless requested.
- “Data cards enter”: keep cards as HTML overlays, animate them toward the 3D anchor, then translate their meaning into particles/nodes.
- “Inside memory”: lower exterior shell opacity, reveal internal field/points, calm camera, add atmospheric fog/depth.
- “Graph becomes timeline”: interpolate node positions from cluster layout to line/calendar blocks; keep labels in HTML for readability.
- “Interface built by particles”: morph particles into layout anchors, then fade/blur-reveal HTML UI exactly over those anchors.

## Quality Rules

- Motion must explain a state change.
- Use one continuous material vocabulary across the page.
- Keep camera motion slow enough for reading unless a brief “impact” moment is intentional.
- Avoid unrelated transitions between sections.
- If a visual metaphor makes product meaning less clear, simplify it.
