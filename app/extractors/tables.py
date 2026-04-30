import camelot

def extract_tables(pdf_path: str) -> list[dict]:
    """
    Extrait tous les tableaux d'un PDF.
    Essaie d'abord lattice (tables avec bordures)
    puis stream (tables sans bordures) en fallback.
    Retourne une liste de dicts {headers, rows, page}
    """
    tables_out = []

    # Essai 1 : lattice (tables avec lignes visibles)
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")
        if tables.n > 0:
            for t in tables:
                df = t.df
                tables_out.append({
                    "headers": df.iloc[0].tolist(),
                    "rows": df.iloc[1:].values.tolist(),
                    "page": t.page
                })
            return tables_out
    except Exception:
        pass

    # Essai 2 : stream (tables sans bordures)
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
        for t in tables:
            df = t.df
            tables_out.append({
                "headers": df.iloc[0].tolist(),
                "rows": df.iloc[1:].values.tolist(),
                "page": t.page
            })
    except Exception:
        pass

    return tables_out