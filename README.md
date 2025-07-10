
# MCP-DOC-AGENT

MCP-DOC-AGENT is a developer tool that enables Agentic AI to automatically generate and maintain GitBook-style documentation for codebases. It is designed to help developers and teams keep their documentation up-to-date and comprehensive with minimal manual effort.

## Overview
Under the hood, MCP-DOC-AGENT performs the following steps:
- Retrieves repository information and generates a repository tree to understand the structure.
- Ignores development folders and files (e.g., node_modules, .env, and other irrelevant files).
- Scans all important files to generate context for documentation.
- Sequentially generates key markdown files for the project.
- Uses Docsify to create and serve GitBook-style documentation.
- Allows ongoing maintenance and updates to the generated docs.

It leverages a powerful stack including:
- **uv**: For fast Python package management and execution.
- **fastmcp** and **mcp**: For agent orchestration and server management.
- **cursor**: For code navigation and analysis.
- **Agentic AI**: For intelligent code understanding and documentation generation.
- **Docsify**: For rendering and maintaining beautiful, interactive documentation sites.

## Features
- **GitBook-Style Documentation:** Automatically generates and maintains documentation in a familiar, interactive format.
- **Repository Analysis:** Provides detailed information about repository structure, files, and content.
- **Smart File Selection:** Ignores unnecessary dev files and folders, focusing on what matters.
- **Contextual Scanning:** Scans and analyzes important files to generate rich documentation context.
- **Custom Tools:** Includes utilities for file content extraction, repository details, and more.
- **Extensible Architecture:** Easily add new tools or extend existing ones for custom workflows.

## Project Structure
```
app/
  main.py                # Main entry point for the application
  server.py              # Server logic for running the agent
  deepwiki/
    deepwiki_extractor.py  # Core logic for extracting documentation
    prompt/
      prompt.txt           # Prompt templates for extraction
    tools/
      client.py            # Client utilities
      file_content.py      # File content extraction logic
      file_info.py         # File metadata utilities
      repository_details.py# Repository details extraction
      repository_tree.py   # Repository tree structure logic
```

## Getting Started
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd mcp-doc-agent
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using Poetry:
   ```sh
   poetry install
   ```
3. **Integrate with MCP Agent:**
   - Add this server as a tool in your MCP agent configuration. Example configuration:
     ```json
     {
       "mcpServers": {
         "mcp-doc-agent": {
           "command": "uv",
           "args": [
             "--directory",
             "/path/to/mcp-doc-agent/app",
             "run",
             "main.py"
           ]
         }
       }
     }
     ```
   - This will run the server using the correct command and arguments for integration with your MCP agent.

## Requirements
- Python 3.12+
- See `pyproject.toml` for dependencies

## Usage
Once integrated, your Agentic AI agent will use this server to:
- Analyze your codebase and generate a repository tree
- Ignore dev files/folders and focus on important code
- Generate markdown documentation files for your project
- Use Docsify to serve and maintain a GitBook-style documentation site

You can customize prompts and tools as needed for your workflow.

## License
See the `LICENCE` file for license information.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.
