# Cloud Glyph — Agent Skill Guide

> This file instructs AI coding agents on how to read, navigate, and edit documentation within the Cloud Glyph project.

## Project Overview

Cloud Glyph is an **Avalonia** desktop + browser application that renders a Markdown-based Wiki from flat files. The entire documentation lives under `src/CloudGlyph/Assets/Docs/content/` — no database, no API.

```
src/CloudGlyph/
├── Assets/Docs/
│   ├── config/
│   │   └── languages.json          ← Master language list (source of truth)
│   ├── content/
│   │   ├── languages_index.json    ← [Auto‑generated] language availability
│   │   ├── en/                     ← English docs
│   │   │   ├── tree.json           ← [Auto‑generated] navigation tree
│   │   │   ├── 0_Welcome/
│   │   │   │   └── index.md
│   │   │   ├── 1_QuickStart/
│   │   │   │   └── index.md
│   │   │   └── ...
│   │   └── zh/                     ← Chinese docs (mirror structure)
│   │       ├── tree.json
│   │       ├── 0_欢迎/
│   │       │   └── index.md
│   │       └── ...
│   └── scripts/
│       ├── gen_tree.py             ← [Build] scans content/ → tree.json
│       └── gen_lang_index.py       ← [Build] scans content/ → languages_index.json
├── ViewModels/
│   └── DocumentViewModel.cs        ← Loads indexes, switches languages
└── Views/
	├── MainView.axaml              ← UI: toolbar + tree + markdown viewer
	└── MainView.axaml.cs           ← Theme, WebView wiring
```

## Adding or Editing Wiki Content

### 1. Create a Page

Create a directory under `content/{lang}/` with an `index.md`:

```
content/en/2_Architecture/overview/index.md
content/en/2_Architecture/deployment/index.md
```

- **Directory name** is the URL-safe path key.
- **Numeric prefix** (`1_`, `2_`, `2.5_`) controls sort order; it is **stripped** from the displayed title.
- The scanned directory name (prefix stripped) becomes the **page title** (e.g. `2_Architecture` → `"Architecture"`).
- Each directory that contains an `index.md` becomes a **tree node**. Subdirectories become **children**.

### 2. Write Markdown

```markdown
# Page Title

Regular Markdown with **bold**, *italic*, `code`, and [links](https://example.com).

## Supported Extensions

| Feature | Syntax |
|---|---|
| KaTeX formula | `$E = mc^2$` or `$$...$$` |
| Code highlight | ` ```lang ... ``` ` |
| Mermaid diagram | ` ```mermaid ... ``` ` |
| PlantUML | ` ```plantuml ... ``` ` |
| Task list | `- [x] done` `- [ ] todo` |
| Footnote | `text[^1]` then `[^1]: detail` |
| Video embed | YouTube / Bilibili / Vimeo URLs (auto-detected) |
| HTML | Full inline HTML allowed, including `<style>`, `<div>`, `<span>` |
```

### 3. Conventions

- **One `index.md` per directory.** The scanner looks only for `index.md`.
- **File encoding:** UTF-8 (required for multi‑language).
- **Image / asset path:** Currently served via `avares://` URIs; for now place assets in the same directory and reference relatively.
- **Front matter:** Not required (the app parses the first `<h1>` as the page title from tree.json).

### 4. Adding a New Language

1. Add the language code and display name in `config/languages.json`.
2. Create `content/{code}/` with at least one page (e.g. `0_Welcome/index.md`).
3. Rebuild — `gen_lang_index.py` and `gen_tree.py` run automatically.

> **Important:** `content/languages_index.json` and `content/*/tree.json` are **build-generated** and listed in `.gitignore`. Do not edit them manually.

## Architecture Notes for Agents

### App Startup Flow

1. `DocumentViewModel` constructor calls `InitializeAsync()`
2. `LoadLanguagesAsync()` reads `languages_index.json` → populates the language ComboBox
3. `LoadTreeAsync()` reads `{lang}/tree.json` → builds page navigation tree
4. User selects a node → `LoadContentAsync()` reads `{lang}/{path}/index.md`
5. Content is rendered via `MarkdownView` (AvalonMarkdown — WebView-based)

### Language Switching

- The top toolbar has a `ComboBox` bound to `DocumentViewModel.TopLanguages` (all available languages).
- `OnSelectedLanguageChanged` triggers `ReloadAsync()` which reloads the tree and re-renders the current page (or falls back to the first node).

### Theme

- The app follows the system theme (dark/light) via `PlatformColorValues`.
- Markdown content uses `var(--accent-color)` and `var(--text-color)` for dynamic theming.

### Rendering Engine

- Backed by **AvalonMarkdown** (NuGet), which wraps `markdown-it` + `highlight.js` + `KaTeX` + `Mermaid` in a WebView.
- Markdown files can contain **inline HTML + CSS** (including `<style>` blocks and `@keyframes` animations).
- The renderer fully supports dark/light mode switching via CSS custom properties.

## .gitignore — Auto‑generated Files

The following are **build outputs** and are gitignored:

```
src/CloudGlyph/Assets/Docs/content/languages_index.json
src/CloudGlyph/Assets/Docs/content/*/tree.json
```

## Project Tech Stack

| Layer | Technology |
|---|---|
| UI framework | Avalonia 11 |
| Language | C# (.NET 10) |
| Markdown renderer | AvalonMarkdown (Avalonia WebView + markdown-it) |
| MVVM | CommunityToolkit.Mvvm (source generators) |
| Theme | VeloxDev.DynamicTheme |
| Build scripts | Python 3 (gen_tree.py / gen_lang_index.py) |
| Desktop target | Win / macOS / Linux |
| Browser target | WebAssembly (via Avalonia.Browser) |
