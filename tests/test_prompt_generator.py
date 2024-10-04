import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
import pytest
from docs2prompt.prompt_generator import PromptGenerator
from docs2prompt.custom_types import PromptProject

@pytest.fixture
def sample_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a temporary document
        doc_path = Path(tmpdir) / "test_doc.txt"
        with open(doc_path, "w") as f:
            f.write("This is a test document.")

        # Create a PromptProject instance
        project = PromptProject(
            name="Test Project",
            max_tokens=1000,
            role="Test Assistant",
            purpose="Testing",
            instructions="1. Test instruction\n2. Another test instruction",
            documents=[str(doc_path)]
        )
        yield project

def test_generate_prompt(sample_project):
    generator = PromptGenerator()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_output.xml"
        generator.generate_prompt(sample_project, str(output_file))

        # Check if the output file exists
        assert output_file.exists()

        # Parse the XML and check its structure
        tree = ET.parse(output_file)
        root = tree.getroot()

        assert root.tag == "prompt"
        assert root.find("role").text == "Test Assistant"
        assert root.find("purpose").text == "Testing"
        
        instructions = root.find("instructions").text
        assert "1. Test instruction" in instructions
        assert "2. Another test instruction" in instructions

        documents = root.find("documents")
        assert len(documents) == 1
        
        document = documents.find("document")
        assert document.get("index") == "1"
        assert document.find("source").text == "test_doc.txt"
        assert document.find("document_content").text == "This is a test document."

def test_generate_prompt_missing_document(sample_project):
    generator = PromptGenerator()
    
    # Add a non-existent document to the project
    sample_project.documents.append("/path/to/non_existent_doc.txt")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_output.xml"
        generator.generate_prompt(sample_project, str(output_file))

        # Parse the XML and check its structure
        tree = ET.parse(output_file)
        root = tree.getroot()

        documents = root.find("documents")
        assert len(documents) == 1  # Only the existing document should be included
