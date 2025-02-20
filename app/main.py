from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.core.database import lifespan

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
