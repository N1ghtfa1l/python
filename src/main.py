from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from src.routers.user import router as user_router
from src.routers.token import router as user_auth
from src.routers.post import router as user_post
from src.routers.posts import router as get_posts
from src.controllers.websocket import router as wb_rout
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:5173/",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(
    router=user_router,
    prefix='/user'
)
app.include_router(
    router=user_auth,
    prefix='/auth'
)
app.include_router(
    router=user_post,
    prefix='/create'
)
app.include_router(
    router=get_posts,
    prefix='/user'
)
app.include_router(
    router=wb_rout,
    prefix='/chat'
)
