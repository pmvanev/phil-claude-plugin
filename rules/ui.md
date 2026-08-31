---
paths:
  - "**/*.{tsx,jsx,vue,svelte,css,scss,sass,less,html}"
  - "**/components/**"
  - "**/pages/**"
  - "**/layouts/**"
  - "**/styles/**"
---

# UI Guide

## Design Aesthetics

1. **Use Rich Aesthetics**: The user should be wowed at first glance. Use best practices in modern web design (e.g. vibrant colors, dark modes, glassmorphism, and dynamic animations) to create a stunning first impression.
2. **Prioritize Visual Excellence**: Implement designs that feel extremely premium:
   - Avoid generic colors (plain red, blue, green). Use curated, harmonious color palettes (e.g., HSL tailored colors, sleek dark modes).
   - Use modern typography (e.g., from Google Fonts like Inter, Roboto, or Outfit) instead of browser defaults.
   - Use smooth gradients.
   - Add subtle micro-animations for enhanced user experience.
3. **Use a Dynamic Design**: An interface that feels responsive and alive encourages interaction. Achieve this with hover effects and interactive elements. Micro-animations improve user engagement.
4. **Premium Designs**: Make a design that feels premium and state of the art. Avoid simple minimum viable products.
5. **Don't use placeholders**: ship a real asset rather than a grey box. Where the environment offers an
   image-generation tool, use it; otherwise source or commit a real image. (This bullet named a
   `generate_image` tool until 2026-08-31. No such tool exists in this plugin or in Claude Code, so the
   instruction was unfollowable — a standard that cannot be obeyed is worse than one that is merely
   ignored, because it reads as a failure to comply.)

## What this file is, and what it is not

**This is build-time guidance, and nothing reviews against it.** "Wow at first glance" and "avoid simple
minimum viable products" are directions for making something, not defects anyone can flag: there is no
objective form of *not premium enough*. Read it while building a UI. Do not expect a reviewer to enforce
it, because none does, and that is deliberate rather than an oversight.

**The checkable guardrails that used to live here moved to `ux.md` on 2026-08-31** — reduced-motion
variants, the effect budget on constrained devices, and legibility at small sizes. They were the one part
of this file a reviewer could act on, so they went where the reviewer looks. The split is by
*checkability*, not by subject: the cost of an animation and its reduced-motion variant are reviewed in
`ux.md`; whether the animation is attractive is the taste question, and it stays here.

Usability and accessibility on mobile — reflow, touch targets, gestures, orientation — have always been
`ux.md`'s, not this file's.
