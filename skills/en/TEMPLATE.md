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

### Content Organization (3-Tier)

The Wiki uses a "directory-as-page" organization. The Agent determines the tier based on the number of entries in Project_List:

| Tier | Scenario | Structure | When |
|---|---|---|---|
| **Single** | One project | `content/{lang}/` — content goes directly under language root | `Project_List` has **1 entry** |
| **Multi** | 2-5 projects | `content/{lang}/{project}/` — each project gets its own directory | `Project_List` has **2-5 entries** |
| **Framework / Monorepo** | 6+ projects | `content/{lang}/{category}/` — group by **functional category**, not by individual project | `Project_List` has **6+ entries** |

**Framework / Monorepo tier rules:**
- Categories are based on **functional areas** (e.g. Core, Adapters, Generator, Templates, Examples), not on individual project names
- Create 2-8 category directories based on the module discovery results
- Each category has a `0_quickstart/`, `1_api/`, `2_architecture/` sub-structure as needed
- This prevents overwhelming navigation with 40+ individual project entries

```
# Example: Framework / Monorepo (40+ projects)
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

```
# Single project example
content/en/
├── 0_Welcome/
│   └── index.md              ← Welcome page (no sub-pages)
├── 1_quickstart/
│   ├── index.md              ← Quick start overview
│   ├── 01_getting-started/
│   │   └── index.md          ← Sub-page
│   └── 02_advanced-usage/
│       └── index.md          ← Sub-page
├── 2_api/
│   ├── index.md              ← API overview
│   ├── Controllers/
│   │   └── index.md          ← Sub-page
│   └── Services/
│       └── index.md          ← Sub-page
├── 3_architecture/
│   ├── index.md              ← Architecture overview
│   ├── 01_project_structure/
│   │   └── index.md          ← Sub-page
│   ├── 02_class_hierarchy/
│   │   └── index.md          ← Sub-page
│   └── 03_request_lifecycle/
│       └── index.md          ← Sub-page
└── 4_copyright/
	└── index.md              ← Copyright (no sub-pages)

# Multi project example (2-5 projects)
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

## Workflow

> 0.Start

> 1.Deploy mode detection and variable confirmation

> 2.Tech stack analysis

> 3.Constraint loading

> 4.Module discovery

### Content Writing Phase (Steps 5-8)

Pages are written in **reader consumption order**: Quick Start (first read) → APIs → Architecture → Copyright (last read). This order ensures that earlier pages can reference later ones where appropriate.

> 5.Write【Quick Start】— `{category}/0_quickstart/` (index.md with getting-started code samples)

> 6.Write【APIs】— `{category}/1_api/` (full API reference documentation)

> 7.Write【Software Engineering Analysis】— `{category}/2_architecture/` (architecture, class diagrams, sequences)

> 8.Write【Copyright】— `{category}/3_copyright/` (license and attribution)

### Polish & Publish (Steps 9-11)

> 9.Write【Welcome】— `0_Welcome/` (or `0_欢迎/` for zh). Execute after all content pages exist but before Review. Welcome is the first navigation entry but the **last page written** because it summarizes all other pages.

> 10.Review — Full per-page audit including: code authenticity verification, diagram syntax check, navigation index regeneration (`python gen_tree.py`), and project build (`dotnet build`)

> 11.End

## Skill Index

<!-- SKILL_INDEX -->
