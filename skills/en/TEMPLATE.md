# Cloud Glyph Skills

## Responsibility

This skill system provides an AI Agent with a Wiki documentation authoring workflow. You must strictly follow this pipeline to produce documentation that meets the specification.

## Variable Conventions

> **Wiki_Root** — The root directory for output documents (the parent of `skills/`). The Agent may only create, modify, or delete documents under Wiki_Root.

> **Deploy_Mode** — Deployment mode:
> - `nested`: Wiki repo is a subdirectory inside a project; Agent should document the parent project (excluding the Wiki itself)
> - `standalone`: Wiki repo is used independently; Agent cannot auto-discover the project and must ask the user

> **Solution_Root** — The solution root of the project being documented
> - `nested` mode: Auto-discovered by Agent (parent of Wiki_Root)
> - `standalone` mode: Provided by the user

> **Project_List** — The list of projects being documented. In `nested` mode, exclude the Wiki repo's own projects (i.e. CloudGlyph project)

> **Language_List** — The language scope of the Wiki. The Agent should determine the user's desired languages in Step 1 via interactive tools or direct inquiry, then verify availability against `languages.json`. Unsupported languages should be recorded and reported at the end without interrupting the pipeline.

## Content Model

The Wiki uses a "directory-as-page" organization. The Agent must follow two core rules:

> **Rule 1: Directory name = navigation structure** — Each Wiki page corresponds to a directory. Directory names use `{number}_` prefix for ordering, e.g. `0_Welcome`, `01_project_structure`. The Agent must use appropriate numeric prefixes when creating directories.

> **Rule 2: Content file convention** — Each directory must have exactly one `index.md` file as the page content. Directories may contain child subdirectories for sub-pages (which also follow Rule 1).

> **Rule 3: Directory name must match the target language** — Directory names must be in the language of the content, not in English. For example, if `Language_List = ["zh"]`, use `0_欢迎` instead of `0_Welcome`, `1_快速入门` instead of `1_quickstart`, `2_API参考` instead of `2_api`, `3_架构分析` instead of `3_architecture`. Exception: Proper nouns and brand names (e.g. "VeloxDev", "MVVM", "AOP") that are universally recognized in their original form.

### Content Organization (Type-Based Decision)

The Wiki uses a "directory-as-page" organization. The Agent **must not** decide the structure based on project count alone. Instead, determine the **nature of the target** being documented:

#### Decision Rule

> **Is the target a self-contained framework, class library, or product?** (e.g. WPF, Entity Framework, VeloxDev, React, a NuGet library, a game engine, etc.)

| If... | Then... |
|---|---|
| **Yes** — it is a cohesive product/framework/library | Always use **Category** organization: `content/{lang}/{category}/` — group by **functional area** (Core, Adapters, Tools, etc.), never by individual `.csproj`. Ignore how many sub-projects it has. |
| **No** — the solution is a collection of independent apps/tools/services | **Ask the user** how to organize. Present the available options and let them decide. Do not guess. |

> **Rationale:** A framework with 40+ sub-projects is still one thing (the framework). A solution with 2 completely independent web apps is two separate things. Count alone cannot distinguish these cases.

#### Category Organization (for frameworks, libraries, products)

- Categories sit **directly under `content/{lang}/`** — no `{ProductName}/` or `{SolutionName}/` wrapper directory
- Categories are based on **functional areas** discovered in Module Discovery, not on individual project names
- Create 2-8 category directories based on the module discovery results
- Each category has a `0_quickstart/`, `1_api/`, `2_architecture/` sub-structure as needed
- **Important:** Do NOT create a `{Project}/` or `{Product}/` wrapper directory. Example: `content/zh/1_Core/0_quickstart/` is correct; `content/zh/VeloxDev/1_Core/0_quickstart/` is wrong.

```
# Example: Category organization (framework / library / product)
content/en/
├── 0_Welcome/
│   └── index.md
├── 1_Core/
│   ├── 0_quickstart/
│   │   └── index.md
│   ├── 1_api/
│   │   └── index.md
│   └── 2_architecture/
│       └── index.md
├── 2_Adapters/
│   ├── 0_quickstart/
│   │   └── index.md
│   └── 1_api/
│       └── index.md
├── 3_Generator/
│   ├── 0_quickstart/
│   │   └── index.md
│   └── 1_api/
│       └── index.md
├── 4_Templates/
│   └── 0_quickstart/
│       └── index.md
├── 5_Examples/
│   └── 0_quickstart/
│       └── index.md
└── 6_copyright/
	└── index.md
```

#### Per-Project Organization (only when user explicitly chooses this)

If the user opts for per-project structure (e.g. a solution containing multiple independent apps):

