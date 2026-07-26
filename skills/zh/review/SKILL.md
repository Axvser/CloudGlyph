# 审核

## 职责

对所有生成的 Wiki 内容进行系统审查，确保质量、准确性和一致性。

## 检查清单

### 模块覆盖率审计

- [ ] 对照模块列表，检查所有模块是否都已写入文档
- [ ] 遗漏的模块立即补写

### 代码真实性验证

- [ ] 每个代码块中涉及的方法名、参数名、类型确认存在于实际源码中
- [ ] 不存在编造的代码

### 图语法验证

- [ ] Mermaid：方向/类型有效、参与者已声明、括号平衡
- [ ] KaTeX：`$...$` 和 `$$...$$` 成对平衡
- [ ] PlantUML：`@startuml`/`@enduml` 成对、参与者已声明

### 结构一致性

- [ ] 数字前缀正确（如 `01_`、`02_`）
- [ ] 每个目录都存在 `index.md`
- [ ] 不存在本地 Markdown 链接（`[text](local/path/)`）

### 跨语言对等

- [ ] 如果启用了多语言，检查所有页面在所有语言中是否存在

## 预提交流程

1. 逐项检查清单
2. 对任何失败项立即修正
3. 修正后重新检查
4. 全部 ✅ 后通过质量门
- [ ] **Structural consistency** — Numeric prefixes follow conventions, all required `index.md` files exist
- [ ] **Rendering compatibility** — Mermaid/KaTeX/PlantUML syntax is correct and will render in AvalonMarkdown
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
