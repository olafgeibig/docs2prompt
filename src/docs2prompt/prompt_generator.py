import os
import xml.etree.ElementTree as ET
import logging
from .custom_types import PromptProject

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a class for generating prompt XML files
class PromptGenerator:
    def generate_prompt(self, prompt_project: PromptProject, output_file: str):
        # Create the root element of the XML
        root = ET.Element("prompt")

        # Add role element to the XML
        role = ET.SubElement(root, "role")
        role.text = prompt_project.role

        # Add purpose element to the XML
        purpose = ET.SubElement(root, "purpose")
        purpose.text = prompt_project.purpose

        # Add instructions element to the XML
        instructions = ET.SubElement(root, "instructions")
        # Split the instructions into individual lines and format them as a numbered list
        instructions_list = prompt_project.instructions.split('\n')
        instructions.text = "\n".join([f"{i+1}. {inst}" for i, inst in enumerate(instructions_list)])

        # Add documents element to the XML
        documents = ET.SubElement(root, "documents")
        for index, document_path in enumerate(prompt_project.documents, start=1):
            # Check if the document file exists, if not, log a warning and skip it
            if not os.path.exists(document_path):
                logger.warning(f"Document '{document_path}' does not exist and will be skipped.")
                continue

            # Create a document element with an index attribute
            document_element = ET.SubElement(documents, "document", index=str(index))
            # Add the source element containing the filename of the document
            source = ET.SubElement(document_element, "source")
            source.text = os.path.basename(document_path)

            # Add the document content element containing the file's content
            document_content = ET.SubElement(document_element, "document_content")
            with open(document_path, "r") as file:
                content = file.read()
                document_content.text = content

        # Write the XML to the specified output file
        tree = ET.ElementTree(root)
        with open(output_file, "wb") as xml_file:
            tree.write(xml_file, encoding="utf-8", xml_declaration=True)

        # Log that the XML file was successfully written
        logger.info(f"Prompt XML successfully written to {output_file}")