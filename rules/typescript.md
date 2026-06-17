---
paths:
  - "**/*.{ts,tsx}"
---

# TypeScript Idioms

Language-specific best practices for modern TypeScript. These supplement the language-agnostic principles in `coding.md`. Flag the violation, name the preferred form. Defer formatting (semicolons, quotes, spacing) to the project's formatter (Prettier/Biome).

---

## Type Safety

| Prefer | Over | Why |
|--------|------|-----|
| `unknown` + narrowing | `any` | `any` disables type checking; `unknown` forces a check |
| Discriminated unions | boolean flags or loose objects | Exhaustive, compiler-checked branches |
| `as const` | widened literal types | Preserves literal types; readonly tuples/objects |
| Type guards / `satisfies` | `as` type assertions | Assertions bypass checking; guards prove the type |
| `readonly` fields & `ReadonlyArray` | mutable-by-default | Communicates and enforces immutability |
| Strict `null` checks | optional-but-untracked | Catches null/undefined at compile time |

## Constants & Enums

| Prefer | Over | Why |
|--------|------|-----|
| Named `const` | repeated magic literals | Searchable, single source of truth |
| Union of string literals (`'a' \| 'b'`) or `as const` object | numeric `enum` | No runtime cost, better narrowing, tree-shakeable |
| `const enum` only when justified | regular `enum` | Avoids generated lookup objects (mind `isolatedModules`) |

## Functions & Async

- **`async/await`** over raw `.then()` chains; never mix the two in one flow.
- **No floating promises** — `await`, `return`, or explicitly `void` every promise. An un-awaited async call is a bug.
- **`Promise.all`** for independent async work instead of sequential `await`s in a loop.
- **Narrow parameter types** — accept the minimal interface needed, not a whole god-object, but use `Pick`/`Omit` rather than restating shapes.
- **Return types on exported functions** — explicit, so inference changes don't silently alter the public API.

## Idioms to Flag

| Prefer | Over | Why |
|--------|------|-----|
| Optional chaining `a?.b?.c` | nested `&&` guards | Concise, intent-clear |
| Nullish coalescing `x ?? d` | `x \|\| d` where `0`/`''`/`false` are valid | `\|\|` mistreats falsy-but-valid values |
| `Array.map/filter/reduce` | imperative index loops that transform | Declarative |
| `interface` for object shapes / `type` for unions & aliases | mixing arbitrarily | Consistency; `interface` merges, `type` composes |
| `import type { X }` | value import used only as a type | Erased at compile time, avoids cycles |
| `??=` / `&&=` / `?.()` | verbose equivalents | Modern, clear |

## Avoid

- **`@ts-ignore`** → use `@ts-expect-error` with a comment, or fix the type.
- **Non-null assertion `!`** scattered through code → narrow properly; `!` hides real null bugs.
- **`Function`, `Object`, `{}` as types** → they mean "almost anything"; use precise shapes.
- **Enums in `.d.ts`/library boundaries** without care → prefer literal unions for portability.

**Do not flag** correct, idiomatic code, or style the formatter owns.
