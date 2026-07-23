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

## 🚀 From Template to Publish

Since this repository is a **GitHub template**, you can create your own Wiki site in just a few clicks, keeping all Wiki files separate from your main project code.

### Step 1: Create a Wiki Repository from Template

1. Go to the [CloudGlyph](https://github.com/Axvser/CloudGlyph) repository page
2. Click **"Use this template"** → **"Create a new repository"**
3. Choose an owner and enter a repository name (e.g., `MyProject-Wiki`)
4. Select **Public** (GitHub Pages requires public for free plans)
5. Click **"Create repository from template"**

> This repo becomes your standalone Wiki site, completely independent from your main project.

### Step 2: Clone the Wiki Repo Into Your Project Directory

Clone the Wiki repo as a subdirectory **inside your existing project** so your project's AI Agent can read the `skills/` instructions directly:

```bash
# Enter your existing project directory
cd your-main-project

# Clone the Wiki repo into a subdirectory (e.g., docs/ or wiki/)
git clone https://github.com/<your-username>/MyProject-Wiki.git docs/wiki
```

Your project structure will look like:

```
your-main-project/
├── src/
├── tests/
├── docs/wiki/          ← Wiki repo (independent Git history)
│   ├── skills/         ← Agent reads instructions here
│   ├── src/CloudGlyph/Assets/Docs/content/   ← Agent writes content here
│   └── ...
└── README.md
```

### Step 3: Work on a New Branch

Create a **new branch** in your main project to keep the main branch clean:

```bash
git checkout -b docs/wiki-content
```

Now ask your project's AI Agent to read `docs/wiki/skills/SKILL.md`. The Agent will write Wiki content into `docs/wiki/src/CloudGlyph/Assets/Docs/content/` following the instructions.

### Step 4: Configure GitHub Pages for the Wiki Repo

Go to the Wiki repo's Settings (`MyProject-Wiki`):

1. **Settings → Pages**
2. **Build and deployment → Source → Select `GitHub Actions`**

Pages will automatically recognize the `actions/deploy-pages@v5` step in the workflow.

### Step 5: Push to Publish

Once content is ready, push the Wiki repo to trigger deployment:

```bash
cd docs/wiki
git add .
git commit -m "Add wiki content"
git push origin master
```

- **Auto-trigger**: Push changes under `src/CloudGlyph/Assets/Docs/**`
- **Manual trigger**: Actions tab → "Deploy Avalonia Browser to GitHub Pages" → Run workflow

Your site will be at:

```
https://<your-username>.github.io/MyProject-Wiki/
```
</p>