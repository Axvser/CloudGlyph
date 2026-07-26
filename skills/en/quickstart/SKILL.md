# Quick Start

## Responsibility

Write Quick Start guides for each functional module, showing the simplest, most declarative usage.

## Writing Principles

### Find the Simplest Entry Point

For each API, identify its simplest declarative usage:

| Pattern | Simplest (Quick Start) | Detailed (API Deep Dive) |
|---|---|---|
| Configuration | `services.AddX(opts => opts.Key = val)` | Custom `IConfigureOptions<X>` |
| Middleware | `app.UseX()` extension method | Custom `IMiddleware` implementation |
| Routing | `[Route]` + `[HttpGet]` attributes | Custom `IControllerActivator` |
| Logging | `ILogger<T>` DI injection | Custom `ILoggerProvider` |

### Example

Suppose we need to document a .NET background service Quick Start:

```markdown
### Adding a Background Service

1. Create a class that inherits `BackgroundService`:

```csharp
public class DataSyncService : BackgroundService
{
	private readonly ILogger<DataSyncService> _logger;

	public DataSyncService(ILogger<DataSyncService> logger)
	{
		_logger = logger;
	}

	protected override async Task ExecuteAsync(CancellationToken stoppingToken)
	{
		while (!stoppingToken.IsCancellationRequested)
		{
			_logger.LogInformation("Syncing data...");
			await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
		}
	}
}
```

2. Register in `Program.cs`:

```csharp
builder.Services.AddHostedService<DataSyncService>();
```
```

### Formatting Requirements

- Each step uses a code block showing complete, runnable code
- Brief explanation before code (1-3 sentences)
- Advanced patterns marked as "see API deep dive"
- Output location: `content/{lang}/{Project}/quickstart/{Module}/index.md`
