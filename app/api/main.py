from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import os
import time
import mlflow
from app.agent.graph import agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PDF Extraction Agent",
    description="Agent IA pour extraire des données structurées depuis des PDFs",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

mlflow.set_experiment("pdf-extraction-agent")

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Fichier PDF requis")

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        with mlflow.start_run():
            mlflow.set_tag("filename", file.filename)
            start_time = time.time()

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
            duration = time.time() - start_time

            mlflow.log_metric("pages", output["pages"])
            mlflow.log_metric("tables_found", len(output["tables"]))
            mlflow.log_metric("names_found", len(output["names"]))
            mlflow.log_metric("dates_found", len(output["dates"]))
            mlflow.log_metric("amounts_found", len(output["amounts"]))
            mlflow.log_metric("processing_time_seconds", duration)
            mlflow.log_metric("errors_count", len(result["errors"]))

            return JSONResponse(output)

    finally:
        os.unlink(tmp_path)

@app.get("/health")
def health():
    return {"status": "ok", "message": "PDF Extraction Agent is running"}