from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Submission
from app.schemas import SubmissionCreate
from datetime import datetime

router = APIRouter()

@router.post("/submit")
def submit_form(payload: SubmissionCreate, db: Session = Depends(get_db)):
    new_submission = Submission(data=payload.data, submitted_at=datetime.utcnow())
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Submission saved successfully"}

@router.get("/submissions")
def get_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).order_by(Submission.submitted_at.desc()).all()
