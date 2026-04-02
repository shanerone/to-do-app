from contextlib import asynccontextmanager

from db.database import create_tables, delete_tables
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import router as auth_router
from routers.tasks import router as task_router
from routers.categories import router as category_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    print("DB ready")
    yield
    print("Off")


app = FastAPI(title="To-Do App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(category_router)

