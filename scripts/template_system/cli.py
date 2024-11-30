"""
Command-line interface for the template management system.

This module provides a command-line interface for interacting with
the template management system.
"""

import click
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from .core import TemplateManager, TemplateDeploymentError
from .models import (
    DocumentMetadataModel,
    DocumentRelationshipModel,
    DocumentStatus,
    DocumentClassification,
    RelationshipType
)

@click.group()
def cli():
    """HexProperty Template Management System CLI"""
    pass

@cli.command()
@click.argument('template_type')
@click.argument('target_path')
@click.option('--doc-id', required=True, help='Unique document identifier')
@click.option('--title', required=True, help='Document title')
@click.option('--version', default='1.0.0', help='Document version')
@click.option('--status', type=click.Choice(['draft', 'review', 'approved', 'archived']),
             default='draft', help='Document status')
@click.option('--author', help='Document author')
@click.option('--department', help='Responsible department')
@click.option('--classification',
             type=click.Choice(['public', 'internal', 'confidential', 'restricted']),
             default='internal', help='Document classification')
@click.option('--config', default='config.yaml', help='Path to configuration file')
def deploy(template_type: str,
          target_path: str,
          doc_id: str,
          title: str,
          version: str,
          status: str,
          author: Optional[str],
          department: Optional[str],
          classification: str,
          config: str):
    """
    Deploy a template with metadata.
    
    Example:
        template deploy architecture docs/auth-service.md \\
            --doc-id AUTH-001 \\
            --title "Authentication Service Architecture" \\
            --author "John Doe" \\
            --department "Engineering"
    """
    try:
        # Initialize template manager
        manager = TemplateManager(Path(config))
        
        # Create metadata model
        metadata = DocumentMetadataModel(
            doc_id=doc_id,
            version=version,
            status=DocumentStatus(status),
            author=author or "Unknown",
            department=department,
            classification=DocumentClassification(classification)
        )
        
        # Deploy template
        record = manager.deploy_template(
            template_type=template_type,
            target_path=Path(target_path),
            metadata=metadata
        )
        
        if record.status == 'success':
            click.echo(f"Template deployed successfully to {target_path}")
        else:
            click.echo(f"Template deployment failed: {record.error}", err=True)
    
    except TemplateDeploymentError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('target_path')
@click.option('--config', default='config.yaml', help='Path to configuration file')
def rollback(target_path: str, config: str):
    """
    Rollback a template deployment.
    
    Example:
        template rollback docs/auth-service.md
    """
    try:
        manager = TemplateManager(Path(config))
        backup_path = manager.rollback_deployment(target_path)
        
        if backup_path:
            click.echo(f"Deployment rolled back. Backup saved to {backup_path}")
        else:
            click.echo("Rollback failed: No previous successful deployment found")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

@cli.command()
@click.option('--config', default='config.yaml', help='Path to configuration file')
def history(config: str):
    """
    Show deployment history.
    
    Example:
        template history
    """
    try:
        manager = TemplateManager(Path(config))
        records = manager.get_deployment_history()
        
        if not records:
            click.echo("No deployment history found")
            return
        
        for record in records:
            status_color = 'green' if record.status == 'success' else 'red'
            click.echo(
                f"{record.timestamp} - "
                f"{click.style(record.status, fg=status_color)} - "
                f"{record.template_type} -> {record.target_path}"
            )
            if record.error:
                click.echo(f"  Error: {record.error}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
