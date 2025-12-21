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
def add(description: str, status: str):
    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

        task_id = str(len(tasks) + 1)

        tasks[task_id] = {
        "Task ID": task_id,
        "description": description,
        "status": status,   
        "created_at": datetime.now().isoformat()
        }

    with open("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-/tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=5)
    print(f"Task {description} added successfully.")

@app.command()
def goodbye():
    print("Goodbye!")
    
if __name__ == "__main__":
    app()


