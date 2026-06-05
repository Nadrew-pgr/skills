# UI Coherence

Immersive sites fail when the 3D is memorable but the UI feels generic, inconsistent, or hardcoded.

## Design Tokens

Centralize:

- colors and semantic accents
- border radius
- spacing scale
- typography scale and font choices
- shadows, glows, borders, blur values
- motion durations and easings
- z-index layers
- breakpoints and container widths

Changing the product’s radius, accent, surface style, or shadow intensity should require editing one token, not many components.

## Component Discipline

- Create shared primitives for buttons, links, panels, cards, badges, inputs, labels, sections, CTAs, and any project-specific interaction surface.
- Do not duplicate one-off button/card styles across sections.
- Use project UI libraries when they fit the stack, then adapt through tokens and wrappers.
- Prefer HTML for readable UI, not WebGL text.
- Use icons for familiar controls when clearer than text.

## Premium UI Rules

- Start with composition, hierarchy, spacing, and contrast before decoration.
- Avoid default glassmorphism, cyan/purple gradients, card grids, and dashboard mosaics unless the brand requires them.
- Product surfaces should feel operable, not like fake decorative screenshots.
- Text must not overlap or wrap awkwardly inside controls on desktop or mobile.
- Keep first viewport focused: product/brand, promise, CTA, dominant visual.
- Use short product language, not design commentary.

## Responsive Rules

- Keep the same product meaning across desktop/mobile.
- Simplify 3D on mobile before sacrificing readability.
- Avoid long pinned scroll sequences on mobile unless carefully tested.
- Verify real viewport screenshots, not only CSS assumptions.
