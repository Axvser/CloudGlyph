# Review

## Responsibility

Systematically review **all** generated Wiki content to ensure quality, accuracy, and consistency. This is a **full audit** of every page, every code sample, and every diagram — not a spot check. Only pass the quality gate when every checklist item is marked ✅.

## Checklist

### Module Coverage Audit

- [ ] Cross-reference **every entry** in the module list from Phase 3; verify every module has been documented
- [ ] Immediately fill any missing modules

---

### Code Authenticity Verification (CRITICAL — Full Per-Page Audit)

For **every page** in the Wiki, extract all code blocks containing API references. For each reference:

- [ ] **Class/method names** — search the codebase to confirm each type and member exists **with the documented signature**
- [ ] **Namespace/module paths** — verify they match the actual project structure (e.g. `global::VeloxDev.MVVM` not `VeloxDev.MVVM.Abstractions`)
- [ ] **Method parameters and return types** — cross-check against the source declaration; document must match reality
- [ ] **Exception declarations** — if the doc lists thrown exceptions, confirm they exist in the method signature or XML comments
- [ ] **Property/field names** — every property or field referenced must be present on the declared type
- [ ] **Removed/deprecated APIs** — flag any doc references to `[Obsolete]` or removed members for correction
- [ ] **No fabricated code** — every code block must trace back to a real source file

---

### Diagram Syntax Validation

- [ ] **Mermaid** — direction/type valid, participants declared, brackets balanced, arrows correct
- [ ] **KaTeX** — all `$...$` and `$$...$$` inline/block pairs are balanced, no mismatched delimiters
- [ ] **PlantUML** — `@startuml` / `@enduml` paired, participants declared before use, `activate`/`deactivate` paired, `alt`/`else`/`end` structure correct

---

### Structural Consistency

- [ ] Numeric prefixes follow conventions (e.g. `01_`, `02_`)
- [ ] `index.md` exists in **every** page directory (root and sub-pages)
- [ ] No local Markdown links (`[text](local/path/)`) — use relative navigation via the tree instead
- [ ] Page titles and hierarchy are clear and navigable

---

### Cross-language Parity

- [ ] If multi-language is enabled, **every** page exists in **all** selected languages
- [ ] No missing or outdated pages across language versions

---

### Navigation Index Verification

- [ ] **Regenerate tree.json** — Run the tree generator script (e.g. `python gen_tree.py`) to rebuild the navigation index from the current directory structure
- [ ] **Verify tree output** — Confirm the regenerated tree.json includes **all** new pages with correct nesting
- [ ] **Build the project** — Run `dotnet build` to verify the application compiles and all assets (including new content) are embedded as AvaloniaResource

---

## Pre-Commit Verification Flow

1. For **every page** in the Wiki, extract all code blocks containing API references
2. For each reference, use the repo-reading notes from Phase 1 or perform **targeted symbol searches** to confirm existence
3. If an API reference cannot be verified, **fix the doc to match reality** or remove the reference
4. Re-check diagram syntax (Mermaid/PlantUML) after any content corrections
5. Regenerate navigation index (`gen_tree.py`)
6. Build the project (`dotnet build`)
7. Only after all items are ✅, mark the quality gate as passed
