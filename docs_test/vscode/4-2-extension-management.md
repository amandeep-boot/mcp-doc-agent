# Extension Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/vs/platform/extensionManagement/common/abstractExtensionManagementService.ts](src/vs/platform/extensionManagement/common/abstractExtensionManagementService.ts)
- [src/vs/platform/extensionManagement/common/extensionGalleryService.ts](src/vs/platform/extensionManagement/common/extensionGalleryService.ts)
- [src/vs/platform/extensionManagement/common/extensionManagement.ts](src/vs/platform/extensionManagement/common/extensionManagement.ts)
- [src/vs/platform/extensionManagement/common/extensionManagementIpc.ts](src/vs/platform/extensionManagement/common/extensionManagementIpc.ts)
- [src/vs/platform/extensionManagement/common/extensionManagementUtil.ts](src/vs/platform/extensionManagement/common/extensionManagementUtil.ts)
- [src/vs/platform/extensionManagement/node/extensionManagementService.ts](src/vs/platform/extensionManagement/node/extensionManagementService.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionEditor.ts](src/vs/workbench/contrib/extensions/browser/extensionEditor.ts)
- [src/vs/workbench/contrib/extensions/browser/extensions.contribution.ts](src/vs/workbench/contrib/extensions/browser/extensions.contribution.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsActions.ts](src/vs/workbench/contrib/extensions/browser/extensionsActions.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsList.ts](src/vs/workbench/contrib/extensions/browser/extensionsList.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsViewer.ts](src/vs/workbench/contrib/extensions/browser/extensionsViewer.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsViewlet.ts](src/vs/workbench/contrib/extensions/browser/extensionsViewlet.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsViews.ts](src/vs/workbench/contrib/extensions/browser/extensionsViews.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsWidgets.ts](src/vs/workbench/contrib/extensions/browser/extensionsWidgets.ts)
- [src/vs/workbench/contrib/extensions/browser/extensionsWorkbenchService.ts](src/vs/workbench/contrib/extensions/browser/extensionsWorkbenchService.ts)
- [src/vs/workbench/contrib/extensions/browser/media/extension.css](src/vs/workbench/contrib/extensions/browser/media/extension.css)
- [src/vs/workbench/contrib/extensions/browser/media/extensionActions.css](src/vs/workbench/contrib/extensions/browser/media/extensionActions.css)
- [src/vs/workbench/contrib/extensions/browser/media/extensionEditor.css](src/vs/workbench/contrib/extensions/browser/media/extensionEditor.css)
- [src/vs/workbench/contrib/extensions/browser/media/extensionsViewlet.css](src/vs/workbench/contrib/extensions/browser/media/extensionsViewlet.css)
- [src/vs/workbench/contrib/extensions/browser/media/extensionsWidgets.css](src/vs/workbench/contrib/extensions/browser/media/extensionsWidgets.css)
- [src/vs/workbench/contrib/extensions/common/extensions.ts](src/vs/workbench/contrib/extensions/common/extensions.ts)
- [src/vs/workbench/contrib/extensions/test/electron-browser/extensionRecommendationsService.test.ts](src/vs/workbench/contrib/extensions/test/electron-browser/extensionRecommendationsService.test.ts)
- [src/vs/workbench/contrib/extensions/test/electron-browser/extensionsActions.test.ts](src/vs/workbench/contrib/extensions/test/electron-browser/extensionsActions.test.ts)
- [src/vs/workbench/contrib/extensions/test/electron-browser/extensionsViews.test.ts](src/vs/workbench/contrib/extensions/test/electron-browser/extensionsViews.test.ts)
- [src/vs/workbench/contrib/extensions/test/electron-browser/extensionsWorkbenchService.test.ts](src/vs/workbench/contrib/extensions/test/electron-browser/extensionsWorkbenchService.test.ts)
- [src/vs/workbench/services/extensionManagement/browser/extensionEnablementService.ts](src/vs/workbench/services/extensionManagement/browser/extensionEnablementService.ts)
- [src/vs/workbench/services/extensionManagement/common/extensionManagement.ts](src/vs/workbench/services/extensionManagement/common/extensionManagement.ts)
- [src/vs/workbench/services/extensionManagement/common/extensionManagementChannelClient.ts](src/vs/workbench/services/extensionManagement/common/extensionManagementChannelClient.ts)
- [src/vs/workbench/services/extensionManagement/common/extensionManagementServerService.ts](src/vs/workbench/services/extensionManagement/common/extensionManagementServerService.ts)
- [src/vs/workbench/services/extensionManagement/common/extensionManagementService.ts](src/vs/workbench/services/extensionManagement/common/extensionManagementService.ts)
- [src/vs/workbench/services/extensionManagement/common/webExtensionManagementService.ts](src/vs/workbench/services/extensionManagement/common/webExtensionManagementService.ts)
- [src/vs/workbench/services/extensionManagement/electron-browser/extensionManagementServerService.ts](src/vs/workbench/services/extensionManagement/electron-browser/extensionManagementServerService.ts)
- [src/vs/workbench/services/extensionManagement/electron-browser/remoteExtensionManagementService.ts](src/vs/workbench/services/extensionManagement/electron-browser/remoteExtensionManagementService.ts)
- [src/vs/workbench/services/extensionManagement/test/browser/extensionEnablementService.test.ts](src/vs/workbench/services/extensionManagement/test/browser/extensionEnablementService.test.ts)

