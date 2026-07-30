# 功能模块发现

## 职责

发现所有功能模块及其职责边界，为后续编写 Quick Start、API 文档和软件工程分析提供清单

## 操作流程

### 1. 判断项目类型

首先判断[Project_Root]的性质：
- **小型/中型项目**（有明确目录结构、项目文件可枚举）→ 按下方 2→3→4 顺序执行
- **大型框架/产品/平台**（目录层级深、项目文件多、仅看目录无法理解功能边界）→ **以 Demo/测试为驱动**：
  > 优先扫描 Examples/、samples/、tests/ 目录，从实际使用模式反推功能模块；
  > 用测试文件和 Demo 代码中的命名空间、类名、API 调用来推断功能边界；
  > 再回头与目录结构交叉验证，而非从目录结构出发。

### 2. 扫描项目结构

列出[Project_Root]下所有项目/目录，读取每个项目的定义文件：

```
# .NET 示例
Solution: MyApp.slnx
├── src/MyApp.Core/          ← 类库
│   └── MyApp.Core.csproj
├── src/MyApp.Web/           ← Web 应用
│   └── MyApp.Web.csproj
└── tests/MyApp.Tests/       ← 测试项目
    └── MyApp.Tests.csproj
```

> 注：大型项目此步仅作辅助验证，主要功能列表来源于 Demo/测试分析。

### 3. 识别模块职责

对每个项目，读取其内部目录结构和代表性文件：

```
# 读取 MyApp.Web 的 Controllers/ 目录
# 确认这是一个 ASP.NET Core Web API 模块
# 功能：提供 RESTful API 端点
```

**关键：同时检查与该模块相关的 Demo/示例和测试项目。** 这些揭示了实际的 API 表面和惯用使用模式：

```
# Examples/MyApp.Web/ 包含可运行的 REST API Demo
# → 提取端点模式、中间件配置、DI 注册

# tests/MyApp.Web.Tests/ 包含控制器测试
# → 提取请求构造、状态码断言
```

> 对于大型项目，Demo 和测试是识别功能模块的主要手段——不要仅依赖目录名推测功能。

### 4. 梳理依赖关系

读取 `.csproj` / 等效文件中的 ProjectReference 和 PackageReference：

```xml
<ItemGroup>
  <ProjectReference Include="..\MyApp.Core\MyApp.Core.csproj" />
  <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
</ItemGroup>
```

### 5. 生成模块职责表

| 模块 | 类型 | 职责 | 依赖 |
|---|---|---|---|
| MyApp.Core | 类库 | 领域模型、业务逻辑 | 无 |
| MyApp.Web | Web 应用 | REST API、中间件 | MyApp.Core, Serilog |
| MyApp.Tests | 测试 | 单元测试、集成测试 | xUnit, MyApp.Core |

## 输出

- 完整的模块列表（名称、路径、类型）及性质标注（目录驱动 / Demo-测试驱动）
- 每个模块的确认职责（基于文件内容或 Demo/测试使用模式，非猜测）
- 项目间依赖图
