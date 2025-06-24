# Source Control Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [extensions/git/package.json](extensions/git/package.json)
- [extensions/git/package.nls.json](extensions/git/package.nls.json)
- [extensions/git/src/actionButton.ts](extensions/git/src/actionButton.ts)
- [extensions/git/src/api/api1.ts](extensions/git/src/api/api1.ts)
- [extensions/git/src/api/extension.ts](extensions/git/src/api/extension.ts)
- [extensions/git/src/api/git.d.ts](extensions/git/src/api/git.d.ts)
- [extensions/git/src/askpass-empty.sh](extensions/git/src/askpass-empty.sh)
- [extensions/git/src/askpass-main.ts](extensions/git/src/askpass-main.ts)
- [extensions/git/src/askpass.sh](extensions/git/src/askpass.sh)
- [extensions/git/src/askpass.ts](extensions/git/src/askpass.ts)
- [extensions/git/src/autofetch.ts](extensions/git/src/autofetch.ts)
- [extensions/git/src/commands.ts](extensions/git/src/commands.ts)
- [extensions/git/src/git.ts](extensions/git/src/git.ts)
- [extensions/git/src/gitEditor.ts](extensions/git/src/gitEditor.ts)
- [extensions/git/src/historyProvider.ts](extensions/git/src/historyProvider.ts)
- [extensions/git/src/ipc/ipcClient.ts](extensions/git/src/ipc/ipcClient.ts)
- [extensions/git/src/ipc/ipcServer.ts](extensions/git/src/ipc/ipcServer.ts)
- [extensions/git/src/main.ts](extensions/git/src/main.ts)
- [extensions/git/src/model.ts](extensions/git/src/model.ts)
- [extensions/git/src/postCommitCommands.ts](extensions/git/src/postCommitCommands.ts)
- [extensions/git/src/repository.ts](extensions/git/src/repository.ts)
- [extensions/git/src/ssh-askpass-empty.sh](extensions/git/src/ssh-askpass-empty.sh)
- [extensions/git/src/ssh-askpass.sh](extensions/git/src/ssh-askpass.sh)
- [extensions/git/src/statusbar.ts](extensions/git/src/statusbar.ts)
- [extensions/git/src/terminal.ts](extensions/git/src/terminal.ts)
- [extensions/git/src/test/git.test.ts](extensions/git/src/test/git.test.ts)
- [extensions/git/src/util.ts](extensions/git/src/util.ts)
- [extensions/git/tsconfig.json](extensions/git/tsconfig.json)
- [src/vs/workbench/api/browser/mainThreadSCM.ts](src/vs/workbench/api/browser/mainThreadSCM.ts)
- [src/vs/workbench/api/common/extHostSCM.ts](src/vs/workbench/api/common/extHostSCM.ts)
- [src/vs/workbench/contrib/scm/browser/activity.ts](src/vs/workbench/contrib/scm/browser/activity.ts)
- [src/vs/workbench/contrib/scm/browser/media/scm.css](src/vs/workbench/contrib/scm/browser/media/scm.css)
- [src/vs/workbench/contrib/scm/browser/menus.ts](src/vs/workbench/contrib/scm/browser/menus.ts)
- [src/vs/workbench/contrib/scm/browser/scm.contribution.ts](src/vs/workbench/contrib/scm/browser/scm.contribution.ts)
- [src/vs/workbench/contrib/scm/browser/scmHistory.ts](src/vs/workbench/contrib/scm/browser/scmHistory.ts)
- [src/vs/workbench/contrib/scm/browser/scmHistoryViewPane.ts](src/vs/workbench/contrib/scm/browser/scmHistoryViewPane.ts)
- [src/vs/workbench/contrib/scm/browser/scmRepositoriesViewPane.ts](src/vs/workbench/contrib/scm/browser/scmRepositoriesViewPane.ts)
- [src/vs/workbench/contrib/scm/browser/scmRepositoryRenderer.ts](src/vs/workbench/contrib/scm/browser/scmRepositoryRenderer.ts)
- [src/vs/workbench/contrib/scm/browser/scmViewPane.ts](src/vs/workbench/contrib/scm/browser/scmViewPane.ts)
- [src/vs/workbench/contrib/scm/browser/scmViewService.ts](src/vs/workbench/contrib/scm/browser/scmViewService.ts)
- [src/vs/workbench/contrib/scm/browser/util.ts](src/vs/workbench/contrib/scm/browser/util.ts)
- [src/vs/workbench/contrib/scm/common/history.ts](src/vs/workbench/contrib/scm/common/history.ts)
- [src/vs/workbench/contrib/scm/common/scm.ts](src/vs/workbench/contrib/scm/common/scm.ts)
- [src/vs/workbench/contrib/scm/test/browser/scmHistory.test.ts](src/vs/workbench/contrib/scm/test/browser/scmHistory.test.ts)
- [src/vscode-dts/vscode.proposed.scmHistoryProvider.d.ts](src/vscode-dts/vscode.proposed.scmHistoryProvider.d.ts)

