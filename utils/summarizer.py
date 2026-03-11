import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        framework="pt"  
    )

summarizer = load_model()

def generate_summary(text):
    if len(text) > 1000:
        text = text[:1000]

    summary = summarizer(
        text,
        max_length=180,
        min_length=80,
        do_sample=False
    )

    return summary[0]["summary_text"]
