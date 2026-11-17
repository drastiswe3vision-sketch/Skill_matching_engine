from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth import router as auth_router
from backend.routes.employee import router as employee_router
from backend.routes.task import router as task_router
from backend.routes.workload_api import router as workload_router
from backend.routes.recommendation import router as recommendation_router

# Create FastAPI app FIRST
app = FastAPI()

# CORS Configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://skill-matching-engine-wheat.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register Routers
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(task_router)
app.include_router(workload_router)
app.include_router(recommendation_router)
