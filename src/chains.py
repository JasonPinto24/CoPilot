def get_retrieval_chain():
    """
    STUB — Jason replaces this at Day 2 sync.
    Interface: chain.invoke({"question": query})
    Returns: {"answer": str, "source_documents": list}
    """
    class StubChain:
        def invoke(self, inputs):
            return {
                "answer": "STUB ANSWER — real retrieval not connected yet",
                "source_documents": [
                    {
                        "page_content": "stub chunk 1 about VPN setup",
                        "metadata": {
                            "source": "stub.md",
                            "page": 1,
                            "type": "doc"
                        }
                    },
                    {
                        "page_content": "stub chunk 2 about Kafka troubleshooting",
                        "metadata": {
                            "source": "stub.md",
                            "page": 2,
                            "type": "doc"
                        }
                    }
                ]
            }
    return StubChain()