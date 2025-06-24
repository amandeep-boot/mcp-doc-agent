# Notebook Editor

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/vs/workbench/api/browser/mainThreadNotebook.ts](src/vs/workbench/api/browser/mainThreadNotebook.ts)
- [src/vs/workbench/api/common/extHostNotebook.ts](src/vs/workbench/api/common/extHostNotebook.ts)
- [src/vs/workbench/contrib/notebook/browser/media/notebook.css](src/vs/workbench/contrib/notebook/browser/media/notebook.css)
- [src/vs/workbench/contrib/notebook/browser/notebook.contribution.ts](src/vs/workbench/contrib/notebook/browser/notebook.contribution.ts)
- [src/vs/workbench/contrib/notebook/browser/notebookBrowser.ts](src/vs/workbench/contrib/notebook/browser/notebookBrowser.ts)
- [src/vs/workbench/contrib/notebook/browser/notebookEditor.ts](src/vs/workbench/contrib/notebook/browser/notebookEditor.ts)
- [src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts](src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts)
- [src/vs/workbench/contrib/notebook/browser/view/notebookCellList.ts](src/vs/workbench/contrib/notebook/browser/view/notebookCellList.ts)
- [src/vs/workbench/contrib/notebook/browser/view/renderers/backLayerWebView.ts](src/vs/workbench/contrib/notebook/browser/view/renderers/backLayerWebView.ts)
- [src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts](src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts)
- [src/vs/workbench/contrib/notebook/browser/view/renderers/webviewMessages.ts](src/vs/workbench/contrib/notebook/browser/view/renderers/webviewMessages.ts)
- [src/vs/workbench/contrib/notebook/browser/view/renderers/webviewPreloads.ts](src/vs/workbench/contrib/notebook/browser/view/renderers/webviewPreloads.ts)
- [src/vs/workbench/contrib/notebook/browser/viewModel/baseCellViewModel.ts](src/vs/workbench/contrib/notebook/browser/viewModel/baseCellViewModel.ts)
- [src/vs/workbench/contrib/notebook/browser/viewModel/codeCellViewModel.ts](src/vs/workbench/contrib/notebook/browser/viewModel/codeCellViewModel.ts)
- [src/vs/workbench/contrib/notebook/browser/viewModel/markupCellViewModel.ts](src/vs/workbench/contrib/notebook/browser/viewModel/markupCellViewModel.ts)
- [src/vs/workbench/contrib/notebook/common/model/notebookCellTextModel.ts](src/vs/workbench/contrib/notebook/common/model/notebookCellTextModel.ts)
- [src/vs/workbench/contrib/notebook/common/model/notebookTextModel.ts](src/vs/workbench/contrib/notebook/common/model/notebookTextModel.ts)
- [src/vs/workbench/contrib/notebook/common/notebookCommon.ts](src/vs/workbench/contrib/notebook/common/notebookCommon.ts)
- [src/vs/workbench/contrib/notebook/common/notebookEditorModel.ts](src/vs/workbench/contrib/notebook/common/notebookEditorModel.ts)
- [src/vs/workbench/contrib/notebook/common/notebookService.ts](src/vs/workbench/contrib/notebook/common/notebookService.ts)

</details>



This document covers the Notebook Editor system in VS Code, which provides the interactive editing experience for Jupyter notebooks and other notebook formats. The Notebook Editor enables users to create, edit, and execute code and markdown cells within a unified interface.

