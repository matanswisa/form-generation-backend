from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Store the submitted form data as a JSON string
    data = Column(String, nullable=False)

    # Optional: if you want to also store the schema
    # schema = Column(String, nullable=True)

    submitted_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "data": json.loads(self.data),
            "submitted_at": self.submitted_at.isoformat()
        }
