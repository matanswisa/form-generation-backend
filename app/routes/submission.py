from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
from database import get_db
from models import Submission
from sqlalchemy import func, cast, Float
router = APIRouter()

@router.post("/submit")
def submit_form(payload: Dict[str, Any], db: Session = Depends(get_db)):
    data = payload.get("data")
    print(data)
    print("Payload",payload)


    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Data must be an object")
    print("#"*40)
    print(type(data))
    print(data)
    print("#"*40)
    print(data['form_type'])
    if 'form_type' not in data or not data['form_type']: 
        raise HTTPException(status_code=400, detail="form_type is required")

    submission = Submission(form_type=data['form_type'], data=data)

    #In case the same submission exists
    existing = db.query(Submission).filter(
        Submission.form_type == data['form_type'],
        Submission.data.op('@>')(data),
        Submission.data.op('<@')(data)
    ).first()

    
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate submission detected")
    
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {"message": "Form saved successfully", "id": submission.id}


@router.get("/submissions")
def get_submissions(db: Session = Depends(get_db)):
    submissions = db.query(Submission).all()
    result = []
    
    if not len(submissions):
        return result
    
    for s in submissions:
        if isinstance(s.data, str):
            try:
                parsed_data = json.loads(s.data)
            except json.JSONDecodeError:
                parsed_data = s.data 
        else:
            parsed_data = s.data

        result.append({
            "id": s.id,
            "data": parsed_data,
            "form_type":s.form_type,
            "submitted_at": s.submitted_at,
        })

    return result

@router.get("/analytics")
def get_submissions_anayltics(db: Session = Depends(get_db)):
    num_of_males = db.query(Submission).filter(func.lower(Submission.data["gender"].astext) == "male").count()
    num_of_females = db.query(Submission).filter(func.lower(Submission.data["gender"].astext) == "female").count()
    total_submissions = db.query(Submission).count()

    avg_age = db.query(
        func.avg(
            cast(Submission.data["age"].astext, Float)
        )
    ).scalar()


    return {
        "total_submissions": total_submissions,
        "submissions_made_by_males": num_of_males,
        "submissions_made_by_females":num_of_females,
        "avg_age":avg_age
    }
