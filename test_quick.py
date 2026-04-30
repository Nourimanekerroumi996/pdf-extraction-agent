from app.agent.graph import agent

initial_state = {
    "pdf_path": "tests/fixtures/sample.pdf",
    "filename": "sample.pdf",
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

print(f"Fichier : {output['filename']}")
print(f"Pages : {output['pages']}")
print(f"Noms : {output['names']}")
print(f"Dates : {output['dates']}")
print(f"Montants : {output['amounts']}")
print(f"Titres : {output['titles'][:3]}")
print(f"Tableaux : {len(output['tables'])}")
print(f"Erreurs : {result['errors']}")