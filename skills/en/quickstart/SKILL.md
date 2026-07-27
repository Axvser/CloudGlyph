# Quick Start

## Responsibility

Write a self-contained runnable tutorial for each feature module, using top-level APIs to build a real working example.

## Writing Principles

### Runnable and Complete

The goal of Quick Start is not minimal code snippets, but guiding the reader from zero to a **truly runnable** project or feature. Each Quick Start should:

- **Have a clear start and end** — begin with project setup/dependency installation, end with verifying the feature works
- **Be replicable** — the reader can follow step by step and get a working program
- **Be practical** — solve a real business scenario or functional need

### Top-Level API First

Use the module's highest-level API (attributes, extension methods, Fluent API, base classes) to show **what it looks like to use**, not **how it's implemented internally**. Low-level interface implementation and manual patterns belong in the API reference.

### Source Discovery (Priority)

> **Priority 1 — Demo/Example projects**
> Search the module's `Examples/` or `samples/` directory, **read all source files in full**. Demo projects are natural Quick Start material — extract their core flow and organize into a step-by-step tutorial.
>
> **Priority 2 — Unit Tests**
> If no Demo exists for a module, **read all test files in full**, extract typical usage flows and compose them into a coherent example.
>
> **Priority 3 (Fallback) — Source code interfaces**
> Only when both Demo and Tests are absent: understand the module's intent from source code and construct a reasonable example. Mark these as *inferred*.

### Structure

```
# {Feature Name}

## Quick Start

### 1. Install / Add Dependency

How to install NuGet package / npm package / module etc.

### 2. Basic Setup / Registration

Register services, create instances, configure settings, etc.

### 3. Core Usage (Step by Step)

Combine top-level APIs step by step, from simple to complete, each with runnable code

### 4. Verification

How to run and verify the feature works (expected output, UI effect, etc.)

### 5. Complete Code

Provide the final complete code files for reference
```

### Output Location

```
content/{lang}/{category}/0_QuickStart/
├── index.md                    ← Overview
├── 0_{FeatureA}/
│   └── index.md
├── 1_{FeatureB}/
│   └── index.md
└── ...
```

## Post-Write Action

After writing Quick Start content:

- [ ] **Regenerate navigation index** — Run the tree generator script (e.g. `python gen_tree.py`) to rebuild tree.json
- [ ] **Build the project** — Run `dotnet build` to verify the new content embeds correctly
