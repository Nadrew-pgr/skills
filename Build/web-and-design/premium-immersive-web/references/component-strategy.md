# Component Strategy

Do not build every UI primitive from scratch when a stable library fits the stack.

## Decision Order

1. Check the project’s existing component system.
2. Reuse the existing system if it has the required primitive.
3. If missing, prefer a compatible library that matches the stack and can be tokenized.
4. Use a single component source where possible to preserve coherence.
5. Wrap imported components in project primitives before spreading them across the app.
6. Hand-roll only when the component is highly custom, performance-sensitive, or central to the brand.

## Agentic UI

For agentic landing moments, a full chat app is often unnecessary.

Useful patterns:

- composer/input bar
- plan card
- approval controls
- tool/action card
- markdown preview
- status stepper
- task queue

Agent Elements or shadcn-style components can be useful references for these patterns, but only import/use them if they fit the project stack and visual system.

## Library Rules

- Do not mix several component libraries casually.
- Do not paste vendor styles directly into many files.
- Centralize theme adaptation in wrappers/tokens.
- Replace library defaults that clash with the project’s art direction.
- Keep accessibility behavior from mature libraries when possible.

## Composer Guidance

If the landing needs one “AI input” moment, usually build or adapt a composer rather than a full agent chat.

The composer should:

- show the concrete request
- support keyboard/submit affordance
- have clear loading/result states
- remain HTML-accessible
- not pretend to run real AI unless it does
