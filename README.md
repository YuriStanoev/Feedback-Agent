# Feedback Triage Agent

An agentic AI system that automatically classifies and prioritizes product feedback using Claude AI, MCP (Model Context Protocol), and PostgreSQL.

## What it does

The agent reads unprocessed feedback from a PostgreSQL database, uses Claude AI to classify each item by category and priority, saves the results back to the database, and generates a summary report — all autonomously in a single run.

## Architecture

- **PostgreSQL** — stores incoming feedback and classification results
- **MCP Server** — exposes 3 tools: `get_unprocessed_feedback`, `save_result`, `get_summary_report`
- **Claude Agent** — calls the MCP tools autonomously to triage all pending feedback

## How to run

1. Clone the repo
2. Add your Anthropic API key to `.env`:

   ANTHROPIC_API_KEY=sk-ant-...

3. Start the infrastructure:

   docker-compose up -d --build

4. Run the MCP server

  cd mcp_server
  python server.py
  
5. Run the agent:

   cd agent
   python agent.py


## Tech stack

Python · PostgreSQL · Docker · Anthropic Claude API · MCP Protocol
