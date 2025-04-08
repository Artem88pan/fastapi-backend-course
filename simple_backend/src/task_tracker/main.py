import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import FastAPI, HTTPException
from typing import List
from task_tracker.models import Task
from task_tracker.llm_client import CloudflareLLMClient
from task_tracker.task_storage import RemoteTaskStorage

app = FastAPI()
storage = RemoteTaskStorage(bin_id='67f39cb88a456b796683ff72', api_key='$2a$10$R6hU9ZDFC2IgNH8K7IPQxexqGRz7.v1vo8A7nJcAq7MIoXbQstHXu')
llm = CloudflareLLMClient(
    "https://task-helper-ai.panov89119018073.workers.dev"
)




@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return await storage.get_all

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    try:
        solution = await llm.get_solution(task.name)
        task.name += f"\n\n Решение от ИИ: \n{solution}"
        await storage.add(task)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated: Task):
    result = await storage.update(task_id, updated)
    if result:
        return result
    raise HTTPException(status_code=404, detail="задача не найдена")    

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    result = await storage.delete(task_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="задача не найдена")    


