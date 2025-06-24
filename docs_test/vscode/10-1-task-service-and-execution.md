# Task Service and Execution

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [extensions/vscode-api-tests/src/singlefolder-tests/terminal.test.ts](extensions/vscode-api-tests/src/singlefolder-tests/terminal.test.ts)
- [extensions/vscode-api-tests/src/singlefolder-tests/workspace.tasks.test.ts](extensions/vscode-api-tests/src/singlefolder-tests/workspace.tasks.test.ts)
- [src/vs/workbench/api/browser/mainThreadTask.ts](src/vs/workbench/api/browser/mainThreadTask.ts)
- [src/vs/workbench/api/common/extHostTask.ts](src/vs/workbench/api/common/extHostTask.ts)
- [src/vs/workbench/api/common/shared/tasks.ts](src/vs/workbench/api/common/shared/tasks.ts)
- [src/vs/workbench/api/node/extHostTask.ts](src/vs/workbench/api/node/extHostTask.ts)
- [src/vs/workbench/contrib/tasks/browser/abstractTaskService.ts](src/vs/workbench/contrib/tasks/browser/abstractTaskService.ts)
- [src/vs/workbench/contrib/tasks/browser/runAutomaticTasks.ts](src/vs/workbench/contrib/tasks/browser/runAutomaticTasks.ts)
- [src/vs/workbench/contrib/tasks/browser/task.contribution.ts](src/vs/workbench/contrib/tasks/browser/task.contribution.ts)
- [src/vs/workbench/contrib/tasks/browser/taskQuickPick.ts](src/vs/workbench/contrib/tasks/browser/taskQuickPick.ts)
- [src/vs/workbench/contrib/tasks/browser/taskService.ts](src/vs/workbench/contrib/tasks/browser/taskService.ts)
- [src/vs/workbench/contrib/tasks/browser/taskTerminalStatus.ts](src/vs/workbench/contrib/tasks/browser/taskTerminalStatus.ts)
- [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts](src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts)
- [src/vs/workbench/contrib/tasks/common/jsonSchema_v2.ts](src/vs/workbench/contrib/tasks/common/jsonSchema_v2.ts)
- [src/vs/workbench/contrib/tasks/common/problemCollectors.ts](src/vs/workbench/contrib/tasks/common/problemCollectors.ts)
- [src/vs/workbench/contrib/tasks/common/taskConfiguration.ts](src/vs/workbench/contrib/tasks/common/taskConfiguration.ts)
- [src/vs/workbench/contrib/tasks/common/taskService.ts](src/vs/workbench/contrib/tasks/common/taskService.ts)
- [src/vs/workbench/contrib/tasks/common/taskSystem.ts](src/vs/workbench/contrib/tasks/common/taskSystem.ts)
- [src/vs/workbench/contrib/tasks/common/tasks.ts](src/vs/workbench/contrib/tasks/common/tasks.ts)
- [src/vs/workbench/contrib/tasks/electron-browser/taskService.ts](src/vs/workbench/contrib/tasks/electron-browser/taskService.ts)
- [src/vs/workbench/contrib/tasks/test/browser/taskTerminalStatus.test.ts](src/vs/workbench/contrib/tasks/test/browser/taskTerminalStatus.test.ts)

</details>



This document covers the task execution system in VS Code, focusing on how tasks are discovered, resolved, and executed. This includes the core task service architecture, the terminal-based execution engine, task lifecycle management, and integration with extensions.

