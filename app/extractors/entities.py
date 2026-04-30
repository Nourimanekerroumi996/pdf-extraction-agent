import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

ENTITY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un extracteur d'entités expert.
Analyse le texte fourni et retourne UNIQUEMENT un JSON valide avec exactement ces champs :
{{
  "titles": ["liste des titres et en-têtes principaux"],
  "dates": ["toutes les dates trouvées"],
  "amounts": ["tous les montants monétaires et numériques importants"],
  "names": ["noms de personnes et organisations"]
}}
Retourne UNIQUEMENT le JSON, rien d'autre."""),
    ("human", "Texte à analyser :\n\n{text}")
])

def extract_entities(text: str) -> dict:
    """
    Utilise Groq (Llama 3) pour extraire les entités importantes du texte.
    Retourne un dict avec titles, dates, amounts, names.
    """
    if not text.strip():
        return {"titles": [], "dates": [], "amounts": [], "names": []}
    
    try:
        chain = ENTITY_PROMPT | llm
        response = chain.invoke({"text": text[:4000]})
        
        # Nettoie les backticks si présents
        raw = re.sub(r"```json|```", "", response.content).strip()
        return json.loads(raw)
    
    except Exception as e:
        print(f"Entity extraction error: {e}")
        return {"titles": [], "dates": [], "amounts": [], "names": []}