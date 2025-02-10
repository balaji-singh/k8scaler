import click

@click.command()
@click.option('--config', default='config.yaml', help='Path to the configuration file')
def cli(config):
    # CLI logic for managing scaling configurations
    click.echo(f'Using config: {config}')

if __name__ == '__main__':
    cli()
