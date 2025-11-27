# src/crew/manager.py
from crewai import Agent, Task, Crew, Process
from typing import Any
from src.crew.agents import GuardianAgents
from src.crew.tasks import GuardianTasks

from datetime import datetime

class OSSGuardianCrew:
    def __init__(self):
        self.agents = GuardianAgents()
        self.tasks = GuardianTasks()

    def run(self, query: str) -> str:
        # 1. Instantiate Agents
        scout = self.agents.repo_scout()
        risk_auditor = self.agents.risk_auditor()
        security_auditor = self.agents.security_auditor()
        cto = self.agents.technical_lead()

        # --- Phase 1: Scout ---
        print(f"\n[Manager] Starting Phase 1: Scouting for '{query}'...")
        find_task = self.tasks.repo_scout_task(scout, query)
        
        crew_scout = Crew(
            agents=[scout],
            tasks=[find_task],
            process=Process.sequential,
            verbose=True,
            step_callback=lambda output: self._on_step_finish(output)
        )
        repo_url = str(crew_scout.kickoff()).strip()
        print(f"[Manager] Found Repo URL: {repo_url}")

        # --- Phase 2: Audit ---
        print(f"\n[Manager] Starting Phase 2: Auditing {repo_url}...")
        risk_task = self.tasks.risk_audit_task(risk_auditor, repo_url)
        security_task = self.tasks.security_audit_task(security_auditor, repo_url)
        
        crew_audit = Crew(
            agents=[risk_auditor, security_auditor],
            tasks=[risk_task, security_task],
            process=Process.sequential,
            verbose=True,
            step_callback=lambda output: self._on_step_finish(output)
        )
        crew_audit.kickoff()
        
        # Extract outputs
        risk_json = str(risk_task.output)
        sec_json = str(security_task.output)
        
        # --- Phase 3: Report ---
        print(f"\n[Manager] Starting Phase 3: Generating Report...")
        report_task = self.tasks.final_report_task(cto, query, risk_json, sec_json)
        
        crew_report = Crew(
            agents=[cto],
            tasks=[report_task],
            verbose=True,
            step_callback=lambda output: self._on_step_finish(output)
        )
        result = crew_report.kickoff()
        
        return str(result)

    def _on_step_finish(self, output: Any):
        from src.crew.callbacks import current_status
        # Try to parse agent from output if possible, or just generic update
        current_status["message"] = f"Step completed: {str(output)[:50]}..."
        # In a real implementation we would want to know WHICH agent finished.
        # For now, the agent's own verbose output goes to stdout, but capturing it for SSE is harder without custom Agent classes.
        # However, we can infer progress by which task finished.
        output_str = str(output)
        if "github.com" in output_str and "http" in output_str:
             current_status["message"] = "Scout finished finding candidates."
        elif "risk_flags" in output_str:
             current_status["message"] = "Risk Auditor finished selection."
        elif "vulnerabilities" in output_str:
             current_status["message"] = "Security Auditor finished audit."
