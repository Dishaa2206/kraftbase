from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from .auth import get_current_user 
from uuid import uuid4

router = APIRouter()

@router.post("/create")
def create_form(form: schemas.FormCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    form_fields = [field.to_dict() for field in form.fields]

    new_form = models.Form(
        title=form.title,
        description=form.description,
        fields=form_fields,
        created_by=current_user.id
    )
    db.add(new_form)
    db.commit()
    db.refresh(new_form)
    return new_form

@router.delete("/delete/{form_id}")
def delete_form(form_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    if form.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this form")

    db.delete(form)
    db.commit()
    return {"message": "Form deleted successfully"}

@router.get("/")
def get_all_forms(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Form).filter(models.Form.created_by == current_user.id).all()

@router.get("/{form_id}")
def get_single_form(form_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")
  
    if form.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this form")

    return form
