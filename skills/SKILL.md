# Cloud Glyph — Agent Skill Index

> **Entry point.** This file is the root index of the agent's skill system.
> The agent MUST read this file first to understand the Wiki content
> authoring model, then load sub-skill files by scenario as needed.
>
> **If the user does not specify an execution path, the agent MUST follow
> the Default Execution Path (Section 3) automatically.**
>
> *Auto-generated — do not edit manually. Rerun `python skills/generate_skill_index.py` to regenerate.*

---

## 1. Wiki Content Authoring Model

The agent writes Wiki pages for Cloud Glyph by working with flat files under
`src/CloudGlyph/Assets/Docs/content/`.

### Directory as Node, One `index.md` Per Page

```
content/en/2_Architecture/overview/index.md   →  tree node "Architecture" > "overview"
content/en/2_Architecture/deployment/index.md  →  tree node "Architecture" > "deployment"
```

- **Directory name** is the URL-safe path key.
- **Numeric prefix** (`1_`, `2_`, `2.5_`) controls sort order; it is **stripped** from the displayed title.
- The prefix-stripped directory name becomes the **page title** (e.g. `2_Architecture` → `"Architecture"`).
- A directory containing `index.md` becomes a **tree node**; subdirectories become **children**.
- Encoding: **UTF-8** (required for multi-language).

### Supported Wiki Content Syntax

Based on **AvalonMarkdown v4.0.0** (`markdown-it 14` + `highlight.js 11` + `KaTeX 0.16` + `Mermaid 11` + `plantuml-encoder`), the following syntax is fully supported:

| Category | Syntax / Description |
|---|---|
| **Standard Markdown** | Headings `#`, bold `**`, italic `*`, links `[text](url)`, images `![alt](src)`, lists, blockquotes `>`, horizontal rules `---`, tables, strikethrough `~~text~~` |
| **Math Formulas** | Inline `$E = mc^2$`, block `$$...$$` (KaTeX rendered) |
| **Code Highlighting** | `` ```lang ... ``` `` where `lang` is any highlight.js supported language (VS Code-style theme) |
| **Mermaid Diagrams** | `` ```mermaid ... ``` `` supports: flowchart, sequence, pie, git, class diagrams |
| **PlantUML** | `` ```plantuml ... ``` `` auto-encoded and rendered via PlantUML online service (SVG output, dark/light aware) |
| **Task Lists** | `- [x] done` / `- [ ] todo` (custom styled checkboxes) |
| **Footnotes** | `text[^1]` followed by `[^1]: detail` |
| **Video Embeds** | Direct video files (`.mp4`/`.webm`/`.ogg`/`.mov`/`.avi`/`.mkv`); auto-detected embeds for YouTube, Bilibili, Vimeo |
| **HTML + CSS** | Full inline HTML support including `<style>`, `<div>`, `<span>`, and `@keyframes` animations |
| **Preview Config** | Dynamically adjustable: font size, line height, code language labels, copy button toggle, max code block height |

### Diagram Validation (Mandatory)

Every Mermaid or PlantUML diagram **must** be validated for syntax correctness before the document is committed. Diagrams with syntax errors break rendering for all readers.

| Validation Rule | Mermaid | PlantUML |
|---|---|---|
| **Direction & type** | Verify `flowchart`/`sequenceDiagram`/`classDiagram`/`pie`/`git` is correct for the content | Verify `@startuml`/`@enduml` markers are present and balanced |
| **Arrow syntax** | `->>`/`-->>`/`-x`/`--)` match standard Mermaid arrow rules | `->`/`-->`/`-down->`/`-right->` follow PlantUML arrow convention |
| **Node/participant labels** | All participants referenced in arrows must be declared | All participants must be declared before use |
| **Bracket/brace balance** | `{}` `[]` `()` are properly paired — no unclosed blocks | `{}` `[]` `()` are properly paired — no unclosed blocks |
| **Keyword casing** | Mermaid keywords (`participant`, `loop`, `alt`, `opt`, `rect`) are lowercase | PlantUML keywords (`participant`, `actor`, `boundary`, `note`, `alt`) are lowercase |
| **Indentation** | Block structures (`loop`/`alt`/`opt`) have consistent indentation to mark scope | Block structures (`alt`/`else`/`group`/`loop`) have consistent indentation |
| **No ambiguous characters** | Avoid unescaped `"` `(` `)` `[` `]` inside labels — use `()` or `[]` wrapping consistently | Avoid special characters in labels without proper escaping |

**Before writing a diagram**, the agent MUST mentally trace the diagram logic to ensure all connections are valid. **After writing**, the agent MUST re-read the code block as if parsing it and confirm every rule above passes.

### Multi-Language

- Language config source file: `config/languages.json`
- To add a language, create `content/{code}/` with at least one `index.md`
- **Never manually edit** `content/languages_index.json` or `content/*/tree.json` (build-generated, listed in `.gitignore`)

### Reference

For the full project structure, startup flow, and theme mechanism, see the root [`SKILL.md`](../SKILL.md).

---

## 2. Sub-Skill Directory Index

Sub-skills are organized into independent directories by scenario. The agent MUST
**only read a sub-skill's `SKILL.md` when the user's request matches that
scenario** — never pre-load them.

