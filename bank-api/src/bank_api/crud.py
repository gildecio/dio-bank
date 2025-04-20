from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
import bank_api.models, bank_api.schemas as schemas

async def deposit(transaction: schemas.TransactionCreate, user_id: int, db: AsyncSession):
    new_tx = models.Transaction(amount=transaction.amount, type="deposit", user_id=user_id)
    db.add(new_tx)
    await db.commit()
    return {"msg": "Depósito realizado com sucesso"}

async def withdraw(transaction: schemas.TransactionCreate, user_id: int, db: AsyncSession):
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id))
    transactions = result.scalars().all()
    saldo = sum(t.amount if t.type == "deposit" else -t.amount for t in transactions)

    if transaction.amount > saldo:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    new_tx = models.Transaction(amount=transaction.amount, type="withdraw", user_id=user_id)
    db.add(new_tx)
    await db.commit()
    return {"msg": "Saque realizado com sucesso"}

async def get_statement(user_id: int, db: AsyncSession):
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id))
    transactions = result.scalars().all()
    return transactions
