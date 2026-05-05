from sqlalchemy import Column, Integer, Float, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.mysql import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    fit_score = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    recommendation = Column(String(50), nullable=True)

    evaluation_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())