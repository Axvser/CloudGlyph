#!/usr/bin/env python3
"""Generate skills/SKILL.md — master agent skill index.

Scans the skills/ directory for all first-level subdirectories containing
SKILL.md, reads their metadata, and auto-generates the Sub-Skill Directory
Index table (Section 2). Sections 1, 3, and 4 are hardcoded as literal
templates, ensuring they remain stable across regenerations.

How to add a new sub-skill:
  1. Create skills/<name>/SKILL.md with a `# Title` and `## When to Load`
  2. (Optional) Add the directory name to CATEGORIES below to place it in
     a specific category group; otherwise it appears under "Other".
  3. Run: python skills/generate_skill_index.py
  4. The index table in skills/SKILL.md will update automatically.
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# Categories: map directory name -> (heading, display order)
# ---------------------------------------------------------------------------
CATEGORIES: dict[str, dict] = {
    # Core Analysis
    "repo-reading":  {"category": "Core Analysis", "order": 10, "scenario": "External repo reading strategy & understanding"},
    "api-docs":      {"category": "Core Analysis", "order": 20, "scenario": "API best-practice discovery from test code → technical docs"},
    "se-analysis":   {"category": "Core Analysis", "order": 30, "scenario": "Software engineering: architecture, class diagrams, sequences, API flows"},
    # Document Creation
    "tutorial":      {"category": "Document Creation", "order": 100, "scenario": "Step-by-step tutorials and getting-started guides"},
    "migration":     {"category": "Document Creation", "order": 110, "scenario": "Migration guides and version upgrade documentation"},
    "comparison":    {"category": "Document Creation", "order": 120, "scenario": "Technology comparison and evaluation documentation"},
    # Operations & Community
    "faq":           {"category": "Operations & Community", "order": 200, "scenario": "FAQ, common issues, and troubleshooting"},
    "contribution":  {"category": "Operations & Community", "order": 210, "scenario": "Contribution guides and community collaboration docs"},
    "adr":           {"category": "Operations & Community", "order": 220, "scenario": "Architecture Decision Records (ADR) and meeting notes"},
    # Quality Assurance
    "review":        {"category": "Quality Assurance", "order": 300, "scenario": "Wiki content review and quality checks"},
    "translation":   {"category": "Quality Assurance", "order": 310, "scenario": "Cross-language document translation and adaptation"},
    "generation":    {"category": "Quality Assurance", "order": 320, "scenario": "Automated Wiki content generation from data or code"},
}

SKILLS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT     = os.path.join(SKILLS_DIR, "SKILL.md")


# ===================================================================
# Hardcoded front-matter (Sections 1, 3, 4 + Section 2 intro)
# ===================================================================
HEADER = """# Cloud Glyph — Agent Skill Index

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
"""

FOOTER = """

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
"""


# ===================================================================
# Utility helpers
# ===================================================================

def discover_sub_skills(skills_dir: str) -> list[str]:
    """Return sorted list of directory names under skills_dir that contain SKILL.md."""
    dirs = []
    for entry in sorted(os.listdir(skills_dir)):
        full = os.path.join(skills_dir, entry)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "SKILL.md")):
            dirs.append(entry)
    return dirs


def read_title(skill_md: str) -> str:
    """Extract the first `# Title` from a SKILL.md file."""
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^#\s+(.+)", line)
                if m:
                    return m.group(1).strip()
    except OSError:
        pass
    return "Untitled"


def read_keywords(skill_md: str) -> str:
    """Extract trigger keywords from the sub-skill."""
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return ""

    # Look for sections that list trigger scenarios: "When to Load", "Applicability"
    section_names = r"(?:When to Load|Applicability)"

    # Try to find one of these sections
    m = re.search(
        rf"##\s+{section_names}\s*\n(.*?)(?:\n##\s|\Z)",
        text,
        re.DOTALL,
    )
    if not m:
        # Fallback: look for quoted phrases anywhere in the document
        quoted = re.findall(r'"([^"]*)"', text)
        if quoted:
            return ", ".join(quoted[:5])
        return ""

    block = m.group(1).strip()
    # Collect quoted strings first
    keywords = re.findall(r'"([^"]*)"', block)
    if keywords:
        return ", ".join(keywords[:5])

    # Fallback: pick first bullet items
    bullets = []
    for line in block.splitlines():
        line = line.strip().lstrip("- *")
        if line and not line.startswith("#"):
            bullets.append(line)
    return ", ".join(bullets[:5])


def get_scenario(dir_name: str) -> str:
    """Return the scenario description for a given sub-skill directory name."""
    entry = CATEGORIES.get(dir_name)
    if entry:
        return entry["scenario"]
    return dir_name.replace("-", " ").title()


# ===================================================================
# Index table generation
# ===================================================================

def build_category_tables(dirs: list[str]) -> str:
    """Group discovered sub-skills by category and produce markdown tables."""
    # Collect entries
    entries: list[tuple[str, str, str, str]] = []  # (category_name, dir_name, scenario, keywords)

    for d in dirs:
        skill_path = os.path.join(SKILLS_DIR, d, "SKILL.md")
        info = CATEGORIES.get(d)
        cat_name = info["category"] if info else "Other"
        scenario = get_scenario(d)
        keywords = read_keywords(skill_path)
        entries.append((cat_name, d, scenario, keywords))

    # Sort by category order, then directory name
    def sort_key(e):
        info = CATEGORIES.get(e[1])
        cat_order = info["order"] if info else 999
        return (cat_order, e[1])

    entries.sort(key=sort_key)

    # Group by category
    groups: dict[str, list[tuple[str, str, str]]] = {}
    for cat_name, d, scenario, keywords in entries:
        groups.setdefault(cat_name, []).append((d, scenario, keywords))

    # Render
    parts = []
    for cat_name in [
        "Core Analysis",
        "Document Creation",
        "Operations & Community",
        "Quality Assurance",
        "Other",
    ]:
        if cat_name not in groups:
            continue
        parts.append(f"### {cat_name}\n")
        parts.append("| Path | Scenario | Trigger Keywords |")
        parts.append("|---|---|---|")
        for d, scenario, keywords in groups[cat_name]:
            path = f"`skills/{d}/SKILL.md`"
            kw = keywords if keywords else "(see sub-skill for details)"
            scenario = scenario.replace("|", "\\|") if scenario else "—"
            parts.append(f"| {path} | {scenario} | {kw} |")
        parts.append("")

    return "\n".join(parts)


# ===================================================================
# Main
# ===================================================================

def main() -> int:
    dirs = discover_sub_skills(SKILLS_DIR)
    if not dirs:
        print("No sub-skill directories found under", SKILLS_DIR)
        return 1

    table = build_category_tables(dirs)
    content = HEADER.strip() + "\n\n" + table.strip() + "\n" + FOOTER.strip() + "\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

    count = len(dirs)
    print(f"✅ Regenerated {OUTPUT}")
    print(f"   Found {count} sub-skill{'s' if count > 1 else ''}: {', '.join(dirs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
