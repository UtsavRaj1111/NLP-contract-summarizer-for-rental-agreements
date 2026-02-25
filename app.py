import streamlit as st
import pandas as pd

from utils.text_extraction import extract_text_from_pdf
from utils.preprocessing import preprocess_text
from utils.clause_extraction import extract_clauses
from utils.summarizer import generate_summary
from utils.translator import translate_text

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ClauseCraft AI",
    page_icon="⚖️",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR ABOUT SECTION
# --------------------------------------------------
with st.sidebar:
    st.title("⚖️ ClauseCraft AI")

    st.markdown("### 📖 About")
    st.write(
        """
        ClauseCraft AI is an NLP-powered legal assistant that simplifies 
        rental agreements using AI. It generates easy-to-read summaries, 
        detects important clauses, and provides confidence-based insights.
        """
    )

    st.markdown("### ✨ Features")
    st.markdown("""
    - AI contract summarization  
    - Semantic clause detection  
    - Multilingual summaries  
    - Confidence scoring  
    - Downloadable summaries  
    """)

    st.markdown("### 🚀 How to Use")
    st.markdown("""
    1. Upload rental agreement PDF  
    2. Choose summary language  
    3. View AI summary  
    4. Explore clause dashboard  
    """)

    st.markdown("### 🛠 Tech Stack")
    st.markdown("""
    - Transformers (BART)  
    - Sentence Transformers  
    - Streamlit  
    - Python NLP Stack  
    """)

# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------
st.title("⚖️ ClauseCraft AI")
st.caption("AI-powered rental agreement intelligence")

st.divider()

# --------------------------------------------------
# FILE + LANGUAGE INPUT
# --------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Rental Agreement", type=["pdf"])

with col2:
    language = st.selectbox(
        "Summary Language",
        ["English", "Hindi", "Tamil", "Telugu", "Marathi"]
    )

st.divider()

# --------------------------------------------------
# PROCESS DOCUMENT
# --------------------------------------------------
if uploaded_file:
    with st.spinner("Analyzing agreement..."):

        raw_text = extract_text_from_pdf(uploaded_file)
        clean_text = preprocess_text(raw_text)

        summary = generate_summary(raw_text)
        clauses = extract_clauses(raw_text)

        final_summary = summary
        if language != "English":
            final_summary = translate_text(summary, language)

    st.success("Document processed successfully!")

    # ==================================================
    # SUMMARY SECTION
    # ==================================================
    st.subheader("📌 Contract Summary")
    st.success(final_summary)

    st.download_button(
        "⬇ Download Summary",
        data=final_summary,
        file_name="ClauseCraft_Summary.txt"
    )

    st.divider()

    # ==================================================
    # CLAUSE DASHBOARD
    # ==================================================
    st.subheader("📊 Clause Intelligence Dashboard")

    table_data = []

    for clause, status in clauses.items():

        # Extract confidence score
        if "(" in status:
            confidence = float(status.split("(")[-1].replace(")", ""))
        else:
            confidence = 0.0

        present = "Present" in status

        table_data.append({
            "Clause": clause,
            "Status": "✅ Present" if present else "❌ Missing",
            "Confidence": confidence
        })

    df = pd.DataFrame(table_data)

    # --------------------------------------------------
    # SORTING OPTION
    # --------------------------------------------------
    sort_option = st.selectbox(
        "Sort Clauses By",
        ["Confidence (High to Low)", "Confidence (Low to High)", "Alphabetical"]
    )

    if sort_option == "Confidence (High to Low)":
        df = df.sort_values(by="Confidence", ascending=False)
    elif sort_option == "Confidence (Low to High)":
        df = df.sort_values(by="Confidence", ascending=True)
    else:
        df = df.sort_values(by="Clause")

    # --------------------------------------------------
    # TABLE DISPLAY
    # --------------------------------------------------
    st.dataframe(df, use_container_width=True)

    # ==================================================
    # CONFIDENCE VISUALIZATION
    # ==================================================
    st.subheader("📈 Confidence Visualization")

    for _, row in df.iterrows():
        st.write(f"**{row['Clause']}**")
        st.progress(min(row["Confidence"], 1.0))

    st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption("ClauseCraft AI • Semantic NLP • Transformer-based Summarization")