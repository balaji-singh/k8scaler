#!/usr/bin/env python
import click
import requests

API_URL = "http://autoscaler-service.default.svc"  # Adjust as needed

@click.group()
def cli():
    """K8Scaler CLI for managing scaling configurations."""
    pass

@cli.command()
def list_sources():
    """List available event sources."""
    response = requests.get(f"{API_URL}/sources")
    click.echo(response.json())

@cli.command()
@click.argument("source_type")
@click.argument("source_url")
def add_source(source_type, source_url):
    """Add a new event source."""
    payload = {"type": source_type, "url": source_url}
    response = requests.post(f"{API_URL}/sources", json=payload)
    click.echo(response.json())

@cli.command()
@click.argument("deployment")
@click.argument("replicas", type=int)
def scale(deployment, replicas):
    """Manually scale a deployment."""
    payload = {"replicas": replicas}
    response = requests.post(f"{API_URL}/manual-override", json=payload)
    click.echo(response.json())

if __name__ == "__main__":
    cli()
