---
name: ui-ux-visual-review
description: Review visible UI, editor surfaces, content visuals, carousels, social posts, video dressing, thumbnails, slides, landing sections, screenshots, or generated visual implementations against product intent, brand/content goal, code implementation, UX, visual polish, responsiveness, accessibility, and project rules. Use when the user asks for UI/UX review, visual QA, content visual critique, carousel review, video overlay/habillage review, screenshot review, "why does this look cheap", reviewer/subagent visual pass, or whether a coded/rendered visual matches the vision before acceptance.
license: MIT
author: Andrew (Nadrew-pgr)
---

# UI UX Visual Review

## Purpose

Use this skill to review a visible surface or visual artifact. It is a reviewer skill, not a production skill.

It applies to:

- product UI and editor surfaces;
- web apps, landing sections, dashboards, in-app screens;
- carousels, social posts, thumbnails, cover visuals, content cards;
- video dressing: lower thirds, captions, title cards, overlays, scene wrappers, motion graphics, end screens;
- slides or visual storyboards;
- generated HTML/CSS/React/Remotion/HyperFrames/Canva-like outputs when code or screenshots are available.

The goal is to answer:

- Does the visual match the product/content promise and target viewer?
- Does it feel premium, finished, legible, and coherent?
- Does the UX or content flow expose the right action/message at the right moment?
- Does the implementation code explain any visual defects?
- Does it respect project rules, brand constraints, acceptance criteria, accessibility, and visual gates?
- What exactly should the implementation agent change?

Default behavior: review and return an actionable handoff. Do not implement changes or create files unless the user explicitly asks, or the project process requires updating an existing review/build-log document.

## No Unnecessary Files

Do not create standalone review files by default.

Prefer a concise response or reviewer handoff in chat. Create or update files only when one of these is true:

- the user explicitly asks for a file;
- the project process requires a build-log/reviewer entry;
- screenshots or visual artifacts must be saved for a visual gate;
- an implementation agent needs a persistent patch brief and the user approved that workflow.

Never create extra README/checklist/archive files just to document the review.

## Required Inputs

Collect as many as are available:

- current issue, product goal, campaign/content goal, or visual brief;
- target user/viewer and platform: desktop, mobile, carousel, YouTube, Shorts, TikTok, LinkedIn, in-app, etc.;
- brand rules, design rules, PRD, acceptance criteria, quality gates, previous feedback;
- live URL, screenshot, video frame, rendered artifact, or preview;
- code files likely responsible for layout, styling, copy, animation, rendering, or export;
- current `git status` when reviewing a local implementation;
- known visual references and license constraints.

If there is no visual evidence, mark the review as `visual evidence unavailable`. If there is no code access, mark code findings as `not code-verified`.

## Code-Aware Review

When code is available, inspect it enough to identify likely root causes. Do not stop at "the screenshot looks wrong".

Look for:

- component structure and ownership boundaries;
- CSS/tokens/theme variables;
- hardcoded dimensions, absolute positioning, fixed heights, bad overflow, conflicting scroll containers;
- responsive breakpoints and container queries;
- text wrapping, long-word handling, line-height, font sizing, icon sizing;
- z-index, stacking, clipping, sticky/fixed positioning;
- image/video asset usage, object-fit, crop, resolution, safe areas;
- animation timing and reduced-motion handling;
- render/export settings for carousels, slides, Remotion, HyperFrames, screenshots, or video frames;
- duplicated visual logic or one-off demo code that should become reusable.

For each code-backed finding, include the likely file/component/selector/function to inspect or change. If exact line numbers are available, cite them. If not, give a precise search target.

## Why Use Multiple Reviewers

Visual review fails when one agent collapses everything into "looks good" or "looks bad". Use separate reviewers/subagents when available because each axis has different failure modes.

Recommended reviewer passes:

- **Visual Design Reviewer**: hierarchy, composition, spacing, typography, color, premium feel.
- **UX/Flow Reviewer**: user journey, action placement, interaction states, keyboard/touch flow.
- **Content Pertinence Reviewer**: clarity, hook, message, narrative order, audience fit, platform fit.
- **Brand/Art Direction Reviewer**: recognizability, tone, consistency, differentiation, visual system.
- **Responsive/Export Reviewer**: mobile/tablet/desktop, carousel crop, video safe areas, aspect ratio, platform constraints.
- **Accessibility/Legibility Reviewer**: contrast, captions, font size, focus, reading speed, motion comfort.
- **Rules/Gates Reviewer**: PRD, acceptance criteria, project visual rules, no-false-done, no-toy-implementation.
- **Code/DX Reviewer**: maintainability, reusable tokens/components, implementation root cause, host integration.
- **Security/License Reviewer**: secrets, personal data, BYOK, file/status truthfulness, asset rights, third-party license boundaries.

If subagents are unavailable, perform a labeled `fallback self-review` using the same hats.

## Review Workflow

1. **Load rules and brief**
   - Read the issue, PRD, design rules, brand rules, acceptance criteria, or content brief.
   - Identify human-review and visual-gate requirements.

2. **Inspect the actual visual**
   - Open the app/artifact or inspect screenshots/video frames.
   - Check relevant viewports, aspect ratios, export crops, or platform safe areas.
   - Do not claim visual verification from code inspection alone.

3. **Inspect the code**
   - Read responsible components/styles/render scripts.
   - Map visual defects to likely implementation causes.
   - Note when the code is fine and the issue is content/art direction instead.

4. **Run reviewer passes**
   - Use subagents/reviewers when available.
   - Keep findings independent, then deduplicate.

