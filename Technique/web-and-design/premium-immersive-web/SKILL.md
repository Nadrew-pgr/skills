---
name: premium-immersive-web
description: Build or review premium immersive websites, 3D landing pages, and scroll-driven web experiences that combine strong art direction, WebGL/R3F scrollytelling, coherent UI/UX, centralized design tokens, component reuse, accessibility, performance, security, and stack alignment. Use when Codex needs to create an award-level landing page, product website, interactive narrative, WebGL scrollytelling page, or immersive SaaS/product experience without sacrificing maintainability or conversion clarity.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Premium Immersive Web

## Description

Use this skill to make immersive websites that feel intentional, performant, coherent, and product-relevant. The goal is not “add 3D”; the goal is to translate a product story into a spatial, scroll-driven web experience without losing UI quality, accessibility, maintainability, or conversion.

## First Pass

Before implementation, produce or infer:

- **Intent**: what the user wants the site to make visitors feel, understand, and do.
- **Narrative spine**: the transformation the site shows from first viewport to final CTA.
- **Visual thesis**: mood, material, energy, and the dominant visual anchor.
- **Interaction model**: scroll, hover, click, keyboard, form, and reduced-motion behavior.
- **Behavior before look**: how the dominant visual behaves, transforms, and hands off across the story.
- **Product proof**: the concrete UI, output, workflow, or artifact that makes the immersive story credible.
- **Stack constraints**: framework, component library, styling system, deployment target, security rules, and performance budget.

If the user already has a strong idea, preserve it. Ask only for missing information that changes architecture, product truth, safety, or scope. If the idea is fuzzy, run a short intake/grill before designing.

## Build Principles

- Build the architecture for the immersive experience from the beginning. Use placeholders where needed; do not create a generic landing that needs a later rewrite.
- Use one dominant visual idea per section. Avoid a sequence of unrelated effects.
- Let the 3D or motion tell the story, while HTML copy keeps the product understandable.
- End in a concrete product surface or proof point. Abstract spectacle alone is not enough.
- Keep visible copy, scenario data, and 3D labels centralized and localizable.
- Use project design tokens and component patterns. Do not hardcode arbitrary colors, radii, spacing, shadows, or UI behavior across files.
- Prefer reusing one coherent component library when it fits the stack; customize it after, rather than hand-rolling every primitive.
- Respect performance, accessibility, security, and the user’s actual stack over visual ambition.

## Reference Loading

Read only the references needed for the task:

- For WebGL/R3F, camera movement, particles, scene state, or scroll choreography, read [3d-scrollytelling.md](references/3d-scrollytelling.md).
- When the user describes a visual metaphor in natural language, read [motion-glossary.md](references/motion-glossary.md).
- For UI coherence, design tokens, centralized styling, responsive polish, and avoiding generic SaaS UI, read [ui-coherence.md](references/ui-coherence.md).
- For deciding whether to use a library, component kit, Agent Elements, shadcn-style components, or custom UI, read [component-strategy.md](references/component-strategy.md).
- For performance, accessibility, forms, APIs, security, and deployment safety, read [performance-security.md](references/performance-security.md).
- For story-first intake, Noomo-derived production heuristics, and AI-assisted site creation workflow, read [strategy-workflow.md](references/strategy-workflow.md).
- For optional external inspiration and source links, read [external-sources.md](references/external-sources.md).

## Recommended Workflow

0. If project intent is fuzzy, use `intake-and-grill` style questioning: one decision at a time, recommended answer first, and infer from docs before asking. When enough is clear, crystallize into a project brief/PRD and issues.
1. Map the story into named states or sections.
2. Define the content/data model before coding UI.
3. Establish design tokens and component primitives.
4. Build the full page skeleton with real copy placeholders from config.
5. Add the dominant visual or WebGL placeholder.
6. Add product proof and CTA behavior.
7. Add scroll choreography and controlled interactions.
8. Review the implementation against the PRD/spec/skill and log mismatches before calling it done.
9. Verify responsive layout, reduced motion, performance, accessibility, security, and visual output.

Before implementation or review, create a compact object lifecycle matrix for important narrative objects: primary interaction surface if relevant, CTA, capture cards, particles, active spheres, lines, labels, product UI, and proof surfaces. For each object, note where it appears, moves, transforms, hides, and what data drives it.

## Non-Negotiables

- One persistent WebGL canvas maximum for an immersive 3D landing.
- No React state updates inside frame loops.
- No fake camera travel by scaling the whole scene.
- No hardcoded visible marketing copy scattered through components.
- No disconnected visual effects that do not map to the narrative.
- No inaccessible canvas-only product UI.
- No unbounded free-form AI simulation inside a marketing page unless explicitly requested.
- No public promise of integrations, AI actions, pricing, or data handling that the product cannot support.
- No fake completion. If work is only a prototype/foundation/partial pass, say that and justify the remaining gap.
- No decorative loop for narrative objects. If a card, particle, line, or UI element represents story progress, it should be tied to scene state or scroll progress, not an unrelated infinite animation.
- No fake affordance. A visible button/input must perform a meaningful action, clearly be disabled, or be styled as cinematic display rather than an actionable control.
- One concern should have one canonical tracking place. Use backlog/issues for actionable work, HITL review for subjective approval, and feature requests for incoming requests; avoid duplicating the same “later” note everywhere.

## Review And Triage Format

Prefer an independent review over autoreview. If the agent has access to subagents or an equivalent independent reviewer, delegate the review pass to one before declaring completion. The reviewer should compare the implementation against the brief, PRD/spec, skill rules, acceptance criteria, and visual output. If no subagent/reviewer capability is available, perform an explicit autoreview and label it as such.

When reviewing an immersive landing or user feedback, classify each item with:

- truth: true, false, partly true, or unverified
- urgency: now, after current pass, later, or future
- scope: small, medium, or large
- affected area: copy, UI, tokens, CTA, WebGL, scene transition, product proof, performance, accessibility, security
- skill/reference to use: for example 3D scrollytelling, motion glossary, UI coherence, component strategy, performance/security
- likely technique: for example GSAP timeline, camera path, instanced spheres, radial falloff, token audit, Framer Motion morph, slash-editor mock

## Validation Checklist

Before handoff:

- The first viewport clearly identifies the product and action.
- Each section has one job and one dominant visual idea.
- The page remains understandable without WebGL and with reduced motion.
- Design tokens centralize colors, radius, spacing, shadows, and typography decisions.
- Shared components handle repeated buttons, panels, cards, forms, project-specific input surfaces, and product surfaces.
- Text does not overlap, wrap badly, or resize controls unexpectedly across desktop and mobile.
- The 3D scene is nonblank, framed correctly, and does not block HTML controls.
- Forms validate input, handle pending/success/error states, and avoid leaking secrets.
- Build/typecheck/lint and browser verification pass when available.
- Visual QA is explicit: screenshot, browser capture, rendered frame/video, or a clear note that visual capture was unavailable and user feedback is needed.
- Review provenance is explicit: subagent/independent review when available; otherwise labeled autoreview.
- Issue status matches reality: `Done` only when acceptance criteria and visual proof are satisfied; otherwise use `Prototype`, `Partial`, or `Foundation` with justification.
- The object lifecycle matrix matches the implemented page; no key object disappears, duplicates, loops, or changes role without explanation.
