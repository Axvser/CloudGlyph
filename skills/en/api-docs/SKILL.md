# API Reference

## Responsibility

Fully enumerate all **interfaces, types, and functions** for each feature module, providing a complete API catalog with signatures.

## Writing Principles

### Full Coverage

API Reference is not about depth or multiple styles — it's about **uncompromising completeness**:

- List all public types (classes, structs, interfaces, enums) in each module
- For each type, list all public members (methods, properties, events, fields)
- Include full signature, parameter descriptions, return value descriptions, and exception declarations

### API Discovery Priority

> **Priority 1 — Demo/Example projects**
> Scan `Examples/` directories for real-world usage of the API, **read all source files in full**. Demo projects reveal the intended public API surface.
>
> **Priority 2 — Unit Tests**
> **Read all test files in full**, extracting API signatures, typical input/output, and edge cases.
>
> **Priority 3 (Fallback) — Source code interfaces**
> Only when no Demo or Test exists: read the public API signatures directly from source files. These must be explicitly marked as *inferred*.

### Entry Template

Record each public member using the following structure:

```markdown
### {TypeName}.{MemberName}

**Signature:**
`{ReturnType} {MemberName}({ParameterList})`

| Parameter | Type | Description |
|---|---|---|
| `{param}` | `{Type}` | {description} |

**Returns:** `{Type}` — {description}

**Exceptions:**
| Exception | Condition |
|---|---|
| `{ExceptionType}` | {condition} |

**Example:**
```csharp
// Source: [Demo/Test/Inferred]
var result = instance.Method(value);
```

**Notes:**
- {additional notes}
```

### Organization

Group by type, and within each type sort by member kind (properties first, then methods):

```markdown
## {Namespace}

### Class: {ClassName}

#### Properties

| Name | Type | Description |
|---|---|---|
| `{Name}` | `{Type}` | {description} |

#### Methods

(Expand each using the entry template)

### Interface: {InterfaceName}

...
```

### Output Location

```
content/{lang}/{category}/1_API_Reference/{Feature}/
├── index.md                    ← Overview
├── 0_{NamespaceA}/
│   └── index.md
├── 1_{NamespaceB}/
│   └── index.md
└── ...
```

## Post-Write Action

After writing API documentation:

- [ ] **Regenerate navigation index** — Run the tree generator script (e.g. `python gen_tree.py`) to rebuild tree.json
- [ ] **Build the project** — Run `dotnet build` to verify the new content embeds correctly
