<p align="center">
  <img src="src/CloudGlyph/Assets/avalonia-logo.ico" width="64" alt="CloudGlyph" />
</p>

<h1 align="center">CloudGlyph</h1>

<p align="center">
  <strong>Agent 编写 → 一键部署 GitHub Pages</strong>
  <br />
  AI Agent 按 <code>skills/</code> 指令写入 Wiki → CloudGlyph 构建 → 自动发布 Pages
</p>

<p align="center">
  <a href="https://axvser.github.io/CloudGlyph/" target="_blank">🌐 在线示例</a> •
  <a href="#-工作流">工作流</a> •
  <a href="#-agent-核心操作区-content">Content</a> •
  <a href="#-skills-指令系统">Skills</a> •
  <a href="#-从-fork-到发布">Fork 到发布</a> •
  <a href="#-本地预览">本地预览</a> •
  <a href="#-修改构建分支">构建分支</a>
</p>

---

> **🌐 已有线上站点：** [https://axvser.github.io/CloudGlyph/](https://axvser.github.io/CloudGlyph/)
>
> Fork 后按本指南配置，立即拥有你专属的 Agent 驱动 Wiki 站点。

---

## 📦 工作流

本项目的交付终点是 **GitHub Pages**，桌面端仅为本地预览手段：

<pre>
                         ┌──────────────────────────────────┐
                         │        AI Agent (Copilot 等)      │
                         │  读取 skills/SKILL.md 获得指令     │
                         └──────────┬───────────────────────┘
                                    │ 写入 / 修改
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
             │   推送 content/ 变更到 {branch} 自动触发 │
             │   也可手动触发 Actions → Run workflow  │
             └──────────────────────────────────────┘
                                ▲
                                │ 调试预览
             ┌──────────────────────────────────────┐
             │     桌面端 (dotnet run)               │
             │     本地查看效果，确认后推送触发部署     │
             └──────────────────────────────────────┘
</pre>

**一句话：** Agent 写 content → 推送到远端 → Actions 自动构建并发布到 Pages。桌面端只是"写完看看效果"的调试工具。

---

## 🎯 Agent 核心操作区：content

Agent 的所有写操作集中在：

<pre>
src/CloudGlyph/Assets/Docs/content/
├── en/                         # 英文文档
│   ├── 0_Welcome/index.md
│   ├── 1_GettingStarted/index.md
│   └── 2_Architecture/
│       ├── index.md
│       └── overview/index.md
├── zh/                         # 中文文档（镜像对称）
│   ├── 0_欢迎/index.md
│   └── ...
├── languages_index.json        # ⚠️ 自动生成，勿手动编辑
└── tree.json                   # ⚠️ 自动生成，勿手动编辑
</pre>

### 目录即节点规则

| 规则 | 说明 |
|------|------|
| 一个目录 = 一个页面 | 目录名即显示标题，内含 index.md |
| 数字前缀控制排序 | 0_Welcome、2_Architecture 的前缀在 UI 中自动隐藏 |
| 嵌套 = 父子层级 | 2_Architecture/overview/ → 导航栏 "Architecture > overview" |
| 索引自动生成 | dotnet build 时运行 Python 脚本自动生成 tree.json，不要手动编辑 |

Agent **不需要** 维护 tree.json 和 languages_index.json，构建脚本会自动扫描目录结构。

---

## 🧠 Skills 指令系统

skills/ 是 Agent 的操作手册。Agent **必须首先读取** skills/SKILL.md，再按需加载子技能：

### 核心分析

| Skill | 写入位置 | 触发场景 |
|-------|---------|----------|
| SKILL.md（入口） | — | 任何 Wiki 任务开始前必读 |
| repo-reading/ | 结构化笔记（供下游消费） | "分析这个仓库" |
| api-docs/ | content/{lang}/{Proj}/api/ | "从测试生成 API 文档" |
| se-analysis/ | content/{lang}/{Proj}/architecture/ | "画架构图" |

### 文档写作

| Skill | 写入位置 | 触发场景 |
|-------|---------|----------|
| tutorial/ | content/ | "写快速上手教程" |
| migration/ | content/ | "写 .NET 迁移指南" |
| comparison/ | content/ | "对比框架 A 和 B" |
| generation/ | content/ | "自动生成 API 参考" |
| faq/ | content/ | "整理 FAQ" |
| adr/ | content/ | "记录架构决策" |

### 质量保障

| Skill | 写入位置 | 触发场景 |
|-------|---------|----------|
| translation/ | content/{目标语言}/ | "翻译为中文" |
| review/ | 审核 content/ 下所有页面 | "审核文档质量" |
| contribution/ | 仓库根目录 CONTRIBUTING.md | "写 CONTRIBUTING.md" |

### 默认执行路径

无明确步骤时（如"写 Wiki"），Agent 自动执行：

<pre>
Phase 1: repo-reading   →  只读分析，产出笔记
Phase 2: api-docs       →  写入 content/{lang}/{Proj}/api/
Phase 3: se-analysis    →  写入 content/{lang}/{Proj}/architecture/
Phase 4: translation    →  对齐 en/ 与 zh/
Phase 5: review         →  质量审核，通过后交付
</pre>

---

## 🚀 从 Fork 到发布

Fork 此仓库后，只需三步即可拥有自己的 Pages 站点：

### Step 1: Fork 并克隆

```bash
git clone https://github.com/<你的用户名>/CloudGlyph.git
cd CloudGlyph
```

### Step 2: 配置 GitHub Pages 部署环境

> 工作流 `.github/workflows/publish.yml` 已写好，无需改动。你需要做的是在 Settings 中授权它部署。

1. **Settings → Environments → New Environment**
2. **名称填入 `github-pages`**（必须与此一致，工作流中硬编码）
3. **Deployment branches → Add deployment branch → 输入你的分支名（如 `master`）→ 保存**

完成以上配置后，Pages 即可使用——工作流中的 `actions/deploy-pages@v5` 会自动被 Pages 识别。

### Step 3: 触发发布

- **自动触发**：推送 `src/CloudGlyph/Assets/Docs/**` 下文件变更到配置的分支
- **手动触发**：Actions 标签 → 选择 "Deploy Avalonia Browser to GitHub Pages" → Run workflow

首次部署后，站点地址为：

```
https://<你的用户名>.github.io/CloudGlyph/
```

可在 Settings → Pages 中确认，或查看 Actions 运行日志中的 `page_url`。

---

## 🖥️ 本地预览

在推送前先在本地查看效果：

```bash
# 环境准备
dotnet workload install wasm-tools
dotnet restore

# 桌面端预览（推荐，启动快）
dotnet run --project src/CloudGlyph.Desktop/CloudGlyph.Desktop.csproj

# 也可浏览器端预览
dotnet run --project src/CloudGlyph.Browser/CloudGlyph.Browser.csproj
```

---

## 🔧 修改构建分支

工作流默认监听 `master` 分支。如需改为其他分支：

编辑 `.github/workflows/publish.yml`：

```yaml
on:
  push:
    branches: ["master"]        # ← 改为你的分支名，如 "main"
    paths:
      - "src/CloudGlyph/Assets/Docs/**"
```

并同步更新环境分支保护：**Settings → Environments → github-pages → Deployment branches** 添加目标分支。

---

## 📝 Agent 快速上手指南

当你（作为 Agent）收到写 Wiki 的任务时，按此流程操作：

1. 读取 `skills/SKILL.md` 了解内容模型与渲染能力
2. 判断任务是否明确指定场景：
   - 明确 → 加载对应子 Skill
   - 不明确 → 按默认执行路径逐阶段推进
3. 所有写入操作仅在 `src/CloudGlyph/Assets/Docs/content/` 下进行
4. 不要手动编辑 `tree.json` / `languages_index.json`
5. 完成所有内容后，建议用户推送触发部署，或手动触发 Actions

---

## 🤝 贡献

欢迎提交 Pull Request！Agent 可参考 `skills/contribution/SKILL.md`。

---

## 📄 许可证

MIT

---

<p align="center">
  <a href="https://axvser.github.io/CloudGlyph/">🌐 Live Demo</a>  •  Built with ❤️ using Avalonia UI & .NET 10
</p>
