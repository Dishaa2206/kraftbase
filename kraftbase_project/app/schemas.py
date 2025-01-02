from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum


class FieldType(str, Enum):
    string = "string"
    number = "number"
    boolean = "boolean"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FormField(BaseModel):
    field_id: str
    type: FieldType
    label: str
    required: bool

    def to_dict(self):
        return self.dict()

class FormCreate(BaseModel):
    title: str
    description: Optional[str] = None
    fields: List[FormField]

class FormSubmissionCreate(BaseModel):
    responses: List[dict]
