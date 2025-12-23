import typer, json
from datetime import datetime
from pathlib import Path

folder = Path("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-")
file_path = folder / "tasks.json"

folder.mkdir(parents=True, exist_ok=True)

if not file_path.exists():
    file_path.write_text(json.dumps({}, ensure_ascii=False), encoding="utf-8")

app = typer.Typer()

@app.command()
def add(description: str):
    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

        task_id = str(len(tasks) + 1)

        tasks[task_id] = {
        "Task ID": task_id,
        "description": description,
        "status": "to do",   
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
        }

    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=5)
    print(f"Task {description} added successfully.")

@app.command()
def delete(task_id: str):
    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
        if task_id in tasks:
            del tasks[task_id]
            with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json","w", encoding="utf-8") as file:
                json.dump(tasks, file, ensure_ascii=False, indent=5)
                print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task {task_id} not found.")

@app.command()
def update(task_id: str, description: str):
    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
        if task_id in tasks:
            tasks[task_id]["description"] = description
            tasks[task_id]["updated_at"] = datetime.now().isoformat()
            with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json","w", encoding="utf-8") as file:
                json.dump(tasks, file, ensure_ascii=False, indent=5)
                print(f"Task {task_id} updated successfully")
        else:
            print(f"Task {task_id} not found")

@app.command()
def mark_done(task_id: str):
    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
        if task_id in tasks:
            tasks[task_id]["status"] = "done"
            tasks[task_id]["updated_at"] = datetime.now().isoformat()
            with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json","w", encoding="utf-8") as file:
                json.dump(tasks, file, ensure_ascii=False, indent=5)
                print(f"Task {task_id} marked as done successfully")
        else:
            print(f"Task {task_id} not found")


    
if __name__ == "__main__":
    app()


