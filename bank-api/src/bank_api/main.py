from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from bank_api.database import engine, Base, get_db
import bank_api.models, bank_api.crud as crud, bank_api.auth as auth
import bank_api.schemas as schemas

app = FastAPI(title="API Bancária Assíncrona")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/signup")
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth.create_user(user, db)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await auth.login_user(form_data, db)

@app.post("/deposit")
async def deposit(transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return await crud.deposit(transaction, current_user.id, db)

@app.post("/withdraw")
async def withdraw(transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return await crud.withdraw(transaction, current_user.id, db)

@app.get("/statement")
async def statement(db: AsyncSession = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return await crud.get_statement(current_user.id, db)
