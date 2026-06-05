# Objections And Failure Modes

Read before a large implementation or after a bad attempt.

## User Objections This Skill Must Prevent

- "I asked for a video, why did you build a website?"
- "I asked for 3D/immersive, why is it flat cards?"
- "The motion is not what I described."
- "It feels generic."
- "The typography is too small."
- "The transition is abrupt."
- "The agent said done but did not visually verify."
- "It works technically but looks wrong."
- "The prompt was one-shot but the result needs rescue."

## Root Causes

- No HyperFrames project contract.
- No DESIGN.md gate.
- No SCRIPT/STORYBOARD before coding.
- No hero frame locking.
- No explicit technique choice for 3D/immersive.
- No timing table.
- No `inspect --at` timestamps.
- Too many simultaneous movements.
- Agent treats video like responsive web UI.
- Agent uses generic visual tropes instead of source context.

## Corrective Rules

- If output is a video, build a HyperFrames composition.
- If source is a website, use `website-to-hyperframes`.
- If user requests 3D, choose a spatial implementation and name it before coding.
- If motion is ambiguous, write a shot spec and use math primitives.
- If content is already in files/docs, use it instead of asking.
- If visual QA is impossible, ask for one screenshot/timestamp and mark the gap.
- If not fully complete, say `Prototype`, `Foundation`, or `Partial`, and justify.

## Scope Control

When time is tight:

1. Keep fewer scenes.
2. Preserve design and readability.
3. Preserve HyperFrames validity.
4. Preserve the one or two signature motions.
5. Cut decorative complexity first.

Do not cut:

- HyperFrames attrs/timeline contract;
- visual identity;
- hero frames;
- lint/inspect;
- the requested 3D/spatial signature if it is central to the brief.
