# Workbench Layout and Editor Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/vs/platform/editor/common/editor.ts](src/vs/platform/editor/common/editor.ts)
- [src/vs/workbench/browser/actions/layoutActions.ts](src/vs/workbench/browser/actions/layoutActions.ts)
- [src/vs/workbench/browser/contextkeys.ts](src/vs/workbench/browser/contextkeys.ts)
- [src/vs/workbench/browser/dnd.ts](src/vs/workbench/browser/dnd.ts)
- [src/vs/workbench/browser/layout.ts](src/vs/workbench/browser/layout.ts)
- [src/vs/workbench/browser/parts/auxiliarybar/auxiliaryBarActions.ts](src/vs/workbench/browser/parts/auxiliarybar/auxiliaryBarActions.ts)
- [src/vs/workbench/browser/parts/editor/editor.contribution.ts](src/vs/workbench/browser/parts/editor/editor.contribution.ts)
- [src/vs/workbench/browser/parts/editor/editor.ts](src/vs/workbench/browser/parts/editor/editor.ts)
- [src/vs/workbench/browser/parts/editor/editorActions.ts](src/vs/workbench/browser/parts/editor/editorActions.ts)
- [src/vs/workbench/browser/parts/editor/editorCommands.ts](src/vs/workbench/browser/parts/editor/editorCommands.ts)
- [src/vs/workbench/browser/parts/editor/editorDropTarget.ts](src/vs/workbench/browser/parts/editor/editorDropTarget.ts)
- [src/vs/workbench/browser/parts/editor/editorGroupView.ts](src/vs/workbench/browser/parts/editor/editorGroupView.ts)
- [src/vs/workbench/browser/parts/editor/editorGroupWatermark.ts](src/vs/workbench/browser/parts/editor/editorGroupWatermark.ts)
- [src/vs/workbench/browser/parts/editor/editorPart.ts](src/vs/workbench/browser/parts/editor/editorPart.ts)
- [src/vs/workbench/browser/parts/editor/media/editorgroupview.css](src/vs/workbench/browser/parts/editor/media/editorgroupview.css)
- [src/vs/workbench/browser/parts/panel/panelActions.ts](src/vs/workbench/browser/parts/panel/panelActions.ts)
- [src/vs/workbench/browser/parts/titlebar/titlebarActions.ts](src/vs/workbench/browser/parts/titlebar/titlebarActions.ts)
- [src/vs/workbench/browser/workbench.contribution.ts](src/vs/workbench/browser/workbench.contribution.ts)
- [src/vs/workbench/browser/workbench.ts](src/vs/workbench/browser/workbench.ts)
- [src/vs/workbench/common/contextkeys.ts](src/vs/workbench/common/contextkeys.ts)
- [src/vs/workbench/common/editor.ts](src/vs/workbench/common/editor.ts)
- [src/vs/workbench/services/editor/browser/editorService.ts](src/vs/workbench/services/editor/browser/editorService.ts)
- [src/vs/workbench/services/editor/common/editorGroupsService.ts](src/vs/workbench/services/editor/common/editorGroupsService.ts)
- [src/vs/workbench/services/editor/common/editorService.ts](src/vs/workbench/services/editor/common/editorService.ts)
- [src/vs/workbench/services/editor/test/browser/editorGroupsService.test.ts](src/vs/workbench/services/editor/test/browser/editorGroupsService.test.ts)
- [src/vs/workbench/services/editor/test/browser/editorService.test.ts](src/vs/workbench/services/editor/test/browser/editorService.test.ts)
- [src/vs/workbench/services/layout/browser/layoutService.ts](src/vs/workbench/services/layout/browser/layoutService.ts)
- [src/vs/workbench/test/browser/workbenchTestServices.ts](src/vs/workbench/test/browser/workbenchTestServices.ts)

</details>



This document covers VS Code's workbench layout system and editor management architecture. The workbench layout defines how the main UI parts (sidebar, panel, editor area, etc.) are arranged and sized, while editor management handles the lifecycle and organization of editors within the editor area.

