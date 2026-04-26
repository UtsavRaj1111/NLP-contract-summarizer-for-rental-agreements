import os
import logging
import json
from flask import Flask, render_template, request, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO

# --- PRODUCTION CONFIGURATION ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['USE_TORCH'] = '1'
os.environ['TRANSFORMERS_NO_TENSORFLOW'] = '1'

# Configure Professional Dual-Logging (Console + File)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

# --- APP INITIALIZATION ---
app = Flask(__name__)

@app.context_processor
def inject_version():
    """Provides a random versioning token to all templates for cache busting."""
    import random
    return dict(_v=random.randint(100, 9999))
# Production Note: Use environment variable for secret_key in real deploy
app.secret_key = os.environ.get("FLASK_SECRET", os.urandom(24))
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploads")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB Safeguard
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Optimized Logic Imports
from utils.text_extraction import extract_text
from utils.classifier import classify_document
from utils.clause_extraction import extract_clauses
from utils.summarizer import generate_summary
from utils.translator import translate_text
from utils.info_extractor import extract_agreement_info
from utils.risk_detector import detect_clause_risk, get_detailed_risks
from utils.report_generator import generate_report
from utils.model_loader import loader
from utils.chatbot import answer_question

ALLOWED_EXTENSIONS = {"pdf", "docx", "jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --- SYSTEM HEALTH MONITORING ---
@app.route("/health")
def health_check():
    """Production health check for monitoring tools."""
    return jsonify({"status": "healthy", "service": "ClauseCraft AI Engine"}), 200

# --- EXPORT REPORT (High-Performance PDF Generation) ---
@app.route("/export", methods=["POST"])
def export_report():
    """Generates a premium branded PDF for the analysis results."""
    try:
        summary = request.form.get("summary", "No Summary Information Available.")
        clauses_raw = request.form.get("clauses", "[]")
        info_raw = request.form.get("info", "{}")
        risks_raw = request.form.get("risks", "[]")
        quality = request.form.get("quality", "0")

        # Decode analysis data for the generator
        clauses = json.loads(clauses_raw)
        info = json.loads(info_raw)
        risks = json.loads(risks_raw)

        pdf_buffer = generate_report(summary, clauses, info, risks, quality)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="ClauseCraft_Analysis_Report.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        logger.error(f"Export Failed: {str(e)}")
        return "Failed to generate legal report.", 500

# --- CHATBOT API ---
@app.route("/api/chat", methods=["POST"])
def chat_api():
    """Handles questions related to the document using NLP extraction."""
    try:
        data = request.get_json()
        question = data.get("question", "")
        document_text = data.get("document_text", "")
        summary_text = data.get("summary_text", "")

        answer = answer_question(question, document_text, summary_text)
        return jsonify({"answer": answer})
    except Exception as e:
        logger.error(f"Chat API Error: {str(e)}")
        return jsonify({"answer": "Sorry, an internal error occurred while processing your request."}), 500

# --- CORE ANALYSIS ENGINE ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Payload rejection: No document file attached.")
            return redirect(request.url)
        
        file = request.files["file"]
        language = request.form.get("language", "English")

        if file.filename == "":
            flash("Selection rejection: No document selected.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                logger.info(f"System Request: Analyzing document '{filename}'...")
                
                # 1. Pipeline: Extraction -> Classification -> Extraction
                raw_text = extract_text(filepath, filename)
                if not raw_text.strip():
                    return "Zero-Text Context: Document is either encrypted or purely graphic without OCR data.", 400

                doc_type, conf = classify_document(raw_text)
                info = extract_agreement_info(raw_text, doc_type)
                summary = generate_summary(raw_text, info)
                clauses = extract_clauses(raw_text, doc_type)
                risks = detect_clause_risk(clauses, doc_type)
                detailed_risks = get_detailed_risks(raw_text)

                # 2. Multilingual Processor
                final_summary = summary
                if language != "English":
                    final_summary = translate_text(summary, language)

                # 3. Intelligence Metrics
                original_words = len(raw_text.split())
                summary_words = len(final_summary.split())
                compression = round((1 - summary_words/original_words) * 100, 1) if original_words > 0 else 0
                
                total = len(clauses)
                present = sum("Present" in v for v in clauses.values())
                quality_score = round((present / total) * 100, 1) if total > 0 else 0

                # 4. Result Formatting (Unified UI State)
                table_data = []
                for clause, status in clauses.items():
                    conf_score = 0
                    if "(" in status and ")" in status:
                        try: conf_score = float(status.split("(")[1].split(")")[0])
                        except: pass
                    
                    state = "Present" if "Present" in status else "Missing"
                    table_data.append({
                        "Clause": clause,
                        "Status": state,
                        "Risk": risks.get(clause, "Informational"),
                        "Confidence": conf_score
                    })

                # 5. Dashboard Hand-off
                return render_template(
                    "result.html",
                    summary=final_summary,
                    clauses=table_data,
                    info=info,
                    compression=compression,
                    quality=quality_score,
                    doc_type=doc_type,
                    confidence=conf,
                    detailed_risks=detailed_risks,
                    # Serialization for export engine
                    json_info=json.dumps(info),
                    json_risks=json.dumps(detailed_risks),
                    json_clauses=json.dumps(table_data),
                    raw_text=raw_text
                )

            except Exception as e:
                logger.error(f"Pipeline Integrity Crash: {str(e)}")
                return f"Internal Intelligence Failure: {str(e)}", 500
            finally:
                if os.path.exists(filepath):
                    try: os.remove(filepath)
                    except: pass
        else:
            flash("Protocol error: Unsupported file extension.")
            return redirect(request.url)

    return render_template("index.html")

# --- SERVER STARTUP ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)