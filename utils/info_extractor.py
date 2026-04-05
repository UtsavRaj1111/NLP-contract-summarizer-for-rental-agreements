import re
import logging

# Configure production logging
logger = logging.getLogger(__name__)

# --- PRE-COMPILED REGEX PATTERNS (Neural-Aware Patterns) ---
# Enhanced to handle legal 'bridge words' (shall be, of, is) and symbols (Rs., ₹, $)
PATTERNS = {
    "Rental Agreement": {
        "Rent Amount": re.compile(r"(?:Monthly Rent|Rent Amount|Rent)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE),
        "Security Deposit": re.compile(r"(?:Security Deposit|Deposit)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE),
        "Lock-in Period": re.compile(r"(?:Lock-in|Lock in|Minimum Term)[^0-9]*(?:is|of|for)?\s*(\d+)\s*(?:months|years)", re.IGNORECASE)
    },
    "Employment Contract": {
        "Annual Salary": re.compile(r"(?:Salary|CTC|Annual Compensation)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE),
        "Joining Date": re.compile(r"(?:Joining Date|Date of Employment)[^0-9]*(?:is|of)?\s*([\d\-\/\w]+)", re.IGNORECASE),
        "Notice Period": re.compile(r"(?:Notice Period|Resignation Notice)[^0-9]*(?:is|of)?\s*(\d+)\s*(?:days|weeks|months)", re.IGNORECASE)
    },
    "Insurance Policy": {
        "Premium": re.compile(r"(?:Premium|Monthly Premium)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE),
        "Sum Insured": re.compile(r"(?:Sum Insured|Coverage Amount)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE),
        "Deductible": re.compile(r"(?:Deductible)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE)
    },
    "Loan Agreement": {
        "Principal Amount": re.compile(r"(?:Principal|Loan Amount)[^0-9₹$]*(?:Rs\.?|₹|\$)?\s*([\d,]+(?:[./-]\d+)?)", re.IGNORECASE),
        "Interest Rate": re.compile(r"(?:Interest Rate|ROI)[^0-9]*(?:is|of)?\s*([\d.]+)\s*%", re.IGNORECASE),
        "Repayment Term": re.compile(r"(?:Term|Loan Duration)[^0-9]*(?:is|of)?\s*(\d+)\s*(?:months|years)", re.IGNORECASE)
    }
}

def extract_agreement_info(text, doc_type="General Legal Document"):
    """
    High-Fidelity Extraction Engine. 
    Handles complex legal sentence structures by capturing the first valid numeric segment 
    immediately following the entity anchor.
    """
    if not text:
        return {}

    # Standardize spaces for easier scanning
    clean_text = " ".join(text.split())
    category_patterns = PATTERNS.get(doc_type, {})
    extracted_data = {}
    
    for key, pattern in category_patterns.items():
        try:
            match = pattern.search(clean_text)
            if match:
                # Capture the first group (the value)
                value = match.group(1).strip()
                # Re-add symbol if it was part of the match's context for UI clarity
                if "Rs" in match.group(0) or "₹" in match.group(0):
                    value = f"Rs. {value}"
                elif "$" in match.group(0):
                    value = f"${value}"
                    
                extracted_data[key] = value
            else:
                extracted_data[key] = "Not Detected"
        except Exception as e:
            logger.error(f"Metadata extraction error for {key}: {e}")
            extracted_data[key] = "Error"
            
    return extracted_data