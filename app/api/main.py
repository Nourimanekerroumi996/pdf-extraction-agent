from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import uuid
from app.agent.graph import agent

app = FastAPI(
    title="PDF Extraction Agent",
    description="Agent IA pour extraire des données structurées depuis des PDFs",
    version="1.0.0"
)

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    """
    Reçoit un PDF, lance l'agent et retourne les données extraites.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Fichier PDF requis")

    # Sauvegarde temporaire du PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Lance l'agent
        initial_state = {
            "pdf_path": tmp_path,
            "filename": file.filename,
            "text": "",
            "pages": 0,
            "tables": [],
            "ocr_results": [],
            "entities": {},
            "errors": [],
            "final_output": None
        }

        result = agent.invoke(initial_state)
        output = result["final_output"]
        return JSONResponse(output)

    finally:
        # Supprime le fichier temporaire
        os.unlink(tmp_path)

@app.get("/health")
def health():
    """Vérifie que l'API est en ligne"""
    return {"status": "ok", "message": "PDF Extraction Agent is running"}