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

### Single Project vs Multi Project

- **If documenting a single project** (Project_List has one entry), content goes directly under `content/{lang}/`, no extra project-level directory needed
- **If documenting multiple projects** (Project_List has multiple entries), each project needs a directory layer to isolate content, e.g. `1_MyApp/`, `2_MyLib/`

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

# Multi project example
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

> 5.Write【Welcome】

> 6.Write【Quick Start】

> 7.Write【APIs】

> 8.Write【Software Engineering Analysis】

> 9.Write【Copyright】

> 10.Review

> 11.End

## Skill Index

<!-- SKILL_INDEX -->
