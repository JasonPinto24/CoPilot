import chainlit as cl
import httpx

# ── FastAPI endpoint URL ──────────────────────────────────────────────────────
API_URL = "http://localhost:8000/ask"


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

    # Show thinking indicator
    async with cl.Step(name="Searching knowledge base...") as step:
        step.output = f"Processing: {question}"

    # Call FastAPI endpoint
    async with httpx.AsyncClient(timeout=120) as client:
        try:
            response = await client.post(
                API_URL,
                json={"question": question}
            )
            result = response.json()

        except Exception as e:
            await cl.Message(
                content=f"Error connecting to the API: {e}"
            ).send()
            return

    # Extract results
    answer    = result.get("answer", "No answer received")
    citations = result.get("citations", [])
    escalated = result.get("escalated", False)

    # Show escalation warning
    if escalated:
        await cl.Message(
            content=(
                "⚠️ **Escalated to Human Support**\n\n"
                f"{answer}"
            ),
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