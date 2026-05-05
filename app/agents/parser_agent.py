import json
from app.services.LLM.ollama_service import ollama_service
from app.services.LLM.mistral_service import mistral_service
from app.util.jsonParser import rectifier

class ParserAgent:
    def parse_resume(self, resume_text: str):
        prompt = f"""
        You are a Senior HR Specialist. Your task is to analyze the provided resume text and extract structured information about the candidate's skills, experience summary, projects, and domain signals.
        Extract structured candidate data from the resume below.

        Return only valid JSON in this format:
        {{
          "skills": [],
          "experience_summary": "",
          "projects": [],
          "domain_signals": []
        }}

        Resume:
        {resume_text}
        """

        #response = ollama_service.generate(prompt)uvi
        response = mistral_service.generate(prompt)

        try:
            print("LLM Response:", response)
            rectified=rectifier.parse_llm_json(response)
            print("rectified Response", rectified)
            return rectified
        except Exception as e:
            print(f"Failed to parse LLM response as JSON: {e}. Returning empty structured data.")
            return {
                "skills": [],
                "experience_summary": "",
                "projects": [],
                "domain_signals": []
            }


parser_agent = ParserAgent()