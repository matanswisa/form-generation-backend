from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    form_type = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
