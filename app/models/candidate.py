from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.db.mysql import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

    resume_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    status = Column(String(50), default="processing")
    resume_file = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())