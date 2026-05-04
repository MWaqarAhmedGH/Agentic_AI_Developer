import json
import time
from typing import List, Dict

# --- COMMUNICATION LAYER ---
class CommunicationHub:
    """Handles messages and task delegation between agents."""
    def __init__(self):
        self.logs: List[str] = []

    def broadcast(self, sender: str, receiver: str, message: str):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [COMM] {sender} -> {receiver}: {message}"
        self.logs.append(log_entry)
        print(log_entry)

# --- SPECIALIZED AGENTS ---
class ResearchAgent:
    def __init__(self, hub: CommunicationHub):
        self.hub = hub
        self.name = "Researcher-01"

    def perform_research(self, topic: str) -> str:
        self.hub.broadcast(self.name, "Manager", "Starting research phase...")
        time.sleep(1)
        data = f"In-depth research on {topic}: AI Agents are projected to handle 40% of customer service by 2027."
        self.hub.broadcast(self.name, "Manager", "Research completed. Sending data.")
        return data

class WritingAgent:
    def __init__(self, hub: CommunicationHub):
        self.hub = hub
        self.name = "Writer-01"

    def compose_report(self, raw_data: str) -> str:
        self.hub.broadcast(self.name, "Manager", "Formatting raw data into a professional report...")
        time.sleep(1)
        report = f"*** PROFESSIONAL REPORT ***\nDATA: {raw_data}\nVERDICT: High Strategic Value.\n*** END ***"
        self.hub.broadcast(self.name, "Manager", "Report composed successfully.")
        return report

# --- ORCHESTRATOR / MANAGER ---
class ManagerAgent:
    def __init__(self):
        self.hub = CommunicationHub()
        self.researcher = ResearchAgent(self.hub)
        self.writer = WritingAgent(self.hub)
        self.name = "Manager-Agent"

    def delegate_goal(self, goal: str):
        print(f"\n--- [ {self.name} SESSION START ] ---")
        self.hub.broadcast(self.name, "Researcher-01", f"Task: Research {goal}")
        
        # 1. Delegate to Researcher
        research_data = self.researcher.perform_research(goal)
        
        # 2. Delegate to Writer
        self.hub.broadcast(self.name, "Writer-01", "Task: Compose report from research data.")
        final_report = self.writer.compose_report(research_data)
        
        print("\n--- [ FINAL DELIVERABLE ] ---")
        print(final_report)
        print("\n--- [ FULL COMMUNICATION LOGS ] ---")
        for log in self.hub.logs:
            print(log)

if __name__ == "__main__":
    manager = ManagerAgent()
    
    # Complex multi-agent goal
    MISSION = "The future of Agentic AI in Enterprise"
    manager.delegate_goal(MISSION)
