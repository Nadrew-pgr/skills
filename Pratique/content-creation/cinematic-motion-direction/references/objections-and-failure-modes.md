# Objections And Failure Modes

Use this reference when planning video work with Remotion, HyperFrames, browser-rendered video, GSAP, or HTML composition tools.

It is not a criticism file. It is a prevention checklist.

## Common External Complaints Found

Sources checked:

- HyperFrames prompt guide: small targeted edits beat long re-specifications; wrong fonts, overlapping captions and off transitions are expected iteration targets.
- HyperFrames AI agents guide: agents should use lint/inspect JSON, catalog-first authoring, and avoid re-authoring from scratch on lint warnings.
- Motion graphics / AI discussion: users complain AI is weak at precise timing, complicated movement, client over-expectation, and final art direction.
- AI animation error analysis: prompt ambiguity, lack of scene memory, probabilistic regeneration, camera instability and drift cause mismatch.
- HyperFrames troubleshooting docs: composition structure, FFmpeg, lint errors, preview stutter, stale preview, diagnostics.
- Reddit report on HyperFrames: user found installation/display/reload flow fragile during beta usage.
- Remotion GitHub issue #4300: render concurrency did not use CPU as expected and higher concurrency was slower in one VPS setup.
- Remotion GitHub discussion #3070: long OffthreadVideo renders hit cache pruning/timeouts; keyframe spacing affected extraction speed.
- Reddit/webdev discussion: Remotion/browser rendering can take multiples of video duration; faster platforms often convert to video primitives instead of running live browser code.

## Objection Map

### "The agent does not understand the exact movement."

Cause:

- user gives aesthetic language only;
- agent jumps to code without a shot spec;
- no hero frame;
- no coordinates/path/easing.
- no explicit statement of what stays still.

Skill response:

- require shot spec;
- use `math-primitives.md`;
- define subject, path, timing, easing, verification timestamps.
- list frozen elements and moving elements separately.
- when in doubt, produce a timing table before code.

### "The AI made something next to my intent."

Cause:

- prompt contains story/brand/context but no motion contract;
- model optimizes for plausible visual output, not the intended choreography;
- no negative constraints;
- no before/after frame;
- no review timestamps.

Skill response:

- convert user intent into exact shot spec before implementation;
- add "must not happen" constraints;
- define acceptance criteria in visual terms;
- render/check hero frame and transition frame;
- revise small deltas, not whole prompt.

### "It looks cool, but wrong."

Cause:

- movement has no narrative role;
- generic transition chosen because it is common;
- agent prioritizes spectacle over product clarity;
- no continuity/handoff between shots.

Skill response:

- every motion gets `intent`;
- name the handoff from previous shot to next shot;
- remove motion without story/product purpose;
- prefer one strong movement over several decorative movements.

### "Text/captions overlap or feel too small."

Cause:

- agent uses web UI scale instead of video scale;
- no safe area;
- no hero frame;
- too many words in one beat.

Skill response:

- lock frame size and format first;
- define safe area;
- set min text size;
- split copy across beats;
- verify at output resolution.

### "The AI cannot be art-directed like a motion designer."

Cause:

- probabilistic video generation is weak at precise revisions;
- changing prompt can regenerate unrelated parts;
- model lacks stable keyframe/curve controls;
- complex movement/timing needs craft.

Skill response:

- use AI for ideation/assets when appropriate;
- use code/GSAP/Remotion/HyperFrames for controllable typography, UI, charts, transitions and timing;
- isolate AI-generated footage from deterministic motion graphics;
- create control points, keyframes, masks, and staged revisions.

### "Preview stutters / looks laggy."

Observed causes:

- expensive CSS paint/composite;
- stacked backdrop blurs;
- huge images;
- animated filters/shadows;
- too many moving elements.

Skill response:

- prefer opacity/transform/clip/mask;
- limit blur and filter animation;
- reduce 4K/60fps unless needed;
- validate with preview and rendered output separately.

### "Render is slower than realtime."

Observed causes:

- browser-rendered video captures frames one by one;
- live DOM/iframe/composition state is expensive;
- high resolution/fps;
- video decoding/keyframe issues;
- poor concurrency assumptions.

Skill response:

- decide whether browser-rendered video is acceptable;
- pre-render static/complex sections when useful;
- avoid live iframe overlays unless necessary;
- segment long renders;
- avoid 4K/60fps by default;
- log render duration vs video duration.

### "Concurrency does not scale like expected."

Observed causes:

