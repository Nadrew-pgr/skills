# HyperFrames Bridge

Use this to map creative intent into HyperFrames source.

## Responsibility Split

This skill:

- defines the production gates;
- defines shots and motion specs;
- requires 3D/immersive treatment when asked;
- requires visual QA and honest completion status.

Native HyperFrames skills:

- define exact composition HTML rules;
- define CLI commands;
- validate clips, timelines, tracks, inspect, preview, render.

## Artifact Flow

For from-zero work:

```text
brief/context
-> DESIGN.md
-> SCRIPT.md
-> STORYBOARD.md
-> static hero frames
-> HyperFrames clips + GSAP timelines
-> lint
-> inspect at storyboard timestamps
-> preview URL
-> render only when needed
```

## Storyboard To HTML Mapping

| Storyboard field | HyperFrames mapping |
|---|---|
| shot id | composition section or clip group ids |
| start/end | `data-start`, `data-duration` |
| hero frame | static CSS layout |
| layers | DOM hierarchy + z-index |
| temporal tracks | `data-track-index` |
| subject | selector for GSAP |
| camera/crop | wrapper transform, CSS 3D camera, crop container, or WebGL camera |
| motion path | GSAP transform, SVG path, Canvas draw loop, or WebGL update |
| transition | dedicated transition clip/timeline |
| visual QA | `inspect --at`, screenshot, preview timestamp |

## Static First Pattern

```html
<div
  id="scene-01"
  class="clip scene scene-01"
  data-start="0"
  data-duration="5"
  data-track-index="1"
>
  <div class="scene-content">
    <h1 class="title">Readable hero title</h1>
    <p class="subtitle">Readable support copy.</p>
  </div>
</div>
```

```js
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
tl.from("#scene-01 .title", { y: 56, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.2);
tl.from("#scene-01 .subtitle", { y: 32, opacity: 0, duration: 0.55, ease: "power2.out" }, 0.38);
window.__timelines["main"] = tl;
```

The CSS hero frame is the truth. GSAP describes how the viewer arrives there.

## 3D Mapping

For pseudo-3D:

- `.stage { perspective: ... }`
- `.world { transform-style: preserve-3d }`
- layers use `translateZ`, `rotateX/Y`, scale, opacity.

For Canvas particles:

- seeded point generation;
- finite timeline progress;
- no `Date.now()`;
- use composition duration/time from HyperFrames timeline context where possible.

For WebGL:

- one canvas in a clip or composition;
- deterministic scene setup;
- no remote runtime asset dependency;
- fallback frame;
- verify rendered frame.

## Verification Mapping

Storyboard says:

```md
Verification:
- 1.2s: title readable
- 3.8s: product UI fully visible
- 5.0s: transition handoff
```

Run:

```bash
npx hyperframes lint
npx hyperframes inspect --at 1.2,3.8,5.0 --json
npx hyperframes preview --port 3017
```

Then visually inspect the Studio URL.
