# 快速开始

## 职责

为每个功能模块编写 Quick Start 指南，展示最简单、最声明式的使用方式。

## 编写原则

### 找到最简单入口

对于每个 API，识别其最简声明式用法：

| 模式 | 最简单（Quick Start） | 详细（API Deep Dive） |
|---|---|---|
| 配置 | `services.AddX(opts => opts.Key = val)` | 自定义 `IConfigureOptions<X>` |
| 中间件 | `app.UseX()` 扩展方法 | 自定义 `IMiddleware` 实现 |
| 路由 | `[Route]` + `[HttpGet]` 属性 | 自定义 `IControllerActivator` |
| 日志 | `ILogger<T>` DI 注入 | 自定义 `ILoggerProvider` |

### 示例

假设要记录一个 .NET 后台服务的 Quick Start：

```markdown
### 添加后台服务

1. 创建继承 `BackgroundService` 的类：

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
            _logger.LogInformation("同步数据中...");
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}
```

2. 在 `Program.cs` 中注册：

```csharp
builder.Services.AddHostedService<DataSyncService>();
```
```

### 格式化要求

- 每个步骤用代码块展示完整可运行的代码
- 代码前有简短说明（1-3 句）
- 高级模式标注「详见 API 深入解读」
- 输出位置：`content/{lang}/{Project}/quickstart/{Module}/index.md`
