from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    node_extract_text,
    node_extract_tables,
    node_extract_ocr,
    node_extract_entities,
    node_aggregate
)

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("extract_text",     node_extract_text)
    graph.add_node("extract_tables",   node_extract_tables)
    graph.add_node("extract_ocr",      node_extract_ocr)
    graph.add_node("extract_entities", node_extract_entities)
    graph.add_node("aggregate",        node_aggregate)

    # Séquence simple : un nœud après l'autre
    graph.set_entry_point("extract_text")
    graph.add_edge("extract_text",     "extract_tables")
    graph.add_edge("extract_tables",   "extract_ocr")
    graph.add_edge("extract_ocr",      "extract_entities")
    graph.add_edge("extract_entities", "aggregate")
    graph.add_edge("aggregate",        END)

    return graph.compile()

agent = build_graph()