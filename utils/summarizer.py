from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_summary(text):

    if not text or len(text.strip()) == 0:
        return "No text found in document."

    # Limit text size for model
    text = text[:3000]

    try:
        summary = summarizer(
            text,
            max_length=150,
            min_length=40,
            do_sample=False
        )

        return summary[0]["summary_text"]

    except Exception:
        return "Unable to generate summary for this document."