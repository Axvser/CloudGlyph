# 欢迎页

## 职责

替换默认的 `0_Welcome/index.md` 为带有 CSS 动画和卡片布局的美观 HTML 着陆页。

## 前置要求

这是工作流的最后一步。必须等待所有内容编写完成后再执行。

## 核心规则

### 禁止编造

欢迎页中的一切内容必须来自实际分析结果。项目名、模块名、功能描述、图标选择、链接都必须能在之前步骤中找到依据。

### 外层容器固定

```html
<div class="cg-wrapper">    ← 此容器不可修改
  <!-- 内部内容可自定义 -->
</div>
```

禁止：`overflow: scroll`、`max-height`、额外 `<div>` 包裹、修改 `cg-wrapper` 的 `text-align`/`padding`/`width`。

## 编写步骤

### Step A: 收集信息

| 来源 | 提取内容 |
|---|---|
| 技术栈分析 | 项目名、技术栈、核心模块列表（3-8 个） |
| 快速开始 | 主要用例流程 |
| APIs | 核心公开 API 分类 |

### Step B: 构建 3 步工作流

根据项目类型设计用户故事：

| 项目类型 | 步骤 1 | 步骤 2 | 步骤 3 |
|---|---|---|---|
| 类库 | 安装 | 初始化 | 使用 |
| Web API | 配置 | 发送请求 | 处理响应 |
| CLI 工具 | 安装 | 运行命令 | 解析输出 |
| 框架 | 创建项目 | 添加组件 | 构建部署 |

### Step C: 构建功能网格

```html
<div class="feat-card cg-feat">
  <span class="feat-icon">⚡</span> 高性能<br>
  <span style="opacity: 0.6;">支持每秒 10 万请求</span>
</div>
```

最多 8 个卡片，每张对应一个经过验证的模块。

### Step D: 底部徽章

```html
<span class="glow-dot" style="background: #4CAF50;"></span>
MIT License
<span class="glow-dot" style="background: #2196F3;"></span>
跨平台
```

## 输出位置


|---|---|---|
| 1st card | `0s` | `style="animation-delay: 0s;"` |
| 2nd card | `0.05-0.12s` | `style="animation-delay: 0.05s;"` |
| 3rd card | `0.10-0.24s` | `style="animation-delay: 0.10s;"` |
| 4th card | `0.15-0.30s` | `style="animation-delay: 0.15s;"` |
| ... increment by +0.05s each | | |

---

## Validation Checklist

Before writing the welcome page, verify the source material:

- [ ] Project name is from an actual build/config file (not guessed)
- [ ] Tagline is descriptive of actual project capabilities
- [ ] Each step card maps to a real user workflow (from demos/tests)
- [ ] Each feature card corresponds to a verified module or capability
- [ ] No feature is listed that lacks evidence from Steps 2-6
- [ ] Emoji choices are thematically appropriate for the capability
- [ ] Footer badges reflect real project attributes
- [ ] Gradient colors match project brand (or defaults used)

## Output Location (relative to `WIKI_ROOT`)

- English: `content/en/0_Welcome/index.md` — always produced
- Additional languages: `content/{lang}/0_Welcome/index.md` — only for languages selected in §1 (Language Selection). Default is English only.

All language variants share the same CSS and HTML structure; only the natural language text differs. Skip any language not in the active language list.
