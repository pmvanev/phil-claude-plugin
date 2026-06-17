---
paths:
  - "**/*.{tsx,jsx}"
---

# React Idioms

Language-specific best practices for modern React (function components + hooks). These supplement `coding.md` and `typescript.md`. Flag the violation, name the preferred form. Assume React 18+ function components unless the file clearly uses class components by design.

---

## Components

| Prefer | Over | Why |
|--------|------|-----|
| Function components + hooks | class components (new code) | Simpler, composable, the modern default |
| Small, single-responsibility components | god-components rendering everything | Readable, testable, reusable |
| Composition (children/slots) | prop-drilling through many layers | Decouples; avoids threading props |
| Context (or a store) for deep shared state | passing props 4+ levels | Removes drilling; mind re-render scope |
| Typed props (`interface Props`) | untyped or `any` props | Contract is explicit and checked |

## Hooks — Rules & Smells

- **Rules of Hooks** — call hooks unconditionally at the top level; never in loops, conditions, or nested functions. Flag any conditional hook call.
- **Exhaustive deps** — `useEffect`/`useMemo`/`useCallback` dependency arrays must list every referenced value. A missing dep is a stale-closure bug; suppressing the lint rule needs justification.
- **`useEffect` is for synchronization with external systems**, not for deriving state. Computing state from props/state in an effect → compute during render instead.
- **Derived values** → compute inline or `useMemo` (only when measured); don't mirror props into state with an effect.
- **Stable callbacks** — `useCallback`/`useMemo` only where referential stability matters (passed to memoized children, effect deps). Don't wrap everything; it's noise.
- **Custom hooks** (`useX`) to extract reusable stateful logic instead of duplicating effect/state blocks.

## Rendering & State

| Prefer | Over | Why |
|--------|------|-----|
| Stable, meaningful `key` (entity id) | array index as `key` | Index keys corrupt state on reorder/insert |
| Functional updates `setX(x => ...)` | `setX(x + 1)` over stale `x` | Correct under batching/closures |
| Minimal, normalized state | redundant/derivable state | Single source of truth; fewer sync bugs |
| Lifting state only as far as needed | global state for local concerns | Keeps re-renders local |
| Conditional render `cond && <X/>` / ternary | imperative DOM manipulation | Declarative |

## JSX & Props

- **No inline object/array/function literals as props** to memoized children (new reference each render breaks memoization) — hoist or `useMemo`/`useCallback`.
- **Fragment `<>...</>`** over wrapper `<div>`s that exist only to satisfy single-root.
- **Spread props (`{...props}`) sparingly** — explicit props document the contract.
- **Accessibility** — interactive elements are real buttons/links with labels, not click-handlers on `<div>`.

## Avoid

- **Direct DOM access / `document.querySelector`** → use refs.
- **Side effects during render** (mutating refs, fetching, subscribing) → move to effects/event handlers.
- **`dangerouslySetInnerHTML`** without sanitization → XSS risk; flag it.
- **Massive `useEffect`** doing many unrelated things → split by concern, one effect per synchronization.

**Do not flag** idiomatic React, premature memoization the project hasn't adopted, or style the formatter owns.
