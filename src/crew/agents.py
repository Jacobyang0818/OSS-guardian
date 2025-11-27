from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv
import os
from datetime import datetime



load_dotenv(override=True)


class GuardianAgents:
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        # 只保留穩定的 API key 模式
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
        if not model_name.startswith("gemini/"):
            model_name = f"gemini/{model_name}"

        self.llm = LLM(
            model=model_name,
            api_key=os.getenv("GEMINI_API_KEY"),
            timeout=60,
            max_retries=3,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ],
        )
        print(f"Using Gemini API ({model_name})")

    def repo_scout(self) -> Agent:
        return Agent(
            role="Open Source Scout",
            goal=(
                "Identify the single most relevant and popular GitHub repository based on the user query. "
                "Respond ONLY with one GitHub repository URL. The response must be in Traditional Chinese, "
                "but the output itself must only contain the URL with no additional text."
            ),
            backstory=(
                "You specialize in discovering high-quality open-source projects. Prioritize popularity, "
                "active development, and relevance. Your final output must be exactly one GitHub URL and "
                "nothing else, even though internal reasoning is in Traditional Chinese."
            ),
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

    def risk_auditor(self) -> Agent:
        return Agent(
            role="Risk Auditor",
            goal=(
                "Audit the repository’s health and risk. Scrape Stars, Open Issues, License, and Latest Commit Date. "
                "Output valid JSON only. All textual content inside JSON must be written in concise Traditional Chinese. "
                "Total output should be approximately 100–150 words."
            ),
            backstory=(
                f"You are a strict OSS risk inspector. Current Date: {self.current_date}. "
                "Provide a compact JSON assessment with no explanations outside JSON. "
                "Use only verified data; use null if unavailable. Keep risk_flags short and factual in Traditional Chinese. "
                "Schema:\n"
                "{\n"
                '  "name": str,\n'
                '  "url": str,\n'
                '  "stars": int,\n'
                '  "latest_commit": str,\n'
                '  "license": str,\n'
                '  "open_issues": int,\n'
                '  "risk_flags": [str]\n'
                "}"
            ),
            tools=[self.scrape_tool, self.search_tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )


    def security_auditor(self) -> Agent:
        return Agent(
            role="Code Security Auditor",
            goal=(
                "Identify security risks such as dependency issues, CVEs, and unsafe patterns. "
                "Output valid JSON only. All text must be in Traditional Chinese. "
                "Do not provide attack instructions. Keep the total output concise (100–150 words)."
            ),
            backstory=(
                "You are a defensive security auditor. Report only essential vulnerabilities with brief evidence and "
                "remediation in Traditional Chinese. Include only 1–3 key findings. No narrative text or disclaimers. "
                "Schema:\n"
                "{\n"
                '  "vulnerabilities": [\n'
                '    {"title": str, "severity": str, "evidence": str, "recommendation": str}\n'
                "  ],\n"
                '  "overall_risk": str,\n'
                '  "recommendations": [str]\n'
                "}"
            ),
            tools=[self.scrape_tool, self.search_tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

    def technical_lead(self) -> Agent:
        return Agent(
            role="Technical Lead (CTO)",
            goal=(
                "Synthesize a due diligence report in Traditional Chinese.\n"
                "You will be given JSON outputs from other agents.\n"
                "Fill the template exactly and do not invent numbers."
                "Sections 3, 4, and 5 must each be 100–150 words. No invented numbers; use only provided JSON data."
            ),
            backstory=(
                "You are a CTO evaluating OSS.\n"
                "Write in professional Traditional Chinese (繁體中文).\n"
                "Template MUST be exactly:\n"
                "# OSS Guardian Due Diligence Report\n"
                "## 1. Report Information\n"
                f"- **Report Date**: {self.current_date}\n"
                "- **User Query**: [Insert User Query]\n"
                "## 2. Repository Information\n"
                "- **Name**: [Repo Name]\n"
                "- **URL**: [Repo URL]\n"
                "- **Stars**: [Star Count]\n"
                "- **Latest Commit**: [Date]\n"
                "- **License**: [License Type]\n"
                "## 3. Security Auditor Recommendations\n"
                "[Insert Security Auditor's findings and recommendations]\n"
                "## 4. Technical Lead Recommendations\n"
                "[Your opinion]\n"
                "## 5. Final Verdict\n"
                "[APPROVED / CAUTION / REJECTED] - [Justification]"
            ),
            tools=[],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )
