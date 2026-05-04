import json
import os
from agent import RAGAssistant

def run_comprehensive_rag_check():
    # Path to the knowledge file
    KNOWLEDGE_PATH = "knowledge.txt"
    
    print("--- [ PHASE 2: COMPREHENSIVE RAG ASSISTANT CHECK ] ---")
    
    # 1. VERIFY DOCUMENT UPLOAD/LOAD
    print(f"Step 1: Verifying Document 'Upload' (Loading {KNOWLEDGE_PATH})...")
    if not os.path.exists(KNOWLEDGE_PATH):
        print(f"   [ERROR]: Knowledge file missing!")
        return
        
    assistant = RAGAssistant(KNOWLEDGE_PATH)
    num_chunks = len(assistant.store.chunks)
    print(f"   [RESULT]: Document successfully processed into {num_chunks} chunks.")

    # 2. VERIFY VECTOR STORE (RETRIEVAL LOGIC)
    print("\nStep 2: Testing Vector Store (Semantic Retrieval)...")
    query = "NexusCore orchestration"
    retrieved = assistant.store.retrieve(query)
    
    if retrieved:
        print(f"   [RESULT]: Retrieved {len(retrieved)} relevant chunks for query '{query}'.")
        print(f"   [PREVIEW]: {retrieved[0][:60]}...")
    else:
        print(f"   [ERROR]: Retrieval failed for a valid query.")

    # 3. VERIFY CONTEXTUAL ANSWERS
    print("\nStep 3: Validating Contextual Answer Generation...")
    questions = [
        "What is NexusCore?",
        "How can I contact the company?",
        "Tell me about the weather in London." # Negative test (out of context)
    ]

    for q in questions:
        response_json = assistant.ask(q)
        response = json.loads(response_json)
        
        print(f"\n   [Question]: {q}")
        if response.get("status") == "success":
            print(f"   [Answer]: {response['answer']}")
            print(f"   [Context Used]: True")
        else:
            print(f"   [Answer]: {response['answer']}")
            print(f"   [Context Used]: False")

    print("\n--- [ FINAL RAG VERIFICATION COMPLETE ] ---")

if __name__ == "__main__":
    # Ensure we are in the correct directory to find knowledge.txt
    run_comprehensive_rag_check()
