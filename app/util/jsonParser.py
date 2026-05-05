import json
import re

class rectifier:
    def __init__(self):
        pass

    def parse_llm_json(self, raw: str):
        try:
            # Remove markdown code fences like ```json ... ```
            cleaned = re.sub(r"^```json\s*", "", raw.strip(), flags=re.IGNORECASE)
            cleaned = re.sub(r"^```\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned).strip()

            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            return None

rectifier = rectifier()