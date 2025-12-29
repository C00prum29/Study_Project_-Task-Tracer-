import typer, json
from datetime import datetime
from pathlib import Path

folder = Path("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-")
file_path = folder / "tasks.json"

folder.mkdir(parents=True, exist_ok=True)

if not file_path.exists():
    file_path.write_text(json.dumps({}, ensure_ascii=False), encoding="utf-8")

app = typer.Typer()

def load_tasks():
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def check_task_exists(task_id, tasks):
    if task_id not in tasks:
        print(f"Task {task_id} not found")
        return False
    return True

def save_tasks(tasks):
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=5)

def date():
    return datetime.now().isoformat()

def print_task(task):
    print(f"Task ID: {task['Task ID']}")
    print(f'Description: {task['description']}')
    print(f'Status: {task['status']}')
    print(f'created at: {task['created_at']}')
    print(f'updated at: {task['updated_at']}')
    print("")

@app.command()
def add(description: str):
    tasks = load_tasks()
    
    task_id = str(len(tasks) + 1)

    tasks[task_id] = {
        "Task ID": task_id,
        "description": description,
        "status": "to do",   
        "created_at": date(),
        "updated_at": date()
        }

    save_tasks(tasks)
    print(f"Task {description} added successfully.")



@app.command()
def delete(task_id: str):
    tasks = load_tasks()

    if not check_task_exists(task_id, tasks):
        return

    del tasks[task_id]

    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.") 



@app.command()
def update(task_id: str, description: str):
    tasks = load_tasks()

    if not check_task_exists(task_id, tasks):
        return

    tasks[task_id]["description"] = description
    tasks[task_id]["updated_at"] = date()

    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.") 



@app.command()
def mark_status(task_id: str, status: str):
    tasks = load_tasks()

    if not check_task_exists(task_id, tasks):
        return
    
    tasks[task_id]['status'] = status
    tasks[task_id]['updated_at'] = date()

    save_tasks(tasks)
    print(f'Task {task_id} marked as done successfully')



@app.command()
def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print('No tasks found.')
        return
    
    for task in tasks.values():
        print_task(task)



@app.command()
def list_by_status(status: str):
    tasks = load_tasks()
    filtered = [task for task in tasks.values() if task['status'] == status]

    if not filtered:
        print(f'No tasks with status {status} found')
    
    for task in filtered:
        print_task(task)



if __name__ == "__main__":
    app()