- CPU/core utilization depends on renderer, browser, OS, media decode, cache and container settings;
- higher concurrency can add overhead.

Skill response:

- do not promise linear scaling;
- benchmark small representative renders;
- tune concurrency empirically;
- keep render settings in config;
- include machine/env details in logs.

### "Long video with source media times out."

Observed causes:

- off-thread video frame extraction;
- cache pruning;
- poor source video keyframe spacing;
- remote media or large assets;
- cloud timeout limits.

Skill response:

- re-encode source media with reasonable keyframe intervals;
- increase/cache tune when supported;
- split long videos into scenes;
- keep source assets local/bundled when possible;
- avoid giant media in early drafts.

### "HyperFrames feels fragile."

Observed causes:

- invalid root composition;
- missing `data-composition-id`;
- missing timed clip attributes;
- overlapping tracks;
- stale preview/cache;
- FFmpeg not installed;
- wrong framework assumptions by agents.

Skill response:

- use HyperFrames native skill for implementation;
- run lint/doctor/validate where available;
- specify plain HTML composition, not React/Vue;
- keep `data-*` contract explicit;
- keep small targeted prompts after scaffold.

### "Rendered output differs from preview."

Observed causes:

- preview frame rate hides/differs from frame capture;
- fonts/assets not bundled;
- nondeterministic randomness;
- async timeline construction;
- media playback controlled manually.

Skill response:

- deterministic timelines only;
- seeded randomness only;
- explicit asset paths;
- key timestamp render checks;
- never rely only on live preview.

### "Text is unreadable / too small."

Observed causes:

- agent designs for web page, not video frame;
- too much information on one shot;
- mobile/vertical safe area ignored;
- motion applied during reading.

Skill response:

- lock hero frame;
- define safe area and minimum text sizes;
- animate text in/out, not while reading;
- verify at output resolution.

### "Motion feels generic."

Observed causes:

- no narrative role for movement;
- every scene uses same fade/slide;
- decorative particles/gradients;
- no handoff between shots.

Skill response:

- each motion gets intent;
- preserve visual handoffs;
- use recurring motion motifs;
- remove animation that does not explain product/story.

## Tool Choice Guidance

Use HyperFrames when:

- output is HTML/GSAP video;
- agent should create deterministic MP4 from standard web primitives;
- scenes are mostly graphic/composition based;
- skill/runtime constraints are acceptable.
- you want agent-friendly HTML composition with lint/inspect/render loops.

Use Remotion when:

- React component model is core;
- video is part of a React app/product;
- data-driven video generation needs React ecosystem;
- team accepts render/bundle/concurrency complexity.

Do not choose Remotion just because "React is familiar" if the desired output is a simple timed graphic sequence. HyperFrames or plain FFmpeg may be simpler.

Use simpler FFmpeg/image pipeline when:

- video is mostly static slides/screenshots;
- speed matters more than live DOM;
- transitions are simple;
- deterministic batch rendering is the priority.

Use manual/editor workflow when:

- creative ambiguity is high;
- human taste iteration matters more than programmatic scale;
- source footage/audio is complex.

## Preflight Checklist

- Output dimensions and fps locked.
- Duration budget locked.
- Tool choice justified.
- Source assets exist with paths.
- Hero frames specified.
- Motion spec written.
- Moving vs frozen elements listed.
- Negative constraints listed.
- Acceptance timestamps listed.
- Expensive CSS effects justified.
- Render verification timestamps listed.
- Fallback plan exists if preview/render diverge.

## Sources

- HyperFrames troubleshooting: https://hyperframes.heygen.com/guides/troubleshooting
- HyperFrames prompting guide: https://hyperframes.heygen.com/guides/prompting
- HyperFrames AI agents guide: https://hyperframes.video/docs/recipes/ai-agents
- HyperFrames Reddit issue report: https://www.reddit.com/r/heygen/comments/1tbx48z/issues_with_hyperframes/
- Remotion issue #4300: https://github.com/remotion-dev/remotion/issues/4300
- Remotion discussion #3070: https://github.com/orgs/remotion-dev/discussions/3070
- Reddit browser-rendering/Remotion speed discussion: https://www.reddit.com/r/webdev/comments/1scgge9/how_do_some_video_platforms_render_video_faster/
- Motion graphics AI expectations discussion: https://www.reddit.com/r/motiongraphics/comments/1srkhls/my_clients_are_starting_to_ask_about_ai_and_i/
- AI animation error analysis: https://longstories.ai/blog/why-ai-animation-errors-happen
