import click
from docs2prompt.project_manager import create_project

@click.group()
def cli():
    """docs2prompt cli"""
    pass

@click.command()
@click.argument('project_name')
def run(project_name):
    """Run the prompt project."""
    click.echo(f'Run command called with project name: {project_name}')
    click.echo(f'Running prompt project: {project_name}')
    # Add logic to run the prompt project

@click.command()
@click.option('--max_tokens', default=100000, help='Maximum number of tokens allowed for the prompt')
@click.option('--name', prompt='Project name', help='Name of the prompt project')
def create(name, max_tokens):
    """Create a new prompt project with default values."""
    click.echo(f'Create command called with name: {name}, max_tokens: {max_tokens}')
    create_project(name, max_tokens)

# Add all commands to the main CLI group
click.echo('Adding commands to CLI group')
cli.add_command(run)
cli.add_command(create)

if __name__ == '__main__':
    click.echo('Starting CLI application')
    cli()
import click
from docs2prompt.document_manager import DocumentManager

@click.group()
def cli():
    """Docs2Prompt CLI"""
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--whitelist', '-w', multiple=True, help='Whitelist glob patterns')
@click.option('--blacklist', '-b', multiple=True, help='Blacklist glob patterns')
def create_file_list(directory, whitelist, blacklist):
    """Create a list of files from the given directory"""
    doc_manager = DocumentManager()
    file_list = doc_manager.create_file_list(directory, whitelist, blacklist)
    for file in file_list:
        click.echo(file)

if __name__ == '__main__':
    cli()
