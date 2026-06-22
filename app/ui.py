import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chainlit as cl
from src.graph import app as graph_app


# ── On chat start ─────────────────────────────────────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=(
            "👋 Welcome to the **Northwind Systems Knowledge Copilot**!\n\n"
            "Ask me anything about internal procedures, troubleshooting, "
            "or past incidents.\n\n"
            "**Example questions:**\n"
            "- How do I set up VPN at Northwind?\n"
            "- Has anyone seen Kafka consumer lag before?\n"
            "- Summarize the Kubernetes deployment docs"
        )
    ).send()


# ── On message ────────────────────────────────────────────────────────────────
@cl.on_message
async def on_message(message: cl.Message):
    question = message.content

    # Build initial state
    initial_state = {
        "query":       question,
        "messages":    [],
        "tool_output": "",
        "hits":        [],
        "answer":      "",
        "citations":   [],
        "escalated":   False,
        "confidence":  0.0,
    }

    # Show thinking indicator
    # Show thinking indicator
    async with cl.Step(name="Searching knowledge base..."):
        import asyncio
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: graph_app.invoke(initial_state)
        )

    answer    = result.get("answer", "No answer received")
    citations = result.get("citations", [])
    escalated = result.get("escalated", False)

    # Show escalation warning
    if escalated:
        await cl.Message(
            content=f"⚠️ **Escalated to Human Support**\n\n{answer}"
        ).send()
        return

    # Build citation text
    citation_text = ""
    if citations:
        citation_text = "\n\n---\n**Sources:**\n"
        for c in citations:
            citation_text += f"- [{c['n']}] {c['source']} (page {c['page']})\n"

    # Send answer with citations
    await cl.Message(
        content=answer + citation_text
    ).send()