For information about Monaco Editor's text editing capabilities, see [3](#3). For UI component fundamentals like lists and trees, see [2.3](#2.3).

## Overview

The workbench layout system consists of two main layers:

1. **Layout Management**: Controls the arrangement and sizing of major workbench parts (sidebar, panel, editor area, auxiliary bar, etc.)
2. **Editor Management**: Manages editors within the editor area, including grouping, splitting, and lifecycle operations

The system uses a grid-based layout with serializable state that persists across sessions.

## Layout Architecture

### Core Layout Components

```mermaid
graph TB
    subgraph "Workbench Container"
        Layout["Layout<br/>(layout.ts)"]
        
        subgraph "Workbench Parts"
            TitleBar["TitleBar Part"]
            Banner["Banner Part"]
            ActivityBar["ActivityBar Part"]
            SideBar["SideBar Part"]
            EditorPart["EditorPart<br/>(editorPart.ts)"]
            Panel["Panel Part"]
            AuxiliaryBar["AuxiliaryBar Part"]
            StatusBar["StatusBar Part"]
        end
        
        subgraph "Layout Grid"
            SerializableGrid["SerializableGrid<br/>(grid.ts)"]
            GridViews["ISerializableView[]"]
        end
    end
    
    Layout --> SerializableGrid
    SerializableGrid --> GridViews
    GridViews --> TitleBar
    GridViews --> Banner
    GridViews --> ActivityBar
    GridViews --> SideBar
    GridViews --> EditorPart
    GridViews --> Panel
    GridViews --> AuxiliaryBar
    GridViews --> StatusBar
```

The `Layout` class orchestrates the overall workbench structure, managing eight distinct parts arranged in a serializable grid system.

Sources: [src/vs/workbench/browser/layout.ts:138-304](), [src/vs/workbench/browser/parts/editor/editorPart.ts:86-172]()

### Layout State Management

```mermaid
graph LR
    subgraph "State Management"
        LayoutStateModel["LayoutStateModel"]
        RuntimeState["ILayoutRuntimeState"]
        InitState["ILayoutInitializationState"]
        Storage["StorageService"]
    end
    
    subgraph "Layout Properties"
        SidebarPos["Sidebar Position"]
        PanelPos["Panel Position"]
        PartVisibility["Part Visibility"]
        WindowState["Window State"]
        ZenMode["Zen Mode"]
    end
    
    LayoutStateModel --> RuntimeState
    LayoutStateModel --> InitState
    LayoutStateModel --> Storage
    
    RuntimeState --> SidebarPos
    RuntimeState --> PanelPos
    RuntimeState --> PartVisibility
    RuntimeState --> WindowState
    RuntimeState --> ZenMode
```

The layout system maintains persistent state through `LayoutStateModel`, tracking part positions, visibility, and special modes like Zen Mode.

Sources: [src/vs/workbench/browser/layout.ts:54-95](), [src/vs/workbench/browser/layout.ts:625-744]()

## Editor Management System

### Editor Service Architecture

```mermaid
graph TB
    subgraph "Editor Services"
        EditorService["EditorService<br/>(editorService.ts)"]
        EditorGroupsService["IEditorGroupsService"]
        EditorResolverService["IEditorResolverService"]
    end
    
    subgraph "Editor Parts"
        MainEditorPart["MainEditorPart<br/>(editorPart.ts)"]
        AuxEditorPart["AuxiliaryEditorPart"]
    end
    
    subgraph "Editor Groups"
        EditorGroupView1["EditorGroupView<br/>(editorGroupView.ts)"]
        EditorGroupView2["EditorGroupView"]
        EditorGroupViewN["EditorGroupView..."]
    end
    
    subgraph "Editors"
        EditorInput1["EditorInput"]
        EditorInput2["EditorInput"]
        EditorInputN["EditorInput..."]
        EditorPane1["EditorPane"]
        EditorPane2["EditorPane"]
    end
    
    EditorService --> EditorGroupsService
    EditorService --> EditorResolverService
    EditorGroupsService --> MainEditorPart
    EditorGroupsService --> AuxEditorPart
    MainEditorPart --> EditorGroupView1
    MainEditorPart --> EditorGroupView2
    MainEditorPart --> EditorGroupViewN
    EditorGroupView1 --> EditorInput1
    EditorGroupView1 --> EditorInput2
    EditorGroupView2 --> EditorInputN
    EditorInput1 --> EditorPane1
    EditorInput2 --> EditorPane2
```

