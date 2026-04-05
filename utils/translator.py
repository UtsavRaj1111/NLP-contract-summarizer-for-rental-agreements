from .model_loader import loader
import logging

logger = logging.getLogger(__name__)

# Supported language models
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

def translate_text(text, target_language):
    """
    Translates English analysis into the target language.
    Optimized for memory by using the shared ModelLoader singleton.
    """
    model_name = LANGUAGE_MODELS.get(target_language)

    # No translation needed for English or unsupported languages
    if model_name is None:
        return text

    # Use the shared singleton loader
    translator = loader.get_translator(model_name)
    
    if translator is None:
        logger.warning(f"Translation engine for {target_language} unavailable. Falling back to English.")
        return text

    # Handle text in chunks to prevent model context window overflow
    chunk_size = 450
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    try:
        translated_chunks = []
        for chunk in chunks:
            result = translator(chunk)
            translated_chunks.append(result[0]["translation_text"])
        
        return " ".join(translated_chunks)
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return text