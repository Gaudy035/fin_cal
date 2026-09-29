from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, stats, categories, transactions, recurring
from scheduler.recurring import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app:FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(stats.router)
app.include_router(transactions.router)
app.include_router(recurring.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)