import typer, json
from pathlib import Path

folder = Path("C:/Users/cprum/Desktop/Прога/Task_tracker_project/Study_Project_-Task-Tracer-")
file_path = folder / "data.json"

folder.mkdir(parents=True, exist_ok=True)

if not file_path.exists():
    file_path.write_text(json.dumps({}, ensure_ascii=False), encoding="utf-8")

app = typer.Typer()

@app.command()
def hello():
    print("Hello")

if __name__ == "__main__":
    app()