from fastapi import FastAPI, HTTPException
from typing import List
from simple_backend.src.task_tracker.models import TaskStorage, Task

app = FastAPI()
storage = TaskStorage("tasks.json")




@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.get_all

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    try:
        storage.add(task)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    if storage.update(task_id, updated_task):
        return updated_task
    raise HTTPException(status_code=404, detail="задача не найдена")    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = storage.delete(task_id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="задача не найдена")    