5. **Prioritize**
   - `P0`: unusable, unreadable, data-loss/security/legal issue, broken primary flow/export.
   - `P1`: must fix before acceptance; core visual promise, product/content clarity, or main UX is wrong.
   - `P2`: should fix soon; quality gap, polish debt, secondary viewport/platform issue.
   - `P3`: optional polish, future enhancement, taste preference, or hypothesis.

6. **Return implementation handoff**
   - Give the implementation agent exact changes to consider.
   - Include affected files/components/selectors when known.
   - Avoid vague feedback such as "make it better" or "more premium".

## Quality Checklist

Check:

- first impression: started, unfinished, clean, premium, or memorable;
- hierarchy: what the viewer reads first, second, third;
- layout: alignment, whitespace, density, gutters, safe areas, scroll/crop behavior;
- typography: font choice, size, weight, line-height, wrapping, contrast;
- color/material: palette, gradients, glass, depth, shadows, borders, consistency;
- visual assets: relevance, resolution, crop, object-fit, authenticity, no generic filler;
- motion: timing, easing, continuity, attention control, reduced-motion fallback;
- interaction: hover/focus/active/disabled states, gestures, keyboard/touch;
- responsiveness: mobile/tablet/desktop and narrow windows;
- platform fit: carousel slide crop, video frame safe areas, caption readability, social feed preview;
- content clarity: hook, message, proof, CTA, narrative sequence;
- brand fit: recognizable system, tone, premium cues, differentiation;
- accessibility: contrast, focus, captions, reading speed, motion comfort;
- implementation: tokens, reusable components, no fragile one-off layout hacks.

## Cheapness Signals

Flag these when visible:

- debug panels or technical metadata presented as normal UI;
- raw browser/default controls where custom product affordances are expected;
- generic cards, stock-like imagery, weak screenshots, or placeholder copy;
- one-note palette or default gradients with no visual thesis;
- inconsistent radii, shadows, borders, spacing, icon weight, or typography;
- text clipped, overlapping, cramped, too small, or badly wrapped;
- controls that jump/resize on hover;
- scroll conflicts, nested scroll traps, clipped sticky bars;
- carousel slides that rely on too much text or break at crop boundaries;
- video overlays outside safe areas or unreadable over footage;
- captions too fast, too low contrast, or visually detached from the brand;
- UI actions duplicated randomly or hidden in debug panels;
- no clear primary message/action;
- code uses fixed pixel assumptions where the surface must be responsive.

## Editor Surface Checklist

For Markdown/rich/block editors, also check:

- document is the primary surface, not the inspector;
- source/rich/live-preview/preview modes are clear and document-kind aware;
- toolbar is contextual or configurable, not demo chrome;
- slash menu has grouping, search, aliases, keyboard navigation, empty states;
- selected-text actions appear near selection or through a predictable command path;
- AI actions live in toolbar/slash/context/command flows, not only debug panels;
- indentation and nesting are visually exact;
- indentation guides help reading/editing when useful;
- todos look product-grade and preserve source semantics;
- Enter, Backspace, Tab, Shift+Tab, paste, selection, undo/redo work around complex blocks;
- code fences expose language/meta controls without trapping users;
- folding affordances are subtle, aligned, keyboard/focus reachable, and not debug counters;
- save/status truth is present but discreet.

## Content Visual Checklist

For carousels, posts, video dressing, thumbnails, and slides:

- one clear job per frame/slide;
- hook appears immediately and is not buried;
- text amount fits the platform and reading time;
- visual rhythm changes enough to keep attention without breaking brand coherence;
- CTA/proof appears where the format expects it;
- frames are readable when cropped in feed previews;
- captions/lower-thirds/title cards do not cover faces, UI, or key action;
- safe margins are respected for 9:16, 1:1, 4:5, 16:9, and platform UI overlays;
- template system is reusable without making every asset look identical;
- export settings match target platform and resolution.

## Reference And License Rules

Use references for benchmarks, not blind copying.

- Say which products, creators, plugins, or brands were used as inspiration.
- Do not copy code, assets, exact protected styling, names, or implementation from third-party projects without checking license and attribution needs.
- For open-source plugins/assets, record the license when recommending close inspiration.
- Prefer clean-room requirements: describe behavior, composition, timing, and constraints, not copied implementation.

## Output Format

Use this structure:

```md
## Verdict

Accepted / accepted with follow-ups / visual verification pending / not accepted.

## Evidence

- Visual evidence:
- Code inspected:
- Viewports/platforms checked:
- Tooling limits:

## Findings

### [P1] Short finding

- Evidence:
- Code/root cause:
- Why it matters:
- Rule/reference:
- Implementation handoff:

## Hypotheses / Product Opportunities

### [H2] Short hypothesis

- Hypothesis:
- Why it seems plausible:
- Decision needed:

## Reviewer Passes

- Visual Design:
- UX/Flow:
- Content Pertinence:
- Brand/Art Direction:
- Responsive/Export:
- Accessibility/Legibility:
- Rules/Gates:
- Code/DX:
- Security/License:

## Acceptance Decision

- Status:
- Must fix before acceptance:
- Follow-up/backlog:
```

## Guardrails

- Do not accept visual work without visual evidence.
- Do not ignore code when code is available.
- Do not create review files by default.
- Do not implement fixes during the review unless explicitly asked.
- Do not call subjective taste a blocker without tying it to a goal, rule, platform, or user impact.
- Do not hide reviewer findings.
- Do not claim visual verification if browser, screenshot, video, or export tooling failed.
- Do not give vague handoff; name the likely component, style, token, render setting, or content frame to change.
