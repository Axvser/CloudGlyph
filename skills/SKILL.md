# Cloud Glyph Skills

## Responsibility

Strictly follow the workflow defined in this SKILL to produce Wiki documentation that meets specifications

## Variable Conventions

> CloudGlyph_Git:[https://github.com/Axvser/CloudGlyph][ReadOnly][Template Repository] - Cloud Glyph repository address

> CloudGlyph_Child_Git:[request] - Local Wiki repository root. This Wiki repository is an independent repo created from the Cloud Glyph:[Template Repository]. It is not counted in Wiki analysis or writing.

> Project_Root:[request] - Root directory of the project to be documented

> MainSKILL_Path:[CloudGlyph_Child_Git/skills/SKILL.md] - Path to the current skill

> Wiki_Root:[CloudGlyph_Child_Git/src/CloudGlyph/Assets/Docs/content/{languages}/] - Root directory for output documentation, dynamically divided by language.

> LanguageMap_List:[CloudGlyph_Child_Git/src/CloudGlyph/Assets/Docs/config/languages.json] - Range of languages supported by the Wiki

> LanguageTargets_List:[request] - Range of languages the user wants the Wiki to support

## Structure Conventions

⚙ {ID}_{PageName}/ - Folder naming convention when producing Markdown. The tree structure formed by folders is the directory structure the final App renders for the Wiki.

⚙ index.md - Each {ID}_{PageName}/ must have exactly one fixed-name index.md file, otherwise the directory structure will be incomplete. md files may be left blank. More subdirectories can be added to represent sub-items.

⚙ Every directory in the output path MUST contain an index.md — this includes intermediate/parent directories, not just leaf directories. After creating any new subdirectory, immediately verify an index.md exists in every ancestor directory of that path. A common mistake is to create e.g. `2_design_patterns/0_Workflow/index.md` while forgetting `2_design_patterns/index.md`.

Ultimately, the directory will present the following structure. These are five fixed dimensions, and /.../ means you may extend sub-items and add content based on specific functional divisions under the dimension, with no depth limit.

> Wiki_Root/0_Welcome/

> Wiki_Root/1_QuickStart/.../

> Wiki_Root/2_API/.../

> Wiki_Root/3_SE_Analysis/.../

> Wiki_Root/4_Copyright/.../

## Code Style Conventions

⚙ Before writing code blocks in Wiki output, scan source files under 【Project_Root】 to detect the dominant indentation style (tabs vs spaces + width). Generated code blocks MUST match that style. When detection is ambiguous, default to **4 spaces** for .NET/C# projects.

⚙ When extracting code snippets from source files (Demo / Test / source), preserve their original whitespace style — do not convert tabs to spaces or vice versa.

## Accessibility Conventions

⚙ Respect content explicitly marked as non-public in the source code; avoid exposing such content in the Wiki

⚙ Avoid exposing sensitive information in the Wiki, such as passwords, keys, personal information, etc.

## Workflow

> 0.Begin

> 1.Variable Confirmation

> 2.Module Discovery

> 3.Write【QuickStart】

> 4.Write【API Reference】

> 5.Write【SE Analysis】

> 6.Write【Copyright】

> 7.Write【Welcome】

> 8.Review

> 9.End

## Skill Index

Sub-skills are organized into independent directories by scenario. The Agent should only load a sub-skill's `SKILL.md` when the user's request matches the corresponding scenario — do not pre-load.

### Foundation Setup

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/en/context-setup/SKILL.md` | Confirm context | Variable conventions, Tech stack, User SKILL, Target language support, Project root |

### Content Writing

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/en/api-docs/SKILL.md` | API Reference — Full enumeration of interfaces, types, and functions | Extract API from test code, Generate API documentation, Create API reference from tests, Document public APIs |
| `skills/en/copyright/SKILL.md` | Write copyright-related information | Write【Copyright】 |
| `skills/en/module-discovery/SKILL.md` | Discover all functional modules | Discover modules in solution, Analyze project dependencies, Identify module responsibility boundaries, Map inter-module call relationships |
| `skills/en/quickstart/SKILL.md` | Quick Start — Complete runnable tutorial | Write quick start tutorial, Create getting started guide, Write walkthrough for beginners, Write complete example |
| `skills/en/se-analysis/SKILL.md` | Software engineering analysis — architecture, class diagrams, sequences, API flow | Perform software engineering analysis, Draw architecture diagram, Analyze source code flow, Create class hierarchy document, Document request lifecycle |
| `skills/en/welcome-page/SKILL.md` | Create welcome page from template | Write【Welcome】 |

### Quality Assurance

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/en/review/SKILL.md` | Wiki content review and improvement | Review, Quality, Authenticity, Directory structure, Compatibility |

