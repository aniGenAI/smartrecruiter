import json
from app.services.LLM.ollama_service import ollama_service
from app.services.LLM.mistral_service import mistral_service
from app.util.jsonParser import rectifier

class EvaluatorAgent:
    def evaluate(self, candidate_data: dict, evaluator: dict, job_description: str):
        prompt = f"""
        You are acting as: {evaluator.get("designation", "Technical Evaluator")}

        Evaluate this candidate against the job description.

        Candidate:
        {candidate_data}

        Job Description:
        {job_description}

        Evaluation Focus:
        {evaluator.get("evaluation_focus", [])}

        Reasoning Strategy:
        {evaluator.get("reasoning_strategy", "")}

        Scoring Criteria:
        {evaluator.get("scoring_criteria", [])}

        Return only valid JSON:
        {{
          "fit_score": 0,
          "confidence_score": 0,
          "recommendation": "",
          "reasoning": []
        }}
        """

        response = mistral_service.generate(prompt)
        rectified_response = rectifier.parse_llm_json(response)

        try:
            return rectified_response
        except Exception:
            return {
                "fit_score": 0,
                "confidence_score": 0,
                "recommendation": "undetermined",
                "reasoning": []
            }


evaluator_agent = EvaluatorAgent()