The scope includes the editor widget architecture, cell rendering pipeline, webview integration for outputs, and the underlying data models. For information about notebook services and kernel management, see [Notebook System](#6.1). For details about the extension API for notebooks, refer to the Extension System documentation.

## Architecture Overview

The Notebook Editor follows a layered architecture with clear separation between the editor pane, widget implementation, cell management, and underlying data models.

### High-Level Component Structure

```mermaid
graph TB
    NotebookEditor["NotebookEditor<br/>(Editor Pane)"] --> NotebookEditorWidget["NotebookEditorWidget<br/>(Core Widget)"]
    NotebookEditorWidget --> NotebookCellList["NotebookCellList<br/>(Cell Management)"]
    NotebookEditorWidget --> BackLayerWebView["BackLayerWebView<br/>(Output Rendering)"]
    NotebookCellList --> CodeCellRenderer["CodeCellRenderer"]
    NotebookCellList --> MarkupCellRenderer["MarkupCellRenderer"]
    NotebookEditorWidget --> NotebookViewModel["NotebookViewModel"]
    NotebookViewModel --> NotebookTextModel["NotebookTextModel"]
    NotebookTextModel --> NotebookCellTextModel["NotebookCellTextModel[]"]
    CodeCellRenderer --> CodeCellViewModel["CodeCellViewModel"]
    MarkupCellRenderer --> MarkupCellViewModel["MarkupCellViewModel"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/notebookEditor.ts:54-105](), [src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts:138-471](), [src/vs/workbench/contrib/notebook/browser/view/notebookCellList.ts:80-131]()

### Editor Pane and Widget Separation

The `NotebookEditor` serves as the editor pane that integrates with VS Code's editor system, while `NotebookEditorWidget` contains the actual notebook editing implementation.

```mermaid
graph LR
    EditorPane["EditorPane<br/>(VS Code Framework)"] --> NotebookEditor["NotebookEditor<br/>notebookEditor.ts"]
    NotebookEditor --> NotebookEditorWidget["NotebookEditorWidget<br/>notebookEditorWidget.ts"]
    NotebookEditor --> MemoryManagement["Editor Memento<br/>View State Persistence"]
    NotebookEditorWidget --> CellManagement["Cell List & Rendering"]
    NotebookEditorWidget --> WebviewIntegration["Output Webview"]
    NotebookEditorWidget --> ToolbarManagement["Notebook Toolbar"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/notebookEditor.ts:54-143](), [src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts:138-298]()

## Cell Rendering System

The notebook editor uses specialized renderers for different cell types, with a sophisticated rendering pipeline that handles both code and markup cells.

### Cell Renderer Architecture

```mermaid
graph TB
    NotebookCellListDelegate["NotebookCellListDelegate<br/>getTemplateId()"] --> CellRenderers["Cell Renderers"]
    CellRenderers --> CodeCellRenderer["CodeCellRenderer<br/>TEMPLATE_ID: 'code_cell'"]
    CellRenderers --> MarkupCellRenderer["MarkupCellRenderer<br/>TEMPLATE_ID: 'markdown_cell'"]
    
    CodeCellRenderer --> CodeCellTemplate["CodeCellRenderTemplate<br/>Editor + Output Container"]
    MarkupCellRenderer --> MarkdownCellTemplate["MarkdownCellRenderTemplate<br/>Preview + Editor Container"]
    
    CodeCellTemplate --> CellParts1["CellPartsCollection<br/>- CellExecutionPart<br/>- CellProgressBar<br/>- RunToolbar"]
    MarkdownCellTemplate --> CellParts2["CellPartsCollection<br/>- CellFocusPart<br/>- CellDecorations<br/>- CollapsedCellInput"]
    
    CellParts1 --> CodeCellVM["CodeCellViewModel"]
    CellParts2 --> MarkupCellVM["MarkupCellViewModel"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts:57-85](), [src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts:112-235](), [src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts:237-354]()

### Cell Parts System

Each cell is composed of multiple parts that handle different aspects of the cell's functionality and rendering.

```mermaid
graph LR
    CellPartsCollection["CellPartsCollection"] --> CoreParts["Core Parts"]
    CellPartsCollection --> ToolbarParts["Toolbar Parts"]
    
    CoreParts --> CellChatPart["CellChatPart<br/>AI Integration"]
    CoreParts --> CellEditorStatusBar["CellEditorStatusBar<br/>Status Display"]
    CoreParts --> CellFocusIndicator["CellFocusIndicator<br/>Visual Focus State"]
    CoreParts --> CellDecorations["CellDecorations<br/>Cell Decorations"]
    CoreParts --> CellDragAndDropPart["CellDragAndDropPart<br/>DnD Support"]
    
    ToolbarParts --> CellTitleToolbarPart["CellTitleToolbarPart<br/>Cell Actions"]
    ToolbarParts --> BetweenCellToolbar["BetweenCellToolbar<br/>Insert Actions"]
    ToolbarParts --> RunToolbar["RunToolbar<br/>Execution Controls"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts:175-189](), [src/vs/workbench/contrib/notebook/browser/view/renderers/cellRenderer.ts:298-320]()

## Output Rendering and Webview Integration

The notebook editor uses a sophisticated webview-based system for rendering cell outputs, particularly for rich content like HTML, images, and interactive widgets.

### BackLayerWebView Architecture

```mermaid
graph TB
    NotebookEditorWidget --> BackLayerWebView["BackLayerWebView<br/>Output Rendering Engine"]
    BackLayerWebView --> WebviewElement["IWebviewElement<br/>Webview Container"]
    BackLayerWebView --> InsetMapping["Map<IDisplayOutputViewModel, ICachedInset>"]
    BackLayerWebView --> RendererMessaging["IScopedRendererMessaging<br/>Extension Communication"]
    
    WebviewElement --> WebviewPreloads["webviewPreloads.ts<br/>Injected JavaScript"]
    WebviewPreloads --> RendererRegistry["Notebook Renderers<br/>Extension-provided"]
    WebviewPreloads --> OutputHandling["Output Event Handling<br/>- Focus/Blur<br/>- Mouse Events<br/>- Scroll Events"]
    
    InsetMapping --> CachedInsets["ICachedInset<br/>- outputId<br/>- versionId<br/>- cellInfo<br/>- renderer"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/view/renderers/backLayerWebView.ts:128-225](), [src/vs/workbench/contrib/notebook/browser/view/renderers/webviewPreloads.ts:92-500]()

### Output Rendering Pipeline

```mermaid
graph LR
    CellOutput["ICellOutput<br/>Cell Output Data"] --> OutputViewModel["ICellOutputViewModel<br/>Display Abstraction"]
    OutputViewModel --> MimeTypeResolution["resolveMimeTypes()<br/>Renderer Selection"]
    MimeTypeResolution --> RenderDecision["IInsetRenderOutput<br/>Html vs Extension"]
    
    RenderDecision --> HtmlRendering["IRenderPlainHtmlOutput<br/>Direct HTML"]
    RenderDecision --> ExtensionRendering["IRenderOutputViaExtension<br/>Custom Renderer"]
    
    HtmlRendering --> WebviewInsertion["Webview DOM Insertion"]
    ExtensionRendering --> RendererActivation["Extension Renderer<br/>Activation & Messaging"]
    
    WebviewInsertion --> DimensionTracking["Output Dimension<br/>Tracking & Updates"]
    RendererActivation --> DimensionTracking
```

Sources: [src/vs/workbench/contrib/notebook/browser/notebookBrowser.ts:103-121](), [src/vs/workbench/contrib/notebook/browser/view/renderers/backLayerWebView.ts:535-670]()

## Data Model Layer

The notebook editor operates on a multi-layered data model that separates text content, cell metadata, and view state.

### Model Hierarchy

```mermaid
graph TB
    NotebookTextModel["NotebookTextModel<br/>Document Root"] --> NotebookCells["cells: readonly ICell[]"]
    NotebookTextModel --> DocumentMetadata["metadata: NotebookDocumentMetadata"]
    NotebookTextModel --> TransientOptions["transientOptions: TransientOptions"]
    
    NotebookCells --> NotebookCellTextModel["NotebookCellTextModel<br/>Individual Cell Data"]
    NotebookCellTextModel --> CellTextBuffer["textBuffer: IReadonlyTextBuffer"]
    NotebookCellTextModel --> CellMetadata["metadata: NotebookCellMetadata"]
    NotebookCellTextModel --> CellOutputs["outputs: ICellOutput[]"]
    NotebookCellTextModel --> InternalMetadata["internalMetadata: NotebookCellInternalMetadata"]
    
    CellOutputs --> NotebookCellOutputTextModel["NotebookCellOutputTextModel<br/>Output Data Management"]
```

Sources: [src/vs/workbench/contrib/notebook/common/model/notebookTextModel.ts:570-615](), [src/vs/workbench/contrib/notebook/common/model/notebookCellTextModel.ts:25-125]()

### View Model Layer

```mermaid
graph TB
    NotebookViewModel["NotebookViewModel<br/>View State Management"] --> ViewCells["viewCells: ICellViewModel[]"]
    NotebookViewModel --> SelectionState["Selection & Focus State"]
    NotebookViewModel --> LayoutInfo["NotebookLayoutInfo"]
    
    ViewCells --> CodeCellViewModel["CodeCellViewModel<br/>Code Cell View State"]
    ViewCells --> MarkupCellViewModel["MarkupCellViewModel<br/>Markdown Cell View State"]
    
    CodeCellViewModel --> CodeCellLayout["CodeCellLayoutInfo<br/>- editorHeight<br/>- outputTotalHeight<br/>- outputContainerOffset"]
    CodeCellViewModel --> ExecutionState["Execution State<br/>- isExecuting<br/>- executionOrder"]
    CodeCellViewModel --> OutputViewModels["outputsViewModels: ICellOutputViewModel[]"]
    
    MarkupCellViewModel --> MarkupCellLayout["MarkupCellLayoutInfo<br/>- editorHeight<br/>- previewHeight<br/>- foldHintHeight"]
    MarkupCellViewModel --> EditingState["Editing State<br/>- editState<br/>- renderedHtml"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/viewModel/notebookViewModelImpl.ts:40-100](), [src/vs/workbench/contrib/notebook/browser/viewModel/codeCellViewModel.ts:30-125](), [src/vs/workbench/contrib/notebook/browser/viewModel/markupCellViewModel.ts:22-110]()

## Cell List Management

The `NotebookCellList` manages the virtual scrolling and rendering of cells within the notebook editor.

### Cell List Architecture

```mermaid
graph TB
    WorkbenchList["WorkbenchList<CellViewModel>"] --> NotebookCellList["NotebookCellList<br/>Cell Management"]
    NotebookCellList --> NotebookCellListView["NotebookCellListView<br/>Custom List Implementation"]
    NotebookCellList --> ViewZones["NotebookViewZones<br/>Custom Content Areas"]
    NotebookCellList --> CellOverlays["NotebookCellOverlays<br/>Overlay Management"]
    
    NotebookCellListView --> VirtualizedRendering["Virtualized Cell Rendering"]
    NotebookCellListView --> ScrollManagement["Scroll Event Handling"]
    
    ViewZones --> INotebookViewZone["INotebookViewZone<br/>- afterModelPosition<br/>- domNode<br/>- heightInPx"]
    CellOverlays --> INotebookCellOverlay["INotebookCellOverlay<br/>- cell<br/>- domNode"]
    
    NotebookCellList --> VisibleRanges["visibleRanges: ICellRange[]<br/>Viewport Management"]
    NotebookCellList --> HiddenRanges["Hidden Range Support<br/>Folding & Filtering"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/view/notebookCellList.ts:80-131](), [src/vs/workbench/contrib/notebook/browser/view/notebookCellListView.ts:1-100]()

## Toolbar and UI Components

The notebook editor includes multiple toolbar areas and UI components for notebook and cell-level actions.

### Toolbar System

```mermaid
graph TB
    NotebookEditorWidget --> ToolbarContainers["Toolbar Containers"]
    ToolbarContainers --> NotebookTopToolbar["NotebookEditorWorkbenchToolbar<br/>Document-level Actions"]
    ToolbarContainers --> CellToolbars["Cell-level Toolbars"]
    
    CellToolbars --> CellTitleToolbar["CellTitleToolbarPart<br/>Cell Action Menu"]
    CellToolbars --> CellDeleteToolbar["Cell Delete Actions"]
    CellToolbars --> CellInsertToolbar["Between-cell Insert"]
    CellToolbars --> CellExecuteToolbar["Cell Execution Controls"]
    
    NotebookTopToolbar --> KernelSelection["Kernel Selection UI"]
    NotebookTopToolbar --> DocumentActions["Document Actions<br/>- Save<br/>- Export<br/>- Trust"]
    
    CellTitleToolbar --> MenuIds["MenuId Configuration<br/>- cellTitleToolbar<br/>- cellDeleteToolbar<br/>- cellInsertToolbar<br/>- cellExecuteToolbar"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts:189-194](), [src/vs/workbench/contrib/notebook/browser/viewParts/notebookEditorToolbar.ts:1-50]()

## Event System and State Management

The notebook editor uses a sophisticated event system to coordinate between different layers and components.

### Event Flow

```mermaid
graph LR
    ModelEvents["Model Events<br/>NotebookTextModel"] --> ViewModelEvents["View Model Events<br/>NotebookViewModel"]
    ViewModelEvents --> WidgetEvents["Widget Events<br/>NotebookEditorWidget"]
    WidgetEvents --> UIUpdates["UI Updates<br/>Cell List & Renderers"]
    
    ModelEvents --> CellContentChanged["onDidChangeContent"]
    ModelEvents --> CellOutputChanged["onDidChangeOutputs"]
    ModelEvents --> CellMetadataChanged["onDidChangeMetadata"]
    
    ViewModelEvents --> SelectionChanged["onDidChangeSelection"]
    ViewModelEvents --> VisibleRangesChanged["onDidChangeVisibleRanges"]
    ViewModelEvents --> CellStateChanged["onDidChangeCellState"]
    
    WidgetEvents --> LayoutChanged["onDidChangeLayout"]
    WidgetEvents --> ActiveCellChanged["onDidChangeActiveCell"]
    WidgetEvents --> FocusChanged["onDidChangeFocus"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts:140-185](), [src/vs/workbench/contrib/notebook/browser/notebookViewEvents.ts:1-100]()

## Integration Points

The Notebook Editor integrates with various VS Code systems and provides extension points for customization.

### Extension Integration

```mermaid
graph TB
    NotebookEditor --> ExtensionAPI["Extension API Integration"]
    ExtensionAPI --> NotebookRenderers["Notebook Renderers<br/>Custom Output Rendering"]
    ExtensionAPI --> NotebookSerializers["Notebook Serializers<br/>File Format Support"]
    ExtensionAPI --> KernelProviders["Kernel Providers<br/>Execution Environments"]
    
    NotebookRenderers --> RendererMessaging["INotebookRendererMessagingService<br/>Bidirectional Communication"]
    NotebookSerializers --> NotebookService["INotebookService<br/>Format Registration"]
    KernelProviders --> KernelService["INotebookKernelService<br/>Kernel Management"]
    
    ExtensionAPI --> ContributionPoints["Contribution Points<br/>- commands<br/>- menus<br/>- keybindings"]
```

Sources: [src/vs/workbench/contrib/notebook/browser/notebookEditorWidget.ts:309-361](), [src/vs/workbench/contrib/notebook/common/notebookRendererMessagingService.ts:1-50]()

The Notebook Editor provides a comprehensive editing experience for interactive documents, combining rich text editing, code execution, and extensible output rendering in a unified interface that integrates seamlessly with VS Code's editor framework.