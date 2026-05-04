import json
from typing import Dict, Any

def get_weather(location: str) -> str:
    """
    Mock function to simulate getting weather data.
    In a real scenario, this would call a weather API.
    """
    # Simple mock data
    weather_data = {
        "london": "15°C and Cloudy",
        "new york": "22°C and Sunny",
        "tokyo": "18°C and Rainy"
    }
    
    location_lower = location.lower()
    if location_lower in weather_data:
        return json.dumps({
            "status": "success",
            "location": location,
            "weather": weather_data[location_lower]
        })
    else:
        return json.dumps({
            "status": "error",
            "message": f"Weather data for '{location}' not found."
        })

def process_agent_request(request: Dict[str, Any]) -> str:
    """
    Simulates an AI Agent's decision-making process for tool calling.
    It takes a JSON-like request, validates it, and calls the appropriate tool.
    """
    try:
        # Step 1: Validate Action
        action = request.get("action")
        parameters = request.get("parameters", {})

        if not action:
            return json.dumps({
                "status": "error",
                "message": "Missing 'action' in request."
            })

        # Step 2: Tool Routing (Function Calling)
        if action == "get_weather":
            location = parameters.get("location")
            if not location:
                return json.dumps({
                    "status": "error",
                    "message": "Missing 'location' parameter for get_weather action."
                })
            
            # Execute the tool
            return get_weather(location)
        
        else:
            return json.dumps({
                "status": "error",
                "message": f"Unknown action: {action}"
            })

    except Exception as e:
        # Error handling as per requirements
        return json.dumps({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        })

if __name__ == "__main__":
    # Example 1: Successful Tool Call
    print("Test 1: Successful Tool Call")
    req1 = {"action": "get_weather", "parameters": {"location": "London"}}
    print(process_agent_request(req1))
    print("-" * 30)

    # Example 2: Error Handling (Missing Parameter)
    print("Test 2: Error Handling (Missing Parameter)")
    req2 = {"action": "get_weather", "parameters": {}}
    print(process_agent_request(req2))
    print("-" * 30)

    # Example 3: Error Handling (Unknown Action)
    print("Test 3: Error Handling (Unknown Action)")
    req3 = {"action": "book_flight", "parameters": {"to": "Paris"}}
    print(process_agent_request(req3))
    print("-" * 30)
