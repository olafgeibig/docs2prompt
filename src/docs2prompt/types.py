from pydantic import BaseModel, Field
from typing import List

class PromptProject(BaseModel):
    name: str = Field(..., title="Project Name", description="The name of the prompt project.")
    max_tokens: int = Field(..., title="Maximum Tokens", description="The maximum number of tokens allowed for the generated prompt.")
    purpose: str = Field(..., title="Prompt Purpose", description="The purpose of the prompt being generated.")
    instructions: str = Field(..., title="Prompt Instructions", description="Specific instructions or guidelines for the prompt generation.")
    documents: List[str] = Field(..., title="Document File Paths", description="List of file paths to the documents that will be included in the prompt.")