```
content/en/
├── 0_Welcome/
│   └── index.md
├── 1_MyApp/
│   ├── 0_quickstart/
│   │   ├── index.md
│   │   ├── 01_getting-started/
│   │   │   └── index.md
│   │   └── 02_advanced-usage/
│   │       └── index.md
│   ├── 1_api/
│   │   ├── index.md
│   │   ├── Controllers/
│   │   │   └── index.md
│   │   └── Services/
│   │       └── index.md
│   └── 2_architecture/
│       ├── index.md
│       ├── 01_project_structure/
│       │   └── index.md
│       └── 02_class_hierarchy/
│           └── index.md
├── 2_MyLib/
│   ├── 0_quickstart/
│   │   ├── index.md
│   │   └── 01_getting-started/
│   │       └── index.md
│   └── 1_api/
│       ├── index.md
│       └── Services/
│           └── index.md
└── 3_copyright/
	└── index.md
```
```

## Code Authenticity Priority (CRITICAL)

Every code snippet in Wiki documentation **must** come from a real source. The Agent must follow this strict priority hierarchy when discovering API usage examples:

> **Priority 1 (Highest) — Demo/Example projects**
> Scan `Examples/` or `samples/` directories for real-world usage. These show the intended top-level API surface and the most idiomatic patterns.
> 
> **Priority 2 — Unit Tests**
> Extract usage patterns from test files (e.g. `*Test*.cs`, `*Spec*.cs`). Tests exercise real APIs with real parameters and edge cases.
>
> **Priority 3 (Fallback) — Source code self-discovery**
> Only when no Demo or Test exists for a module: read the source code interfaces, extract method signatures, and construct minimal usage examples. These must be explicitly marked as *inferred* if not verified against an actual call site.
>
> **Rule:** If a code block contains a class name, method name, or API call that does not exist in the codebase, it is a **fabrication** and must be fixed before the Review step. The Agent must verify every referenced symbol by searching the actual source files.

## Code Styling

The SKILL system imposes **no requirements** on code indentation or formatting style in documentation code blocks. The Agent should follow the indentation style already present in the project's own source files (tabs, spaces, etc.), or use whichever produces readable, consistent output.

## Workflow

> 0.Start

> 1.Deploy mode detection and variable confirmation

> 2.Tech stack analysis

> 3.Constraint loading

> 4.Module discovery

### Content Writing Phase (Steps 5-8)

Pages are written in **reader consumption order**: Quick Start → APIs → Architecture → Copyright. This order ensures that earlier pages can reference later ones where appropriate.

#### ⚡ Per-Module Micro-Loop (Steps 5→6→7)

When `Project_List` contains **multiple modules**, Steps 5→6→7 execute as a **micro-loop per module**, not as three batch passes across all modules. This prevents context overload and ensures each module's API and analysis chapters benefit from the module-specific Quick Start written just before them.

**Correct pattern — per-module micro-loop:**
```
For Module A:
  5.Write【Quick Start for Module A】
  6.Write【APIs for Module A】
  7.Write【SE Analysis for Module A】
For Module B:
  5.Write【Quick Start for Module B】
  6.Write【APIs for Module B】
  7.Write【SE Analysis for Module B】
... (repeat for each module)
Then 8.Write【Copyright】 (global, one pass)
```

**Wrong pattern — batch per step (do NOT do this):**
```
5.Write【Quick Start for ALL modules】   ← Token explosion, context loss
6.Write【APIs for ALL modules】
7.Write【SE Analysis for ALL modules】
```

For **single-project** tier (only 1 module), the micro-loop collapses naturally to one iteration; treat it the same way.

> 5.Write【Quick Start】— `{category}/0_quickstart/` (index.md with getting-started code samples)

> 6.Write【APIs】— `{category}/1_api/` (full API reference documentation)

> 7.Write【Software Engineering Analysis】— `{category}/2_architecture/` (architecture, class diagrams, sequences)

> 8.Write【Copyright】— `{category}/3_copyright/` (license and attribution)

### Polish & Publish (Steps 9-11)

> 9.Write【Welcome】— `0_Welcome/` (or `0_欢迎/` for zh). Execute after all content pages exist but before Review. Welcome is the first navigation entry but the **last page written** because it summarizes all other pages.

> 10.Review — Full per-page audit including: code authenticity verification, diagram syntax check, navigation index regeneration (`python gen_tree.py`), and project build (`dotnet build`)

> 11.End

### Workflow Continuity

The workflow must **never silently stop** due to tool-call limits, token limits, timeouts, or any other infrastructure constraint. If the Agent reaches an execution limit or encounters a discontinuity:

1. **Do not fabricate results** to simulate completion
2. **Record observation** of where the workflow stopped and what has been done
3. **Ask the user** whether to continue, providing the current progress summary and estimated remaining work
4. Resume from the recorded checkpoint upon user confirmation

This rule applies to all phases: Module Discovery, Content Writing, and Review. A partial output is acceptable only if the user explicitly agrees to terminate early.

## Skill Index

<!-- SKILL_INDEX -->
