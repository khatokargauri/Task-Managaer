from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid, json, os
app = FastAPI()
DB_FILE = "tasks.json"
class Task(BaseModel):
    id: str
    title: str
    completed: bool
    createdAt: datetime
class TaskRequest(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
def load_db():
    if not os.path.exists(DB_FILE) or os.stat(DB_FILE).st_size == 0:
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return [Task(**t) for t in json.load(f)]
        except json.JSONDecodeError:
            return []
def save_db(tasks):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([t.dict() for t in tasks], f, default=str, indent=4)
@app.get("/tasks")
def get_tasks():
    return load_db()
@app.post("/tasks")
def create_task(req: TaskRequest):
    tasks = load_db()
    new_task = Task(
        id=str(uuid.uuid4()),
        title=req.title,
        completed=False,
        createdAt=datetime.now()
    )
    tasks.append(new_task)
    save_db(tasks)
    return new_task
@app.patch("/tasks/{task_id}")
def update_task(task_id: str, req: TaskRequest):
    tasks = load_db()
    for t in tasks:
        if t.id == task_id:
            if req.completed is not None: t.completed = req.completed
            if req.title is not None: t.title = req.title
            save_db(tasks)
            return t
    raise HTTPException(status_code=404)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    tasks = [t for t in load_db() if t.id != task_id]
    save_db(tasks)
    return {"status": "ok"}
@app.get("/")
def read_index():
    return FileResponse('index.html')