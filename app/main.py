from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.main import api_router
from app.core.db import init_db
from app.api.utils.users_auth_utils import get_user_auth


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Lifespan start")
    try:
       init_db()
       yield
    except Exception as e:
       print(f"error {e}")
       print("Lifespan Ends")

# Initialize the fastapi instance to create a server
app = FastAPI(
    title= settings.TITLE,
    description= settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=life_span
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"status": True, "Message": "Api is running"}


app.include_router(api_router)