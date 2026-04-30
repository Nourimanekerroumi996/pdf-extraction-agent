import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from pdf2image import convert_from_path

def extract_ocr(pdf_path: str) -> list[str]:
    """
    Extrait le texte d'un PDF scanné via OCR.
    Convertit chaque page en image puis lit les pixels.
    Ne se déclenche que si le PDF est scanné (pas de texte direct).
    """
    results = []
    
    try:
        # Convertit chaque page PDF en image
        images = convert_from_path(pdf_path, dpi=200)
        
        for img in images:
            # Lit le texte dans l'image (anglais)
            text = pytesseract.image_to_string(img, lang="eng")
            if text.strip():
                results.append(text.strip())
    except Exception as e:
        print(f"OCR error: {e}")
    
    return results