from sentence_transformers import SentenceTransformer, util
import re

# Load semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Clause descriptions
CLAUSE_REFERENCES = {
    "Rent": "monthly payment amount paid by tenant to landlord",
    "Security Deposit": "refundable deposit amount held by landlord",
    "Term": "duration of rental agreement period",
    "Termination": "conditions to end or cancel the agreement",
    "Maintenance": "responsibility for repairs and utilities",
    "Use of Premises": "rules for using the rented property",
    "Governing Law": "legal jurisdiction of agreement"
}


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+|\n', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return sentences


def extract_clauses(text):

    sentences = split_sentences(text)

    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

    results = {}

    for clause, meaning in CLAUSE_REFERENCES.items():

        clause_embedding = model.encode(meaning, convert_to_tensor=True)

        scores = util.cos_sim(clause_embedding, sentence_embeddings)[0]

        max_score = float(scores.max().item())

        if max_score > 0.45:
            results[clause] = f"Present ({round(max_score,2)})"
        else:
            results[clause] = f"Missing ({round(max_score,2)})"

    return results


def find_clause_evidence(text, clause_name):

    sentences = split_sentences(text)

    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

    clause_description = CLAUSE_REFERENCES[clause_name]
    clause_embedding = model.encode(clause_description, convert_to_tensor=True)

    scores = util.cos_sim(clause_embedding, sentence_embeddings)[0]

    best_index = scores.argmax().item()
    best_score = scores[best_index].item()

    if best_score < 0.40:
        return "No strong clause evidence detected"

    return sentences[best_index].strip()