from pydantic import BaseModel, Field
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)

class TransactionOut(BaseModel):
    amount: float
    type: str

    class Config:
        orm_mode = True
