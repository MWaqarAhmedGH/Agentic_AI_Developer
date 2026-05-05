import json
import re
import os
import cohere
from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field as SQLField, Session, SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

# --- Database Layer ---
class SearchRecord(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    query: str
    result_summary: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.join(BASE_DIR, "agent_database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- Tools ---
class Tools:
    @staticmethod
    def web_search(query: str) -> str:
        return f"Results for '{query}': AI agents are becoming mainstream in 2026."

    @staticmethod
    def save_to_db(query: str, summary: str) -> str:
        with Session(engine) as session:
            record = SearchRecord(query=query, result_summary=summary)
            session.add(record)
            session.commit()
            session.refresh(record)
            return f"Record saved with ID: {record.id}"

    @staticmethod
    def send_email(recipient: str, body: str) -> str:
        if "@" not in recipient:
            return "Error: Invalid email address."
        return f"Email sent successfully to {recipient}."

# --- AI Orchestrator ---
class IntelligentMultiToolAgent:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        self.co = cohere.Client(self.api_key)
        create_db_and_tables()

    def handle_request(self, user_input: str):
        print(f"\n[User Request]: {user_input}")
        
        tools_spec = [
            {"name": "web_search", "description": "Search the web", "parameter_definitions": {"query": {"type": "string"}}},
            {"name": "save_to_db", "description": "Save data to database", "parameter_definitions": {"query": {"type": "string"}, "summary": {"type": "string"}}},
            {"name": "send_email", "description": "Send an email", "parameter_definitions": {"recipient": {"type": "string"}, "body": {"type": "string"}}}
        ]

        response = self.co.chat(message=user_input, tools=tools_spec, model="command-nightly")

        if response.tool_calls:
            results = []
            for call in response.tool_calls:
                print(f"[Agent]: Executing tool '{call.name}'...")
                if call.name == "web_search":
                    res = Tools.web_search(call.parameters["query"])
                elif call.name == "save_to_db":
                    res = Tools.save_to_db(call.parameters["query"], call.parameters["summary"])
                elif call.name == "send_email":
                    res = Tools.send_email(call.parameters["recipient"], call.parameters["body"])
                results.append({"call": call, "outputs": [{"result": res}]})
            
            final = self.co.chat(message=user_input, tool_results=results, model="command-nightly")
            return final.text
        return response.text

if __name__ == "__main__":
    agent = IntelligentMultiToolAgent()
    print("--- [ REAL AI MULTI-TOOL ORCHESTRATION ] ---")
    print(agent.handle_request("Search for AI trends and save them to my database."))
