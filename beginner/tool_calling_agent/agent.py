import json
import os
import cohere
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ToolCallingAgent:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY missing in .env file!")
        self.co = cohere.Client(self.api_key)

    def get_weather(self, location: str) -> str:
        """Mock tool for getting weather."""
        weather_data = {"london": "15°C", "new york": "22°C", "tokyo": "18°C"}
        return weather_data.get(location.lower(), "Weather data not available")

    def run(self, user_input: str):
        print(f"\n[User]: {user_input}")
        
        # Define the tools for Cohere
        tools = [
            {
                "name": "get_weather",
                "description": "Gets the current weather for a location",
                "parameter_definitions": {
                    "location": {
                        "description": "The city to get weather for",
                        "type": "string",
                        "required": True
                    }
                }
            }
        ]

        # Use Cohere to decide if a tool should be called
        response = self.co.chat(
            message=user_input,
            tools=tools,
            model="command-nightly"
        )

        # Check if the model wants to call a tool
        if response.tool_calls:
            for call in response.tool_calls:
                if call.name == "get_weather":
                    location = call.parameters["location"]
                    result = self.get_weather(location)
                    print(f"[Agent]: Calling get_weather for {location}...")
                    
                    # Final response from agent using the tool result
                    final_response = self.co.chat(
                        message=user_input,
                        tool_results=[{"call": call, "outputs": [{"weather": result}]}],
                        model="command-nightly"
                    )
                    return final_response.text
        else:
            return response.text

if __name__ == "__main__":
    try:
        agent = ToolCallingAgent()
        print("--- [ REAL AI TOOL CALLING ] ---")
        print(f"Agent Response: {agent.run('What is the weather in London?')}")
    except Exception as e:
        print(f"Error: {e}")
