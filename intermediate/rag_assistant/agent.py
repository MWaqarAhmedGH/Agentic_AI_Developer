import json
import os
import re
from typing import List, Dict

class DocumentStore:
    """Simulates a Vector Database with high-precision word matching."""
    def __init__(self):
        self.chunks: List[str] = []

    def load_document(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document {file_path} not found.")
        
        with open(file_path, "r") as f:
            content = f.read()
            # Split by double newlines for logical paragraphs
            self.chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        
        print(f"[RAG] Successfully loaded {len(self.chunks)} knowledge chunks.")

    def retrieve(self, query: str, top_k: int = 1) -> List[str]:
        """
        Uses Set Intersection for precision. 
        Ensures 'me' doesn't match 'Development'.
        """
        # Clean and tokenize query into a set of unique words
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        
        # Filter out common stop words to focus on meaning
        STOP_WORDS = {"is", "the", "what", "are", "where", "about", "in", "to", "of", "and", "me", "tell"}
        meaningful_query_words = query_words - STOP_WORDS
        
        if not meaningful_query_words:
            return []

        scored_chunks = []
        for chunk in self.chunks:
            # Tokenize chunk into a set of unique words
            chunk_words = set(re.findall(r'\b\w+\b', chunk.lower()))
            
            # Count common words between query and chunk
            matches = meaningful_query_words.intersection(chunk_words)
            score = len(matches)
            
            if score >= 1:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:top_k]]

class RAGAssistant:
    def __init__(self, knowledge_file: str):
        self.store = DocumentStore()
        self.store.load_document(knowledge_file)
        # TEACHER NOTE: This is where you would initialize a real LLM client
        self.api_key = os.getenv("AI_API_KEY", "MOCK_MODE")

    def ask(self, question: str) -> str:
        print(f"\n[User Question]: {question}")
        
        # 1. Retrieval
        context_chunks = self.store.retrieve(question)
        
        if not context_chunks:
            return json.dumps({
                "answer": "I'm sorry, I couldn't find any information about that in my knowledge base.",
                "context_used": False,
                "mode": "API_READY_" + self.api_key
            }, indent=2)

        # 2. Contextual Answer
        context_text = " ".join(context_chunks)
        return json.dumps({
            "answer": f"STRICT CONTEXT ANSWER: {context_text[:150]}...",
            "status": "success",
            "context_used": True,
            "mode": "API_READY_" + self.api_key
        }, indent=2)

if __name__ == "__main__":
    KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "knowledge.txt")
    assistant = RAGAssistant(KNOWLEDGE_PATH)

    # TEST: Hallucination Prevention (Weather in London)
    # This should now return "I couldn't find any information"
    print("--- [VERIFYING HALLUCINATION PREVENTION] ---")
    print(assistant.ask("Tell me about the weather in London."))
    
    # TEST: Accurate Retrieval (Location)
    print("\n--- [VERIFYING ACCURATE RETRIEVAL] ---")
    print(assistant.ask("Where is the Nexe-Agent office?"))
