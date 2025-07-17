from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import submission
from app.models import Base
from app.database import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route module
app.include_router(submission.router)
