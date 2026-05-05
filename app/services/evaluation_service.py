from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job import Job
from app.models.evaluation import Evaluation

from app.agents.router_agent import router_agent
from app.agents.evaluator_agent import evaluator_agent


class EvaluationService:
    def evaluate_candidate(self, candidate_id: int, job_id: int, db: Session):
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        job = db.query(Job).filter(Job.id == job_id).first()

        if not candidate or not job:
            return None

        evaluator = router_agent.build_evaluator(candidate.parsed_data or {})

        result = evaluator_agent.evaluate(
            candidate_data=candidate.parsed_data or {},
            evaluator=evaluator,
            job_description=job.description
        )

        evaluation = Evaluation(
            candidate_id=candidate.id,
            job_id=job.id,
            fit_score=result.get("fit_score"),
            confidence_score=result.get("confidence_score"),
            recommendation=result.get("recommendation"),
            evaluation_data={
                "evaluator": evaluator,
                "reasoning": result.get("reasoning", [])
            }
        )

        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)

        return evaluation


evaluation_service = EvaluationService()