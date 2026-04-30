from app.agent.state import AgentState
from app.extractors.text import extract_text
from app.extractors.tables import extract_tables
from app.extractors.ocr import extract_ocr
from app.extractors.entities import extract_entities
from app.schemas.output import ExtractedDocument
import os

def node_extract_text(state: AgentState) -> AgentState:
    """Nœud 1 : extrait le texte du PDF"""
    try:
        text, pages = extract_text(state["pdf_path"])
        return {**state, "text": text, "pages": pages}
    except Exception as e:
        return {**state, "errors": state["errors"] + [f"text: {str(e)}"]}

def node_extract_tables(state: AgentState) -> AgentState:
    """Nœud 2 : extrait les tableaux du PDF"""
    try:
        tables = extract_tables(state["pdf_path"])
        return {**state, "tables": tables}
    except Exception as e:
        return {**state, "errors": state["errors"] + [f"tables: {str(e)}"], "tables": []}

def node_extract_ocr(state: AgentState) -> AgentState:
    """Nœud 3 : OCR seulement si PDF scanné (peu de texte)"""
    if len(state.get("text", "")) > 200:
        return {**state, "ocr_results": []}
    try:
        ocr = extract_ocr(state["pdf_path"])
        return {**state, "ocr_results": ocr}
    except Exception as e:
        return {**state, "errors": state["errors"] + [f"ocr: {str(e)}"], "ocr_results": []}

def node_extract_entities(state: AgentState) -> AgentState:
    """Nœud 4 : extrait les entités avec Groq"""
    text = state.get("text", "") or " ".join(state.get("ocr_results", []))
    if not text.strip():
        return {**state, "entities": {}}
    try:
        entities = extract_entities(text)
        return {**state, "entities": entities}
    except Exception as e:
        return {**state, "errors": state["errors"] + [f"entities: {str(e)}"], "entities": {}}

def node_aggregate(state: AgentState) -> AgentState:
    """Nœud 5 : assemble le résultat final"""
    entities = state.get("entities", {})
    output = ExtractedDocument(
        filename=state["filename"],
        pages=state.get("pages", 0),
        text=state.get("text", ""),
        tables=state.get("tables", []),
        images_text=state.get("ocr_results", []),
        titles=entities.get("titles", []),
        dates=entities.get("dates", []),
        amounts=entities.get("amounts", []),
        names=entities.get("names", []),
        raw_entities=entities
    )
    return {**state, "final_output": output.model_dump()}