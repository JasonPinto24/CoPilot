import os
from dotenv import load_dotenv
load_dotenv()

print("=== Testing Carolin's Setup ===")
print()

# Test 1: Environment variables
print("Test 1: Environment variables")
print("Qdrant URL:", bool(os.getenv("QDRANT_URL")))
print("Cohere key:", bool(os.getenv("COHERE_API_KEY")))
print("LangSmith key:", bool(os.getenv("LANGCHAIN_API_KEY")))
print()

# Test 2: Ollama
print("Test 2: Ollama")
from langchain_ollama import ChatOllama
llm = ChatOllama(model="qwen2.5:7b", base_url="http://localhost:11434")
response = llm.invoke("say hello in one word")
print("Ollama works:", response.content)
print()

# Test 3: LangGraph
print("Test 3: LangGraph")
from langgraph.graph import StateGraph, END
print("LangGraph imports work")
print()

# Test 4: Chainlit
print("Test 4: Chainlit")
import chainlit
print("Chainlit imports work")
print()

# Test 5: FastAPI
print("Test 5: FastAPI")
from fastapi import FastAPI
print("FastAPI imports work")
print()

# Test 6: Qdrant (shared with Jason)
print("Test 6: Qdrant connection")
from qdrant_client import QdrantClient
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
collections = client.get_collections()
print("Qdrant works:", collections)
print()

print("=== All tests passed. Carolin setup complete ===")