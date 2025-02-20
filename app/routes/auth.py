from fastapi import APIRouter, HTTPException
import asyncpg

from app.models.auth import UserCreate, UserLogin
from app.utils.auth import get_password_hash, authenticate_user
from app.core.database import db

router = APIRouter(tags=["Authentication"], prefix='/auth')

@router.post('/signin')
async def create_user(user:UserCreate):
    hashed_password = get_password_hash(user.password)
    query = """
        INSERT INTO users (email, username, hashed_password)
        VALUES ($1, $2, $3)
    """
    try:
        await db.execute(query, user.email, user.username, hashed_password)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    return {"msg":"User Created"}

@router.post('/login')
async def login_user(user:UserLogin):
    token = await authenticate_user(user.email, user.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    return {"access_token": token, "token_type": "bearer"}

