"""
Core template management system implementation.

This module contains the main TemplateManager class that orchestrates
the template deployment process using various services.
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import (
    DocumentMetadataModel,
    DocumentRelationshipModel,
    ConfigModel,
    DeploymentRecord
)
from .services import (
    ConfigService,
    GitService,
    TemplateService,
    DependencyService,
    DeploymentHistoryService
)

class TemplateDeploymentError(Exception):
    """Base exception for template deployment errors"""
    pass

class ConfigurationError(TemplateDeploymentError):
    """Configuration related errors"""
    pass

class CircularDependencyError(TemplateDeploymentError):
    """Circular dependency detection errors"""
    pass

class TemplateManager:
    """
    Main orchestrator for the template management system.
    
    This class coordinates the various services to provide a unified
    interface for template deployment and management.
    
    Attributes:
        config (ConfigModel): System configuration
        config_service (ConfigService): Configuration management service
        git_service (Optional[GitService]): Git operations service
        template_service (TemplateService): Template processing service
        dependency_service (DependencyService): Dependency validation service
        history_service (DeploymentHistoryService): Deployment history service
    """
    def __init__(self, config_path: Path):
        """
        Initialize the template manager with configuration.
        
        Args:
            config_path (Path): Path to configuration file
        
        Raises:
            ConfigurationError: If configuration is invalid
        """
        self.config_service = ConfigService(config_path)
        self.config = self.config_service.load_config()
        
        # Initialize services
        self.template_service = TemplateService(Path(self.config.templates_dir))
        self.dependency_service = DependencyService()
        self.history_service = DeploymentHistoryService(
            Path(self.config.deployment_history_path),
            self.config.max_history_entries
        )
        
        # Optional Git service
        self.git_service = None
        if self.config.git_repo_path:
            self.git_service = GitService(Path(self.config.git_repo_path))
    
    def deploy_template(self,
                       template_type: str,
                       target_path: Path,
                       metadata: DocumentMetadataModel,
                       relationships: Optional[List[DocumentRelationshipModel]] = None,
                       template_content: Optional[str] = None) -> DeploymentRecord:
        """
        Deploy a template with metadata and relationships.
        
        This method orchestrates the entire template deployment process:
        1. Validates dependencies and relationships
        2. Processes the template with metadata
        3. Deploys the processed template
        4. Records the deployment
        5. Commits changes if Git is enabled
        
        Args:
            template_type (str): Type of template being deployed
            target_path (Path): Path where template should be deployed
            metadata (DocumentMetadataModel): Template metadata
            relationships (Optional[List[DocumentRelationshipModel]]): Template relationships
            template_content (Optional[str]): Raw template content
        
        Returns:
            DeploymentRecord: Record of the deployment
        
        Raises:
            TemplateDeploymentError: If deployment fails
        """
        try:
            # Validate dependencies if relationships provided
            if relationships:
                self.dependency_service.check_circular_dependencies({
                    metadata.doc_id: relationships
                })
            
            # Load template content if not provided
            if template_content is None:
                template_path = self.template_service.base_path / f"{template_type}.md"
                if not template_path.exists():
                    raise TemplateDeploymentError(f"Template not found: {template_path}")
                with template_path.open('r') as f:
                    template_content = f.read()
            
            # Process template
            processed_content = self.template_service.process_template(
                template_content,
                metadata,
                relationships
            )
            
            # Calculate checksum
            checksum = hashlib.sha256(processed_content.encode()).hexdigest()
            
            # Create deployment record
            record = DeploymentRecord(
                template_type=template_type,
                target_path=str(target_path),
                timestamp=datetime.now(),
                status='pending',
                version=metadata.version,
                checksum=checksum,
                metadata={
                    'template_path': str(template_path) if template_content is None else None,
                    'author': metadata.author,
                    'department': metadata.department,
                    'classification': metadata.classification.value
                }
            )
            
            try:
                # Deploy template
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with target_path.open('w') as f:
                    f.write(processed_content)
                
                # Update record status
                record.status = 'success'
                
                # Commit if Git enabled
                if self.git_service:
                    self.git_service.commit_template(target_path, template_type)
            except Exception as e:
                record.status = 'failed'
                record.error = str(e)
                raise
            finally:
                # Record deployment
                self.history_service.record_deployment(record)
            
            return record
        except Exception as e:
            raise TemplateDeploymentError(f"Template deployment failed: {e}") from e
    
    def rollback_deployment(self, target_path: str) -> Optional[Path]:
        """
        Rollback a template deployment.
        
        Args:
            target_path (str): Path to the template to rollback
        
        Returns:
            Optional[Path]: Path to backup file if rollback successful
        """
        return self.history_service.rollback(target_path)
    
    def get_deployment_history(self) -> List[DeploymentRecord]:
        """Get deployment history"""
        return self.history_service.history
    
    def validate_dependencies(self, relationships: Dict[str, List[DocumentRelationshipModel]]) -> None:
        """
        Validate relationships for circular dependencies.
        
        Args:
            relationships (Dict[str, List[DocumentRelationshipModel]]): 
                Mapping of document IDs to their relationships
        
        Raises:
            CircularDependencyError: If circular dependencies are detected
        """
        self.dependency_service.check_circular_dependencies(relationships)
