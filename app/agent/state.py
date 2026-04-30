from typing import TypedDict

class AgentState(TypedDict):
    pdf_path: str
    filename: str
    text: str
    pages: int
    tables: list
    ocr_results: list
    entities: dict
    errors: list
    final_output: dict | None