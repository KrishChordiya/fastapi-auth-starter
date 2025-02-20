from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

from app.core.database import db
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):

    query = "SELECT id,hashed_password FROM users WHERE email = $1"
    user_record = await db.fetchrow(query, email)
    if not user_record: return False

    if not pwd_context.verify(password, user_record[-1]): return False

    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "id":str(user_record[0]),
        "exp":expire
    }

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


