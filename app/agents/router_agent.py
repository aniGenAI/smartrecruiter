import json
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service
from app.services.LLM.ollama_service import ollama_service
from app.services.LLM.mistral_service import mistral_service
from app.util.jsonParser import rectifier

class RouterAgent:
    def build_evaluator(self, parsed_data: dict):
        routing_text = " ".join([
            " ".join(parsed_data.get("skills", [])),
            parsed_data.get("experience_summary", ""),
            " ".join(parsed_data.get("domain_signals", []))
        ])

        vector = embedding_service.encode(routing_text)

        # Step 1: Search similar evaluator from memory
        similar_evaluators = qdrant_service.search_evaluator_memory(vector)

        # Step 2: Reuse evaluator if similarity is strong
        if similar_evaluators and similar_evaluators[0].score >= 0.85:
            return similar_evaluators[0].payload["evaluator"]

        # Step 3: Generate new evaluator only if no strong match exists
        prompt = f"""
        You are a skill routing system. you synthesize an evaluator profile based on the candidate's skills, experience, and domain signals. The evaluator profile will guide the evaluation agent on how to assess the candidate effectively.

        Candidate profile:
        {parsed_data}

        Generate a dynamic evaluator profile in valid JSON.

        Return only JSON:
        {{
          "designation": "",
          "evaluation_focus": [],
          "reasoning_strategy": "",
          "scoring_criteria": []
        }}
        """
     
        response = mistral_service.generate(prompt)
        rectified_response = rectifier.parse_llm_json(response)

        try:
            evaluator = rectified_response
        except Exception:
            evaluator = {
                "designation": "Generic evaluator",
                "evaluation_focus": [],
                "reasoning_strategy": "",
                "scoring_criteria": []
            }

        # Step 4: Store newly synthesized evaluator for reuse
        qdrant_service.store_evaluator_memory(
            vector=vector,
            payload={
                "skills": parsed_data.get("skills", []),
                "evaluator": evaluator
            }
        )

        return evaluator


router_agent = RouterAgent()