
from fastapi import FastAPI

from app.routers import students


app = FastAPI(
    title="Student Management System API",
    description="REST API for managing students with FastAPI and MySQL",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Welcome to Student Management System API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(students.router)