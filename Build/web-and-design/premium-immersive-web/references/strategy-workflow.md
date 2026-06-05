# Strategy Workflow

Use this when the project needs a strong immersive concept before implementation, or when feedback shows the build is drifting into random spectacle.

## Intake / Grill

Infer from project docs first. Ask only if a decision changes story, architecture, public promise, or scope. Ask one question at a time and give a recommended answer first.

Minimum decisions:

1. Visitor: who is this for?
2. Desired action: what should they do at the end?
3. Before/after: what changes in the visitor's understanding?
4. One remembered idea: what should remain after 10 seconds?
5. Proof: what real product, artifact, workflow, or output makes the story credible?
6. Visual metaphor: what object/system best explains the product?
7. Behavior: how should that object move, react, transform, and hand off?
8. Interaction: what is scroll-driven, hover-driven, click-driven, form-driven, or passive?
9. Constraints: stack, content, assets, perf budget, accessibility, mobile, security, deploy target.
10. Public promises: what must not be claimed yet?

Route when needed:

- fuzzy project -> `intake-and-grill`
- current/external facts needed -> `grill-with-research`
- enough context -> `to-project-brief` or project PRD
- build breakdown -> `to-issues`

## Noomo-Derived Heuristics

These are production heuristics, not visual style rules.

- Story first, not effect first: start with audience, problem, before/after, emotional shift, and one remembered idea.
- Behavior before look: decide how the visual system behaves before polishing how it looks.
- Spatial logic matters: movement through, around, toward, or inside the scene should match product meaning.
- Use 3D to clarify complexity, not to decorate a normal page.
- Hybrid wins: keep readable UI, forms, labels, and dashboards in HTML; use 3D for spatial metaphor, transformation, and memory.
- Performance is design: plan LOD, GPU instancing, simplified mobile, static fallbacks, and asset budgets early.
- Avoid surprise drift: after major visual changes, compare against the story/brief and do visual QA.
- Ask why behind visual feedback; fix the underlying narrative mismatch, not only the symptom.
- Choose medium intentionally: video for controlled pacing, web for exploration, interaction, conversion, and product proof.

## AI-Assisted Immersive Site Workflow

1. Intake/grill until story and constraints are clear.
2. Write brief/PRD: problem, audience, promise, narrative spine, visual thesis, proof, CTA, constraints, out-of-scope.
3. Write storyboard: scene states, object lifecycle, transitions, copy, acceptance criteria.
4. Convert to issues: thin vertical slices, each demoable.
5. Build foundation: routing, i18n/content config, tokens, components, one-canvas architecture.
6. Build dominant visual with placeholders first.
7. Add scroll state and camera/object choreography.
8. Add product proof and CTA flow.
9. Verify visually: browser screenshots, mobile, reduced motion, console, nonblank canvas.
10. Correction pass: compare implementation against brief/storyboard/skill; log only true follow-ups.

## Acceptance

A pass is not done until:

- first viewport says who/what/action;
- every scene has one job;
- visual behavior maps to the story;
- product proof exists;
- CTA path works or is explicitly mocked;
- content/tokens/components are centralized;
- visual QA happened or is explicitly blocked.
