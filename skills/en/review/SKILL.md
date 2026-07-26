# Review

## Responsibility

Systematically review all generated Wiki content to ensure quality, accuracy, and consistency.

## Checklist

### Module Coverage Audit

- [ ] Cross-reference against the module list; verify all modules have been documented
- [ ] Immediate补写 missing modules

### Code Authenticity Verification

- [ ] Every method name, parameter name, and type in code blocks confirmed to exist in actual source code
- [ ] No fabricated code

### Diagram Syntax Validation

- [ ] Mermaid: direction/type valid, participants declared, brackets balanced
- [ ] KaTeX: `$...$` and `$$...$$` pairs balanced
- [ ] PlantUML: `@startuml`/`@enduml` paired, participants declared

### Structural Consistency

- [ ] Numeric prefixes correct (e.g. `01_`, `02_`)
- [ ] `index.md` exists in every directory
- [ ] No local Markdown links (`[text](local/path/)`)

### Cross-language Parity

- [ ] If multi-language is enabled, check all pages exist in all languages

## Pre-commit Flow

1. Check each item on the checklist
2. Fix any failures immediately
3. Re-check after fixes
4. Pass quality gate only when all items are ✅

### Structural consistency
- [ ] Numeric prefixes follow conventions, all required `index.md` files exist

### Rendering compatibility
- [ ] Mermaid/KaTeX/PlantUML syntax is correct and will render in AvalonMarkdown
	  - [ ] Mermaid: direction/type valid, arrows correct, participants declared, brackets balanced
	  - [ ] PlantUML: `@startuml`/`@enduml` balanced, participants declared, arrow directions explicit
	  - [ ] KaTeX: all `$...$` and `$$...$$` inline/block pairs are balanced, no mismatched delimiters
- [ ] **Multi-language parity** — No missing or outdated pages across language versions
- [ ] **Discoverability** — Page titles and hierarchy are clear and navigable

### API Existence Verification (CRITICAL)

Every API reference appearing in the written documentation must be verified against the **actual source code** of the target repository. This includes:

- [ ] **Class/method names** in ` ``` ... ``` ` code examples — search the codebase to confirm each type and member exists with the documented signature
- [ ] **Namespace/module paths** in documentation — verify they match the actual project structure
- [ ] **Method parameters and return types** — cross-check against the source declaration; document must match reality
- [ ] **Exception declarations** — if the doc lists thrown exceptions, confirm they exist in the method signature or are documented in XML comments
- [ ] **Property/field names** — every property or field referenced in the doc must be present on the declared type
- [ ] **Removed/deprecated APIs** — if the target repo has `[Obsolete]` attributes or removed members, flag any doc references to them

### Pre-Commit Verification Flow

1. For every page in the Wiki, extract all code blocks containing API references
2. For each reference, use the repo-reading notes from Phase 1 or perform targeted symbol searches to confirm existence
3. If an API reference cannot be verified, **flag it for correction** — either fix the doc to match reality or remove the reference
4. Re-check diagram syntax (Mermaid/PlantUML) after any content corrections
5. Only after all items are ✅, mark the quality gate as passed
