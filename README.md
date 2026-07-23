<p align="center">
  <img src="src/CloudGlyph/Assets/avalonia-logo.ico" width="64" alt="CloudGlyph" />
</p>

<h1 align="center">CloudGlyph</h1>

<p align="center">
  <strong>Agent Write → One-Click Deploy to GitHub Pages</strong>
  <br />
  AI Agent writes Wiki via <code>skills/</code> instructions → CloudGlyph builds → Auto-publish to Pages
</p>

<p align="center">
  <a href="https://axvser.github.io/CloudGlyph/" target="_blank">🌐 Live Demo</a> •
  <a href="#-workflow">Workflow</a> •
  <a href="#-agent-core-area-content">Content</a> •
  <a href="#-skills-instruction-system">Skills</a> •
  <a href="#-from-fork-to-publish">Fork to Publish</a> •
  <a href="#-local-preview">Local Preview</a> •
  <a href="#-changing-the-build-branch">Build Branch</a>
</p>

<p align="center">
  <sub><a href="README.zh.md">🇨🇳 中文版本</a></sub>
</p>

---

> **🌐 Live site:** [https://axvser.github.io/CloudGlyph/](https://axvser.github.io/CloudGlyph/)
>
> Fork and follow this guide to get your own Agent-driven Wiki site.

---

## 📦 Workflow

The delivery target of this project is **GitHub Pages**; the desktop app is only a local preview tool:

<pre>
                         ┌──────────────────────────────────┐
                         │       AI Agent (Copilot, etc.)    │
                         │  Reads skills/SKILL.md for tasks  │
                         └──────────┬───────────────────────┘
                                    │ Writes / Modifies
                                    ▼
             ┌──────────────────────────────────────┐
             │  src/CloudGlyph/Assets/Docs/content/ │
             │  ├── en/0_Welcome/index.md           │
             │  └── zh/0_欢迎/index.md               │
             └──────────────────┬───────────────────┘
                                │ dotnet publish → WASM
                                ▼
             ┌──────────────────────────────────────┐
             │     GitHub Actions → GitHub Pages     │
             │   Pushing content/ changes to {branch} │
             │   triggers auto-deploy                 │
             │   Or manually: Actions → Run workflow  │
             └──────────────────────────────────────┘
                                ▲
                                │ Debug Preview
             ┌──────────────────────────────────────┐
             │     Desktop App (dotnet run)          │
             │     View locally, then push to deploy │
             └──────────────────────────────────────┘
</pre>

**In one sentence:** Agent writes content → push to remote → Actions auto-builds and deploys to Pages. The desktop app is just a "preview after writing" debugging tool.

---

## 🎯 Agent Core Area: content

All Agent write operations go into:

<pre>
src/CloudGlyph/Assets/Docs/content/
├── en/                         # English docs
│   ├── 0_Welcome/index.md
│   ├── 1_GettingStarted/index.md
│   └── 2_Architecture/
│       ├── index.md
│       └── overview/index.md
├── zh/                         # Chinese docs (mirror symmetry)
│   ├── 0_欢迎/index.md
│   └── ...
├── languages_index.json        # ⚠️ Auto-generated, do not edit
└── tree.json                   # ⚠️ Auto-generated, do not edit
</pre>

### Directory-as-Node Rules

| Rule | Description |
|------|-------------|
| One directory = one page | Directory name is the display title; contains index.md |
| Numeric prefix controls sorting | Prefixes like 0_Welcome, 2_Architecture are hidden in the UI |
| Nesting = parent-child hierarchy | 2_Architecture/overview/ → nav shows "Architecture > overview" |
| Index auto-generated | dotnet build runs a Python script to generate tree.json; do not edit manually |

Agent **does not** need to maintain tree.json or languages_index.json — the build script scans the directory structure automatically.

---

## 🧠 Skills Instruction System

`skills/` is the Agent's operations manual. The Agent **must first read** `skills/SKILL.md`, then load sub-skills as needed:

### Core Analysis

| Skill | Write Location | Trigger |
|-------|---------------|---------|
| SKILL.md (entry) | — | Must read before any Wiki task |
| repo-reading/ | Structured notes (for downstream consumption) | "Analyze this repository" |
| api-docs/ | content/{lang}/{Proj}/api/ | "Generate API docs from tests" |
| se-analysis/ | content/{lang}/{Proj}/architecture/ | "Draw architecture diagrams" |

### Documentation Writing

| Skill | Write Location | Trigger |
|-------|---------------|---------|
| tutorial/ | content/ | "Write a quick-start tutorial" |
| migration/ | content/ | "Write a .NET migration guide" |
| comparison/ | content/ | "Compare Framework A and B" |
| generation/ | content/ | "Auto-generate API reference" |
| faq/ | content/ | "Compile an FAQ" |
| adr/ | content/ | "Record architecture decisions" |

### Quality Assurance

| Skill | Write Location | Trigger |
|-------|---------------|---------|
| translation/ | content/{target language}/ | "Translate to Chinese" |
| review/ | Reviews all pages under content/ | "Review documentation quality" |
| contribution/ | Repository root CONTRIBUTING.md | "Write CONTRIBUTING.md" |

### Default Execution Path

When no explicit steps are given (e.g., "write Wiki"), the Agent automatically executes:

<pre>
Phase 1: repo-reading   →   Read-only analysis, produce notes
Phase 2: api-docs       →   Write to content/{lang}/{Proj}/api/
Phase 3: se-analysis    →   Write to content/{lang}/{Proj}/architecture/
Phase 4: translation    →   Align en/ and zh/
Phase 5: review         →   Quality review, then deliver
</pre>

---

## 🚀 From Fork to Publish

After forking this repo, follow three simple steps to get your own Pages site:

### Step 1: Fork and Clone

```bash
git clone https://github.com/<your-username>/CloudGlyph.git
cd CloudGlyph
```

### Step 2: Configure GitHub Pages Build Source

> The workflow `.github/workflows/publish.yml` is already written — no changes needed. You just need to tell Pages to use it in Settings.

1. **Settings → Pages**
2. **Build and deployment → Source → Select `GitHub Actions`**

Once configured, Pages will automatically recognize the `actions/deploy-pages@v5` step in the workflow and complete the deployment.

### Step 3: Trigger a Publish

- **Auto-trigger**: Push changes under `src/CloudGlyph/Assets/Docs/**` to your configured branch
- **Manual trigger**: Actions tab → Select "Deploy Avalonia Browser to GitHub Pages" → Run workflow

After first deploy, your site will be at:

```
https://<your-username>.github.io/CloudGlyph/
```

You can confirm in Settings → Pages, or check the `page_url` in the Actions run log.

---

## 🖥️ Local Preview

Preview locally before pushing to check the results:

```bash
# Environment setup
dotnet workload install wasm-tools
dotnet restore

# Desktop preview (recommended, fast startup)
dotnet run --project src/CloudGlyph.Desktop/CloudGlyph.Desktop.csproj

# Or browser preview
dotnet run --project src/CloudGlyph.Browser/CloudGlyph.Browser.csproj
```

---

## 🔧 Changing the Build Branch

The workflow listens on the `master` branch by default. To change it:

Edit `.github/workflows/publish.yml`:

```yaml
on:
  push:
    branches: ["master"]        # ← Change to your branch, e.g., "main"
    paths:
      - "src/CloudGlyph/Assets/Docs/**"
```

No additional settings needed — GitHub Actions will automatically use the branch configured in the workflow.

---

## 📝 Agent Quick Start Guide

When you (as an Agent) receive a task to write Wiki content, follow this process:

1. Read `skills/SKILL.md` to understand the content model and rendering capabilities
2. Determine if the task specifies a clear scenario:
   - Clear → Load the corresponding sub-skill
   - Unclear → Follow the default execution path phase by phase
3. All write operations go only into `src/CloudGlyph/Assets/Docs/content/`
4. Do not manually edit `tree.json` / `languages_index.json`
5. After completing all content, suggest the user push to trigger deployment, or manually trigger Actions

---

## 🤝 Contributing

Pull Requests are welcome! Agents can refer to `skills/contribution/SKILL.md`.

---

## 📄 License

MIT

---

<p align="center">
  <a href="https://axvser.github.io/CloudGlyph/">🌐 Live Demo</a>  •  Built with ❤️ using Avalonia UI & .NET 10
</p>