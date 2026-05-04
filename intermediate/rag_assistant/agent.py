import json
import os
from typing import List, Dict

class DocumentStore:
    """Simulates a Vector Database by storing and retrieving text chunks."""
    def __init__(self):
        self.chunks: List[str] = []

    def load_document(self, file_path: str):
        """Reads a file and splits it into smaller chunks for granular retrieval."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document {file_path} not found.")
        
        with open(file_path, "r") as f:
            content = f.read()
            # Professional splitting logic: split by double newlines (paragraphs)
            self.chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        
        print(f"[RAG] Successfully loaded {len(self.chunks)} knowledge chunks from {file_path}.")

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        """
        Simulates Vector Search/Semantic Retrieval.
        Uses a refined scoring system to ensure relevance.
        """
        # Common stop words to ignore to increase precision
        STOP_WORDS = {"is", "the", "what", "are", "where", "about", "in", "to", "of", "and"}
        query_words = [w.lower() for w in query.split() if w.lower() not in STOP_WORDS]
        
        if not query_words:
            return []

        scored_chunks = []
        for chunk in self.chunks:
            chunk_lower = chunk.lower()
            # Score based on meaningful keywords
            score = sum(1 for word in query_words if word in chunk_lower)
            
            # Professional Threshold: Must match at least one significant keyword
            if score >= 1:
                # Boost score if multiple keywords match
                scored_chunks.append((score, chunk))

        # Sort by relevance score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:top_k]]

class RAGAssistant:
    def __init__(self, knowledge_file: str):
        self.store = DocumentStore()
        self.store.load_document(knowledge_file)

    def ask(self, question: str) -> str:
        """The RAG process: Retrieve relevant context -> Generate Answer."""
        print(f"\n[User Question]: {question}")
        
        # 1. Retrieval Phase
        context_chunks = self.store.retrieve(question)
        
        if not context_chunks:
            return json.dumps({
                "answer": "I'm sorry, I couldn't find any information about that in my knowledge base.",
                "context_used": False
            }, indent=2)

        # 2. Generation Phase (Simulated)
        # In a real app, this context would be sent to an LLM like GPT-4.
        context_text = " ".join(context_chunks)
        
        # Professional "Contextual Answer" generation
        # Here we simulate the LLM's ability to extract specific info from the retrieved context.
        return json.dumps({
            "answer": f"Based on the company profile: {context_text[:150]}...",
            "full_retrieved_context": context_chunks,
            "status": "success"
        }, indent=2)

if __name__ == "__main__":
    # Path to the knowledge file created in the previous step
    KNOWLEDGE_PATH = "intermediate/rag_assistant/knowledge.txt"
    
    # Initialize the Assistant
    assistant = RAGAssistant(KNOWLEDGE_PATH)

    # Test 1: Specific Retrieval (Products)
    print("--- [TEST 1: Querying Products] ---")
    print(assistant.ask("What are the core products of Nexe-Agent?"))

    # Test 2: Specific Retrieval (Location)
    print("\n--- [TEST 2: Querying Location] ---")
    print(assistant.ask("Where is the office located?"))

    # Test 3: Out of Context Query
    print("\n--- [TEST 3: Irrelevant Question] ---")
    print(assistant.ask("What is the weather in Paris?"))
