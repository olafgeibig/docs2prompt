import json
from pathlib import Path
from docs2prompt.main import create_project

def test_create_project(tmp_path):
    # Use a temporary directory for the test
    project_name = "test_project"
    test_output = tmp_path / f"{project_name}.json"

    # Change the current working directory to tmp_path
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Call the function
        create_project(project_name)
        
        # Check if the file was created
        assert test_output.exists()
        
        # Check the content of the file
        with test_output.open() as f:
            project_data = json.load(f)
        
        assert project_data["name"] == project_name
        assert project_data["max_tokens"] == 1000
        assert "Describe the purpose of your project here." in project_data["purpose"]
        assert "List your instructions here." in project_data["instructions"]
        assert project_data["documents"] == []
    finally:
        # Change back to the original working directory
        os.chdir(original_cwd)
