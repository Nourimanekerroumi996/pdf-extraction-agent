from app.extractors.entities import extract_entities

texte = """
FACTURE N°2024-001
Date : 12 mars 2024
Client : Jean Dupont
Société : ABC Consulting

Produit          Prix
Développement    1500€
Réunion          200€

Total : 1700€
Signé par : Marie Martin
"""

resultat = extract_entities(texte)
print(f"Titres : {resultat['titles']}")
print(f"Dates : {resultat['dates']}")
print(f"Montants : {resultat['amounts']}")
print(f"Noms : {resultat['names']}")