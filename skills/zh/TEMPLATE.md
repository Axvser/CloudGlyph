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

> **规则 3：目录名必须匹配目标语言** — 目录名必须使用内容语言而非英语。例如 `Language_List = ["zh"]` 时，使用 `0_欢迎` 而非 `0_Welcome`、`1_快速入门` 而非 `1_quickstart`、`2_API参考` 而非 `2_api`、`3_架构分析` 而非 `3_architecture`。例外：被普遍认可的原始形式专有名词和品牌名（如 "VeloxDev"、"MVVM"、"AOP"）。

### 内容组织（三层级）

Agent 根据 Project_List 中的条目数决定层级：

| 层级 | 场景 | 结构 | 条件 |
|---|---|---|---|
| **单项目** | 一个项目 | `content/{lang}/` — 内容直接放在语言根目录下 | `Project_List` 有 **1 个条目** |
| **多项目** | 2-5 个项目 | `content/{lang}/{project}/` — 每个项目独立目录 | `Project_List` 有 **2-5 个条目** |
| **框架/单体仓库** | 6+ 个项目 | `content/{lang}/{category}/` — 按**功能领域**分组，而非按单个项目 | `Project_List` 有 **6+ 个条目** |

**框架/单体仓库层级规则：**
- 分类基于**功能领域**（如核心库、适配器、生成器、模板、示例），而非单个项目名
- 根据模块发现结果创建 2-8 个分类目录
- 每个分类根据需要包含 `0_快速入门/`、`1_API参考/`、`2_架构分析/` 子结构
- 防止导航被 40+ 个单独项目条目淹没

```
# 示例：框架/单体仓库（40+ 项目）
content/zh/
├── 0_欢迎/
│   └── index.md
├── 1_核心库/
│   ├── 0_快速入门/
│   │   └── index.md
│   ├── 1_API参考/
│   │   └── index.md
│   └── 2_架构分析/
│       └── index.md
├── 2_适配器/
│   ├── 0_快速入门/
│   │   └── index.md
│   └── 1_API参考/
│       └── index.md
├── 3_生成器/
│   ├── 0_快速入门/
│   │   └── index.md
│   └── 1_API参考/
│       └── index.md
├── 4_模板/
│   └── 0_快速入门/
│       └── index.md
├── 5_示例/
│   └── 0_快速入门/
│       └── index.md
└── 6_版权/
    └── index.md
```

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

# 多项目示例（2-5 个项目）
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

### 内容编写阶段（步骤 5-8）

页面按**读者消费顺序**编写：快速入门（最先读）→ API → 架构分析 → 版权（最后读）。此顺序确保前面的页面可以在适当位置引用后面的页面。

> 5.编写【快速入门】— `{category}/0_快速入门/`（含入门代码示例的 index.md）

> 6.编写【API 参考】— `{category}/1_API参考/`（完整 API 参考文档）

> 7.编写【软件工程分析】— `{category}/2_架构分析/`（架构、类图、时序图）

> 8.编写【版权】— `{category}/3_版权/`（许可证和署名）

### 润色与发布阶段（步骤 9-11）

> 9.编写【欢迎页】— `0_欢迎/`（英文为 `0_Welcome/`）。在所有内容页面编写完成后、审核之前执行。欢迎页是导航的第一个条目，但却是**最后编写的页面**，因为它总结所有其他页面。

> 10.审核 — 全面的逐页审计，包括：代码真实性验证、图表语法检查、导航索引重新生成（`python gen_tree.py`）和项目构建（`dotnet build`）

> 11.结束

## 技能索引

<!-- SKILL_INDEX -->
