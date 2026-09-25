import os

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI(title="DevOps Task API")

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
MONGO_USERNAME = os.getenv("DB_USERNAME")
MONGO_PASSWORD = os.getenv("DB_PASSWORD")

MONGO_URI = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"
    "@mongodb:27017"
    "/?authSource=admin"
)

client = MongoClient(MONGO_URI)

db = client["devops_tasks"]
tasks_collection = db["tasks"]


@app.get("/")
def root():
    return {
        "message": "DevOps Task API is running"
    }


@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }


@app.get("/tasks")
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    return tasks
@app.post("/tasks")
def create_task(task: Task):
    tasks_collection.insert_one(task.model_dump())
    return task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    result = tasks_collection.update_one(
        {"id": task_id},
        {"$set": task.model_dump()}
    )

    if result.matched_count == 0:
        return {"error": "Task not found"}

    return task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    result = tasks_collection.delete_one({"id": task_id})

    if result.deleted_count == 0:
        return {"error": "Task not found"}

    return {
        "message": "Task deleted",
        "id": task_id
    }
