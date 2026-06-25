import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import chainlit as cl
from src.graph import app as graph_app

# ── On chat start ─────────────────────────────────────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=(
            "# 🏢 Northwind Systems Knowledge Copilot\n\n"
            "Your AI-powered assistant for internal IT knowledge.\n\n"
            "---\n\n"
            "### What I can help you with:\n\n"
            "🔍 **Find procedures** — SOPs, runbooks, setup guides\n\n"
            "🎫 **Search past incidents** — Has anyone solved this before?\n\n"
            "📋 **Summarize documents** — Get the key points fast\n\n"
            "⚠️ **Honest escalation** — I tell you when I don't know\n\n"
            "---\n\n"
            "### Try these questions:\n\n"
            "```\nHow do I set up VPN at Northwind?\n```\n"
            "```\nHas anyone seen Kafka consumer lag before?\n```\n"
            "```\nSummarize the Kubernetes deployment docs\n```\n"
            "```\nWhat is Northwind's deployment policy for Singapore?\n```\n\n"
            "---\n"
            "*Powered by LangGraph + Ollama + Qdrant + Cohere*"
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
    async with cl.Step(name="🔍 Searching knowledge base...") as step:
        step.output = f"Processing: *{question}*"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: graph_app.invoke(initial_state)
        )

    answer    = result.get("answer", "No answer received")
    citations = result.get("citations", [])
    escalated = result.get("escalated", False)
    confidence = result.get("confidence", 0.0)

    # Show escalation warning
    if escalated:
        await cl.Message(
            content=(
                "## ⚠️ Escalated to Human Support\n\n"
                f"{answer}\n\n"
                "---\n"
                "*This query has been logged for knowledge base improvement.*"
            )
        ).send()
        return

    # Build citation elements
    citation_text = ""
    if citations:
        citation_text = "\n\n---\n### 📚 Sources\n\n"
        for c in citations:
            icon = "🎫" if c.get("type") == "ticket" else "📄"
            citation_text += f"{icon} **[{c['n']}]** `{c['source']}` — page {c['page']}\n\n"

    # Add confidence indicator
    if confidence >= 0.9:
        confidence_badge = "🟢 High confidence"
    elif confidence >= 0.5:
        confidence_badge = "🟡 Medium confidence"
    else:
        confidence_badge = "🟠 Low confidence"

    # Send answer with citations and confidence
    await cl.Message(
        content=(
            f"{answer}"
            f"{citation_text}"
            f"\n\n---\n*{confidence_badge} · Rerank score: {confidence:.2f}*"
        )
    ).send()