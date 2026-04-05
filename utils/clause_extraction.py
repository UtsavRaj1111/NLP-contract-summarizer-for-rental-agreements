from utils.model_loader import loader
from sentence_transformers import util
import re

# Use the shared SentenceTransformer
model = loader.get_sentence_transformer()

# Expanded Categories and Clauses
CLAUSE_DOMAIN_XREF = {
    "Rental Agreement": {
        "Rent Amount": "monthly rent payment paid to landlord",
        "Security Deposit": "refundable amount held for damages",
        "Termination": "conditions to cancel the lease",
        "Maintenance": "responsibility for repairs",
        "Use of Premises": "how the property can be used"
    },
    "Employment Contract": {
        "Job Title": "official position and duties",
        "Salary & Bonus": "compensation and incentives",
        "Benefits": "insurance PTO and stock options",
        "Confidentiality": "protecting employer's trade secrets",
        "Non-Compete": "restriction on legal working for competitors"
    },
    "Insurance Policy": {
        "Premium": "recurring payment to maintain coverage",
        "Coverage Scope": "what events or assets are insured",
        "Exclusions": "events or items not covered",
        "Deductible": "out-of-pocket cost before insurance pays",
        "Claim Process": "steps to file for insurance payout"
    },
    "Loan Agreement": {
        "Principal Amount": "total money borrowed from lender",
        "Interest Rate": "cost of borrowing as percentage APY",
        "Repayment Term": "schedule to pay back total loan",
        "Collateral": "asset pledged to secure the loan",
        "Default Terms": "consequences of missed payments"
    },
    "Terms & Conditions": {
        "Data Usage": "how user information is collected and used",
        "Cookies": "tracking technologies on website or app",
        "Liability Limit": "maximum legal responsibility of owner",
        "Termination": "closing of user accounts",
        "Dispute Resolution": "arbitration or legal jurisdiction"
    },
    "Non-Disclosure Agreement": {
        "Confidential Info": "definition of protected information",
        "Obligations": "what parties must do to protect data",
        "Permitted Use": "authorized context for sharing info",
        "Duration": "how long data must stay secret",
        "Return of Info": "deleting or returning data after use"
    },
    "General Legal Document": {
        "Governing Law": "legal jurisdiction of the contract",
        "Severe-ability": "legal status if part of contract is invalid",
        "Amendments": "process for changing contract terms",
        "Notices": "how official contact must be made",
        "Signatures": "legal execution by all parties"
    }
}

# --------------------------------------------------
# SAFE SENTENCE SPLITTING
# --------------------------------------------------
def split_sentences(text):
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+|\n', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) == 0:
        sentences = [text[:1000]]
    
    # Efficient split for CPU processing
    return sentences[:300]


# --------------------------------------------------
# DYNAMIC CLAUSE DETECTION
# --------------------------------------------------
def extract_clauses(text, doc_type="General Legal Document"):
    
    sentences = split_sentences(text)
    
    # Get relevant benchmarks
    benchmarks = CLAUSE_DOMAIN_XREF.get(doc_type, CLAUSE_DOMAIN_XREF["General Legal Document"])

    if not sentences:
        return {clause: "Missing (0.0)" for clause in benchmarks}

    # Use ModelLoader for embeddings
    try:
        sentence_embeddings = model.encode(sentences, convert_to_tensor=True, batch_size=32)
    except Exception:
        return {clause: "Missing (0.0)" for clause in benchmarks}

    results = {}

    for clause, definition in benchmarks.items():
        clause_embedding = model.encode(definition, convert_to_tensor=True)
        scores = util.cos_sim(clause_embedding, sentence_embeddings)[0]
        max_score = float(scores.max().item())

        if max_score > 0.40:
            results[clause] = f"Present ({round(max_score,2)})"
        else:
            results[clause] = f"Missing ({round(max_score,2)})"

    return results