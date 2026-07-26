# Cloud Glyph Skills

## 职责

本技能体系为 AI Agent 提供 Wiki 文档编写工作流，你将严格遵循该工作流程，产出符合规范的文档

## 变量约定

> **Wiki_Root** — 产出文档的根目录（即 `skills/` 所在目录的父目录），Agent仅允许在Wiki_Root下创建、修改、删除文档文件

> **Deploy_Mode** — 部署模式：
> - `nested`：Wiki 仓库作为子目录挂在某个项目下；Agent 应文档化父项目（排除 Wiki 自身）
> - `standalone`：Wiki 仓库独立使用；Agent 无法自动发现项目，必须询问用户

> **Solution_Root** — 被文档化项目的解决方案根目录
> - `nested` 模式：由 Agent 自动发现（Wiki_Root 的父目录）
> - `standalone` 模式：由用户提供

> **Project_List** — 被文档化项目的列表。在 `nested` 模式下，排除 Wiki 仓库自身的源码项目（即 CloudGlyph 项目）

> **Language_List** — Wiki 的语言支持范围。Agent 应在第 1 步通过交互工具或直接询问确定用户所需语种，再比对 `languages.json` 验证可用性；不支持的语种记录差异并在最后告知用户，不中断流程。

## 内容模型

Wiki 采用"目录即页面"的组织方式。Agent 必须遵守以下两条核心规则：

> **规则 1：目录名即导航结构** — 每个 Wiki 页面对应一个目录。目录名使用 `{数字}_` 前缀控制排序，如 `0_Welcome`、`01_project_structure`。Agent 在创建目录时须使用合适的数字前缀以保证页面顺序。

> **规则 2：内容文件约定** — 每个目录下有且只有一个名为 `index.md` 的内容文件作为该页面的正文。目录内可包含更多子目录来表示子页面（子页面也遵守规则 1）。

### 单项目 vs 多项目

- **如果只文档化一个项目**（Project_List 中只有一个条目），则内容直接放在 `content/{lang}/` 下，无需额外项目层目录
- **如果文档化多个项目**（Project_List 中有多个条目），则每个项目需要一层目录来隔离各自的内容，如 `1_MyApp/`、`2_MyLib/`

```
# 单项目示例
content/en/
├── 0_Welcome/
│   └── index.md              ← 欢迎页（仅此页无子页）
├── 1_quickstart/
│   ├── index.md              ← 快速开始总览
│   ├── 01_getting-started/
│   │   └── index.md          ← 子页
│   └── 02_advanced-usage/
│       └── index.md          ← 子页
├── 2_api/
│   ├── index.md              ← API 总览
│   ├── Controllers/
│   │   └── index.md          ← 子页
│   └── Services/
│       └── index.md          ← 子页
├── 3_architecture/
│   ├── index.md              ← 架构总览
│   ├── 01_project_structure/
│   │   └── index.md          ← 子页
│   ├── 02_class_hierarchy/
│   │   └── index.md          ← 子页
│   └── 03_request_lifecycle/
│       └── index.md          ← 子页
└── 4_copyright/
    └── index.md              ← 版权（无子页）

# 多项目示例
content/en/
├── 0_Welcome/
│   └── index.md
├── 1_MyApp/
│   ├── 0_quickstart/
│   │   ├── index.md
│   │   ├── 01_getting-started/
│   │   │   └── index.md
│   │   └── 02_advanced-usage/
│   │       └── index.md
│   ├── 1_api/
│   │   ├── index.md
│   │   ├── Controllers/
│   │   │   └── index.md
│   │   └── Services/
│   │       └── index.md
│   └── 2_architecture/
│       ├── index.md
│       ├── 01_project_structure/
│       │   └── index.md
│       └── 02_class_hierarchy/
│           └── index.md
├── 2_MyLib/
│   ├── 0_quickstart/
│   │   ├── index.md
│   │   └── 01_getting-started/
│   │       └── index.md
│   └── 1_api/
│       ├── index.md
│       └── Services/
│           └── index.md
└── 3_copyright/
    └── index.md
```

## 工作流

> 0.开始

> 1.部署模式检测与变量确认

> 2.技术栈分析

> 3.约束加载

> 4.功能模块发现

> 5.编写【欢迎】

> 6.编写【快速开始】

> 7.编写【APIs】

> 8.编写【软件工程分析】

> 9.编写【版权】

> 10.审核

> 11.结束

## 技能索引

<!-- SKILL_INDEX -->