The editor system uses a hierarchical structure where `EditorService` coordinates with `EditorGroupsService` to manage multiple editor parts, each containing multiple editor groups.

Sources: [src/vs/workbench/services/editor/browser/editorService.ts:39-96](), [src/vs/workbench/browser/parts/editor/editorPart.ts:86-236]()

### Editor Group Layout

```mermaid
graph LR
    subgraph "Editor Groups Arrangement"
        GridWidget["Grid<EditorGroupView>"]
        
        subgraph "Group 1"
            EG1["EditorGroupView"]
            E1["Editor A"]
            E2["Editor B"]
            E3["Editor C"]
        end
        
        subgraph "Group 2"
            EG2["EditorGroupView"]
            E4["Editor D"]
            E5["Editor E"]
        end
        
        subgraph "Group 3"
            EG3["EditorGroupView"]
            E6["Editor F"]
        end
    end
    
    GridWidget --> EG1
    GridWidget --> EG2
    GridWidget --> EG3
    EG1 --> E1
    EG1 --> E2
    EG1 --> E3
    EG2 --> E4
    EG2 --> E5
    EG3 --> E6
```

Editor groups are arranged using the same grid system as the overall layout, allowing flexible splitting and resizing of editor areas.

Sources: [src/vs/workbench/browser/parts/editor/editorPart.ts:154-157](), [src/vs/workbench/browser/parts/editor/editorGroupView.ts:116-175]()

## Key Interfaces and Services

### IWorkbenchLayoutService

The main interface for layout operations:

| Method | Purpose |
|--------|---------|
| `isVisible(part: Parts)` | Check part visibility |
| `setPartHidden(hidden: boolean, part: Parts)` | Toggle part visibility |
| `toggleZenMode()` | Enter/exit zen mode |
| `centerMainEditorLayout(active: boolean)` | Toggle centered editor layout |
| `setPanelAlignment(alignment: PanelAlignment)` | Set panel alignment |

Sources: [src/vs/workbench/services/layout/browser/layoutService.ts:225-398]()

### IEditorGroupsService

Manages editor group operations:

| Method | Purpose |
|--------|---------|
| `addGroup(location: GroupLocation, direction: GroupDirection)` | Create new editor group |
| `removeGroup(group: IEditorGroup)` | Remove editor group |
| `moveGroup(group: IEditorGroup, location: GroupLocation)` | Move group position |
| `arrangeGroups(arrangement: GroupsArrangement)` | Arrange group layout |

Sources: [src/vs/workbench/services/editor/common/editorGroupsService.ts:188-445]()

### EditorGroupView Lifecycle

```mermaid
sequenceDiagram
    participant Client
    participant EditorService
    participant EditorGroupsService
    participant EditorGroupView
    participant EditorInput
    participant EditorPane

    Client->>EditorService: openEditor(input, options)
    EditorService->>EditorGroupsService: getActiveGroup()
    EditorGroupsService->>EditorGroupView: openEditor(input, options)
    EditorGroupView->>EditorInput: create/resolve
    EditorGroupView->>EditorPane: setInput(input)
    EditorPane-->>EditorGroupView: onDidFocus
    EditorGroupView-->>EditorService: onDidActiveEditorChange
    EditorService-->>Client: editor opened
```

