## ⚖️ ClauseCraft AI
NLP Contract Summarizer for Rental Agreements

ClauseCraft AI is an NLP-powered legal assistant designed to automatically analyze rental agreements.
It extracts key information, summarizes contracts, detects clauses, identifies potential legal risks, and provides suggestions for safer agreements.

This project helps tenants, landlords, and legal professionals quickly understand complex rental contracts.

 ## Features
 
📄 Contract Text Extraction

● Extracts text from uploaded PDF rental agreements
● Handles structured and semi-structured documents

🧠 Automatic Contract Summarization

● Uses NLP techniques to generate a concise summary
● Highlights important sections of the agreement

📑 Clause Detection

● Automatically identifies key clauses such as:
● Rent payment terms
● Security deposit conditions
● Termination clauses
● Maintenance responsibilities
● Penalties and obligations

⚠️ Risk Detection

● Detects potentially risky or unfair clauses, including:
● One-sided termination rights
● Excessive penalties
● Ambiguous obligations

📊 Key Information Extraction

● Extracts structured information including:
● Tenant name
● Landlord name
● Rent amount
● Lease duration
● Security deposit
● Property address

🌍 Translation Support

● Supports translation of contract summaries for better accessibility.

📑 Report Generation

● Generates a structured analysis report of the agreement.

📊 Visualization Dashboard

● Displays insights using Altair charts inside the Streamlit interface.

## Project Architecture
NLP Contract Summarizer for Rental Agreements
│
├── app.py
│
├── utils
│   ├── text_extraction.py
│   ├── preprocessing.py
│   ├── clause_extraction.py
│   ├── summarizer.py
│   ├── info_extractor.py
│   ├── risk_detector.py
│   ├── suggestions.py
│   ├── translator.py
│   └── report_generator.py
│
├── sample_docs
│   └── RENTAL AGREEMENT.pdf
│
├── requirements.txt
├── runtime.txt
├── packages.txt
└── .gitignore

## Tech Stack

Frontend:
● Streamlit

NLP & Data Processing:
● Python
● NLTK / SpaCy (or similar NLP tools)
● Regex
● Transformers 

Visualization:
● Altair
● Pandas

Document Processing:
● PDF text extraction libraries

## Installation
Clone the repository:
git clone https://github.com/yourusername/clausecraft-ai.git
cd clausecraft-ai

## Create virtual environment:
python -m venv venv

## Activate environment:
Mac/Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

## Install dependencies:
pip install -r requirements.txt

## Running the Application
Start the Streamlit server:
streamlit run app.py

The application will open at:
http://localhost:8501

## Example Workflow

1️⃣ Upload a rental agreement PDF
2️⃣ The system extracts the text
3️⃣ NLP modules process the contract

The system then provides:
● Contract summary
● Extracted clauses
● Risk analysis
● Suggestions
● Structured report

## Example Output
The application produces:
📄 Contract Summary
⚠️ Risky Clauses
📑 Clause Breakdown
📊 Visual Analytics
📑 Downloadable Report

## Core Modules
● text_extraction.py
Extracts raw text from uploaded documents.

● preprocessing.py
Cleans and prepares text for NLP processing.

● clause_extraction.py
Detects legal clauses using rule-based and NLP methods.

● summarizer.py
Generates contract summaries.

● info_extractor.py
Extracts key structured details from agreements.

● risk_detector.py
Identifies risky clauses using heuristic rules.

● suggestions.py
Suggests safer clause alternatives.

● translator.py
Provides multilingual support.

● report_generator.py
Creates a structured legal analysis report.

## Limitations

● Not a substitute for professional legal advice
● Accuracy depends on contract formatting
● May miss complex legal nuances

## Future Improvements

● AI-based clause classification using transformers
● Multi-language contract analysis
● OCR support for scanned PDFs
● Legal compliance checks by region
● Automatic contract comparison
● Downloadable PDF legal reports

## Contributing
Contributions are welcome!

● Steps:
Fork the repository

● Create a feature branch
git checkout -b feature/new-feature

● Commit changes
git commit -m "Add new feature"

● Push to GitHub and create a PR




