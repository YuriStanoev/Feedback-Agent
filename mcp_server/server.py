from mcp.server.fastmcp import FastMCP
import psycopg2, os

mcp = FastMCP("Feedback MCP Server")


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "feedbackdb"),
        user=os.getenv("DB_USER", "agent"),
        password=os.getenv("DB_PASSWORD", "secret")
    )


@mcp.tool()
def get_unprocessed_feedback() -> list[dict]:
    # Returns all feedback items not yet classified.

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id, f.source, f.text
        FROM feedback f
        LEFT JOIN results r ON f.id = r.feedback_id
        WHERE r.id is NULL
        ORDER BY f.created_at""")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "source": r[1], "text": r[2]} for r in rows]


@mcp.tool()
def save_result(feedback_id: int, category: str, priority: str, summary: str) -> str:
    # Saves the agent's classification back to the database.
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (feedback_id, category, priority, summary) VALUES (%s, %s, %s, %s)",
        (feedback_id, category, priority, summary)
    )
    conn.commit()
    conn.close()
    return f"Saved result for feedback_id={feedback_id}"


@mcp.tool()
def get_summary_report() -> dict:
    # Returns aggregated stats: count per category and priority.
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT category, priority, COUNT(*) FROM results GROUP BY category, priority")
    rows = cur.fetchall()
    conn.close()
    return {"stats": [{"category": r[0], "priority": r[1], "count": r[2]} for r in rows]}


if __name__ == "__main__":
    ##mcp.run()
    ##mcp.run(transport="sse", host="0.0.0.0", port=8000)
    mcp.run(transport="sse")
