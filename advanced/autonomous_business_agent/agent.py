import json
import time
import os
import cohere
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load API Key
load_dotenv()

class BusinessTools:
    """Mock tools for the Autonomous Agent to use."""
    @staticmethod
    def market_search(topic: str) -> str:
        return f"Real-time market analysis for {topic}: Emerging trends show high adoption of AI agents in Q3."

    @staticmethod
    def competitor_analysis(topic: str) -> str:
        return f"Intelligence report on {topic}: Key competitors are shifting to multi-agent architectures."

    @staticmethod
    def save_report(content: str) -> str:
        return f"Business Report saved successfully. Reference ID: {int(time.time())}"

class IntelligentBusinessAgent:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY missing in .env file!")
        
        self.co = cohere.Client(self.api_key)
        self.tools = BusinessTools()
        self.execution_logs: List[str] = []

    def log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.execution_logs.append(log_entry)
        print(log_entry)

    def generate_ai_plan(self, goal: str) -> List[Dict[str, str]]:
        """
        Step 1: AI Task Planning.
        Uses Cohere to break down a goal into specific tool calls.
        """
        self.log(f"Consulting AI Brain for goal: '{goal}'")
        
        prompt = f"""
        You are a Business Strategy Manager. Break down the following goal into a sequence of tasks.
        Goal: {goal}
        
        Available Tools:
        - market_search: Gather market trends.
        - competitor_analysis: Analyze rivals.
        - save_report: Finalize findings.
        
        Return ONLY a JSON list of tasks in this format:
        [
            {{"task": "tool_name", "reason": "why this step is needed"}}
        ]
        """
        
        try:
            response = self.co.chat(message=prompt, model="command-nightly")
            # Extract JSON from response (handling potential markdown)
            json_str = response.text.strip().replace('```json', '').replace('```', '')
            plan = json.loads(json_str)
            self.log(f"AI Plan approved with {len(plan)} steps.")
            return plan
        except Exception as e:
            self.log(f"AI Planning failed: {e}. Falling back to default safety plan.")
            return [{"task": "market_search", "reason": "Initial research"}]

    def execute_goal(self, goal: str):
        """
        Main Loop: AI Reasoning & Execution.
        """
        self.log("Initializing AI-Powered Execution Engine...")
        
        # 1. PLAN with AI
        tasks = self.generate_ai_plan(goal)
        results = []

        # 2. EXECUTE with Reasoning
        for i, task_info in enumerate(tasks, 1):
            task_type = task_info["task"]
            reason = task_info["reason"]
            
            self.log(f"Step {i} ({task_type}): {reason}")
            
            # Simulated Reasoning: Routing to the correct tool
            if task_type == "market_search":
                result = self.tools.market_search(goal)
            elif task_type == "competitor_analysis":
                result = self.tools.competitor_analysis(goal)
            elif task_type == "save_report":
                summary = " | ".join(results)
                result = self.tools.save_report(summary)
            else:
                result = f"Skipping unknown task: {task_type}"
            
            self.log(f"Tool Result: {result}")
            results.append(result)
            time.sleep(1)

        self.log("Mission accomplished. Agent standing down.")
        return self.execution_logs

if __name__ == "__main__":
    try:
        agent = IntelligentBusinessAgent()
        
        # High-level Business Goal
        GOAL = "I want a complete market and competitor breakdown for Agentic AI in 2026"
        
        print("\n--- [ REAL AI AUTONOMOUS SESSION ] ---")
        logs = agent.execute_goal(GOAL)
        
    except Exception as e:
        print(f"Critical Error: {e}")
