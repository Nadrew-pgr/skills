# Framework Notes: HyperFrames

Use this when implementing with HyperFrames. Also load the native HyperFrames skill.

## Fit

HyperFrames is a good fit when:

- output is deterministic HTML/CSS/GSAP -> MP4;
- an AI agent authors compositions end-to-end;
- scenes are graphic, text, UI, data, explainer, launch, or product-demo oriented;
- plain HTML is acceptable;
- render loop can run lint/inspect/render commands.

## Contract

- Composition is HTML, not React/Vue.
- Timed visible elements use `class="clip"` plus `data-start`, `data-duration`, `data-track-index`.
- Timelines are GSAP and registered synchronously.
- Use `window.__timelines`.
- No uncontrolled randomness.
- Use native CLI/lint/inspect/render JSON outputs when available.
- Prefer catalog/blocks when a tested visual primitive exists.

## AI Failure Modes

Observed/documented:

- agent guesses generic web video conventions when skill is not invoked;
- agent creates React/Vue components instead of HyperFrames HTML;
- agent forgets `class="clip"` or timing attrs;
- agent creates invalid composition root;
- text/captions overlap because no hero frame was locked;
- long prompt causes re-authoring instead of small edits;
- 4K/60fps request slows render without improving result enough;
- assets omitted or paths guessed;
- preview stutters when CSS paint is expensive.

## Prevention

- Start from a motion spec, not a vibe prompt.
- Invoke HyperFrames skill explicitly.
- Use lint/inspect before expensive render.
- Use catalog-first authoring when possible.
- Iterate with small edits: "title 2x bigger", "move captions up", "fade out at 0:08".
- Keep defaults at 1920x1080, 30fps unless there is a concrete reason.
- Avoid heavy animated blur/filter/shadows.
- Verify rendered output at key timestamps.

## Sources

- HyperFrames prompting guide: https://hyperframes.mintlify.app/guides/prompting
- HyperFrames AI agents guide: https://hyperframes.video/docs/recipes/ai-agents
- HyperFrames troubleshooting: https://hyperframes.heygen.com/guides/troubleshooting
