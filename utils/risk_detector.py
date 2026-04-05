from utils.model_loader import loader
from sentence_transformers import util

# Shared model for semantic search
model = loader.get_sentence_transformer()

# --- Risk Category Definitions ---
ADVANCED_RISK_BENCHMARKS = {
    "Hidden Charges": {
        "description": "unforeseen administrative fees, additional levies, or hidden processing costs",
        "level": "High Risk",
        "explanation": "This clause may contain hidden financial obligations not explicitly stated in the primary payment terms.",
        "suggestion": "Request an itemized list of all potential 'administrative' or 'unforeseen' costs before signing."
    },
    "One-sided Obligations": {
        "description": "unilateral rights to terminate, change terms without notice, or exempt one party from liability",
        "level": "High Risk",
        "explanation": "The contract grants disproportionate power to one party, potentially leaving you without legal recourse.",
        "suggestion": "Ensure reciprocal rights for termination and require at least 30 days written notice for any changes."
    },
    "Penalty Clauses": {
        "description": "liquidated damages, forfeiture of deposit, or heavy financial penalties for minor breaches",
        "level": "Medium Risk",
        "explanation": "Excessive penalties for minor contract deviations could lead to significant financial loss.",
        "suggestion": "Review the 'liquidated damages' amount and ensure it reflects actual possible loss rather than a penalty."
    },
    "Legal Loopholes": {
        "description": "at sole discretion, without prior notice, excluding warranties, or vague discretionary language",
        "level": "High Risk",
        "explanation": "Vague language like 'at sole discretion' allows the other party to bypass standard legal protections.",
        "suggestion": "Replace 'sole discretion' with 'mutual agreement' or 'reasonable cause' to ensure fairness."
    }
}

# Standard Clause-based risks
RISK_PROFILES = {
    "Rental Agreement": {
        "High Risk": ["Rent Amount", "Security Deposit", "Termination"],
        "Medium Risk": ["Maintenance"],
        "Low Risk": ["Use of Premises"]
    },
    "Employment Contract": {
        "High Risk": ["Salary & Bonus", "Non-Compete"],
        "Medium Risk": ["Job Title", "Benefits"],
        "Low Risk": ["Confidentiality"]
    },
    "Insurance Policy": {
        "High Risk": ["Premium", "Exclusions", "Coverage Scope"],
        "Medium Risk": ["Deductible"],
        "Low Risk": ["Claim Process"]
    },
    "Loan Agreement": {
        "High Risk": ["Principal Amount", "Interest Rate", "Default Terms"],
        "Medium Risk": ["Repayment Term"],
        "Low Risk": ["Collateral"]
    },
    "Terms & Conditions": {
        "High Risk": ["Liability Limit", "Data Usage"],
        "Medium Risk": ["Termination", "Dispute Resolution"],
        "Low Risk": ["Cookies"]
    },
    "Non-Disclosure Agreement": {
        "High Risk": ["Confidential Info", "Obligations"],
        "Medium Risk": ["Duration", "Return of Info"],
        "Low Risk": ["Permitted Use"]
    },
    "General Legal Document": {
        "High Risk": ["Signatures", "Governing Law"],
        "Medium Risk": ["Amendments", "Notices"],
        "Low Risk": ["Severe-ability"]
    }
}

def detect_clause_risk(clauses, doc_type="General Legal Document"):
    """Determines risk based on missing mandatory clauses."""
    risks = {}
    profile = RISK_PROFILES.get(doc_type, RISK_PROFILES["General Legal Document"])
    for clause, status in clauses.items():
        if "Present" in status:
            risks[clause] = "Low Risk"
            continue
        if "Missing" in status:
            risks[clause] = "High Risk" if clause in profile["High Risk"] else ("Medium Risk" if clause in profile["Medium Risk"] else "Low Risk")
        else:
            risks[clause] = "Medium Risk"
    return risks

def get_detailed_risks(text):
    """
    Scans document text for advanced legal pitfalls.
    Returns a list of high-impact risk objects.
    """
    if not text: return []
    
    # We split into large blocks to keep semantic context
    blocks = [text[i:i+1500] for i in range(0, len(text), 1200)]
    try:
        block_embeddings = model.encode(blocks, convert_to_tensor=True, batch_size=8)
    except:
        return []

    identified_risks = []

    for risk_name, meta in ADVANCED_RISK_BENCHMARKS.items():
        risk_embedding = model.encode(meta["description"], convert_to_tensor=True)
        scores = util.cos_sim(risk_embedding, block_embeddings)[0]
        max_score = float(scores.max().item())

        # Higher threshold for specific risk detection to avoid noise
        if max_score > 0.45:
            identified_risks.append({
                "type": risk_name,
                "level": meta["level"],
                "explanation": meta["explanation"],
                "suggestion": meta["suggestion"]
            })

    return identified_risks