### Core Analysis

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/repo-reading/SKILL.md` | External repo reading strategy & understanding | Analyze this repo, Understand the project structure, Where is the entry point, What does this project do, How is this project organized |
| `skills/api-docs/SKILL.md` | API best-practice discovery from test code → technical docs | Write API docs from tests, Extract API documentation from test code, Generate API reference from test cases, Document public API based on tests |
| `skills/se-analysis/SKILL.md` | Software engineering: architecture, class diagrams, sequences, API flows | Software engineering analysis, Draw architecture diagram, Analyze source code flow, Create class hierarchy documentation, Document request lifecycle |

### Document Creation

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/tutorial/SKILL.md` | Step-by-step tutorials and getting-started guides | Write a quickstart tutorial, Create a getting started guide, Write a walkthrough for beginners, Write a from-scratch example |
| `skills/migration/SKILL.md` | Migration guides and version upgrade documentation | Migrate from .NET Framework to .NET 8, Upgrade guide for the latest version, Breaking changes documentation, Migrate from library A to library B |
| `skills/comparison/SKILL.md` | Technology comparison and evaluation documentation | Compare framework A and framework B, Technology selection evaluation, X vs Y comparison, What are the pros and cons of this approach |

### Operations & Community

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/faq/SKILL.md` | FAQ, common issues, and troubleshooting | Compile an FAQ, Write a troubleshooting guide, Troubleshooting documentation, Extract FAQ from Issues |
| `skills/contribution/SKILL.md` | Contribution guides and community collaboration docs | Write CONTRIBUTING.md, Create a contribution guide, How to contribute to this project, Explain the PR workflow |
| `skills/adr/SKILL.md` | Architecture Decision Records (ADR) and meeting notes | Record an architecture decision, Write an ADR, Organize meeting notes, Decision log |

### Quality Assurance

| Path | Scenario | Trigger Keywords |
|---|---|---|
| `skills/review/SKILL.md` | Wiki content review and quality checks | Review documentation quality, Check for broken links, Audit Wiki content, Validate documentation structure, Ensure rendering compatibility |
| `skills/translation/SKILL.md` | Cross-language document translation and adaptation | Translate to Chinese, Create Japanese version, Add bilingual support, Translate documentation to another language |
| `skills/generation/SKILL.md` | Automated Wiki content generation from data or code | Generate API reference, Create changelog from Git, Build glossary from data file, Generate configuration reference, Auto-generate documentation from source |
---

## 3. Default Execution Path

**When the user does not explicitly specify how to proceed** (e.g., the user
simply says "write a Wiki for this repo" without further instructions), the
agent MUST follow the default path below. Each phase auto-advances to the next
upon completion.

### Path Overview

```
Phase 1: Repo Reading     →  Phase 2: API Docs       →  Phase 3: SE Analysis
(understand the repo)       (extract API best practices)  (software engineering analysis)
                                                           ↓
                                                      Phase 4: Translation
                                                      (bilingual output alignment)
                                                           ↓
                                                      Phase 5: Review
                                                      (final quality gate)
```

### Phase Details

| Phase | Sub-Skill Loaded | Output | Delivery Location |
|---|---|---|---|
| **Phase 1** | `repo-reading/SKILL.md` | Repo structure notes, module identification, entry points | Intermediate — not written directly to Wiki |
| **Phase 2** | `api-docs/SKILL.md` | Public API reference docs (parameter tables, examples, edge cases) | `content/en/{Project}/api/` and `content/zh/{Project}/api/` |
| **Phase 3** | `se-analysis/SKILL.md` | Architecture overview, class diagrams, sequences, flow analysis | `content/en/{Project}/architecture/` and `content/zh/{Project}/architecture/` |
| **Phase 4** | `translation/SKILL.md` | Ensure bilingual output from phases 2 & 3 is consistent | Fill missing translations, align terminology |
| **Phase 5** | `review/SKILL.md` | Final quality gate: validate diagrams, verify all API references exist in the target repo, check links and structure | Audit report + corrections applied to all written pages |

### Conventions

1. **Read before write** — Phase 1 is read-only, producing structured notes for downstream phases
2. **Phase-by-phase** — Complete one phase before entering the next; no parallelism
3. **Bilingual by default** — Phases 2 and 3 write to both `en/` and `zh/` directories simultaneously
4. **Mirrored structure** — English and Chinese directory structures are symmetric mirrors
5. **Final quality gate** — Phase 5 audits all pages written in phases 2-4 before delivery

### Applicability

| User says | Follows default path? |
|---|---|
| "Write a Wiki for this repo" | ✅ Yes (all 5 phases) |
| "Analyze this repo and generate docs" | ✅ Yes (all 5 phases) |
| "Create Wiki pages for project X" | ✅ Yes (all 5 phases) |
| "Write API docs for this repo" | ❌ No — Phase 2 only |
| "Draw an architecture diagram" | ❌ No — Phase 3 only |
| "Review existing Wiki quality" | ❌ No — Phase 5 only |

---

## 4. Usage Rules

1. Always start from **this file** to understand the Wiki content authoring model and available rendering capabilities
2. Determine the scenario from the user's request:
   - User did NOT specify an execution strategy → **follow the Default Execution Path (Section 3)**
   - User specified a specific scenario → load only the corresponding sub-skill
3. When executing the default path, **notify the user** of the current phase and the next planned phase after each completion
4. After completing the task, **do NOT retain** sub-skill context for unrelated future tasks
5. New scenarios can be added at any time by creating a new sub-directory and updating this index