</details>



This document covers VS Code's Source Control Management (SCM) system, which provides a generic framework for integrating version control systems like Git into the editor. The SCM system consists of a core framework that defines common abstractions for source control providers, along with built-in implementations like the Git extension.

For information about the Extension System that enables third-party SCM providers, see [Extension System](#4). For details about UI Components like Trees and Lists used in SCM views, see [UI Components: Lists and Trees](#2.3).

## SCM Framework Architecture

The SCM framework provides a provider-based architecture where different version control systems can register providers that implement common interfaces. The core abstractions include repositories, resource groups, resources, and input boxes for commit messages.

```mermaid
graph TB
    subgraph "SCM Core Framework"
        ISCMService["ISCMService<br/>scmService.ts"]
        ISCMViewService["ISCMViewService<br/>scmViewService.ts"]
        ISCMProvider["ISCMProvider<br/>interface"]
        ISCMRepository["ISCMRepository<br/>interface"]
    end
    
    subgraph "UI Layer"
        SCMViewPane["SCMViewPane<br/>scmViewPane.ts"]
        SCMHistoryViewPane["SCMHistoryViewPane<br/>scmHistoryViewPane.ts"]
        SCMRepositoriesViewPane["SCMRepositoriesViewPane<br/>scmRepositoriesViewPane.ts"]
    end
    
    subgraph "Extension API"
        MainThreadSCM["MainThreadSCM<br/>mainThreadSCM.ts"]
        ExtHostSCM["ExtHostSCM<br/>extHostSCM.ts"]
    end
    
    subgraph "Git Extension"
        GitExtension["Git Extension<br/>main.ts"]
        Repository["Repository<br/>repository.ts"]
        GitHistoryProvider["GitHistoryProvider<br/>historyProvider.ts"]
    end
    
    ISCMService --> ISCMProvider
    ISCMProvider --> ISCMRepository
    ISCMViewService --> SCMViewPane
    ISCMViewService --> SCMHistoryViewPane
    ISCMViewService --> SCMRepositoriesViewPane
    
    MainThreadSCM --> ISCMService
    ExtHostSCM --> MainThreadSCM
    
    GitExtension --> ExtHostSCM
    Repository --> ISCMRepository
    GitHistoryProvider --> Repository
```

The `ISCMService` acts as the central registry for SCM providers, while `ISCMViewService` manages the visual presentation of source control information. Each provider implements `ISCMProvider` and can create multiple `ISCMRepository` instances.

Sources: [src/vs/workbench/contrib/scm/common/scm.ts:34-200](), [src/vs/workbench/contrib/scm/common/scmService.ts](), [src/vs/workbench/contrib/scm/browser/scmViewService.ts]()

## SCM Provider Interface

The `ISCMProvider` interface defines the contract that all source control providers must implement. It includes methods for managing repositories, handling input validation, and providing commands.

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| `ISCMProvider` | Core provider interface | `getOriginalResource()`, `createRepository()` |
| `ISCMRepository` | Repository abstraction | `provider`, `input`, `resourceGroups` |
| `ISCMResourceGroup` | Groups of related resources | `id`, `label`, `resourceStates` |
| `ISCMResource` | Individual file resources | `resourceUri`, `command`, `decorations` |
| `ISCMInput` | Commit message input | `value`, `placeholder`, `validateInput()` |

The provider system supports features like input validation, action buttons, and history providers through optional interfaces.

Sources: [src/vs/workbench/contrib/scm/common/scm.ts:92-180]()

## Git Extension Implementation

The Git extension serves as the primary implementation of the SCM framework, providing comprehensive Git functionality within VS Code.

```mermaid
graph TB
    subgraph "Git Extension Core"
        GitMain["main.ts<br/>Extension Entry"]
        Model["Model<br/>model.ts"]
        CommandCenter["CommandCenter<br/>commands.ts"]
    end
    
    subgraph "Git Operations"
        Git["Git<br/>git.ts"]
        Repository["Repository<br/>repository.ts"]
        GitHistoryProvider["GitHistoryProvider<br/>historyProvider.ts"]
    end
    
    subgraph "Resource Management"
        Resource["Resource<br/>repository.ts:49-333"]
        ResourceCommandResolver["ResourceCommandResolver<br/>repository.ts:491-602"]
        GitResourceGroup["GitResourceGroup<br/>repository.ts:335-337"]
    end
    
    subgraph "UI Components"
        ActionButton["ActionButton<br/>actionButton.ts"]
        StatusBar["StatusBarCommands<br/>statusbar.ts"]
        ProgressManager["ProgressManager<br/>repository.ts:346-404"]
    end
    
    GitMain --> Model
    GitMain --> CommandCenter
    Model --> Repository
    Repository --> Git
    Repository --> GitHistoryProvider
    Repository --> Resource
    Resource --> ResourceCommandResolver
    Repository --> GitResourceGroup
    Repository --> ActionButton
    Repository --> StatusBar
    Repository --> ProgressManager
```

The Git extension creates a `Repository` instance for each Git repository, which implements the `ISCMRepository` interface and manages resource states, commands, and history.

Sources: [extensions/git/src/main.ts:39-150](), [extensions/git/src/model.ts:174-550](), [extensions/git/src/repository.ts:1-50]()

## Git Repository Model

The `Repository` class is the core of Git integration, managing repository state and providing Git operations through the SCM framework.

```mermaid
graph TB
    subgraph "Repository State"
        RepositoryState["RepositoryState<br/>enum"]
        HEAD["HEAD<br/>Branch"]
        Refs["refs<br/>Ref[]"]
        Remotes["remotes<br/>Remote[]"]
    end
    
    subgraph "Resource Groups"
        MergeGroup["mergeGroup<br/>ResourceGroupType.Merge"]
        IndexGroup["indexGroup<br/>ResourceGroupType.Index"]
        WorkingTreeGroup["workingTreeGroup<br/>ResourceGroupType.WorkingTree"]
        UntrackedGroup["untrackedGroup<br/>ResourceGroupType.Untracked"]
    end
    
    subgraph "Operations"
        OperationManager["OperationManager<br/>operation.ts"]
        AutoFetcher["AutoFetcher<br/>autofetch.ts"]
        FileWatcher["DotGitWatcher<br/>repository.ts:439-489"]
    end
    
    subgraph "UI Integration"
        SourceControl["SourceControl<br/>VS Code API"]
        QuickDiffProvider["QuickDiffProvider<br/>interface"]
        FileDecorationProvider["FileDecorationProvider<br/>interface"]
    end
    
    RepositoryState --> HEAD
    RepositoryState --> Refs
    RepositoryState --> Remotes
    
    MergeGroup --> Resource
    IndexGroup --> Resource
    WorkingTreeGroup --> Resource
    UntrackedGroup --> Resource
    
    OperationManager --> Git
    AutoFetcher --> Git
    FileWatcher --> Repository
    
    Repository --> SourceControl
    Repository --> QuickDiffProvider
    Repository --> FileDecorationProvider
```

Each `Repository` maintains four resource groups that categorize files by their Git status, and provides operations through the `OperationManager` to ensure thread safety.

Sources: [extensions/git/src/repository.ts:37-47](), [extensions/git/src/repository.ts:603-1500](), [extensions/git/src/operation.ts]()

## SCM View Components

The SCM UI consists of multiple view panes that present source control information in different ways.

```mermaid
graph TB
    subgraph "Main SCM View"
        SCMViewPane["SCMViewPane<br/>scmViewPane.ts"]
        InputRenderer["InputRenderer<br/>scmViewPane.ts:299-421"]
        ResourceGroupRenderer["ResourceGroupRenderer<br/>scmViewPane.ts:431-490"]
        ResourceRenderer["ResourceRenderer<br/>scmViewPane.ts:532-800"]
    end
    
    subgraph "Repository Management"
        SCMRepositoriesViewPane["SCMRepositoriesViewPane<br/>scmRepositoriesViewPane.ts"]
        RepositoryRenderer["RepositoryRenderer<br/>scmRepositoryRenderer.ts"]
    end
    
    subgraph "History View"
        SCMHistoryViewPane["SCMHistoryViewPane<br/>scmHistoryViewPane.ts"]
        HistoryItemRenderer["HistoryItemRenderer<br/>scmHistoryViewPane.ts"]
        HistoryItemChangeRenderer["HistoryItemChangeRenderer<br/>scmHistoryViewPane.ts"]
    end
    
    subgraph "Tree Infrastructure"
        WorkbenchAsyncDataTree["WorkbenchCompressibleAsyncDataTree<br/>listService.ts"]
        TreeDataSource["SCMTreeDataSource<br/>scmViewPane.ts"]
        TreeSorter["SCMTreeSorter<br/>scmViewPane.ts"]
    end
    
    SCMViewPane --> InputRenderer
    SCMViewPane --> ResourceGroupRenderer
    SCMViewPane --> ResourceRenderer
    SCMViewPane --> WorkbenchAsyncDataTree
    
    SCMRepositoriesViewPane --> RepositoryRenderer
    SCMHistoryViewPane --> HistoryItemRenderer
    SCMHistoryViewPane --> HistoryItemChangeRenderer
    
    WorkbenchAsyncDataTree --> TreeDataSource
    WorkbenchAsyncDataTree --> TreeSorter
```

The main `SCMViewPane` uses a tree structure with specialized renderers for different node types, while the history view provides a graph visualization of commit history.

Sources: [src/vs/workbench/contrib/scm/browser/scmViewPane.ts:115-2500](), [src/vs/workbench/contrib/scm/browser/scmHistoryViewPane.ts:1-2000](), [src/vs/workbench/contrib/scm/browser/scmRepositoriesViewPane.ts]()

## Extension API Bridge

The SCM system exposes its functionality to extensions through a bridge between the extension host and main thread.

```mermaid
graph LR
    subgraph "Extension Host"
        ExtHostSCM["ExtHostSCM<br/>extHostSCM.ts"]
        SCMProviderImpl["SourceControlManager<br/>extHostSCM.ts:800-1200"]
        SCMRepositoryImpl["SourceControlManager<br/>extHostSCM.ts:600-800"]
    end
    
    subgraph "Main Thread"
        MainThreadSCM["MainThreadSCM<br/>mainThreadSCM.ts"]
        MainThreadProvider["MainThreadSCMProvider<br/>mainThreadSCM.ts:200-600"]
        MainThreadRepository["MainThreadSCMRepository<br/>mainThreadSCM.ts:100-200"]
    end
    
    subgraph "VS Code API"
        vscode_scm["vscode.scm<br/>createSourceControl()"]
        SourceControlAPI["SourceControl<br/>VS Code API"]
    end
    
    vscode_scm --> ExtHostSCM
    ExtHostSCM --> SCMProviderImpl
    SCMProviderImpl --> SCMRepositoryImpl
    
    ExtHostSCM -.->|RPC| MainThreadSCM
    MainThreadSCM --> MainThreadProvider
    MainThreadProvider --> MainThreadRepository
    
    MainThreadSCM --> ISCMService
```

Extensions create SCM providers through the `vscode.scm.createSourceControl()` API, which creates proxy objects that communicate with the main thread via RPC.

Sources: [src/vs/workbench/api/common/extHostSCM.ts:1-1500](), [src/vs/workbench/api/browser/mainThreadSCM.ts:1-1000]()

## SCM Data Flow

The SCM system processes repository changes through a pipeline that updates UI components and notifies extensions.

```mermaid
graph TB
    subgraph "Data Sources"
        FileSystem["File System Changes"]
        GitOperations["Git Operations<br/>git.ts"]
        UserActions["User Actions<br/>commands.ts"]
    end
    
    subgraph "Repository Layer"
        Repository["Repository<br/>repository.ts"]
        ResourceUpdate["updateResources()<br/>repository.ts:1200-1400"]
        ResourceGroups["Resource Groups<br/>merge, index, working, untracked"]
    end
    
    subgraph "SCM Framework"
        ISCMService["ISCMService<br/>onDidChangeRepository"]
        ISCMViewService["ISCMViewService<br/>onDidChangeSelectedRepos"]
    end
    
    subgraph "UI Updates"
        SCMViewPane["SCM View Pane<br/>tree refresh"]
        StatusBar["Status Bar<br/>branch info"]
        Decorations["File Decorations<br/>git status"]
    end
    
    FileSystem --> Repository
    GitOperations --> Repository
    UserActions --> Repository
    
    Repository --> ResourceUpdate
    ResourceUpdate --> ResourceGroups
    ResourceGroups --> ISCMService
    
    ISCMService --> ISCMViewService
    ISCMViewService --> SCMViewPane
    ISCMService --> StatusBar
    ISCMService --> Decorations
```

Repository state changes trigger updates through the SCM service, which notifies views and other components to refresh their display.

Sources: [extensions/git/src/repository.ts:1200-1500](), [src/vs/workbench/contrib/scm/browser/scmViewPane.ts:2000-2500](), [src/vs/workbench/contrib/scm/browser/activity.ts]()

## History Provider System

The SCM framework includes support for history providers that can display commit graphs and timeline information.

```mermaid
graph TB
    subgraph "History Interfaces"
        ISCMHistoryProvider["ISCMHistoryProvider<br/>history.ts"]
        ISCMHistoryItem["ISCMHistoryItem<br/>commit data"]
        ISCMHistoryItemRef["ISCMHistoryItemRef<br/>branch/tag refs"]
    end
    
    subgraph "Git History Implementation"
        GitHistoryProvider["GitHistoryProvider<br/>historyProvider.ts"]
        GitCommitData["Git Commit Data<br/>log operations"]
        BranchTracking["Branch Tracking<br/>ref management"]
    end
    
    subgraph "History UI"
        SCMHistoryViewPane["SCMHistoryViewPane<br/>graph visualization"]
        HistoryItemRenderer["History Item Renderer<br/>commit display"]
        GraphRenderer["Graph Renderer<br/>branch lines"]
    end
    
    ISCMHistoryProvider --> ISCMHistoryItem
    ISCMHistoryProvider --> ISCMHistoryItemRef
    
    GitHistoryProvider --> ISCMHistoryProvider
    GitHistoryProvider --> GitCommitData
    GitHistoryProvider --> BranchTracking
    
    SCMHistoryViewPane --> ISCMHistoryProvider
    SCMHistoryViewPane --> HistoryItemRenderer
    SCMHistoryViewPane --> GraphRenderer
```

The Git extension implements the history provider interface to display commit graphs, branch relationships, and commit details in the SCM history view.

Sources: [src/vs/workbench/contrib/scm/common/history.ts](), [extensions/git/src/historyProvider.ts:40-400](), [src/vs/workbench/contrib/scm/browser/scmHistoryViewPane.ts:300-800]()