from utils.model_loader import loader
from sentence_transformers import util

DOCUMENT_PROTOTYPES = {
    "Rental Agreement": "rental lease agreement for residential or commercial property between landlord and tenant",
    "Employment Contract": "employment agreement between employer and employee regarding job role salary and benefits",
    "Insurance Policy": "insurance policy coverage for health life vehicle or property with premium and deductible",
    "Loan Agreement": "loan agreement between lender and borrower regarding principal amount interest rate and repayment",
    "Terms & Conditions": "website terms and conditions privacy policy user rights and data usage agreement",
    "Non-Disclosure Agreement": "contract to protect confidential information and trade secrets between parties"
}

def classify_document(text):
    """
    Classifies a document based on semantic similarity to predefined prototypes.
    """
    if not text or len(text.strip()) < 50:
        return "General Legal Document", 0.0

    # We take the first 1000 characters for classification to be efficient and accurate
    sample_text = text[:1000]
    
    # Use the shared model from ModelLoader
    model = loader.get_sentence_transformer()
    
    doc_embedding = model.encode(sample_text, convert_to_tensor=True)
    
    best_type = "General Legal Document"
    max_score = 0.0

    for doc_type, description in DOCUMENT_PROTOTYPES.items():
        proto_embedding = model.encode(description, convert_to_tensor=True)
        score = util.cos_sim(doc_embedding, proto_embedding)[0].item()
        
        if score > max_score:
            max_score = score
            best_type = doc_type

    # Threshold for classification
    if max_score < 0.35:
        return "General Legal Document", max_score

    return best_type, round(max_score, 2)
