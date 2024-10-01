
# Project Plan: Docs2Prompt

## Project Overview
Docs2Prompt aims to convert documents into a token efficient format that is easily understood by AI models for addding context to complex prompts. The tools allows to define prompt projets to create a complex prompt that matches the needs of the user's projects that uses an AI as a project assistant. Usually language models have a knowledge cutoff date, so they usually do not have the knowledge of the latest updates. This tool allows to create a prompt enriched with documentation that is easy to understand by AI models.

## Core Concepts
- **Crawling and Extraction**: Retrieve documentation from online sources or local directories.
- **Document Conversion**: Transform the extracted documentation into a standard format that is well understood by AI models, probably Markdown.
- **Compression** Reduce the size of the converted documents to be token effcient without a loss of information. This might lead to a format that is not readable by humans.
- **Prompt Generation** Generate contents for a prompt that is easy to understand by AI models.
- **Prompt Projects**: Define and store project definitions for generating a prompt that specify which documentation from the pool are included in a prompt.

## Requirements
- Python. The tool will be developed in Python.
- AI Usage. Some tasks of the tool will require access to AI models but it should be used cost effciently
- LLM abstraction. Enables users to choose from a variety of models and provides a unified programming model for AI models.
- API based. Enables usage in different application types: commandline tool, web service, desktop app. API is python first but with an HTTP API in mind
- 

## Features

### MVP
The initial version will focus on:
- Manual import of documentation into a source directory.
- A simple command-line interface for user interaction.
  - create project: outputs an empty project file the user must edit
  - run project: executes the project and outputs the prompt
  - token count: counts the tokens of the prompt
- Creation of basic prompt projects with a project file to define the project name, source subdirectories, and an output file.
- Conversion of documentation to Markdown format
- Token optimization through basic compression, removing unnecessary content withoiut information loss, and ensuring source code integrity.
- Generate a prompt in the claude long context format

### Future Expansions:
- Implement a web crawler to automatically extract online documentation.
- Git integration to fetch and update documentation from repositories.
- An AI agent to find the location of the documentation in a git repository.
- Conversion of images with diagrams into a text based markup format that can easily be understood bt LLMs, like PlantUML or mermaid
- Advanced token optimization techniques, including natural language processing (NLP) and automated summarization.
- Interactive selection of documentation sections through a configuration file or GUI. Support multiple sets of such selections per prompt project
- pyproject.toml integration for a prompt project. Ability to import dependencies from pyproject.toml files or update the prompt project accroding to the depenccy updates
- Allow different versions of the same documentation, so it can be used by different prompt projects that use a different version of the same documentation.
- Filter the content by criterias in natual language so the an LLM can perform the filtering.

## Prompt Format
Taken from the [Long context propting tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips) by Anthropic
```xml
<role>
  {{LLM role}}
</role>
<purpose>
  {{prompt purpose description}}
</purpose>
<instructions>
  {{prompt instructions as a numbered list}}
<instructions>
<documents>
  <document index="1">
    <source>annual_report_2023.pdf</source>
    <document_content>
      {{ANNUAL_REPORT}}
    </document_content>
  </document>
  <document index="2">
    <source>competitor_analysis_q2.xlsx</source>
    <document_content>
      {{COMPETITOR_ANALYSIS}}
    </document_content>
  </document>
</documents>

## Types
```python
class PromptProject(BaseModel):
    name: str = Field(..., title="Project Name", description="The name of the prompt project.")
    max_tokens: int = Field(..., title="Maximum Tokens", description="The maximum number of tokens allowed for the generated prompt.")
    purpose: str = Field(..., title="Prompt Purpose", description="The purpose of the prompt being generated.")
    instructions: str = Field(..., title="Prompt Instructions", description="Specific instructions or guidelines for the prompt generation.")
    documents: List[str] = Field(..., title="Document File Paths", description="List of file paths to the documents that will be included in the prompt.")
```