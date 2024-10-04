from pathlib import Path
import subprocess
import logging
from typing import Optional

from .custom_types import PromptProject  # Adjust the import based on actual usage
from .token_optimizer import optimize_content

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(ch)

def detect_file_type(file_path: Path) -> str:
    """
    Determine the file type based on its extension.
    
    Args:
        file_path (Path): Path to the file.
        
    Returns:
        str: File extension in lowercase.
    """
    return file_path.suffix.lower()

def convert_word_to_markdown(file_path: Path, output_path: Path) -> Path:
    """
    Convert a Word document to Markdown using pandoc.
    
    Args:
        file_path (Path): Path to the .docx file.
        output_path (Path): Path to save the converted .md file.
        
    Returns:
        Path: Path to the converted Markdown file.
    """
    try:
        subprocess.run(
            ['pandoc', str(file_path), '-f', 'docx', '-t', 'markdown', '-o', str(output_path)],
            check=True
        )
        logger.debug(f"Converted DOCX to Markdown: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert DOCX to Markdown: {e}")
        raise

def convert_pdf_to_markdown(file_path: Path, output_path: Path) -> Path:
    """
    Convert a PDF to Markdown using pandoc.
    
    Args:
        file_path (Path): Path to the .pdf file.
        output_path (Path): Path to save the converted .md file.
        
    Returns:
        Path: Path to the converted Markdown file.
    """
    try:
        subprocess.run(
            ['pandoc', str(file_path), '-f', 'pdf', '-t', 'markdown', '-o', str(output_path)],
            check=True
        )
        logger.debug(f"Converted PDF to Markdown: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert PDF to Markdown: {e}")
        raise

def convert_text_to_markdown(file_path: Path, output_path: Path) -> Path:
    """
    Convert a plain text file to Markdown.
    
    Args:
        file_path (Path): Path to the .txt file.
        output_path (Path): Path to save the converted .md file.
        
    Returns:
        Path: Path to the Markdown file.
    """
    try:
        content = file_path.read_text()
        output_path.write_text(content)
        logger.debug(f"Converted TXT to Markdown: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to convert TXT to Markdown: {e}")
        raise

def convert_rst_to_markdown(file_path: Path, output_path: Path) -> Path:
    """
    Convert a reStructuredText file to Markdown using pandoc.
    
    Args:
        file_path (Path): Path to the .rst file.
        output_path (Path): Path to save the converted .md file.
        
    Returns:
        Path: Path to the converted Markdown file.
    """
    try:
        subprocess.run(
            ['pandoc', str(file_path), '-f', 'rst', '-t', 'markdown', '-o', str(output_path)],
            check=True
        )
        logger.debug(f"Converted RST to Markdown: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert RST to Markdown: {e}")
        raise

def convert_to_markdown(file_path: Path) -> Optional[Path]:
    """
    Convert a given file to Markdown based on its file type.
    
    Args:
        file_path (Path): Path to the source file.
        
    Returns:
        Optional[Path]: Path to the converted Markdown file or None if conversion fails.
    """
    file_type = detect_file_type(file_path)
    output_path = file_path.with_suffix('.md')
    
    try:
        if file_type == '.docx':
            return convert_word_to_markdown(file_path, output_path)
        elif file_type == '.pdf':
            return convert_pdf_to_markdown(file_path, output_path)
        elif file_type == '.txt':
            return convert_text_to_markdown(file_path, output_path)
        elif file_type in ['.rst', '.restructuredtext']:
            return convert_rst_to_markdown(file_path, output_path)
        else:
            logger.warning(f"Unsupported file type: {file_type}. Attempting fallback method.")
            return fallback_convert(file_path, output_path)
    except Exception as e:
        logger.error(f"Error converting {file_path}: {e}")
        return fallback_convert(file_path, output_path)

def fallback_convert(file_path: Path, output_path: Path) -> Optional[Path]:
    """
    Fallback method for converting unsupported file types.
    Writes a placeholder Markdown file indicating unsupported format.
    
    Args:
        file_path (Path): Path to the source file.
        output_path (Path): Path to save the fallback .md file.
        
    Returns:
        Optional[Path]: Path to the fallback Markdown file.
    """
    try:
        placeholder_content = (
            f"# Unsupported Format\n\n"
            f"The file type `{file_path.suffix}` is not supported for automatic conversion.\n"
            f"Please convert `{file_path.name}` manually to Markdown."
        )
        output_path.write_text(placeholder_content)
        logger.info(f"Created fallback Markdown file: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to create fallback Markdown file: {e}")
        return None
