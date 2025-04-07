from typing import List, Optional
from models import Task



class TaskStorage:
    def __init__(self, filename: str= 'task.json'):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            self._save([])

    def _load(self) -> List[Task]:
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task(**item) for item in data]
                
    
    def _save(self, tasks: List[Task]):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, ensure_ascii=False, indent=4)

    def get_all(self) -> List[Task]:
        return self._load
    
    def add(self, task: Task):
        tasks = self._load()
        if any(t.id == task.id for t in tasks):
              raise ValueError('задача с таким индификатором уже существует')
        tasks.append(task)
        self._save(tasks)
    def update(self, task_id: int, updated: Task) -> bool:
        tasks = self._load()
        for i, t in enumerate(tasks):
            if t.id == task_id:
                tasks[i] = updated
                self._save(tasks)
                return True
        return False

    def delete(self, task_id: int) -> Optional[Task]:
        tasks = self._load()
        for t in tasks:
            if t.id == task_id:
                tasks.remove(t)
                self._save(tasks)
                return t
        return None
                        
              
