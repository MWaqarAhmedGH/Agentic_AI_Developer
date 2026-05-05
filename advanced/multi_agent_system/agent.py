import os
import cohere
import time
from dotenv import load_dotenv

load_dotenv()

class MultiAgentSystem:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        self.co = cohere.Client(self.api_key)

    def researcher(self, topic: str):
        print(f"[Researcher]: Searching for data on {topic}...")
        prompt = f"Provide a brief research summary about: {topic}"
        response = self.co.chat(message=prompt, model="command-nightly")
        return response.text

    def writer(self, research_data: str):
        print(f"[Writer]: Drafting a professional report...")
        prompt = f"Transform this raw research into a professional 3-sentence summary: {research_data}"
        response = self.co.chat(message=prompt, model="command-nightly")
        return response.text

    def manager(self, goal: str):
        print(f"--- [ MANAGER STARTING MISSION: {goal} ] ---")
        
        # 1. Delegate to Researcher
        research = self.researcher(goal)
        print(f"[System]: Research data received.")
        
        # 2. Delegate to Writer
        final_report = self.writer(research)
        
        print("\n--- [ FINAL COLLABORATIVE DELIVERABLE ] ---")
        print(final_report)

if __name__ == "__main__":
    system = MultiAgentSystem()
    system.manager("The impact of Agentic AI on Software Engineering in 2026")
