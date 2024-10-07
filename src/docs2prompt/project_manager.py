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

from pathlib import Path
from typing import List, Optional
from docs2prompt.document_manager import DocumentManager

class ProjectManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.document_manager = DocumentManager()

    def create_project(self, directory: str, whitelist: Optional[List[str]] = None, blacklist: Optional[List[str]] = None):
        """Create a new project with the given parameters"""
        self.file_list = self.document_manager.create_file_list(directory, whitelist, blacklist)
        # TODO: Add more project creation logic here

    def update_project(self, add_files: Optional[List[str]] = None, remove_files: Optional[List[str]] = None):
        """Update the project's file list"""
        self.file_list = self.document_manager.edit_file_list(add_files, remove_files)
        # TODO: Add more project update logic here

    def get_file_list(self) -> List[Path]:
        """Get the current file list for the project"""
        return self.file_list
