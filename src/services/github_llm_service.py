import os
import requests
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GitHubLLMService:
    def __init__(self):
        self.api_key = os.getenv("GITHUB_TOKEN")
        if not self.api_key:
            raise ValueError("GitHub token not found in environment variables")
        
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4.1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_api_call(self, messages: list) -> str:
        try:
            response = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=self.headers,
                json={
                    "messages": messages,
                    "temperature": 1,
                    "top_p": 1,
                    "model": self.model
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"GitHub API error: {str(e)}")
            return f"Error: GitHub API error - {str(e)}"
    
    async def generate_tailored_resume(self, resume_content: str, job_description: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a professional resume writer."
            },
            {
                "role": "user",
                "content": f"""
                Based on the following resume and job description, generate an updated resume that:
                1. Highlights relevant experience and skills
                2. Uses keywords from the job description
                3. Maintains the original format and structure
                4. Is tailored to the specific role
                
                Original Resume:
                {resume_content}
                
                Job Description:
                {job_description}
                """
            }
        ]
        return await self._make_api_call(messages)
    
    async def generate_cover_letter(self, resume_content: str, job_description: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an expert cover letter writer and hiring strategist."
            },
            {
                "role": "user",
                "content": f"""Using the resume and job description provided below, craft a highly compelling, polished, and professional cover letter for a deeply experienced candidate applying to this role.

Your goal is to:
    • Align the candidate's experience to the four most important requirements or focus areas in the job description.
    • Highlight quantified impact and comparative framing (e.g., improved vs. baseline, outperforming past methods, industry benchmarks).
    • Show strategic thinking and leadership beyond technical skills.
    • Demonstrate clear interest in the company, industry, and mission.
    • Close with a confident, engaging, and warm call to action.

The voice should be:
    • Executive-level and articulate
    • Tailored to the company and role
    • Insightful, not generic or templated
    • 100% in prose (no bullets)

⸻

Inputs
Candidate Resume:
{resume_content}

Job Description:
{job_description}

⸻

Output:
Write a tailored cover letter (1 page) addressed to the hiring team. Include candidate name and contact info at the top. Use a clear structure with an engaging opening, compelling middle focused on alignment and impact, and a strong, warm closing."""
            }
        ]
        return await self._make_api_call(messages) 