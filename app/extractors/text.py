import pdfplumber

def extract_text(pdf_path: str) -> tuple[str, int]:
    """
    Extrait le texte complet d'un PDF page par page.
    Retourne (texte_complet, nombre_de_pages)
    """
    full_text = []
    
    with pdfplumber.open(pdf_path) as pdf:
        pages = len(pdf.pages)
        
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
    
    return "\n\n".join(full_text), pages