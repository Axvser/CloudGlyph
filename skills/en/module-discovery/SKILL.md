# Module Discovery

## Responsibility

Discover all functional modules and their responsibility boundaries, providing the inventory for subsequent Quick Start, API documentation, and software engineering analysis

## Workflow

### 1. Assess Project Type

First determine the nature of [Project_Root]:
- **Small/Medium project** (clear directory layout, enumerable project files) → follow steps 2→3→4 in order
- **Large framework/product/platform** (deep directories, many project files, directory structure alone doesn't reveal functional boundaries) → **use Demo/Tests as the driver**:
  > Prioritize scanning Examples/, samples/, tests/ directories, inferring functional modules from actual usage patterns;
  > Use namespaces, class names, and API calls found in test files and Demo code to deduce functional boundaries;
  > Then cross-verify against the directory structure, rather than starting from it.

### 2. Scan Project Structure

List all projects/directories under [Project_Root] and read each project's definition file:

```
# .NET example
Solution: MyApp.slnx
├── src/MyApp.Core/          ← Class library
│   └── MyApp.Core.csproj
├── src/MyApp.Web/           ← Web application
│   └── MyApp.Web.csproj
└── tests/MyApp.Tests/       ← Test project
	└── MyApp.Tests.csproj
```

> For large projects, this step is supplementary validation — the primary module list comes from Demo/Test analysis.

### 3. Identify Module Responsibilities

For each project, read its internal directory structure and representative files:

```
# Read MyApp.Web's Controllers/ directory
# Confirms this is an ASP.NET Core Web API module
# Purpose: Provides RESTful API endpoints
```

**Critical: Also check for Demo/Example and Test projects related to each module.** These reveal the actual API surface and idiomatic usage patterns:

```
# Examples/MyApp.Web/ contains a working REST API demo
# → Extract endpoint patterns, middleware setup, DI registration

# tests/MyApp.Web.Tests/ has controller tests
# → Extract request construction, status code assertions
```

> For large projects, Demo and Tests are the primary means of identifying functional modules — do not rely solely on directory names to infer functionality.

### 4. Map Dependencies

Read ProjectReference and PackageReference from `.csproj` / equivalent files:

```xml
<ItemGroup>
  <ProjectReference Include="..\MyApp.Core\MyApp.Core.csproj" />
  <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
</ItemGroup>
```

### 5. Generate Module Responsibility Table

| Module | Type | Responsibility | Dependencies |
|---|---|---|---|
| MyApp.Core | Class Library | Domain models, business logic | None |
| MyApp.Web | Web Application | REST API, middleware | MyApp.Core, Serilog |
| MyApp.Tests | Tests | Unit tests, integration tests | xUnit, MyApp.Core |

## Output

- Complete module list (name, path, type) with nature annotation (directory-driven / Demo-Test-driven)
- Confirmed responsibility for each module (based on file content or Demo/Test usage patterns, not guesswork)
- Inter-project dependency graph