</details>



This document covers VS Code's extension management system, which handles the discovery, installation, updating, and lifecycle management of extensions within the workbench. The system encompasses both platform-level services for core extension operations and workbench-level components for user interface and interaction.

For information about the extension host and runtime execution of extensions, see [Extension Host and Language Features](#4.1). For details about the build system that packages extensions, see [Build System and Package Management](#1.2).

## Architecture Overview

The extension management system is organized into multiple layers that separate platform concerns from workbench-specific functionality:

### Extension Management System Architecture

```mermaid
graph TB
    subgraph "Platform Layer"
        ExtMgmt["ExtensionManagementService"]
        Gallery["ExtensionGalleryService"]
        Scanner["ExtensionsScannerService"]
        Downloader["ExtensionsDownloader"]
    end
    
    subgraph "Workbench Layer"
        WorkbenchExtMgmt["ExtensionManagementService"]
        Enablement["ExtensionEnablementService"]
        WorkbenchSvc["ExtensionsWorkbenchService"]
        RecommendationSvc["ExtensionRecommendationsService"]
    end
    
    subgraph "UI Layer"
        ExtActions["ExtensionsActions"]
        ExtViews["ExtensionsViews"]
        ExtEditor["ExtensionEditor"]
        ExtViewlet["ExtensionsViewPaneContainer"]
    end
    
    subgraph "Extension Host"
        ExtHost["Extension Host Process"]
    end
    
    ExtMgmt --> Scanner
    ExtMgmt --> Downloader
    Gallery --> ExtMgmt
    
    WorkbenchExtMgmt --> ExtMgmt
    Enablement --> WorkbenchExtMgmt
    WorkbenchSvc --> WorkbenchExtMgmt
    WorkbenchSvc --> Gallery
    WorkbenchSvc --> RecommendationSvc
    
    ExtActions --> WorkbenchSvc
    ExtViews --> WorkbenchSvc
    ExtEditor --> WorkbenchSvc
    ExtViewlet --> ExtViews
    
    WorkbenchExtMgmt --> ExtHost
```

Sources: [src/vs/workbench/contrib/extensions/browser/extensions.contribution.ts:88-91](), [src/vs/workbench/services/extensionManagement/common/extensionManagementService.ts:59-129](), [src/vs/platform/extensionManagement/node/extensionManagementService.ts:72-106]()

## Core Extension Management Services

### IExtensionManagementService

The `IExtensionManagementService` is the primary interface for extension lifecycle operations. The platform-level implementation handles the actual installation, uninstallation, and scanning of extensions.

```mermaid
graph LR
    subgraph "Extension Management Services"
        IExtMgmt["IExtensionManagementService"]
        NativeExtMgmt["ExtensionManagementService (Native)"]
        WebExtMgmt["WebExtensionManagementService"]
        AbstractExtMgmt["AbstractExtensionManagementService"]
    end
    
    subgraph "Core Operations"
        Install["install()"]
        Uninstall["uninstall()"]
        GetInstalled["getInstalled()"]
        UpdateMetadata["updateMetadata()"]
    end
    
    IExtMgmt --> NativeExtMgmt
    IExtMgmt --> WebExtMgmt
    AbstractExtMgmt --> NativeExtMgmt
    AbstractExtMgmt --> WebExtMgmt
    
    NativeExtMgmt --> Install
    NativeExtMgmt --> Uninstall
    NativeExtMgmt --> GetInstalled
    NativeExtMgmt --> UpdateMetadata
```

Key responsibilities include:
- Installing extensions from VSIX files or gallery
- Uninstalling extensions and cleaning up files
- Scanning installed extensions
- Managing extension metadata and profiles

Sources: [src/vs/platform/extensionManagement/common/extensionManagement.ts:525-543](), [src/vs/platform/extensionManagement/node/extensionManagementService.ts:72-243]()

### ExtensionsWorkbenchService

The `ExtensionsWorkbenchService` provides the main workbench-level API for extension operations:

```mermaid
graph TB
    subgraph "ExtensionsWorkbenchService"
        WorkbenchSvc["ExtensionsWorkbenchService"]
        ExtensionModel["Extension Model"]
        QueryEngine["Query Engine"]
        UpdateChecker["Auto Update Checker"]
    end
    
    subgraph "Extension States"
        Installing["Installing"]
        Installed["Installed"]
        Uninstalling["Uninstalling"]
        Uninstalled["Uninstalled"]
    end
    
    subgraph "Data Sources"
        Local["Local Extensions"]
        Gallery["Gallery Extensions"]
        Recommendations["Recommendations"]
    end
    
    WorkbenchSvc --> ExtensionModel
    WorkbenchSvc --> QueryEngine
    WorkbenchSvc --> UpdateChecker
    
    ExtensionModel --> Installing
    ExtensionModel --> Installed
    ExtensionModel --> Uninstalling
    ExtensionModel --> Uninstalled
    
    QueryEngine --> Local
    QueryEngine --> Gallery
    QueryEngine --> Recommendations
```

The service manages:
- Extension state tracking and notifications
- Auto-update functionality
- Extension queries and filtering
- Integration with gallery and local extension sources

Sources: [src/vs/workbench/contrib/extensions/browser/extensionsWorkbenchService.ts:591-735](), [src/vs/workbench/contrib/extensions/common/extensions.ts:39-44]()

## Extension Gallery Integration

### ExtensionGalleryService

The `ExtensionGalleryService` handles communication with the VS Code Marketplace:

```mermaid
graph LR
    subgraph "Gallery Service"
        GallerySvc["ExtensionGalleryService"]
        Query["query()"]
        GetExtensions["getExtensions()"]
        Download["download()"]
        GetManifest["getManifest()"]
    end
    
    subgraph "Marketplace API"
        MarketplaceAPI["VS Code Marketplace"]
        QueryEndpoint["/extensionquery"]
        AssetEndpoint["/assets"]
    end
    
    subgraph "Gallery Operations"
        Search["Extension Search"]
        Metadata["Extension Metadata"]
        Assets["Extension Assets"]
        Statistics["Usage Statistics"]
    end
    
    GallerySvc --> Query
    GallerySvc --> GetExtensions
    GallerySvc --> Download
    GallerySvc --> GetManifest
    
    Query --> QueryEndpoint
    Download --> AssetEndpoint
    GetManifest --> AssetEndpoint
    
    Query --> Search
    GetExtensions --> Metadata
    Download --> Assets
    Query --> Statistics
```

Key capabilities:
- Searching and filtering extensions in the marketplace
- Downloading extension packages and assets
- Retrieving extension manifests and metadata
- Reporting usage statistics

Sources: [src/vs/platform/extensionManagement/common/extensionGalleryService.ts:396-421](), [src/vs/platform/extensionManagement/common/extensionManagement.ts:396-421]()

## Extension Installation and Management

### Installation Process

The extension installation process involves multiple coordinated steps:

```mermaid
graph TD
    StartInstall["Install Request"]
    ValidateExt["Validate Extension"]
    CheckCompat["Check Compatibility"]
    DownloadExt["Download Extension"]
    ExtractVSIX["Extract VSIX"]
    ScanMetadata["Scan Metadata"]
    UpdateProfile["Update Profile"]
    NotifyInstalled["Notify Installation Complete"]
    
    StartInstall --> ValidateExt
    ValidateExt --> CheckCompat
    CheckCompat --> DownloadExt
    DownloadExt --> ExtractVSIX
    ExtractVSIX --> ScanMetadata
    ScanMetadata --> UpdateProfile
    UpdateProfile --> NotifyInstalled
    
    subgraph "Validation Steps"
        ValidateExt
        CheckCompat
    end
    
    subgraph "Download & Extract"
        DownloadExt
        ExtractVSIX
    end
    
    subgraph "Registration"
        ScanMetadata
        UpdateProfile
    end
```

The `InstallExtensionTask` class coordinates this process:

Sources: [src/vs/platform/extensionManagement/node/extensionManagementService.ts:280-293](), [src/vs/platform/extensionManagement/common/abstractExtensionManagementService.ts:37-50]()

### Extension Actions

Extension actions provide the user interface for extension operations:

```mermaid
graph TB
    subgraph "Extension Actions"
        InstallAction["InstallAction"]
        UninstallAction["UninstallAction"]
        UpdateAction["UpdateAction"]
        EnableAction["EnableDropDownAction"]
        DisableAction["DisableDropDownAction"]
    end
    
    subgraph "Compound Actions"
        InstallDropdown["InstallDropdownAction"]
        ButtonWithDropdown["ButtonWithDropDownExtensionAction"]
        ManageAction["ExtensionEditorManageExtensionAction"]
    end
    
    subgraph "Status Actions"
        StatusAction["ExtensionStatusAction"]
        RuntimeAction["ExtensionRuntimeStateAction"]
        InstallingAction["InstallingLabelAction"]
    end
    
    InstallDropdown --> InstallAction
    ButtonWithDropdown --> UninstallAction
    ManageAction --> EnableAction
    ManageAction --> DisableAction
    
    InstallAction --> StatusAction
    UpdateAction --> RuntimeAction
    InstallAction --> InstallingAction
```

Action classes extend `ExtensionAction` and provide:
- Context-sensitive visibility and enablement
- Integration with extension state changes
- Dropdown menus for complex operations

Sources: [src/vs/workbench/contrib/extensions/browser/extensionsActions.ts:285-319](), [src/vs/workbench/contrib/extensions/browser/extensionsActions.ts:428-496]()

## Extension Views and UI

### Extensions Viewlet Structure

The Extensions viewlet organizes extension management into multiple specialized views:

```mermaid
graph TB
    subgraph "Extensions Viewlet"
        ViewPaneContainer["ExtensionsViewPaneContainer"]
        SearchInput["Extension Search Input"]
        ViewRegistry["Views Registry"]
    end
    
    subgraph "Extension Views"
        InstalledView["Server Installed Extensions View"]
        RecommendedView["Recommended Extensions View"]
        PopularView["Popular Extensions View"]
        EnabledView["Enabled Extensions View"]
        DisabledView["Disabled Extensions View"]
        OutdatedView["Outdated Extensions View"]
        BuiltinView["Built-in Extensions View"]
    end
    
    subgraph "Specialized Views"
        WorkspaceRec["Workspace Recommendations"]
        UntrustedView["Untrusted Workspace Extensions"]
        VirtualView["Virtual Workspace Extensions"]
        DeprecatedView["Deprecated Extensions"]
    end
    
    ViewPaneContainer --> SearchInput
    ViewPaneContainer --> ViewRegistry
    
    ViewRegistry --> InstalledView
    ViewRegistry --> RecommendedView
    ViewRegistry --> PopularView
    ViewRegistry --> EnabledView
    ViewRegistry --> DisabledView
    ViewRegistry --> OutdatedView
    ViewRegistry --> BuiltinView
    
    ViewRegistry --> WorkspaceRec
    ViewRegistry --> UntrustedView
    ViewRegistry --> VirtualView
    ViewRegistry --> DeprecatedView
```

Each view is registered dynamically based on context and provides filtered extension lists with specific query criteria.

Sources: [src/vs/workbench/contrib/extensions/browser/extensionsViewlet.ts:111-132](), [src/vs/workbench/contrib/extensions/browser/extensionsViews.ts:112-171]()

### Extension Editor

The `ExtensionEditor` displays detailed information about individual extensions:

```mermaid
graph LR
    subgraph "Extension Editor"
        EditorPane["ExtensionEditor"]
        Template["Editor Template"]
        Navbar["Navigation Bar"]
        Content["Content Container"]
    end
    
    subgraph "Editor Tabs"
        Readme["Readme Tab"]
        Features["Features Tab"]
        Changelog["Changelog Tab"]
        Dependencies["Dependencies Tab"]
        ExtensionPack["Extension Pack Tab"]
    end
    
    subgraph "Header Components"
        Icon["Extension Icon"]
        Title["Extension Title"]
        Publisher["Publisher Info"]
        Actions["Action Bar"]
        Status["Status Widget"]
    end
    
    EditorPane --> Template
    Template --> Navbar
    Template --> Content
    
    Navbar --> Readme
    Navbar --> Features
    Navbar --> Changelog
    Navbar --> Dependencies
    Navbar --> ExtensionPack
    
    Template --> Icon
    Template --> Title
    Template --> Publisher
    Template --> Actions
    Template --> Status
```

The editor provides comprehensive extension information including manifests, readme content, and interactive actions.

Sources: [src/vs/workbench/contrib/extensions/browser/extensionEditor.ts:209-256](), [src/vs/workbench/contrib/extensions/browser/extensionEditor.ts:426-456]()

## Extension Enablement and State Management

### Extension Enablement Service

The `ExtensionEnablementService` manages the enabled/disabled state of extensions:

```mermaid
graph TB
    subgraph "Enablement Service"
        EnablementSvc["ExtensionEnablementService"]
        GlobalStorage["Global Enablement Storage"]
        WorkspaceStorage["Workspace Enablement Storage"]
        StateProvider["Enablement State Provider"]
    end
    
    subgraph "Enablement States"
        EnabledGlobally["EnabledGlobally"]
        DisabledGlobally["DisabledGlobally"]
        EnabledWorkspace["EnabledWorkspace"]
        DisabledWorkspace["DisabledWorkspace"]
        DisabledByTrust["DisabledByTrustRequirement"]
        DisabledByVirtual["DisabledByVirtualWorkspace"]
        DisabledByMalicious["DisabledByMalicious"]
    end
    
    subgraph "State Influences"
        WorkspaceTrust["Workspace Trust"]
        VirtualWorkspace["Virtual Workspace"]
        MaliciousExt["Malicious Extensions"]
        UserConfig["User Configuration"]
    end
    
    EnablementSvc --> GlobalStorage
    EnablementSvc --> WorkspaceStorage
    EnablementSvc --> StateProvider
    
    StateProvider --> EnabledGlobally
    StateProvider --> DisabledGlobally
    StateProvider --> EnabledWorkspace
    StateProvider --> DisabledWorkspace
    StateProvider --> DisabledByTrust
    StateProvider --> DisabledByVirtual
    StateProvider --> DisabledByMalicious
    
    WorkspaceTrust --> DisabledByTrust
    VirtualWorkspace --> DisabledByVirtual
    MaliciousExt --> DisabledByMalicious
    UserConfig --> DisabledGlobally
```

The service considers multiple factors when determining extension enablement including workspace trust, virtual workspace support, and malicious extension detection.

Sources: [src/vs/workbench/services/extensionManagement/browser/extensionEnablementService.ts:1-49](), [src/vs/workbench/services/extensionManagement/common/extensionManagement.ts:85-128]()

## Extension Lifecycle Events

### Event Flow Architecture

Extension management operations trigger events that coordinate updates across the system:

```mermaid
graph TD
    subgraph "Installation Events"
        InstallStart["onInstallExtension"]
        InstallComplete["onDidInstallExtensions"]
        InstallError["Installation Error"]
    end
    
    subgraph "Uninstallation Events"
        UninstallStart["onUninstallExtension"]
        UninstallComplete["onDidUninstallExtension"]
        UninstallError["Uninstallation Error"]
    end
    
    subgraph "State Change Events"
        EnablementChange["onEnablementChanged"]
        MetadataUpdate["onDidUpdateExtensionMetadata"]
        ProfileChange["onDidChangeProfile"]
    end
    
    subgraph "Listeners"
        WorkbenchService["ExtensionsWorkbenchService"]
        StatusUpdater["StatusUpdater"]
        ActivityService["ActivityService"]
        RecommendationService["RecommendationService"]
    end
    
    InstallStart --> WorkbenchService
    InstallComplete --> WorkbenchService
    InstallComplete --> StatusUpdater
    
    UninstallComplete --> WorkbenchService
    UninstallComplete --> ActivityService
    
    EnablementChange --> WorkbenchService
    MetadataUpdate --> WorkbenchService
    ProfileChange --> RecommendationService
```

Event coordination ensures that UI components stay synchronized with extension state changes and that dependent services are notified of relevant changes.

Sources: [src/vs/workbench/contrib/extensions/browser/extensionsWorkbenchService.ts:593-622](), [src/vs/workbench/services/extensionManagement/common/extensionManagementService.ts:65-87]()