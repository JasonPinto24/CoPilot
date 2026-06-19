from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    query:        str
    messages:     Annotated[list, add_messages]
    tool_output:  str
    hits:         list
    answer:       str
    citations:    list
    escalated:    bool
    confidence:   float