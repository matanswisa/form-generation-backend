from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json

from database import get_db
from models import Submission

router = APIRouter()

@router.post("/submit")
def submit_form(payload: Dict[str, Any], db: Session = Depends(get_db)):
    data = payload.get("data")

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Data must be an object")


    submission = Submission(data=data)
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {"message": "Form saved successfully", "id": submission.id}


@router.get("/submissions")
def get_submissions(db: Session = Depends(get_db)):
    submissions = db.query(Submission).all()
    result = []

    for s in submissions:
        # Make sure 'data' is a Python dict, not stringified
        if isinstance(s.data, str):
            try:
                parsed_data = json.loads(s.data)
            except json.JSONDecodeError:
                parsed_data = s.data  # fallback
        else:
            parsed_data = s.data

        result.append({
            "id": s.id,
            "data": parsed_data,
            "submitted_at": s.submitted_at,
        })

    return result
