from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from uuid import uuid4
from .auth import get_current_user  

router = APIRouter()

@router.post("/{form_id}")
def submit_form(
    form_id: int, 
    submission: schemas.FormSubmissionCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)  
):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    if form.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to submit to this form")

    new_submission = models.FormSubmission(
        form_id=form_id, 
        data=submission.responses
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission


@router.get("/{form_id}")
def get_form_submissions(
    form_id: int, 
    page: int = 1, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) 
):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    if form.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view submissions for this form")

    # Fetch submissions with pagination
    submissions = db.query(models.FormSubmission).filter(models.FormSubmission.form_id == form_id).offset((page - 1) * limit).limit(limit).all()
    total_count = db.query(models.FormSubmission).filter(models.FormSubmission.form_id == form_id).count()
    
    return {
        "total_count": total_count,
        "page": page,
        "limit": limit,
        "submissions": submissions
    }
