import json
from pathlib import Path
from .custom_types import PromptProject
from .document_processor import convert_to_markdown
from .token_optimizer import optimize_content  # Ensure this module exists

def create_project(name, max_tokens, directory, purpose, instructions, documents):
    output_file = Path(directory) / f"{name}.json"
    project = PromptProject(
        name=name,
        max_tokens=max_tokens,
        role="AI Assistant",  # Adjust as needed
        purpose=purpose,
        instructions=instructions,
        documents=list(documents)
    )
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
    generate_prompt(project)

def generate_prompt(project: PromptProject):
    print(f"Running project: {project.name}")
    accumulated_content = ""

    # Process each document
    for doc_path_str in project.documents:
        doc_path = Path(doc_path_str)
        if doc_path.exists():
            markdown_path = convert_to_markdown(doc_path)
            if markdown_path:
                content = markdown_path.read_text()
                optimized_content = optimize_content(content)
                accumulated_content += optimized_content + "\n"
        else:
            print(f"Document not found: {doc_path}")

    # Construct the prompt
    prompt_content = (
        f"<role>{project.role}</role>\n"
        f"<purpose>{project.purpose}</purpose>\n"
        f"<instructions>{project.instructions}</instructions>\n"
        f"<content>{accumulated_content}</content>"
    )

    # Save the prompt to a file
    prompt_file = Path(f"{project.name}_prompt.txt")
    with open(prompt_file, "w") as f:
        f.write(prompt_content)
    print(f"Prompt generated: {prompt_file}")