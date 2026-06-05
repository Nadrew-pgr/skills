# Performance And Security

Premium immersive work must stay fast, safe, and accessible.

## Performance

- Render critical hero text before heavy WebGL.
- Dynamically import WebGL-heavy client components when the framework supports it.
- Use image/font optimization from the stack.
- Avoid large models/textures in v1.
- Avoid frame-loop React state updates.
- Test LCP, INP, CLS where possible.
- Use reduced-motion fallbacks and mobile simplification.
- Avoid many large translucent/blurred DOM layers.

## Accessibility

- Keep product UI and CTAs in semantic HTML.
- Preserve keyboard navigation and focus states.
- Respect `prefers-reduced-motion`.
- Ensure text contrast over 3D or video backgrounds.
- Avoid relying on color alone for states.
- Provide fallback content if canvas fails.

## Security

- Do not expose secrets in client code.
- Validate form input server-side when a backend exists.
- Add honeypot/rate limiting or equivalent protection for public forms when practical.
- Avoid logging sensitive user content.
- Be careful with third-party scripts, trackers, and remote assets.
- Do not claim data access, integrations, or agent actions unless they are real or clearly framed as future/planned.

## Verification

- Run typecheck/build/lint where available.
- Check browser console for errors.
- Verify CTA states: idle, input, pending, success, error.
- Verify mobile and reduced-motion.
- Confirm no blank canvas.
