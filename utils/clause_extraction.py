from sentence_transformers import SentenceTransformer, util
import re

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Clause semantic descriptions
CLAUSE_REFERENCES = {
    "Rent": "monthly payment amount paid by tenant to landlord",
    "Security Deposit": "refundable deposit amount held by landlord",
    "Term": "duration of rental agreement period",
    "Termination": "conditions to end or cancel the agreement",
    "Maintenance": "responsibility for repairs and utilities",
    "Use of Premises": "rules for using the rented property",
    "Governing Law": "legal jurisdiction of agreement"
}


# --------------------------------------------------
# SAFE SENTENCE SPLITTING
# --------------------------------------------------
def split_sentences(text):

    if not text:
        return []

    # split by punctuation or newline
    sentences = re.split(r'(?<=[.!?])\s+|\n', text)

    # remove empty
    sentences = [s.strip() for s in sentences if s.strip()]

    # if extraction failed, fallback
    if len(sentences) == 0:
        sentences = [text[:500]]

    # limit for performance
    sentences = sentences[:200]

    return sentences


# --------------------------------------------------
# CLAUSE DETECTION
# --------------------------------------------------
def extract_clauses(text):

    sentences = split_sentences(text)

    # Safety check
    if not sentences:
        return {clause: "Missing (0.0)" for clause in CLAUSE_REFERENCES}

    try:

        sentence_embeddings = model.encode(
            sentences,
            convert_to_tensor=True,
            batch_size=16
        )

    except Exception:
        return {clause: "Missing (0.0)" for clause in CLAUSE_REFERENCES}

    results = {}

    for clause, meaning in CLAUSE_REFERENCES.items():

        clause_embedding = model.encode(
            meaning,
            convert_to_tensor=True
        )

        scores = util.cos_sim(clause_embedding, sentence_embeddings)[0]

        max_score = float(scores.max().item())

        if max_score > 0.45:
            results[clause] = f"Present ({round(max_score,2)})"
        else:
            results[clause] = f"Missing ({round(max_score,2)})"

    return results