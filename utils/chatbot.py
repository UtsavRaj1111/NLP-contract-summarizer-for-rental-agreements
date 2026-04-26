import logging
from .model_loader import loader

logger = logging.getLogger(__name__)

def answer_question(question: str, document_text: str, summary_text: str) -> str:
    """
    Answers a question based on the document text.
    It combines the summary and original text to provide a solid context window.
    """
    try:
        if not question or not question.strip():
            return "Please provide a valid question."
        
        if not document_text and not summary_text:
            return "No document context available to answer the question."

        qa_pipeline = loader.get_qa_pipeline()
        
        # Combine summary and text. Note that transformers QA models handle limited sequence lengths,
        # so keeping the summary first makes sure high-level details are always included.
        # Alternatively, we just use the raw document text as context since we want extractive answers.
        # In practice for large documents we would split text, but for simple MVP QA pipeline:
        context = f"Summary: {summary_text}\n\nDocument Details: {document_text}"
        
        # In case the context is huge, we will let pipeline handle it, but keep a reasonable limit
        # Remove manual truncation or increase dramatically
        max_context_length = 15000 
        if len(context) > max_context_length:
            context = context[:max_context_length]
            
        # Retrieve top 5 candidates to avoid generic short answers like '1'
        results = qa_pipeline(question=question, context=context, top_k=5)
        
        if isinstance(results, dict):
            results = [results]
            
        best_answer = ""
        highest_score = 0
        
        # Iterate and find the most meaningful answer
        for res in results:
            ans_text = res.get('answer', '').strip()
            score = res.get('score', 0)
            
            # Skip single characters or single digits which are usually list indices
            if len(ans_text) <= 2 and ans_text.isdigit():
                continue
                
            if score > highest_score:
                highest_score = score
                best_answer = ans_text
                
        # Fallback if everything was filtered out
        if not best_answer and results:
            best_answer = results[0].get('answer', '')
            highest_score = results[0].get('score', 0)
        
        if highest_score < 0.01 or not best_answer:
            return "I couldn't find a highly confident answer in the document."
            
        # Capitalize the first letter for UX
        if best_answer:
            best_answer = best_answer[0].upper() + best_answer[1:]
            
        return best_answer
        
    except Exception as e:
        logger.error(f"Chatbot extracted failed: {str(e)}")
        return "Sorry, I encountered an error while trying to answer your question."