For information about task configuration schemas and problem matchers, see [Task System](#10). For terminal integration details, see [Integrated Terminal](#5).

## Architecture Overview

The task execution system is built around a layered architecture with clear separation between task management, execution engines, and extension integration.

### Core Service Architecture

```mermaid
graph TB
    subgraph "Task Service Layer"
        AbstractTaskService["AbstractTaskService"]
        ITaskService["ITaskService"]
        TaskQuickPick["TaskQuickPick"]
    end
    
    subgraph "Execution Layer" 
        TerminalTaskSystem["TerminalTaskSystem"]
        ITaskSystem["ITaskSystem"]
        TaskTerminalStatus["TaskTerminalStatus"]
    end
    
    subgraph "Extension Integration"
        ExtHostTask["ExtHostTask"]
        MainThreadTask["MainThreadTask"]
        TaskProvider["ITaskProvider"]
    end
    
    subgraph "Configuration Layer"
        TaskConfiguration["TaskConfiguration"]
        ProblemMatcher["ProblemMatcher"]
        TaskDefinitionRegistry["TaskDefinitionRegistry"]
    end
    
    AbstractTaskService --> TerminalTaskSystem
    AbstractTaskService --> TaskQuickPick
    TerminalTaskSystem --> TaskTerminalStatus
    ExtHostTask --> MainThreadTask
    MainThreadTask --> AbstractTaskService
    AbstractTaskService --> TaskProvider
    AbstractTaskService --> TaskConfiguration
    TerminalTaskSystem --> ProblemMatcher
```

Sources: [src/vs/workbench/contrib/tasks/browser/abstractTaskService.ts:197-395](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:142-258](), [src/vs/workbench/contrib/tasks/common/taskService.ts:64-108]()

### Task Type Hierarchy

```mermaid
graph TB
    Task["Task (base)"]
    ContributedTask["ContributedTask"]
    CustomTask["CustomTask"] 
    ConfiguringTask["ConfiguringTask"]
    InMemoryTask["InMemoryTask"]
    
    Task --> ContributedTask
    Task --> CustomTask
    Task --> ConfiguringTask
    Task --> InMemoryTask
    
    subgraph "Execution Types"
        ShellExecution["ShellExecution"]
        ProcessExecution["ProcessExecution"] 
        CustomExecution["CustomExecution"]
    end
    
    Task --> ShellExecution
    Task --> ProcessExecution
    Task --> CustomExecution
```

Sources: [src/vs/workbench/contrib/tasks/common/tasks.ts:889-1200](), [src/vs/workbench/contrib/tasks/common/tasks.ts:290-317]()

## Task Lifecycle Management

### Task Discovery and Resolution

The task system discovers tasks from multiple sources and resolves them through a multi-stage process:

| Stage | Component | Description |
|-------|-----------|-------------|
| Discovery | `AbstractTaskService.getWorkspaceTasks()` | Scans workspace for task configurations |
| Provider Integration | `ITaskProvider.provideTasks()` | Collects tasks from extensions |
| Variable Resolution | `TerminalTaskSystem._resolveVariablesFromSet()` | Resolves variables like `${workspaceFolder}` |
| Dependency Resolution | `TerminalTaskSystem._executeTask()` | Handles task dependencies |
| Execution | `TerminalTaskSystem.run()` | Executes the task in a terminal |

```mermaid
sequenceDiagram
    participant User
    participant AbstractTaskService
    participant TaskProvider
    participant TerminalTaskSystem
    participant Terminal
    
    User->>AbstractTaskService: run(task)
    AbstractTaskService->>TaskProvider: provideTasks()
    TaskProvider-->>AbstractTaskService: tasks[]
    AbstractTaskService->>TerminalTaskSystem: run(task, resolver)
    TerminalTaskSystem->>TerminalTaskSystem: _resolveVariablesFromSet()
    TerminalTaskSystem->>TerminalTaskSystem: _executeTask()
    TerminalTaskSystem->>Terminal: createTerminal()
    Terminal-->>TerminalTaskSystem: terminal instance
    TerminalTaskSystem-->>AbstractTaskService: ITaskExecuteResult
    AbstractTaskService-->>User: TaskExecution
```

Sources: [src/vs/workbench/contrib/tasks/browser/abstractTaskService.ts:794-873](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:276-308](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:517-603]()

### Task Execution States

Tasks progress through defined states during execution, tracked by the `TaskEventKind` enum:

```mermaid
stateDiagram-v2
    [*] --> Start: "TaskEventKind.Start"
    Start --> AcquiredInput: "TaskEventKind.AcquiredInput" 
    AcquiredInput --> DependsOnStarted: "TaskEventKind.DependsOnStarted"
    DependsOnStarted --> Active: "TaskEventKind.Active"
    Active --> ProcessStarted: "TaskEventKind.ProcessStarted"
    ProcessStarted --> ProcessEnded: "TaskEventKind.ProcessEnded"
    ProcessEnded --> Inactive: "TaskEventKind.Inactive"
    ProcessStarted --> Terminated: "TaskEventKind.Terminated"
    Inactive --> [*]
    Terminated --> [*]
```

Sources: [src/vs/workbench/contrib/tasks/common/tasks.ts:1301-1330](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:446-454]()

## Terminal Task System

The `TerminalTaskSystem` is the primary execution engine that runs tasks in VS Code's integrated terminals.

### Execution Flow

The execution process involves several key components working together:

```mermaid
graph LR
    subgraph "Pre-Execution"
        VerifiedTask["VerifiedTask"]
        VariableResolver["VariableResolver"]
        DependencyResolver["DependencyResolver"]
    end
    
    subgraph "Execution Core"
        TerminalCreation["Terminal Creation"]
        ShellLaunchConfig["IShellLaunchConfig"]
        ProcessExecution["Process Execution"]
    end
    
    subgraph "Monitoring"
        ProblemCollector["ProblemCollector"]
        TaskTerminalStatus["TaskTerminalStatus"]
        ProgressTracking["Progress Tracking"]
    end
    
    VerifiedTask --> VariableResolver
    VariableResolver --> DependencyResolver
    DependencyResolver --> TerminalCreation
    TerminalCreation --> ShellLaunchConfig
    ShellLaunchConfig --> ProcessExecution
    ProcessExecution --> ProblemCollector
    ProcessExecution --> TaskTerminalStatus
    ProblemCollector --> ProgressTracking
```

Sources: [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:110-140](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:676-689](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:712-779]()

### Key Execution Classes

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `TerminalTaskSystem` | Main execution engine | `run()`, `_executeTask()`, `terminate()` |
| `VerifiedTask` | Validated task ready for execution | `verify()`, `getVerifiedTask()` |
| `VariableResolver` | Resolves task variables | `resolve()`, `_replacer()` |
| `TaskTerminalStatus` | Terminal status management | `addTerminal()`, `eventActive()` |

### Terminal Management

The system maintains several data structures to track active terminals and tasks:

```typescript
// From TerminalTaskSystem class
private _activeTasks: IStringDictionary<IActiveTerminalData>
private _terminals: IStringDictionary<ITerminalData>
private _idleTaskTerminals: LinkedMap<string, string>
private _sameTaskTerminals: IStringDictionary<string>
```

Sources: [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:184-191](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:55-78]()

## Task Configuration and Providers

### Task Provider System

Extensions register task providers through the `ITaskProvider` interface to contribute tasks:

```mermaid
graph TB
    subgraph "Extension Host"
        ExtHostTask["ExtHostTask"]
        TaskProvider["TaskProvider"]
        ExtensionAPI["Extension API"]
    end
    
    subgraph "Main Thread"
        MainThreadTask["MainThreadTask"]
        AbstractTaskService["AbstractTaskService"]
        TaskDefinitionRegistry["TaskDefinitionRegistry"]
    end
    
    ExtensionAPI --> TaskProvider
    TaskProvider --> ExtHostTask
    ExtHostTask --> MainThreadTask
    MainThreadTask --> AbstractTaskService
    TaskDefinitionRegistry --> AbstractTaskService
    
    AbstractTaskService --> TaskExecution["Task Execution"]
```

Sources: [src/vs/workbench/api/common/extHostTask.ts:34-51](), [src/vs/workbench/api/browser/mainThreadTask.ts:484-520](), [src/vs/workbench/contrib/tasks/browser/abstractTaskService.ts:727-744]()

### Task Resolution Process

Task resolution involves multiple phases to transform raw task definitions into executable tasks:

```mermaid
sequenceDiagram
    participant Extension
    participant ExtHostTask
    participant MainThreadTask
    participant AbstractTaskService
    participant TerminalTaskSystem
    
    Extension->>ExtHostTask: registerTaskProvider()
    ExtHostTask->>MainThreadTask: $registerTaskProvider()
    
    Note over AbstractTaskService: User requests task execution
    
    AbstractTaskService->>MainThreadTask: getTaskProvider()
    MainThreadTask->>ExtHostTask: $provideTasks()
    ExtHostTask->>Extension: provideTasks()
    Extension-->>ExtHostTask: Task[]
    ExtHostTask-->>MainThreadTask: TaskDTO[]
    MainThreadTask-->>AbstractTaskService: Task[]
    
    AbstractTaskService->>TerminalTaskSystem: run(task)
    TerminalTaskSystem->>TerminalTaskSystem: _resolveVariablesFromSet()
    TerminalTaskSystem-->>AbstractTaskService: ITaskExecuteResult
```

Sources: [src/vs/workbench/api/common/extHostTask.ts:95-122](), [src/vs/workbench/api/browser/mainThreadTask.ts:521-580](), [src/vs/workbench/contrib/tasks/browser/abstractTaskService.ts:1264-1320]()

## Task Dependencies and Problem Matching

### Dependency Execution

Tasks can depend on other tasks, executed either in parallel or sequence:

```mermaid
graph TB
    subgraph "Task A (Main)"
        TaskA_Start["Start"]
        TaskA_Deps["Check Dependencies"]
        TaskA_Execute["Execute"]
        TaskA_End["Complete"]
    end
    
    subgraph "Dependencies"
        TaskB["Task B"]
        TaskC["Task C"]
        TaskD["Task D"]
    end
    
    TaskA_Start --> TaskA_Deps
    TaskA_Deps --> TaskB
    TaskA_Deps --> TaskC
    TaskA_Deps --> TaskD
    
    TaskB --> TaskA_Execute
    TaskC --> TaskA_Execute
    TaskD --> TaskA_Execute
    TaskA_Execute --> TaskA_End
    
    subgraph "Execution Order"
        Parallel["DependsOrder.parallel"]
        Sequence["DependsOrder.sequence"]
    end
```

Sources: [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:528-577](), [src/vs/workbench/contrib/tasks/common/tasks.ts:492-495]()

### Problem Matcher Integration

Problem matchers parse task output to identify and report issues:

| Component | Purpose |
|-----------|---------|
| `StartStopProblemCollector` | Handles problem matching for finite tasks |
| `WatchingProblemCollector` | Handles problem matching for background/watching tasks |
| `ProblemMatcherRegistry` | Registry of available problem matchers |

```mermaid
graph LR
    TaskOutput["Task Terminal Output"]
    ProblemMatcher["Problem Matcher"]
    MarkerService["IMarkerService"]
    ProblemsPanel["Problems Panel"]
    
    TaskOutput --> ProblemMatcher
    ProblemMatcher --> MarkerService
    MarkerService --> ProblemsPanel
    
    subgraph "Problem Collector Types"
        StartStop["StartStopProblemCollector"]
        Watching["WatchingProblemCollector"]
    end
    
    ProblemMatcher --> StartStop
    ProblemMatcher --> Watching
```

Sources: [src/vs/workbench/contrib/tasks/common/problemCollectors.ts:38-94](), [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:1188-1254]()

## Integration Points

### Extension API Surface

The task system exposes a comprehensive API for extensions:

| API Component | Purpose | Key Methods |
|---------------|---------|-------------|
| `tasks.registerTaskProvider()` | Register task providers | Extension registration |
| `tasks.executeTask()` | Execute tasks programmatically | Task execution |
| `tasks.fetchTasks()` | Get available tasks | Task discovery |
| `tasks.onDidStartTask` | Task lifecycle events | Event handling |

### Terminal Integration

Tasks integrate deeply with the terminal system for execution and status display:

```mermaid
graph TB
    subgraph "Terminal Integration"
        ITerminalService["ITerminalService"]
        ITerminalInstance["ITerminalInstance"]
        TerminalStatusList["TerminalStatusList"]
        TaskTerminalStatus["TaskTerminalStatus"]
    end
    
    subgraph "Task System"
        TerminalTaskSystem["TerminalTaskSystem"]
        AbstractTaskService["AbstractTaskService"]
    end
    
    TerminalTaskSystem --> ITerminalService
    ITerminalService --> ITerminalInstance
    ITerminalInstance --> TerminalStatusList
    TaskTerminalStatus --> TerminalStatusList
    TerminalTaskSystem --> TaskTerminalStatus
```

Sources: [src/vs/workbench/contrib/tasks/browser/terminalTaskSystem.ts:221-257](), [src/vs/workbench/contrib/tasks/browser/taskTerminalStatus.ts:40-68](), [extensions/vscode-api-tests/src/singlefolder-tests/workspace.tasks.test.ts:26-144]()