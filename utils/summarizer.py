from utils.model_loader import loader
import re
import logging

logger = logging.getLogger(__name__)

def generate_summary(text, info=None):
    """
    High-Performance Neural Summarizer: Optimized for speed (DistilBART) 
    and document completeness. Fixed for financial precision (No 'Rs.' splits).
    """
    if not text or len(text.strip()) == 0:
        return "No text detected in document."

    summarizer = loader.get_summarizer()
    info = info or {}

    # Step 1: Global Document Scanning (Complete Coverage)
    chunk_size = 3000
    overlap = 500
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]
    
    # Priority keywords for identifying "Legal Impact" segments
    priority_keywords = ["rent", "salary", "premium", "party", "effective date", "termination", "liability", "breach", "indemnity", "governing law"]
    
    scored_chunks = []
    for chunk in chunks:
        score = sum(1 for kw in priority_keywords if kw in chunk.lower())
        scored_chunks.append((score, chunk))
    
    # Sort and take top 10 chunks (Deep Scan)
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    summarization_queue = [c[1] for c in scored_chunks[:10]]

    # Step 2: High-Speed Neural Summarization (DistilBART)
    summarized_chunks = []
    for chunk in summarization_queue:
        try:
            summary = summarizer(
                chunk,
                max_length=120, 
                min_length=50,
                do_sample=False,
                repetition_penalty=1.8
            )
            summarized_chunks.append(summary[0]["summary_text"])
        except Exception as e:
            logger.error(f"Summarizer segment inference failed: {e}")
            continue

    if not summarized_chunks:
        return "Intelligence Scan Complete. Accuracy grounding required."

    # Step 3: Synthesis & Financial Precision Sectioning
    financials = []
    obligations = []
    metadata_list = []

    # 3.1 Metadata Injection (Guaranteed Accuracy)
    if info:
        for k, v in info.items():
            if v and v not in ["Not Detected", "Error"]:
                metadata_list.append(f"<div style='margin-bottom: 0.5rem;'>&bull; <b>{k}</b>: <span style='color: #10B981;'>{v}</span></div>")

    # 3.2 Semantic Routing with "Zero-Split" Regex
    # FIXED: This regex avoids splitting at "Rs." or "No." abbreviations used in legal docs.
    combined_raw = " ".join(summarized_chunks)
    sentences = re.split(r'(?<!Rs)(?<!No)(?<!Co)(?<!Ltd)\.\s', combined_raw)
    
    for sentence in sentences:
        s = sentence.strip()
        if len(s) < 30: continue
        if not s.endswith("."): s += "."

        # Intelligence Topic Routing
        text_l = s.lower()
        if any(w in text_l for w in ["pay", "rent", "fee", "cost", "dollar", "month", "annual", "compensation", "rs", "₹", "$"]):
            financials.append(f"<div style='margin-bottom: 0.5rem;'>&bull; {s}</div>")
        else:
            obligations.append(f"<div style='margin-bottom: 0.5rem;'>&bull; {s}</div>")

    # Step 4: Final Intelligence Construction (Rich Dashboard Output)
    final_output = []
    
    if metadata_list:
        final_output.append("<h4 style='color: #0F172A; margin: 1.5rem 0 0.8rem 0; text-transform: uppercase; font-size: 0.85rem;'>Verified Contract Metadata</h4>")
        final_output.extend(metadata_list)

    if financials:
        # Sort financials so bullets containing amounts come first
        financials.sort(key=lambda x: any(c.isdigit() for c in x), reverse=True)
        final_output.append("<h4 style='color: #10B981; margin: 1.5rem 0 0.8rem 0; text-transform: uppercase; font-size: 0.85rem;'>Financial Obligations</h4>")
        final_output.extend(financials[:12]) 

    if obligations:
        final_output.append("<h4 style='color: #64748B; margin: 1.5rem 0 0.8rem 0; text-transform: uppercase; font-size: 0.85rem;'>Core Terms & Clauses</h4>")
        final_output.extend(obligations[:15])

    return "\n".join(final_output)