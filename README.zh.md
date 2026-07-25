<h1 align="center">Cloud Glyph</h1>

<p align="center">
  基于 <a href="https://www.avaloniaui.net/">Avalonia UI</a> 框架构建的浏览器端 Wiki 站点生成器
</p>

<p align="center">
  <strong>Agent 编写 → 一键部署到 GitHub Pages</strong>
  <br />
  AI Agent 按 <code>skills/</code> 指令编写 Wiki → CloudGlyph 构建 → 自动发布到 Pages
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a>
</p>

---

> **🌐 线上站点：** [https://axvser.github.io/CloudGlyph/](https://axvser.github.io/CloudGlyph/)
>
> 使用本模板并按照本指南操作，即可获得你自己的 Agent 驱动 Wiki 站点。

---

## 🤖 Agent 说明

> **如果你是一个正在阅读本 README 的 AI 编码 Agent：** 你的任务是为包含此目录的仓库构建 Wiki 文档。
>
> **首先加载 `skills/SKILL.md`** — 该文件是 Agent 技能系统的主索引。它定义了：
>
> 1. **上下文与前提条件** — 模板仓库标识、根目录选择、`.gitignore` 规则、**语言选择（默认英语，用户可选择启用更多语言）**、Git 分支策略
> 2. **Wiki 内容撰写模型** — 如何编写页面（目录即节点，每页一个 `index.md`）、所有支持的渲染语法（KaTeX、Mermaid、PlantUML、代码高亮、视频嵌入等）、多语言约定
> 3. **框架执行管线** — 一个强制性的 8 步管线：Git 状态 → 项目分析 → 测试/示例发现 → 快速入门写作 → 软件工程分析 → API 深入分析 → 审查与质量门 → 欢迎页面落地，支持热插拔的前置/后置钩子
> 4. **子技能目录索引** — 12+ 个按需加载的专业子技能，适用于特定场景
>
> 严格按照顺序执行管线。

---

## 🚀 从模板到发布 — 用户指南

此仓库是一个 **GitHub 模板仓库**。你的工作流程是：

```
1. 从本模板创建你自己的 Wiki 仓库（在 GitHub 上）
2. 在你的项目仓库中创建一个新分支
3. 将 Wiki 仓库克隆到该分支作为子目录
4. 让你的 AI Agent 读取该子目录中的 skills/SKILL.md
5. Agent 编写内容 → 你推送 Wiki 仓库 → GitHub Pages 自动部署
```

### 配置：选择你的名称

在本指南中，用你自己的选择替换以下占位符：

| 占位符 | 含义 | 示例 |
|---|---|---|
| `<your-wiki-branch>` | 项目中用于存放 Wiki 子目录的分支 | `docs/wiki-content` |
| `<your-wiki-path>` | Wiki 仓库在项目中的克隆路径 | `docs/wiki` |

> **为什么这很重要：** AI Agent 从你给出的命令中读取这些值。选择一致的名称可以避免路径混乱。

### 第 1 步：从模板创建你的 Wiki 仓库

首先在 GitHub 上创建一个**独立的 Wiki 仓库** — 这个仓库将托管你发布的站点。

1. 进入 [CloudGlyph](https://github.com/Axvser/CloudGlyph) 仓库页面
2. 点击 **"Use this template"** → **"Create a new repository"**
3. 选择所有者并输入仓库名称（例如 `MyProject-Wiki` 或直接 `Wiki`）
4. 选择 **Public**（免费计划下 GitHub Pages 需要公开仓库）
5. 点击 **"Create repository from template"**

> 这个仓库（`MyProject-Wiki`）现在是**你的** Wiki 站点仓库。它有自己独立的 Git 历史，并将发布到 GitHub Pages。

### 第 2 步：在你的项目中创建一个新分支

现在进入**你自己的项目仓库**（你想要编写文档的代码）：

```bash
cd your-main-project

# 创建一个新分支，将 Wiki 工作与主分支隔离
git checkout -b <your-wiki-branch>
```

> 使用专用分支可以将 Wiki 目录排除在主分支之外。内容定稿后可以删除此分支。

> **⚠️ 重要：** AI Agent 必须在 Wiki 子目录（`<your-wiki-path>/`）内执行所有 Git 操作（`add`、`commit`、`push`、`branch`），而不是在项目根目录。如果 Agent 在错误的目录运行 `git`，它将对你的项目仓库而不是 Wiki 仓库进行操作——导致所有 Wiki 内容被静默遗漏。

### 第 3 步：将 Wiki 仓库克隆到你的项目分支中

在新分支内，将你的 Wiki 仓库克隆为**子目录**。这样，你的 AI Agent 可以在同一个工作区中同时访问你的源代码（用于分析）和 Wiki 仓库的 `skills/` 指令（用于编写）：

```bash
# 在 your-main-project 的 <your-wiki-branch> 分支下
git clone https://github.com/<你的用户名>/MyProject-Wiki.git <your-wiki-path>
```

你的项目结构现在看起来如下：

```
your-main-project/                          ← 你的项目仓库（实际代码）
├── src/                                    ← 你的源代码（Agent 分析此目录）
├── tests/                                  ← 你的测试（Agent 在此发现 API 用法）
├── <your-wiki-path>/                       ← 你的 Wiki 仓库（从 CloudGlyph 模板克隆）
│   ├── skills/                             ← Agent 从此处读取指令
│   │   ├── SKILL.md                        ← 主索引：入口点
│   │   ├── generate_skill_index.py         ← 索引重新生成器（添加子技能后运行）
│   │   └── ...（12+ 个子技能目录）
│   ├── src/CloudGlyph/Assets/Docs/content/ ← Agent 在此编写 Wiki 内容
│   │   ├── en/                             ← 英语页面
│   │   └── zh/                             ← 中文页面（可选）
│   └── .github/workflows/                  ← 自动部署到 GitHub Pages
└── README.md                               ← 你的项目 README
```

> **重要：** `<your-wiki-path>/` 拥有独立于你项目的 `.git` 历史记录。`<your-wiki-path>/` 内的更改将由你的 Wiki 仓库跟踪。Agent 将自动检测这个嵌套的仓库。

> **⚠️ .gitignore 风险：** 如果你项目的 `.gitignore` 包含诸如 `src/` 或 `**/Docs/**` 的模式，写入 `<your-wiki-path>/src/CloudGlyph/Assets/Docs/content/` 的 Wiki 输出文件可能会变得不可见。在开始之前检查你的 `.gitignore`，或者添加 `!<your-wiki-path>/**` 来豁免 Wiki 目录。

### 第 4 步：指挥你的 AI Agent

告诉你的 AI 编码 Agent（例如 GitHub Copilot、Cursor 或任何支持技能文件的 Agent）。**将 `<your-wiki-path>` 替换为你实际的选择**：

> "读取 `<your-wiki-path>/skills/SKILL.md` 并按照管线为此项目构建 Wiki 文档。"

Agent 将执行以下操作：

1. **自动检测** `skills/SKILL.md` 是在工作区根目录还是嵌套在 `<your-wiki-path>/` 下 — 并据此计算 `WIKI_ROOT` 和 `PROJECT_ROOT`
2. 从 `<your-wiki-path>/skills/SKILL.md` 加载主技能索引
3. 执行 **8 步框架执行管线** — 分析你的源代码、发现测试/示例、编写快速入门指南、生成包含图表的软件工程分析、深入记录 API、运行质量门、构建欢迎页面
4. 将所有内容作为 `index.md` 文件按目录组织写入 `<your-wiki-path>/src/CloudGlyph/Assets/Docs/content/`
5. 每个 Mermaid/PlantUML 图表都将经过语法验证。每个代码片段都将对照你的实际源文件进行验证。不会编造 API。

**要在关闭编辑器后触发此操作，只需将上述引导指令粘贴到你与 Agent 的下一次对话中。**

### 第 5 步：配置 Wiki 仓库的 GitHub Pages

在 GitHub 上进入 Wiki 仓库的 Settings（`https://github.com/<你的用户名>/MyProject-Wiki/settings/pages`）：

1. **Settings → Pages**
2. **Build and deployment → Source → 选择 `GitHub Actions`**

随附的工作流文件（`.github/workflows/deploy-pages.yml`）将被自动识别。

### 第 6 步：推送发布

Agent 完成内容编写后，提交并推送 Wiki 仓库：

```bash
cd <your-wiki-path>
git add .
git commit -m "添加 Wiki 内容"
git push origin master
```

> **⚠️ Git 仓库陷阱：** `cd <your-wiki-path>` 是必需的。如果你（或 Agent）从项目根目录运行 `git add`，它将把文件添加到你的**项目**仓库 — 而不是 Wiki 仓库 — 因为 `<your-wiki-path>/` 是一个嵌套的 `.git` 仓库，对外层 Git 不可见。

- **自动触发**：GitHub Actions 工作流检测 `src/CloudGlyph/Assets/Docs/**` 下的推送
- **手动触发**：Actions 标签 → "Deploy Avalonia Browser to GitHub Pages" → Run workflow

你发布的站点地址为：

```
https://<你的用户名>.github.io/MyProject-Wiki/
```

### 可选：保持技能更新

CloudGlyph 的 `skills/` 目录可能会收到更新。要拉取新的或改进的 Agent 指令：

```bash
cd <your-wiki-path>
git remote add upstream https://github.com/Axvser/CloudGlyph.git
git fetch upstream
git checkout master
git merge upstream/master
# 解决 skills/ 中可能出现的冲突
```