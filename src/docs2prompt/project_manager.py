import json
from pathlib import Path
from docs2prompt.custom_types import PromptProject

def create_project(name: str, max_tokens: int = 100000):
    project = PromptProject(
        name=name,
        max_tokens=max_tokens,
        role="AI Assistant",
        purpose="",
        instructions="",
        documents=[]
    )
    output_file = Path(f"{name}.json")
    with open(output_file, "w") as f:
        json.dump(project.dict(), f, indent=4)
    print(f"New prompt project created: {output_file}")

def run_project(project_name):
    project_file = Path(f"{project_name}.json")
    if not project_file.exists():
        print(f"Project file not found: {project_file}")
        return
    with open(project_file, "r") as f:
        project_data = json.load(f)
    project = PromptProject(**project_data)
    # generate_prompt(project)

