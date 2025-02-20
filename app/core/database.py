import asyncpg
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config import settings
# from pgvector.asyncpg import register_vector

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=5,
            max_size=20,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            # init=self._init_connection
        )

    # async def _init_connection(self, conn):
    #     await register_vector(conn)

    async def disconnect(self):
        await self.pool.close()

    @asynccontextmanager
    async def connection(self):
        async with self.pool.acquire() as conn:
            yield conn

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

db = Database()

async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()