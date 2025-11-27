from crewai.tasks.task_output import TaskOutput
from typing import Any, Dict

# Global state to store the current status
# In a production app with multiple users, this should be a Redis/Database keyed by request ID.
# For this demo, a simple global dict works for single-user testing.
current_status = {
    "step": "idle",
    "message": "Waiting to start..."
}

class StepCallback:
    def __init__(self):
        pass

    def on_step_start(self, task: Any, **kwargs):
        """Called when a task starts"""
        # CrewAI's callback structure can be tricky. 
        # We'll try to infer the agent from the task description or agent role if available.
        agent_role = getattr(task.agent, 'role', 'Unknown Agent')
        current_status["step"] = "working"
        current_status["message"] = f"{agent_role} is working..."
        print(f"DEBUG: Step Start - {current_status['message']}")

    def on_step_end(self, output: TaskOutput, **kwargs):
        """Called when a task ends"""
        current_status["step"] = "completed"
        current_status["message"] = f"Task completed: {output.summary}"
        print(f"DEBUG: Step End - {output.summary}")
