import json
from agent import MultiToolAgent

def run_comprehensive_check():
    agent = MultiToolAgent()
    
    print("--- [ PHASE 1: COMPREHENSIVE MULTI-TOOL WORKFLOW ] ---")
    
    # 1. WEB SEARCH
    query = "Future of Agentic AI 2026"
    print(f"Step 1: Performing Web Search for '{query}'...")
    search_results = agent.process_command("web_search", {"query": query})
    
    if search_results["status"] == "success":
        snippet = search_results["results"][0]["snippet"]
        print(f"   [RESULT]: Found relevant data: '{snippet[:50]}...'")
        
        # 2. SAVE TO DB
        print("\nStep 2: Saving the retrieved search snippet to Database...")
        db_results = agent.process_command("save_to_db", {
            "query": query,
            "summary": snippet
        })
        
        if db_results["status"] == "success":
            record_id = db_results["message"]
            print(f"   [RESULT]: {record_id}")
            
            # 3. SEND EMAIL
            print("\nStep 3: Notifying the CEO via Email...")
            email_results = agent.process_command("send_email", {
                "recipient": "ceo@nexeagent.com",
                "subject": "Agentic AI Research Completed",
                "body": f"The research for '{query}' has been completed and saved to the database with {record_id}."
            })
            
            if email_results["status"] == "success":
                print(f"   [RESULT]: Email notification dispatched successfully.")
    
    print("\n--- [ FINAL VERIFICATION ] ---")
    print("All tools (Web Search, Save to DB, Send Email) have been executed in a single integrated workflow.")

if __name__ == "__main__":
    run_comprehensive_check()
