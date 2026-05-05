from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate
from app.agents.parser_agent import parser_agent
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service


class CandidateService:
    def create_candidate(self, payload: CandidateCreate, db: Session):
        parsed_data = parser_agent.parse_resume(payload.resume_text or "")

        candidate = Candidate(
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
            resume_text=payload.resume_text,
            parsed_data=parsed_data
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        embedding_text = " ".join([
            payload.resume_text or "",
            " ".join(parsed_data.get("skills", [])),
            parsed_data.get("experience_summary", "")
        ])
        vector = embedding_service.encode(embedding_text)
        qdrant_service.upsert_candidate_embedding(
            candidate_id=candidate.id,
            vector=vector,
            payload={
                "candidate_id": candidate.id,
                "full_name": candidate.full_name,
                "skills": parsed_data.get("skills", [])
            }
        )

        return candidate


candidate_service = CandidateService()