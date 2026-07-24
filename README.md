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
  <a href="README.zh.md">🇨🇳 中文版本</a>
</p>

---

> **🌐 Live site:** [https://axvser.github.io/CloudGlyph/](https://axvser.github.io/CloudGlyph/)
>
> Use this template and follow this guide to get your own Agent-driven Wiki site.

---

## 🤖 Agent Instructions

> **If you are an AI coding agent reading this README:** your task is to build Wiki documentation for the repository that contains this directory.
>
> **Start by loading `skills/SKILL.md`** — that file is the master index of the agent skill system. It defines:
>
> 1. **Context & Prerequisites** — template repo identity, root directory selection, `.gitignore` rules, **language selection (default English, user may opt into additional languages)**, Git branch strategy
> 2. **Wiki Content Authoring Model** — how to write pages (directory-as-node, `index.md` per page), all supported rendering syntax (KaTeX, Mermaid, PlantUML, code highlighting, video embeds, etc.), multi-language conventions
> 3. **Framework Execution Pipeline** — a mandatory 8-step pipeline: Git status → project analysis → test/demo discovery → quick start writing → software engineering analysis → API deep dive → review & quality gate → welcome page landing, with hot-pluggable pre/post hooks
> 4. **Sub-Skill Directory Index** — 12+ specialized sub-skills loaded on demand for specific scenarios
>
> Follow the pipeline strictly in order. Every diagram must pass syntax validation. Every code snippet must be verified against actual source files. Do not fabricate APIs.

---

## 🚀 From Template to Publish — User Guide

This repository is a **GitHub template**. Your workflow is:

```
1. Create your own Wiki repo from this template (on GitHub)
2. In your project repo, create a new branch
3. Clone the Wiki repo into that branch as a subdirectory
4. Ask your AI Agent to read skills/SKILL.md from that subdirectory
5. Agent writes content → you push the Wiki repo → GitHub Pages auto-deploys
```

### Step 1: Create Your Own Wiki Repository from Template

Start by creating a **standalone Wiki repository** on GitHub — this will be the repo that hosts your published site.

1. Go to the [CloudGlyph](https://github.com/Axvser/CloudGlyph) repository page
2. Click **"Use this template"** → **"Create a new repository"**
3. Choose an owner and enter a repository name (e.g., `MyProject-Wiki` or just `Wiki`)
4. Select **Public** (GitHub Pages requires public for free plans)
5. Click **"Create repository from template"**

> This repo (`MyProject-Wiki`) is now **your** Wiki site repository. It has its own independent Git history and will be published to GitHub Pages.

### Step 2: Create a New Branch in Your Project

Now go to **your own project repository** (the code you want to document):

```bash
cd your-main-project

# Create a new branch to isolate Wiki work from your main branch
git checkout -b docs/wiki-content
```

> Using a dedicated branch keeps the Wiki directory out of your main branch. You can delete this branch later after content is finalized.

### Step 3: Clone the Wiki Repo Into Your Project Branch

Inside the new branch, clone your Wiki repo as a **subdirectory**. This lets your AI Agent access both your source code (for analysis) and the Wiki repository's `skills/` instructions (for writing) from the same workspace:

```bash
# Inside your-main-project on branch docs/wiki-content
git clone https://github.com/<your-username>/MyProject-Wiki.git docs/wiki
```

Your project structure will now look like this:

```
your-main-project/                  ← Your project repo (your actual code)
├── src/                            ← Your source code (Agent analyzes this)
├── tests/                          ← Your tests (Agent discovers API usage here)
├── docs/wiki/                      ← Your Wiki repo (cloned from CloudGlyph template)
│   ├── skills/                     ← Agent reads instructions from here
│   │   ├── SKILL.md                ← Master index: the entry point
│   │   ├── generate_skill_index.py ← Index regenerator (run after adding sub-skills)
│   │   └── ... (12+ sub-skill dirs)
│   ├── src/CloudGlyph/Assets/Docs/content/   ← Agent writes Wiki content here
│   │   ├── en/                      ← English pages
│   │   └── zh/                      ← Chinese pages (optional)
│   └── .github/workflows/          ← Auto-deploy to GitHub Pages
└── README.md                       ← Your project's README
```

> **Important:** `docs/wiki/` has its own `.git` history independent from your project. Changes inside `docs/wiki/` are tracked by your Wiki repo.

### Step 4: Command Your AI Agent

Tell your AI coding agent (e.g., GitHub Copilot, Cursor, or any agent supporting skill files):

> "Read `docs/wiki/skills/SKILL.md` and follow the pipeline to build Wiki documentation for this project."

The Agent will:
1. Load the master skill index from `docs/wiki/skills/SKILL.md`
2. Execute the **7-step Framework Execution Pipeline** — analyze your source code, discover tests/demos, write quick-start guides, produce software engineering analysis with diagrams, document APIs in depth, and run the final quality gate
3. Write all content into `docs/wiki/src/CloudGlyph/Assets/Docs/content/` as `index.md` files organized by directory
4. Every Mermaid/PlantUML diagram will be syntax-validated. Every code snippet will be verified against your actual source files. No fabricated APIs.

**To trigger this after you close your editor, simply paste the quoted instruction into your next conversation with the agent.**

### Step 5: Configure GitHub Pages for the Wiki Repo

Go to the Wiki repo's Settings on GitHub (`https://github.com/<your-username>/MyProject-Wiki/settings/pages`):

1. **Settings → Pages**
2. **Build and deployment → Source → Select `GitHub Actions`**

The included workflow file (`.github/workflows/deploy-pages.yml`) will be automatically recognized.

### Step 6: Push to Publish

Once the Agent has finished writing content, commit and push the Wiki repo:

```bash
cd docs/wiki
git add .
git commit -m "Add wiki content"
git push origin master
```

- **Auto-trigger**: The GitHub Actions workflow detects pushes under `src/CloudGlyph/Assets/Docs/**`
- **Manual trigger**: Actions tab → "Deploy Avalonia Browser to GitHub Pages" → Run workflow

Your published site will be at:

```
https://<your-username>.github.io/MyProject-Wiki/
```

### Optional: Keeping the Skills Updated

CloudGlyph may receive updates to its `skills/` directory. To pull in new or improved agent instructions:

```bash
cd docs/wiki
git remote add upstream https://github.com/Axvser/CloudGlyph.git
git fetch upstream
git checkout master
git merge upstream/master
# Resolve any conflicts in skills/ if they occur
```
</p>