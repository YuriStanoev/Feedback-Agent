import anthropic, json, asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_unprocessed_feedback",
        "description": "Returns all feedback items not yet classified.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "save_result",
        "description": "Saves classification result to the database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "feedback_id": {"type": "integer"},
                "category": {"type": "string", "enum": ["bug", "feature_request", "performance", "docs", "other"]},
                "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                "summary": {"type": "string", "description": "One sentence summary"}
            },
            "required": ["feedback_id", "category", "priority", "summary"]
        }
    },
    {
        "name": "get_summary_report",
        "description": "Returns aggregated stats after processing.",
        "input_schema": {"type": "object", "properties": {}}
    }
]


async def call_mcp_tool(name, inputs):
    # Connects to the MCP server via SSE and executes the tool
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments=inputs)
            # Getting the text result from MCP response
            return [content.model_dump() for content in result.content]


def call_tool(name, inputs):
    # Helper func for async MCP
    return asyncio.run(call_mcp_tool(name, inputs))


def run_agent():
    print("Starting Feedback Triage Agent (MCP Mode)...\n")
    messages = [
        {
            "role": "user",
            "content": (
                "You are a product feedback triage agent. "
                "Use get_unprocessed_feedback to fetch all pending items. "
                "Classify each one by category and priority, write a one-sentence summary, "
                "and save each result using save_result. "
                "When done, call get_summary_report and print the final stats."
            )
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5-20251101",  # Make sure you're using the correct model
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print("\nAgent:", block.text)
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  -> Calling {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                result = call_tool(block.name, block.input)
                print(f"     Result: {json.dumps(result, ensure_ascii=False)}\n")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    run_agent()
