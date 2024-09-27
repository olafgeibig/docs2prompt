import argparse
import json
from pathlib import Path
from pydantic import ValidationError
from .types import PromptProject

def create_project(project_name):
    output_file = f"{project_name}.json"
    # Create an empty project based on the Pydantic model
    project = PromptProject(
        name=project_name,
        max_tokens=1000,
        purpose="Describe the purpose of your project here.",
        instructions="List your instructions here.",
        documents=[]
    )
    # Serialize to JSON
    with open(output_file, "w") as f:
        json.dump(project.dict(), f, indent=4)
    print(f"New prompt project created: {output_file}")

def run_project():
    try:
        # Load the existing project
        with open("prompt_project.json", "r") as f:
            project_data = json.load(f)
        
        # Validate it against the Pydantic model
        project = PromptProject(**project_data)
        
        # Process the documents and generate the prompt (Placeholder function)
        generate_prompt(project)
        
    except (FileNotFoundError, ValidationError) as e:
        print(f"Error: {str(e)}")

def generate_prompt(project: PromptProject):
    # Here you'd implement your document conversion, token optimization, and prompt generation
    print(f"Running project: {project.name}")
    # Placeholder output for now
    with open("generated_prompt.txt", "w") as f:
        f.write(f"Generated prompt for project: {project.name}")
    print("Prompt generated: generated_prompt.txt")

def main():
    parser = argparse.ArgumentParser(description="Docs2Prompt CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create subcommand
    parser_create = subparsers.add_parser('create', help='Create a new prompt project')
    parser_create.add_argument('project_name', help='Name of the project')
    parser_create.set_defaults(func=create_project)

    # Run subcommand
    parser_run = subparsers.add_parser('run', help='Run the prompt project')
    parser_run.set_defaults(func=run_project)

    # Parse arguments
    args = parser.parse_args()
    if args.command == 'create':
        args.func(args.project_name)
    else:
        args.func()

if __name__ == "__main__":
    main()
