# 软件工程分析

## 职责

产出严谨的软件工程分析文档。使用 **PlantUML** 描绘 API 调用时序图，用 **Mermaid** 展示类层次、架构流程图，用 **KaTeX** 表达算法复杂度。

## 强制性规则

- 每一个代码片段**必须来自实际文件**，并注明文件路径和行范围
- 所有图必须通过语法验证（Mermaid/PlantUML/KaTeX）
- 禁止编造方法签名、类名或执行流
- 如果代码是推断的（无示例可用），必须用标注明确注明

## 页面规划

| 页面 | 内容 | 渲染方式 |
|---|---|---|
| `01_project_structure/index.md` | 模块地图、包依赖图 | Mermaid flowchart + 表格 |
| `02_class_hierarchy/index.md` | 核心类型、接口、继承关系 | Mermaid classDiagram |
| `03_startup_flow/index.md` | 引导序列、DI 注册 | PlantUML 时序图 |
| `04_request_lifecycle/index.md` | 请求→响应完整管道 | PlantUML 时序图 + flowchart |
| `05_api_sequences/index.md` | API 调用时序（核心业务场景） | **PlantUML** |
| `06_data_flow/index.md` | 状态变化、事件驱动、消息传递 | Mermaid flowchart |
| `07_dependencies/index.md` | 外部依赖、中间件、第三方集成 | 表格 + 架构图 |

## API 调用时序图（PlantUML）

这是本技能的**核心交付物**。对于每个核心 API 端点，产出一张 PlantUML 时序图，展示完整的调用链路。

### 基本 REST API 场景

```plantuml
@startuml
!theme plain

actor 用户 as User
participant "Controller" as Ctrl
participant "Service" as Svc
participant "Repository" as Repo
database "Database" as DB

User -> Ctrl: GET /api/users/{id}
activate Ctrl

Ctrl -> Svc: GetUserAsync(id)
activate Svc

Svc -> Repo: FindByIdAsync(id)
activate Repo

Repo -> DB: SELECT * FROM Users WHERE Id = @id
activate DB
DB --> Repo: User 实体
deactivate DB

Repo --> Svc: User?
deactivate Repo

alt 用户存在
    Svc --> Ctrl: 200 OK + User
else 用户不存在
    Svc --> Ctrl: 404 Not Found
end

Ctrl --> User: JSON 响应
deactivate Ctrl
@enduml
```

### 含中间件管道

```plantuml
@startuml
!theme plain

actor 客户端 as Client
participant "Middleware A\\n(认证)" as Auth
participant "Middleware B\\n(日志)" as Log
participant "Controller" as Ctrl
participant "Service" as Svc
collections "DbContext" as Db

Client -> Auth: HTTP 请求
activate Auth

Auth -> Auth: 验证 JWT Token
alt 令牌无效
    Auth --> Client: 401 Unauthorized
    deactivate Auth
    note right: 管道短路，不继续传递
else 令牌有效
    Auth -> Log: 转发请求
    deactivate Auth
    activate Log

    Log -> Log: 记录请求日志
    Log -> Ctrl: 调用 Action
    activate Ctrl

    Ctrl -> Svc: 执行业务逻辑
    activate Svc
    Svc -> Db: 查询/写入
    activate Db
    Db --> Svc: 结果
    deactivate Db
    Svc --> Ctrl: 业务结果
    deactivate Svc

    Ctrl --> Log: ActionResult
    deactivate Ctrl
    Log --> Client: HTTP 响应
    deactivate Log
end
@enduml
```

### 异步/事件驱动场景

```plantuml
@startuml
!theme plain

actor 用户 as User
participant "API" as Api
queue "消息队列" as MQ
participant "事件处理器" as Handler
participant "Service" as Svc
database "Database" as DB

User -> Api: POST /api/orders
activate Api
Api -> DB: 保存订单
activate DB
DB --> Api: order_id
deactivate DB
Api -> MQ: 发布 OrderCreated 事件
Api --> User: 202 Accepted + order_id
deactivate Api

== 异步处理 ==
MQ -> Handler: 消费 OrderCreated
activate Handler
Handler -> Svc: ProcessPayment(order_id)
activate Svc
Svc -> DB: 更新支付状态
activate DB
DB --> Svc: 完成
deactivate DB
Svc --> Handler: 支付结果
deactivate Svc
Handler --> MQ: ACK
deactivate Handler
@enduml
```

### PlantUML 语法验证清单

- [ ] `@startuml` / `@enduml` 成对出现
- [ ] 所有参与者（`actor` / `participant` / `database` / `queue` / `collections`）在使用前声明
- [ ] `activate` / `deactivate` 成对匹配，无遗漏
- [ ] `alt` / `else` / `end` 块结构正确
- [ ] `note right` / `note left` 有明确作用域
- [ ] `== 分隔标题 ==` 用于阶段分隔

## 类图（Mermaid）

```mermaid
classDiagram
    class IUserService {
        <<interface>>
        +GetUserAsync(int id) Task~User?~
        +CreateUserAsync(User user) Task~User~
    }
    class UserService {
        -IUserRepository _repo
        -ILogger _logger
        +GetUserAsync(int id) Task~User?~
        +CreateUserAsync(User user) Task~User~
    }
    class UserController {
        +GetUser(int id) IActionResult
        +CreateUser(CreateUserRequest req) IActionResult
    }
    IUserService <|.. UserService
    UserController --> IUserService
```

> 来源: `src/MyApp.Web/Services/UserService.cs` 第 15-45 行

## 流程图（Mermaid）

```mermaid
flowchart TD
    A[收到 HTTP 请求] --> B{认证通过？}
    B -->|否| C[返回 401]
    B -->|是| D[执行中间件管道]
    D --> E{路由匹配？}
    E -->|否| F[返回 404]
    E -->|是| G[调用 Controller]
    G --> H[执行 Action]
    H --> I[序列化 JSON]
    I --> J[返回响应]
```

## 输出位置

`content/{lang}/{Project}/architecture/`

## 写入后操作

编写软件工程分析内容后：

- [ ] **重新生成导航索引** — 运行树生成脚本（如 `python gen_tree.py`）重建 tree.json
- [ ] **构建项目** — 运行 `dotnet build` 验证新内容正确嵌入


