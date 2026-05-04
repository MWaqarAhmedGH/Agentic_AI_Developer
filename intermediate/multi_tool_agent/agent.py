import json
import re
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from sqlmodel import Field as SQLField, Session, SQLModel, create_engine, select

# --- Professional Database Layer (using SQLModel/SQLite) ---
class SearchRecord(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    query: str
    result_summary: str

import os

# Database setup using dynamic path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.join(BASE_DIR, "agent_database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- Tool 1: Web Search Simulator ---
class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

class WebSearchTool:
    def search(self, query: str) -> List[SearchResult]:
        """Simulates a professional web search API (like Tavily or Google)."""
        # Mocking realistic search results based on the query
        print(f"[Tool] Searching web for: '{query}'...")
        return [
            SearchResult(
                title=f"Top Result for {query}",
                url=f"https://example.com/search?q={query}",
                snippet=f"This is a detailed snippet about {query} containing relevant information."
            ),
            SearchResult(
                title=f"Latest News on {query}",
                url=f"https://news.example.com/{query}",
                snippet=f"Breaking news: New developments in the field of {query} just announced."
            )
        ]

# --- Tool 2: Database Tool ---
class DatabaseTool:
    def save_search(self, query: str, summary: str):
        """Saves search results to a real SQLite database."""
        print(f"[Tool] Saving record to database...")
        with Session(engine) as session:
            record = SearchRecord(query=query, result_summary=summary)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

# --- Tool 3: Email Service Simulator ---
class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str

class EmailTool:
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Simulates sending an email with validation."""
        print(f"[Tool] Validating email recipient: {recipient}")
        # Basic regex for email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, recipient):
            raise ValueError(f"Invalid email address: {recipient}")
            
        print(f"[Tool] Email sent successfully to {recipient}!")
        print(f"       Subject: {subject}")
        return True

# --- The Multi-Tool Agent ---
class MultiToolAgent:
    def __init__(self):
        self.search_tool = WebSearchTool()
        self.db_tool = DatabaseTool()
        self.email_tool = EmailTool()
        create_db_and_tables()

    def process_command(self, action: str, params: dict):
        """Orchestrates tools based on the requested action."""
        try:
            if action == "web_search":
                results = self.search_tool.search(params.get("query", ""))
                return {"status": "success", "results": [r.dict() for r in results]}

            elif action == "save_to_db":
                record_id = self.db_tool.save_search(
                    params.get("query", ""), 
                    params.get("summary", "")
                )
                return {"status": "success", "message": f"Saved with ID: {record_id}"}

            elif action == "send_email":
                self.email_tool.send_email(
                    params.get("recipient", ""),
                    params.get("subject", "Agent Notification"),
                    params.get("body", "")
                )
                return {"status": "success", "message": "Email sent"}

            else:
                return {"status": "error", "message": f"Unknown tool: {action}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

# --- Professional Testing Script ---
if __name__ == "__main__":
    agent = MultiToolAgent()

    print("--- [TEST 1: Web Search] ---")
    search_resp = agent.process_command("web_search", {"query": "Agentic AI"})
    print(json.dumps(search_resp, indent=2))

    print("\n--- [TEST 2: Save to DB] ---")
    db_resp = agent.process_command("save_to_db", {
        "query": "Agentic AI", 
        "summary": "Found 2 relevant articles about Agentic AI trends."
    })
    print(json.dumps(db_resp, indent=2))

    print("\n--- [TEST 3: Send Email] ---")
    email_resp = agent.process_command("send_email", {
        "recipient": "ceo@nexeagent.com",
        "body": "The search and save tasks have been completed successfully."
    })
    print(json.dumps(email_resp, indent=2))

    print("\n--- [TEST 4: Error Handling (Invalid Email)] ---")
    err_resp = agent.process_command("send_email", {
        "recipient": "invalid-email",
        "body": "This should fail."
    })
    print(json.dumps(err_resp, indent=2))
