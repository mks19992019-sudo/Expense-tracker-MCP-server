# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for managing personal expenses locally. This server allows you to track expenses by categories and subcategories using Claude Desktop.

## Setup Instructions

### Prerequisites

Before you begin, make sure you have **uv** (Python package manager) installed on your machine. If not, install it from [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/).

### Step 1: Install FastMCP CLI and Claude Desktop Integration

Run the following command to install fastmcp and set up Claude Desktop integration:

```bash
uv run fastmcp install claude-desktop main.py
```

This command will:
- Install the FastMCP CLI tools
- Set up the necessary configuration for Claude Desktop

### Step 2: Configure Claude Desktop

After running the above command, you need to edit the Claude Desktop configuration file:

1. Open Claude Desktop configuration file (usually located at `~/.claude/config.json` or `%APPDATA%\Claude\config.json` on Windows)

2. Find the `mcpServers` section and locate the entry for this Expense Tracker server

3. Edit the path to use the `uv` command. Your configuration should look similar to:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": ["run", "--with", "fastmcp", "python", "/path/to/your/main.py"]
    }
  }
}
```

**Important**: Replace `/path/to/your/` with the actual path to where you have this project.

### Step 3: Verify uv is Installed

To verify that `uv` is properly installed on your system, run:

```bash
uv --version
```

You should see the version number. If you see "command not found", please install uv first.

## Project Dependencies

This project uses `uv` for dependency management. The dependencies are managed in `pyproject.toml`.

### Adding Dependencies

To add a new dependency to this project, use:

```bash
uv add library_name
```

For example:
```bash
uv add requests
```

### Current Dependencies

- **fastmcp** (>=3.2.0) - Model Context Protocol server framework
- **aiosqlite** (>=0.19.0) - Async SQLite database interface

## How It Works

This MCP server provides tools to:
- Add expense entries with date, amount, category, and subcategory
- Query and manage your expense data
- Organize expenses by predefined categories (Food, Transport, Housing, Utilities, etc.)

All data is stored locally in a SQLite database (`expenses.db`), ensuring your financial data remains private and on your machine.

## Using with Claude Desktop

Once configured, open Claude Desktop and you'll have access to the Expense Tracker tools. You can then ask Claude to help you:
- Record expenses
- Categorize spending
- Review expense data

## Local Development

If you're developing this server locally:

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the server:
   ```bash
   uv run main.py
   ```

The server will start on `localhost:8000` by default.
