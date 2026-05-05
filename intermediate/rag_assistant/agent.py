import json
import os
import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ProfessionalRAGAssistant:
    def __init__(self, knowledge_file: str):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key or self.api_key == "your_real_api_key_here":
            raise ValueError("COHERE_API_KEY missing in .env file!")
        
        self.co = cohere.Client(self.api_key)
        self.documents = self._load_documents(knowledge_file)

    def _load_documents(self, file_path: str):
        """Loads and formats documents for Cohere's RAG."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        
        with open(file_path, "r") as f:
            content = f.read()
            # Cohere expects a list of dicts for RAG
            return [{"title": "Company Profile", "snippet": content}]

    def ask(self, question: str) -> str:
        print(f"\n[Real AI Querying]: {question}")
        try:
            response = self.co.chat(
                message=question,
                documents=self.documents,
                model="command-nightly" # Reliable alias for latest features
            )
            
            return json.dumps({
                "answer": response.text,
                "citations": [c.start for c in response.citations] if hasattr(response, 'citations') else [],
                "status": "success",
                "engine": "Cohere Command-R+"
            }, indent=2)

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "knowledge.txt")
    
    try:
        assistant = ProfessionalRAGAssistant(KNOWLEDGE_PATH)
        
        # Test 1: Real RAG Answer
        print("--- [TESTING REAL COHERE RAG] ---")
        print(assistant.ask("What are the core products of Nexe-Agent?"))
        
    except Exception as e:
        print(f"Setup Error: {e}")