The editor opening process involves coordination between multiple services to resolve inputs and create appropriate editor panes.

Sources: [src/vs/workbench/browser/parts/editor/editorGroupView.ts:785-950](), [src/vs/workbench/services/editor/browser/editorService.ts:478-629]()

## Layout Persistence and Restoration

### State Serialization

The layout system persists its state through several mechanisms:

```mermaid
graph TD
    subgraph "Persistence Layer"
        WorkspaceMemento["Workspace Memento<br/>(per workspace)"]
        ProfileMemento["Profile Memento<br/>(per user profile)"]
        StorageService["StorageService"]
    end
    
    subgraph "Serialized State"
        UIState["IEditorPartUIState"]
        GridSerialized["ISerializedGrid"]
        GroupState["ISerializedEditorGroupModel"]
        LayoutState["Layout Configuration"]
    end
    
    StorageService --> WorkspaceMemento
    StorageService --> ProfileMemento
    WorkspaceMemento --> UIState
    UIState --> GridSerialized
    UIState --> GroupState
    ProfileMemento --> LayoutState
```

Different aspects of layout state are persisted at different scopes - workspace-specific state (like open editors) versus user preferences (like part positions).

Sources: [src/vs/workbench/browser/parts/editor/editorPart.ts:142-143](), [src/vs/workbench/browser/layout.ts:625-744]()

## Editor Group Management

### Group Operations

```mermaid
graph LR
    subgraph "Group Operations"
        Split["splitEditor()"]
        Merge["mergeGroup()"]
        Move["moveGroup()"]
        Close["closeGroup()"]
    end
    
    subgraph "Group Directions"
        Up["GroupDirection.UP"]
        Down["GroupDirection.DOWN"]
        Left["GroupDirection.LEFT"]
        Right["GroupDirection.RIGHT"]
    end
    
    subgraph "Group Arrangements"
        Maximize["MAXIMIZE"]
        Expand["EXPAND"]
        Even["EVEN"]
    end
    
    Split --> Up
    Split --> Down
    Split --> Left
    Split --> Right
    
    Merge --> Move
    Move --> Maximize
    Move --> Expand
    Move --> Even
```

Editor groups support various operations for splitting, merging, and arranging editors in the workspace.

Sources: [src/vs/workbench/services/editor/common/editorGroupsService.ts:23-40](), [src/vs/workbench/services/editor/common/editorGroupsService.ts:47-64]()

### Editor Input Management

Each `EditorGroupView` manages a collection of `EditorInput` instances:

| Component | Responsibility |
|-----------|----------------|
| `EditorGroupModel` | Tracks editor state and order |
| `EditorTitleControl` | Renders tabs and title area |
| `EditorPanes` | Manages editor pane instances |
| `EditorDropTarget` | Handles drag & drop operations |

Sources: [src/vs/workbench/browser/parts/editor/editorGroupView.ts:116-247]()

## Configuration and Customization

The layout system exposes numerous configuration options through VS Code's settings:

### Layout Settings

```typescript
interface IEditorPartOptions {
  showTabs: 'multiple' | 'single' | 'none';
  tabSizing: 'fit' | 'shrink' | 'fixed';
  splitOnDragAndDrop: boolean;
  centeredLayoutFixedWidth: boolean;
  // ... many more options
}
```

### Key Configuration Properties

| Setting | Purpose | Default |
|---------|---------|---------|
| `workbench.editor.showTabs` | Tab display mode | `'multiple'` |
| `workbench.sideBar.location` | Sidebar position | `'left'` |
| `workbench.panel.defaultLocation` | Panel position | `'bottom'` |
| `workbench.editor.splitSizing` | Split editor sizing | `'auto'` |

Sources: [src/vs/workbench/browser/parts/editor/editor.ts:31-149](), [src/vs/workbench/browser/workbench.contribution.ts:49-383]()

This architecture provides a flexible, extensible system for managing VS Code's complex UI layout while maintaining performance and user experience across different workflows and window configurations.