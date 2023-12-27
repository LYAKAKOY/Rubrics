from fastapi import APIRouter
from fastapi import FastAPI

from api.rubrics.handlers import rubrics_router

app = FastAPI(description="Rubrics")
main_api_router = APIRouter()
main_api_router.include_router(rubrics_router, prefix="/rubrics", tags=["rubrics"])
app.include_router(main_api_router)
