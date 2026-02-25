from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load semantic model (runs once)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Define clause categories with semantic descriptions
CLAUSE_REFERENCES = {
    "Rent": "monthly payment amount paid by tenant to landlord",
    "Security Deposit": "refundable deposit amount held by landlord",
    "Term": "duration of rental agreement period",
    "Termination": "conditions to end or cancel the agreement",
    "Maintenance": "responsibility for repairs and utilities",
    "Use of Premises": "rules for using the rented property",
    "Governing Law": "legal jurisdiction of agreement"
}

def extract_clauses(text):
    sentences = text.split(".")  # simple sentence split
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

    results = {}

    for clause, meaning in CLAUSE_REFERENCES.items():
        clause_embedding = model.encode(meaning, convert_to_tensor=True)

        scores = util.cos_sim(clause_embedding, sentence_embeddings)[0]
        max_score = float(scores.max().item())

        # Threshold for presence
        if max_score > 0.45:
            results[clause] = f"Present ({round(max_score, 2)})"
        else:
            results[clause] = f"Missing ({round(max_score, 2)})"

    return results