# Software Engineering Analysis

## Responsibility

Produce rigorous software engineering analysis documentation. Use **PlantUML** for API call sequence diagrams, **Mermaid** for class hierarchies and architecture flowcharts, and **KaTeX** for algorithm complexity.

## Mandatory Rules

- Every code snippet **must come from an actual file**, with file path and line range noted
- All diagrams must pass syntax validation (Mermaid/PlantUML/KaTeX)
- Do not fabricate method signatures, class names, or execution flows
- If code is inferred (no example available), it must be explicitly marked as such

## Page Plan

| Page | Content | Rendering |
|---|---|---|
| `01_project_structure/index.md` | Module map, package dependency graph | Mermaid flowchart + tables |
| `02_class_hierarchy/index.md` | Core types, interfaces, inheritance | Mermaid classDiagram |
| `03_startup_flow/index.md` | Bootstrap sequence, DI registration | PlantUML sequence diagram |
| `04_request_lifecycle/index.md` | Request→response full pipeline | PlantUML sequence + flowchart |
| `05_api_sequences/index.md` | API call sequences (core business scenarios) | **PlantUML** |
| `06_data_flow/index.md` | State changes, event-driven, messaging | Mermaid flowchart |
| `07_dependencies/index.md` | External dependencies, middleware, third-party | Tables + architecture diagram |

## API Call Sequence Diagrams (PlantUML)

This is the **core deliverable** of this skill. For each core API endpoint, produce a PlantUML sequence diagram showing the complete call chain.

### Basic REST API Scenario

```plantuml
@startuml
!theme plain

actor User as User
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
DB --> Repo: User entity
deactivate DB

Repo --> Svc: User?
deactivate Repo

alt User exists
	Svc --> Ctrl: 200 OK + User
else User not found
	Svc --> Ctrl: 404 Not Found
end

Ctrl --> User: JSON response
deactivate Ctrl
@enduml
```

### With Middleware Pipeline

```plantuml
@startuml
!theme plain

actor Client as Client
participant "Middleware A\\n(Auth)" as Auth
participant "Middleware B\\n(Logging)" as Log
participant "Controller" as Ctrl
participant "Service" as Svc
collections "DbContext" as Db

Client -> Auth: HTTP Request
activate Auth

Auth -> Auth: Validate JWT Token
alt Invalid token
	Auth --> Client: 401 Unauthorized
	deactivate Auth
	note right: Pipeline short-circuits
else Valid token
	Auth -> Log: Forward request
	deactivate Auth
	activate Log

	Log -> Log: Log request
	Log -> Ctrl: Invoke Action
	activate Ctrl

	Ctrl -> Svc: Execute business logic
	activate Svc
	Svc -> Db: Query/Write
	activate Db
	Db --> Svc: Result
	deactivate Db
	Svc --> Ctrl: Business result
	deactivate Svc

	Ctrl --> Log: ActionResult
	deactivate Ctrl
	Log --> Client: HTTP Response
	deactivate Log
end
@enduml
```

### Async/Event-Driven Scenario

```plantuml
@startuml
!theme plain

actor User as User
participant "API" as Api
queue "Message Queue" as MQ
participant "Event Handler" as Handler
participant "Service" as Svc
database "Database" as DB

User -> Api: POST /api/orders
activate Api
Api -> DB: Save order
activate DB
DB --> Api: order_id
deactivate DB
Api -> MQ: Publish OrderCreated event
Api --> User: 202 Accepted + order_id
deactivate Api

== Async Processing ==
MQ -> Handler: Consume OrderCreated
activate Handler
Handler -> Svc: ProcessPayment(order_id)
activate Svc
Svc -> DB: Update payment status
activate DB
DB --> Svc: Done
deactivate DB
Svc --> Handler: Payment result
deactivate Svc
Handler --> MQ: ACK
deactivate Handler
@enduml
```

### PlantUML Syntax Validation Checklist

- [ ] `@startuml` / `@enduml` are paired
- [ ] All participants (`actor` / `participant` / `database` / `queue` / `collections`) are declared before use
- [ ] `activate` / `deactivate` are paired with no omissions
- [ ] `alt` / `else` / `end` block structure is correct
- [ ] `note right` / `note left` have clear scope
- [ ] `== Section Title ==` is used for phase separation

## Class Diagram (Mermaid)

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

> Source: `src/MyApp.Web/Services/UserService.cs` lines 15-45

## Flowchart (Mermaid)

```mermaid
flowchart TD
	A[Receive HTTP Request] --> B{Auth Passed?}
	B -->|No| C[Return 401]
	B -->|Yes| D[Execute Middleware Pipeline]
	D --> E{Route Matched?}
	E -->|No| F[Return 404]
	E -->|Yes| G[Invoke Controller]
	G --> H[Execute Action]
	H --> I[Serialize JSON]
	I --> J[Return Response]
```

## Output Location

`content/{lang}/{Project}/architecture/`

## Post-Write Action

After writing SE Analysis content:

- [ ] **Regenerate navigation index** — Run the tree generator script (e.g. `python gen_tree.py`) to rebuild tree.json
- [ ] **Build the project** — Run `dotnet build` to verify the new content embeds correctly
