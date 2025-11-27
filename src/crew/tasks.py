from crewai import Task


class GuardianTasks:
    def repo_scout_task(self, agent, user_query: str) -> Task:
        return Task(
            description=(
                "User query:\n"
                f"{user_query}\n\n"
                "Find ONE best GitHub repo URL. Output only the URL."
            ),
            expected_output="A single GitHub repository URL.",
            agent=agent,
        )

    def risk_audit_task(self, agent, repo_url: str) -> Task:
        return Task(
            description=(
                f"Repository URL: {repo_url}\n\n"
                "1) Scrape the repository page to extract: Stars, License, Open Issues.\n"
                "2) IMPORTANT: Also verify the latest commit date by scraping "
                "'https://github.com/{owner}/{repo}/commits/{default_branch}' "
                "(construct this URL based on the repo info). Compare this with the API result.\n"
                "3) Produce JSON per schema with risk_flags."
            ),
            expected_output="Valid JSON per schema.",
            agent=agent,
        )

    def security_audit_task(self, agent, repo_url: str) -> Task:
        return Task(
            description=(
                f"Repository URL: {repo_url}\n\n"
                "Audit for security issues and CVEs. "
                "Return JSON per schema. Defense only."
            ),
            expected_output="Valid JSON per schema.",
            agent=agent,
        )

    def final_report_task(self, agent, user_query: str, risk_json: str, sec_json: str) -> Task:
        return Task(
            description=(
                "You are given:\n\n"
                f"User Query:\n{user_query}\n\n"
                f"Risk Auditor JSON:\n{risk_json}\n\n"
                f"Security Auditor JSON:\n{sec_json}\n\n"
                "Write final report in Traditional Chinese using the exact template."
            ),
            expected_output="Final report in Traditional Chinese.",
            agent=agent,
        )
