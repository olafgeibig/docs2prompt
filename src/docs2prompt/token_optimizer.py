import re
import logging
from typing import Tuple

# Initialize logging
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

def remove_extra_whitespace(content: str) -> str:
    """
    Remove extra whitespace from the content.

    Args:
        content (str): The input text.

    Returns:
        str: The text with extra whitespace removed.
    """
    content = re.sub(r'\s+', ' ', content)
    return content.strip()

def standardize_line_breaks(content: str) -> str:
    """
    Standardize line breaks to '\n'.

    Args:
        content (str): The input text.

    Returns:
        str: The text with standardized line breaks.
    """
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    return content

def remove_redundant_headers(content: str) -> str:
    """
    Remove redundant headers from the content.

    Args:
        content (str): The input text.

    Returns:
        str: The text with redundant headers removed.
    """
    headers_seen = set()
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if re.match(r'^#+ ', line):
            header = line.strip().lower()
            if header in headers_seen:
                logger.debug(f"Removed redundant header: {header}")
                continue
            headers_seen.add(header)
        new_lines.append(line)
    return '\n'.join(new_lines)

def is_code_block(line: str, in_code_block: bool) -> Tuple[bool, bool]:
    """
    Determine if a line starts or ends a code block.

    Args:
        line (str): The current line of text.
        in_code_block (bool): Whether the current line is inside a code block.

    Returns:
        Tuple[bool, bool]: A tuple indicating if the line is a code block delimiter and the new state of being inside a code block.
    """
    if line.startswith('```'):
        return True, not in_code_block
    return False, in_code_block

def optimize_content(content: str) -> str:
    """
    Apply all optimization techniques to the content.

    Args:
        content (str): The input text.

    Returns:
        str: The optimized text.
    """
    content = remove_extra_whitespace(content)
    content = standardize_line_breaks(content)
    content = remove_redundant_headers(content)
    return content
