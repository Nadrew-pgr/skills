# Framework Notes: Remotion

Use this when implementing with Remotion. Also load native Remotion skills if available.

## Fit

Remotion is a good fit when:

- React is the natural authoring model;
- video is data-driven and componentized;
- the project already uses React/TypeScript;
- app/product code should share UI/data logic with video;
- frame-accurate composition and programmatic rendering matter;
- team accepts renderer, bundle, media, cache, and deployment complexity.

## Contract

- Think in frames, fps, and React components.
- Convert seconds to frames:

```ts
frame = Math.round(seconds * fps)
seconds = frame / fps
```

- Use explicit composition dimensions/fps/duration.
- Use reusable components only when they preserve final frame readability.
- Keep typography large enough for video resolution; web UI proportions are often too small.
- Store design tokens and motion tokens centrally.
- Verify by rendered frames, not component preview only.

## AI Failure Modes

Observed/publicly discussed:

- AI-generated videos can have font sizes/proportions too small.
- Agent may build a React component that is valid but not video-readable.
- Scene transitions can feel off: logos disappear early, text overlaps next scene.
- Fonts may fall back if import/bundling is wrong.
- Browser/renderMedia output may be slower than expected.
- Concurrency does not guarantee linear speedup.
- Long source video with `OffthreadVideo` may trigger cache pruning/timeouts.
- Heavy React trees can create expensive frame rendering.

## Prevention

- Specify output frame size, fps, duration before code.
- Lock hero frames before animation.
- Define min text size per format:
  - 1920x1080 hero title often `90..160px`;
  - 1080x1920 hook title often `84..140px`;
  - captions often `48..96px` depending format and density.
- Use frame numbers for exact timing.
- Create a timing table before implementation.
- Benchmark render speed on a small representative slice.
- Avoid promising realtime/faster-than-realtime render.
- For long source media: re-encode with useful keyframes, tune cache if supported, segment long renders.
- Render still frames at key timestamps and inspect text overlap.

## Sources

- Remotion issue list includes "Skills: How do we prevent the AI from making the font sizes / proportions too small?": https://github.com/remotion-dev/remotion/issues
- Remotion render concurrency issue #4300: https://github.com/remotion-dev/remotion/issues/4300
- Remotion OffthreadVideo discussion #3070: https://github.com/orgs/remotion-dev/discussions/3070
- HyperFrames prompt guide mentions common video-agent symptoms like wrong fonts, overlapping captions, and off transitions: https://hyperframes.mintlify.app/guides/prompting
