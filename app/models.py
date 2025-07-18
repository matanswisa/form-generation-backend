from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSONB, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
