---
license: MIT
author: Andrew (Nadrew-pgr)
---

# Skill — HyperFrames Component Curator

## Goal

Choose whether to reuse, adapt, compose, or create HyperFrames components.

## Required reading

- `branding/hyperframes-component-policy.md`
- `branding/video-style.md`
- `04-video-production-system.md`

## Decision ladder

1. Reuse approved component.
2. Adapt approved component.
3. Compose multiple components.
4. Create custom motion.

## Output

For each scene, return:

- component decision;
- command/component if known;
- reason;
- adaptation required;
- risk of cheapness;
- fallback if component fails.

## Rule

Do not use a component only because it exists.
