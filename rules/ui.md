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
5. **Don't use placeholders**: If you need an image, use your generate_image tool to create a working demonstration.

## Mobile guardrails

The aesthetics above must not degrade on the small touch screens and constrained devices most users bring — scope every rich effect accordingly:

- **Honour `prefers-reduced-motion`**: offer a reduced variant; drop parallax and large scale/pan motion for users who ask for less.
- **Budget effects on constrained devices**: animate only compositor-cheap properties (`transform`, `opacity`); heavy blur, live `filter`, and stacked shadows/gradients cost frames on low-end phones.
- **Keep type and contrast legible at small sizes**: premium type that only reads at desktop scale is a regression on mobile.

Usability and accessibility on mobile — reflow, touch targets, gestures, orientation — live in `ux.md`, not here.
