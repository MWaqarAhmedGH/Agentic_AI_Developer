import json
import operator
from typing import Dict, Any, List

class CalculatorAgent:
    def __init__(self):
        # Memory to store history of operations as per requirements
        self.history: List[Dict[str, Any]] = []
        
        # Define supported math operations
        self.ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow
        }

    def execute(self, action: str, a: float, b: float) -> str:
        """
        Performs the math operation and stores it in memory.
        Returns a structured JSON response.
        """
        try:
            if action not in self.ops:
                return self._error_response(f"Unsupported operation: {action}")

            # Division by zero check
            if action == "/" and b == 0:
                return self._error_response("Division by zero is not allowed.")

            # Perform calculation
            result = self.ops[action](a, b)
            
            # Record in memory
            entry = {
                "operation": action,
                "operand_a": a,
                "operand_b": b,
                "result": result
            }
            self.history.append(entry)

            return json.dumps({
                "status": "success",
                "data": entry,
                "memory_count": len(self.history)
            }, indent=2)

        except Exception as e:
            return self._error_response(str(e))

    def get_history(self) -> str:
        """Returns the full conversation memory."""
        return json.dumps({
            "status": "success",
            "history": self.history
        }, indent=2)

    def _error_response(self, message: str) -> str:
        return json.dumps({
            "status": "error",
            "message": message
        }, indent=2)

if __name__ == "__main__":
    agent = CalculatorAgent()

    # Test 1: Addition
    print("Test 1: 10 + 5")
    print(agent.execute("+", 10, 5))

    # Test 2: Subtraction
    print("\nTest 2: 20 - 7")
    print(agent.execute("-", 20, 7))

    # Test 3: Multiplication
    print("\nTest 3: 6 * 4")
    print(agent.execute("*", 6, 4))
    
    # Test 4: Power (Exponentiation)
    print("\nTest 4: 2 ^ 3")
    print(agent.execute("^", 2, 3))

    # Test 5: Division by zero
    print("\nTest 5: 10 / 0")
    print(agent.execute("/", 10, 0))

    # Test 6: Memory Retrieval
    print("\nTest 6: Retrieve History")
    print(agent.get_history())
