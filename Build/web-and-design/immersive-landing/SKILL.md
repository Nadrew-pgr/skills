---
name: immersive-landing
description: Plan, implement, or review premium immersive landing pages that combine strong frontend art direction, UI Pro Max polish, conversion structure, scrollytelling, product proof, accessibility, and optional WebGL/R3F scenes. Use when Codex needs to build a high-end landing page, immersive SaaS/product page, scroll narrative, launch page, or marketing experience that must feel coherent rather than generic.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Immersive Landing

## Description

Use this skill to orchestrate the full landing experience. It complements `frontend-skill` for visual hierarchy and uses `immersive-3d-scrollytelling` when the page includes WebGL, React Three Fiber, procedural 3D, or scroll-driven spatial motion.

## Skill Composition

When available, combine these skills instead of replacing them:

- `frontend-skill`: composition, hierarchy, restraint, copy, hero quality, product UI taste
- `ui-pro-max` or equivalent project UI skill: component polish, interaction details, high perceived quality
- `immersive-3d-scrollytelling`: one-canvas WebGL architecture, camera motion, scene state, performance

If no separate `ui-pro-max` skill exists, apply the UI Pro Max rules below directly.

## Working Model

Before building, define:

- visitor and outcome: who arrives, what they must understand, and what action they should take
- visual thesis: one sentence for mood, material, energy, and visual anchor
- narrative spine: the transformation the visitor watches happen
- section jobs: one responsibility per section
- interaction thesis: two or three motions that change how the page feels
- conversion path: where the CTA appears, how it behaves, and what proof supports it
- product proof: the concrete UI or artifact that makes the experience credible
- object lifecycle: primary interaction surface if relevant, CTA, cards, particles, active points, labels, product UI and final CTA across all scenes

Do not start from a generic SaaS layout. Start from the story, the behavioral metaphor, and the dominant visual. If intent is fuzzy, use intake-and-grill before designing.

## Narrative Structure

An immersive landing still needs marketing clarity.

- First viewport: brand/product name, literal offer or promise, primary CTA, and one dominant visual.
- Middle: show the transformation through a small number of coherent beats.
- Product proof: reveal the real interface, workflow, output, or artifact. Do not let abstract 3D replace product credibility.
- Final CTA: return to clarity after the immersive sequence.

Use sections as story beats, not decorative blocks. Each section should either explain, prove, deepen, or convert.

## UI Pro Max Rules

Make the DOM UI feel deliberate and production-grade.

- Use project design tokens first. Do not hardcode arbitrary colors, shadows, border radii, or glass effects.
- Keep palettes restrained. Avoid default cyan/purple glassmorphism unless the project explicitly calls for it.
- Use typography, spacing, contrast, and alignment before adding chrome.
- Prefer cardless layouts. Use cards only for repeated items, modals, controls, or genuinely framed product surfaces.
- Keep panels and controls dense but readable. Product UI should feel usable, not like a decorative dashboard collage.
- Make buttons and inputs stable across desktop/mobile; text must not wrap badly, overflow, or resize the layout on hover.
- Use icons for familiar controls when an icon is clearer than text.
- Avoid visible instructional design copy such as “scroll to see the magic” unless the product requires it.

## Motion And Interaction

Motion must clarify the story.

- Scroll drives the base narrative.
- Hover adds sensation and affordance.
- Click creates controlled participation, not an unbounded app inside the landing.
- Keep branches short and convergent unless the brief asks for a real interactive product.
- Use CSS transitions for simple UI micro-interactions. Reserve Framer Motion, GSAP, or heavier libraries for state transitions that matter.
- Do not let animation interfere with reading, CTA use, form completion, or accessibility.
- Each important section-to-section transition must have a deliberate continuity plan. If the visual jumps, fix the transition or document the intended hard cut.
- Do not use infinite decorative loops for objects that are supposed to represent narrative progress.
- Do not show buttons that look actionable unless they trigger the narrative, submit data, or clearly represent a non-interactive cinematic mock.

## Content And i18n

Keep content centralized.

- No visible marketing copy should be hardcoded across components.
- Store section copy, CTA labels, scenarios, 3D labels, and product mock data in dictionaries or config.
- If the landing is localized, localize the narrative scenario too, not only navigation labels.
- Keep copy short enough to scan during motion-heavy sections.

## Implementation Order

Build architecture before spectacle.

1. Create content config, i18n shape, section map, and scene/state map.
2. Build the full scrollable page skeleton and CTA flow without final effects.
3. Add the dominant visual or WebGL placeholder.
4. Add the product proof section.
5. Add scroll/motion state transitions.
6. Add controlled interactions.
7. Review against the brief, PRD, issue acceptance criteria, and relevant skill rules.
8. Perform performance, accessibility, responsive, and visual QA passes.

Do not build a “temporary normal landing” that must be refactored later. Build the structure for the immersive experience from the start, with placeholders where necessary.

## Feedback Triage

Prefer an independent review over autoreview. If the agent has access to subagents or an equivalent independent reviewer, delegate the review pass to one before declaring completion. The reviewer should compare the landing against the brief, PRD/spec, skill rules, acceptance criteria, and visual output. If no subagent/reviewer capability is available, perform an explicit autoreview and label it as such.

For correction passes, answer each feedback item with:

- truth: true, false, partly true, or unverified
- urgency: now, after current pass, later, or future
- scope: small, medium, or large
- affected component/scene
- skill/reference to use
- likely implementation technique

Do not silently drop feedback items. If a visual tool is unavailable, mark visual claims as unverified and request or use a screenshot.

When there is overlap between docs, keep one canonical place:

- backlog/issues: actionable work
- HITL review: subjective visual/product approval
- feature requests: raw incoming request log

Do not copy the same “we will revisit later” item into multiple active documents unless each document adds a different purpose.

## Validation

Before handoff, check:

- first viewport clearly identifies the product and action
- each section has one job
- visual system follows project tokens
- content is centralized and localizable
- CTA works and remains usable
- product proof is concrete
- motion is meaningful, not ornamental
- WebGL, if present, is one persistent canvas and has a reduced-motion fallback
- desktop and mobile screenshots show no incoherent overlap, bad wrapping, or hidden controls
- CTA interactions are visually smooth and keyboard usable
- product proof reflects the intended product surface, not a misleading raw placeholder
- review provenance is explicit: subagent/independent review when available; otherwise labeled autoreview
- status wording is honest: `Done` requires acceptance criteria plus visual evidence when possible; otherwise use `Prototype`, `Partial`, or `Foundation` and justify what remains.
