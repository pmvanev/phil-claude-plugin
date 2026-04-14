---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
---

# Refactoring Catalog

Quick reference of named refactorings from Martin Fowler's *Refactoring*. Use this as a dictionary when reviewing code — name the smell, pick the refactoring, apply it.

---

## Composing Methods

| Refactoring | When to Use |
|-------------|-------------|
| **Extract Function** | A code fragment does one identifiable thing. Give it a name. |
| **Inline Function** | The body is as clear as the name. Remove the indirection. |
| **Extract Variable** | A complex expression is hard to read. Name the parts. |
| **Inline Variable** | The variable name says no more than the expression. |
| **Change Function Declaration** | The name doesn't reveal intent, or parameters are wrong. |
| **Encapsulate Variable** | A widely accessed variable needs controlled access. |
| **Introduce Parameter Object** | Data clump appears as multiple parameters. Group into an object. |
| **Combine Functions into Class** | Several functions operate on the same data. Bundle them. |
| **Split Phase** | Code does two distinct things in sequence. Separate into phases with an intermediate data structure. |

## Moving Features

| Refactoring | When to Use |
|-------------|-------------|
| **Move Function** | A function references elements of another module more than its own. |
| **Move Field** | A field is used more by another class than its own. |
| **Move Statements into Function** | The same code appears before/after every call to a function. Fold it in. |
| **Slide Statements** | Related code is scattered. Group it together. |
| **Split Loop** | A loop does two different things. Split it so each loop does one. |
| **Replace Loop with Pipeline** | A loop transforms data. Use map/filter/reduce instead. |
| **Remove Dead Code** | Code is unreachable or unused. Delete it. |

## Simplifying Conditional Logic

| Refactoring | When to Use |
|-------------|-------------|
| **Decompose Conditional** | A complex conditional obscures intent. Extract condition and branches into named functions. |
| **Consolidate Conditional Expression** | Multiple conditions yield the same result. Combine them. |
| **Replace Nested Conditional with Guard Clauses** | Deep nesting obscures the normal path. Use early returns. |
| **Replace Conditional with Polymorphism** | A conditional switches on type. Use subclasses or strategy pattern. |
| **Introduce Special Case** | Code repeatedly checks for a special value (null, "unknown"). Create a special-case object. |
| **Introduce Assertion** | A section of code assumes something about state. Make the assumption explicit. |

## Encapsulation

| Refactoring | When to Use |
|-------------|-------------|
| **Encapsulate Record** | A raw data record is accessed directly. Wrap it in a class. |
| **Encapsulate Collection** | A getter returns a mutable collection. Return a copy or read-only view. |
| **Replace Primitive with Object** | A primitive carries domain meaning (money, phone, email). Wrap it. |
| **Replace Temp with Query** | A temp variable holds a computed value used in one place. Make it a method. |
| **Extract Class** | A class does two things. Split responsibilities into two classes. |
| **Inline Class** | A class does too little. Fold it into its caller. |
| **Hide Delegate** | Client calls `a.getB().doSomething()`. Add a method on `a` instead. |
| **Remove Middle Man** | A class delegates everything. Let the client call the delegate directly. |

## Refactoring APIs

| Refactoring | When to Use |
|-------------|-------------|
| **Separate Query from Modifier** | A function returns a value and has a side effect. Split it. |
| **Parameterize Function** | Two functions do similar things with different values. Merge with a parameter. |
| **Remove Flag Argument** | A boolean parameter selects between two behaviors. Create two functions. |
| **Preserve Whole Object** | You extract values from an object to pass as arguments. Pass the object. |
| **Replace Parameter with Query** | A parameter can be derived by the callee. Remove it. |
| **Replace Constructor with Factory Function** | Construction logic is complex or needs polymorphism. Use a factory. |

## Organizing Data

| Refactoring | When to Use |
|-------------|-------------|
| **Split Variable** | A variable is assigned more than once for different purposes. One variable per purpose. |
| **Rename Field** | The name doesn't communicate meaning. |
| **Replace Derived Variable with Query** | A variable is computed from others and can drift. Compute on demand. |
| **Change Reference to Value** | A small object is shared but should be compared by value. Make it immutable. |
| **Change Value to Reference** | Copies of data get out of sync. Share a single reference. |

## Dealing with Inheritance

| Refactoring | When to Use |
|-------------|-------------|
| **Pull Up Method/Field** | Duplicate code in sibling subclasses. Move to superclass. |
| **Push Down Method/Field** | Superclass behavior only relevant to one subclass. Move down. |
| **Extract Superclass** | Two classes share similar features. Create a common parent. |
| **Replace Subclass with Delegate** | Inheritance is used for one axis of variation. Use composition. |
| **Replace Superclass with Delegate** | Subclass only uses part of superclass interface. Delegate instead. |
| **Collapse Hierarchy** | A subclass is no different from its parent. Merge them. |

---

## Smell-to-Refactoring Map

Use this to go from observation to action:

| Smell | Primary Refactorings |
|-------|---------------------|
| **Duplicated Code** | Extract Function, Slide Statements, Pull Up Method |
| **Long Function** | Extract Function, Decompose Conditional, Replace Temp with Query, Split Phase |
| **Large Class** | Extract Class, Extract Superclass, Replace Subclass with Delegate |
| **Long Parameter List** | Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query |
| **Feature Envy** | Move Function, Extract Function |
| **Data Clumps** | Introduce Parameter Object, Extract Class |
| **Primitive Obsession** | Replace Primitive with Object, Introduce Parameter Object, Extract Class |
| **Shotgun Surgery** | Move Function, Move Field, Combine Functions into Class |
| **Divergent Change** | Extract Class, Split Phase |
| **Message Chains** | Hide Delegate, Extract Function |
| **Speculative Generality** | Collapse Hierarchy, Inline Function, Inline Class, Remove Dead Code |
| **Comments** | Extract Function, Extract Variable, Introduce Assertion |
| **Mutable Data** | Encapsulate Variable, Split Variable, Replace Derived Variable with Query |
| **Switch Statements** | Replace Conditional with Polymorphism, Introduce Special Case |
| **Dead Code** | Remove Dead Code |
