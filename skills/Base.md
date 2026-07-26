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
