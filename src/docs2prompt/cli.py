import click

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
@click.option('--directory', default='./docs', help='Directory to save the prompt project files')
@click.option('--max_tokens', default=128000, help='Maximum number of tokens allowed for the prompt')
@click.option('--name', prompt='Project name', help='Name of the prompt project')
def create(name, max_tokens, directory):
    """Create a new prompt project with default values."""
    click.echo(f'Create command called with name: {name}, max_tokens: {max_tokens}, directory: {directory}')
    click.echo(f'Creating a new prompt project: {name}')
    click.echo(f'Max tokens: {max_tokens}')
    click.echo(f'Directory: {directory}')
    # Add logic to create the project file with default values

# Add all commands to the main CLI group
click.echo('Adding commands to CLI group')
cli.add_command(run)
cli.add_command(create)

if __name__ == '__main__':
    click.echo('Starting CLI application')
    cli()