import streamlit as st
from transformers import pipeline

LANGUAGE_MODELS = {
    "English": None,
    "Hindi": "Helsinki-NLP/opus-mt-en-hi",
    "Tamil": "Helsinki-NLP/opus-mt-en-ta",
    "Telugu": "Helsinki-NLP/opus-mt-en-te",
    "Marathi": "Helsinki-NLP/opus-mt-en-mr",
    "Punjabi": "Helsinki-NLP/opus-mt-en-pa",
    "Gujarati": "Helsinki-NLP/opus-mt-en-gu",
    "Bengali": "Helsinki-NLP/opus-mt-en-bn",
    "Urdu": "Helsinki-NLP/opus-mt-en-ur",
    "Kannada": "Helsinki-NLP/opus-mt-en-kn"
}

@st.cache_resource
def load_translator(model_name):
    return pipeline(
        "translation",
        model=model_name,
        framework="pt"
    )

def translate_text(text, target_language):
    model_name = LANGUAGE_MODELS.get(target_language)

    # English → no translation needed
    if model_name is None:
        return text

    translator = load_translator(model_name)
    translated = translator(text)
    return translated[0]["translation_text"]
