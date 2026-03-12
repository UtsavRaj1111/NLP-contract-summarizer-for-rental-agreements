import streamlit as st
import pandas as pd
import altair as alt

from utils.text_extraction import extract_text
from utils.clause_extraction import extract_clauses
from utils.summarizer import generate_summary
from utils.translator import translate_text
from utils.info_extractor import extract_agreement_info
from utils.risk_detector import detect_clause_risk
from utils.report_generator import generate_report

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ClauseCraft AI",
    page_icon="⚖️",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("⚖️ ClauseCraft AI")

    st.markdown("### About")
    st.write(
        """
        ClauseCraft AI is an NLP-powered legal assistant that analyzes
        rental agreements. It summarizes contracts, detects clauses,
        identifies risks, and extracts key information automatically.
        """
    )

    st.markdown("### Features")
    st.markdown("""
    - Contract summarization
    - Clause detection
    - Clause evidence highlighting
    - Risk detection
    - Agreement information extraction
    - Smart clause suggestions
    - Clause confidence visualization
    """)

    st.markdown("### Supported Files")
    st.markdown("""
    - PDF
    - DOCX
    - JPG / PNG
    """)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("⚖️ ClauseCraft AI")
st.caption("AI-powered Rental Agreement Analyzer")

st.divider()

# --------------------------------------------------
# FILE INPUT
# --------------------------------------------------
col1, col2 = st.columns([2,1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload Rental Agreement",
        type=["pdf","docx","jpg","png"]
    )

with col2:
    language = st.selectbox(
        "Summary Language",
        ["English","Hindi","Tamil","Telugu","Marathi"]
    )

st.divider()

# --------------------------------------------------
# PROCESS DOCUMENT
# --------------------------------------------------
if uploaded_file:

    with st.spinner("Analyzing document..."):

        raw_text = extract_text(uploaded_file, uploaded_file.name)

        summary = generate_summary(raw_text)

        clauses = extract_clauses(raw_text)

        info = extract_agreement_info(raw_text)

        risks = detect_clause_risk(clauses)

        

        final_summary = summary
        if language != "English":
            final_summary = translate_text(summary, language)

    st.success("Document processed successfully!")

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------
    st.subheader("📌 Contract Summary")
    st.success(final_summary)

    st.download_button(
        "⬇ Download Summary",
        data=final_summary,
        file_name="ClauseCraft_Summary.txt"
    )

# --------------------------------------------------
# SUMMARY COMPRESSION SCORE
# --------------------------------------------------
if uploaded_file:

    raw_text = extract_text(uploaded_file, uploaded_file.name)

    original_words = len(raw_text.split())
    summary_words = len(final_summary.split())

    if original_words > 0:
        compression_ratio = round((1 - summary_words/original_words) * 100,2)
    else:
        compression_ratio = 0

    st.metric("Summary Compression", f"{compression_ratio}%")

# --------------------------------------------------
# AGREEMENT INFORMATION
# --------------------------------------------------
    st.subheader("📄 Extracted Agreement Information")

    if info:
        info_df = pd.DataFrame(info.items(), columns=["Field","Value"])
        st.table(info_df)
    

# --------------------------------------------------
# CLAUSE DASHBOARD
# --------------------------------------------------
    st.subheader("📊 Clause Intelligence Dashboard")

    table_data = []

    for clause, status in clauses.items():

        if "(" in status:
            confidence = float(status.split("(")[1].replace(")",""))
        else:
            confidence = 0

        state = "Present" if "Present" in status else "Missing"

        table_data.append({
            "Clause": clause,
            "Status": state,
            "Risk": risks.get(clause,"Unknown"),
            "Confidence": confidence
        })

    df = pd.DataFrame(table_data)

    st.dataframe(df, use_container_width=True)




# --------------------------------------------------
# AGREEMENT QUALITY SCORE
# --------------------------------------------------
    total = len(clauses)
    present = sum("Present" in v for v in clauses.values())

    quality_score = round((present/total)*100,2)

    st.metric("Agreement Quality Score", f"{quality_score}/100")

# --------------------------------------------------
# CLAUSE CONFIDENCE GRAPH
# --------------------------------------------------
    st.subheader("📈 Clause Confidence Visualization")

    chart_df = df.copy()

    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("Clause:N", sort='-y', title="Clause Type"),
        y=alt.Y("Confidence:Q", scale=alt.Scale(domain=[0,1]), title="Confidence Score"),
        color=alt.Color(
            "Status:N",
            scale=alt.Scale(
                domain=["Present","Missing"],
                range=["green","red"]
            ),
            legend=alt.Legend(title="Clause Status")
        ),
        tooltip=["Clause","Status","Confidence"]
    ).properties(
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

# --------------------------------------------------
# EXPORT REPORT
# --------------------------------------------------
if uploaded_file:

    st.subheader("📄 Download Full AI Report")

    report_file = generate_report(
        final_summary,
        clauses,
        info,
        risks,
        quality_score
    )

    st.download_button(
        label="Download ClauseCraft AI Report",
        data=report_file,
        file_name="ClauseCraft_Report.pdf",
        mime="application/pdf"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption("ClauseCraft AI • NLP Legal Intelligence System")