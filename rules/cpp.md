---
paths:
  - "**/*.{cpp,cc,cxx,c,h,hpp,hxx}"
---

# C++ Idioms

Language-specific best practices for modern C++ (C++17 and later). These supplement the language-agnostic principles in `coding.md` — they catch idiom violations a smell-based review misses. Flag the violation, name the preferred form.

Assume modern C++ unless the project's build config pins an older standard. If a file targets pre-C++11, skip the C++11+ items.

---

## Constants & Macros

| Prefer | Over | Why |
|--------|------|-----|
| `constexpr` / `const` | `#define` for constants | Type-safe, scoped, visible to the debugger |
| `constexpr` function | function-like macro | Type-checked, respects scope, no token-pasting surprises |
| `enum class` | unscoped `enum` or `#define` flags | Scoped, strongly typed, no implicit int conversion |
| `inline constexpr` (C++17) | `extern const` in headers | Single definition across TUs without ODR violations |

## Memory & Resources

| Prefer | Over | Why |
|--------|------|-----|
| `std::unique_ptr` / `std::shared_ptr` | raw `new`/`delete` | RAII; no leaks on early return or exception |
| `std::make_unique` / `std::make_shared` | `new` passed to a smart pointer | Exception-safe, single allocation for `shared_ptr` |
| Stack objects / RAII wrappers | manual acquire/release pairs | Release is automatic and exception-safe |
| `std::span` / `std::string_view` (C++17) | pointer + length parameter pairs | Bounds-aware, non-owning, no lifetime ambiguity |

## Types & Initialization

| Prefer | Over | Why |
|--------|------|-----|
| `nullptr` | `NULL` or `0` | Type-safe null; correct overload resolution |
| `auto` for obvious/verbose types | repeating long type names | Less noise, no narrowing on the declared type |
| Uniform/brace init `{}` | `()` where narrowing matters | Prevents silent narrowing conversions |
| `using` alias | `typedef` | Reads left-to-right, supports templates |
| `= default` / `= delete` | hand-written trivial or suppressed special members | Intent explicit; compiler generates optimal code |

## Functions & Classes

- **Rule of 0/3/5** — If a class manages a resource, declare all five special members (or none, leaning on RAII members). A class with a destructor but default copy is a red flag.
- **`override` / `final`** — Always mark overriding virtuals `override`. A virtual override missing the keyword is a bug waiting to happen.
- **`const`-correctness** — Member functions that don't mutate state should be `const`; parameters passed by reference and not modified should be `const&`.
- **Pass by value + `std::move`** for sink parameters; pass `const&` for read-only large objects; pass by value for cheap types.
- **`[[nodiscard]]`** on functions whose return value must not be ignored (factories, error codes, `empty()`).
- **`noexcept`** on move constructors/assignment and on functions that genuinely cannot throw.

## Idioms to Flag

- C-style casts `(T)x` → use `static_cast` / `reinterpret_cast` / `const_cast` (intent + searchability).
- C arrays and raw loops → `std::array` / `std::vector` and range-based `for` or `<algorithm>`.
- `printf`/manual buffers → `std::format` (C++20) or typed streams.
- Output parameters via pointer → return by value (move semantics make this cheap) or `std::optional` / `std::expected`.
- Manual index loops that map/filter/reduce → `<algorithm>` (`std::transform`, `std::ranges` in C++20).

**Do not flag** idioms that are correct for the project's pinned standard, or micro-optimizations the surrounding code style does not adopt.
