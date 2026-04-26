from sentence_transformers import SentenceTransformer
from transformers import pipeline
import torch
import logging

# Configure basic logging for model loading diagnostics
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Singleton for shared model management to save RAM and improve speed.
    Optimized for production and CPU-only environments.
    """
    _instance = None
    _sentence_transformer = None
    _summarizer = None
    _qa_pipeline = None
    _translator_cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def get_sentence_transformer(self):
        """Loads semantic model once and caches it."""
        if self._sentence_transformer is None:
            try:
                logger.info("Initializing SentenceTransformer (all-MiniLM-L6-v2)...")
                # Using small model (80MB) for production speed/efficiency
                self._sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.error(f"Failed to load SentenceTransformer: {e}")
                raise RuntimeError("AI Intelligence Layer failed to initialize.")
        return self._sentence_transformer

    def get_summarizer(self):
        """Loads summarization pipeline once and caches it."""
        if self._summarizer is None:
            try:
                logger.info("Initializing Summarization Pipeline (sshleifer/distilbart-cnn-12-6)...")
                # This distilled model is 800MB (half of BART-Large) and 3x faster on CPU.
                self._summarizer = pipeline(
                    "summarization",
                    model="sshleifer/distilbart-cnn-12-6",
                    device=-1 
                )
            except Exception as e:
                logger.error(f"Failed to load Summarizer: {e}")
                raise RuntimeError("AI Summarization Engine failed to initialize.")
        return self._summarizer

    def get_qa_pipeline(self):
        """Loads question answering pipeline once and caches it."""
        if self._qa_pipeline is None:
            try:
                logger.info("Initializing QA Pipeline (deepset/minilm-uncased-squad2)...")
                # Fast, lightweight model for CPU QA tasks
                self._qa_pipeline = pipeline(
                    "question-answering",
                    model="deepset/minilm-uncased-squad2",
                    device=-1
                )
            except Exception as e:
                logger.error(f"Failed to load QA Pipeline: {e}")
                raise RuntimeError("AI Chatbot Engine failed to initialize.")
        return self._qa_pipeline

    def get_translator(self, model_name):
        """Unified translation management."""
        if model_name not in self._translator_cache:
            try:
                logger.info(f"Initializing Translator Model: {model_name}...")
                self._translator_cache[model_name] = pipeline(
                    "translation",
                    model=model_name,
                    framework="pt",
                    device=-1
                )
            except Exception as e:
                logger.error(f"Failed to load Translator ({model_name}): {e}")
                return None
        return self._translator_cache[model_name]

# Global Singleton
loader = ModelLoader()
