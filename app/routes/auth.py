from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenRequest
from app.services.auth import authenticate_user, create_access_token, get_password_hash
from app.core.database import db
from app.core.config import settings
import asyncpg

router = APIRouter(tags=["Authentication"])

@router.post("/auth/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    query = """
        INSERT INTO users (email, username, hashed_password)
        VALUES ($1, $2, $3)
        RETURNING id, email, username, is_active
    """
    try:
        user_record = await db.fetchrow(
            query, user.email, user.username, hashed_password
        )
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    return user_record

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    token_data: TokenRequest  # Changed from OAuth2PasswordRequestForm
):
    user = await authenticate_user(token_data.email, token_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}