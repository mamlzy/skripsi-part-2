from fastapi import APIRouter

from app.api import routes_dataset, routes_health, routes_model, routes_piutang, routes_referensi


api_router = APIRouter()
api_router.include_router(routes_health.router, tags=["Kesehatan Sistem"])
api_router.include_router(routes_referensi.router, prefix="/referensi", tags=["Referensi"])
api_router.include_router(routes_piutang.router, prefix="/piutang", tags=["Data Piutang"])
api_router.include_router(routes_dataset.router, prefix="/dataset", tags=["Dataset"])
api_router.include_router(routes_model.router, prefix="/model", tags=["Model Naive Bayes"])
