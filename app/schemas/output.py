from pydantic import BaseModel, Field
from typing import Optional

class TableData(BaseModel):
    headers: list[str]
    rows: list[list[str]]
    page: int

class ExtractedDocument(BaseModel):
    filename: str
    pages: int
    text: str = Field(description="Texte brut complet")
    tables: list[TableData] = Field(default_factory=list)
    images_text: list[str] = Field(default_factory=list)
    titles: list[str] = Field(default_factory=list)
    dates: list[str] = Field(default_factory=list)
    amounts: list[str] = Field(default_factory=list)
    names: list[str] = Field(default_factory=list)
    raw_entities: dict = Field(default_factory=dict)