from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    pdf_path: str
    filename: str
    text: str
    pages: int
    tables: Annotated[list, operator.add]
    ocr_results: Annotated[list, operator.add]
    entities: dict
    errors: Annotated[list, operator.add]
    final_output: dict | None