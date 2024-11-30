"""
Service layer for the template management system.

This module contains all the service classes that implement the core
business logic of the template management system.
"""

import git
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from loguru import logger
from dataclasses import asdict

from .models import (
    DocumentMetadataModel,
    DocumentRelationshipModel,
    ConfigModel,
    DeploymentRecord,
    DocumentStatus,
    DocumentClassification
)

class BaseService:
    """Base class for all services with common logging and error handling"""
    def __init__(self, logger_context: Optional[Dict[str, Any]] = None):
        self.logger_context = logger_context or {}
    
    def log_error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log error with optional extra context"""
        context = {**self.logger_context, **(extra or {})}
        logger.error(message, extra=context)
    
    def log_info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log info with optional extra context"""
        context = {**self.logger_context, **(extra or {})}
        logger.info(message, extra=context)


class ConfigService(BaseService):
    """
    Manages configuration loading and validation.
    
    This service is responsible for loading and validating the system
    configuration, ensuring all required settings are present and valid.
    """
    def __init__(self, config_path: Path):
        super().__init__({"service": "ConfigService"})
        self.config_path = config_path
    
    def load_config(self) -> ConfigModel:
        """
        Load and validate configuration from file.
        
        Returns:
            ConfigModel: Validated configuration object
        
        Raises:
            ConfigurationError: If configuration is invalid or missing
        """
        try:
            with self.config_path.open('r') as f:
                config_data = yaml.safe_load(f)
            config = ConfigModel(**config_data)
            self.log_info(f"Configuration loaded successfully from {self.config_path}")
            return config
        except Exception as e:
            self.log_error(f"Configuration loading failed: {e}")
            raise ConfigurationError(f"Failed to load configuration: {e}")


class GitService(BaseService):
    """
    Manages Git-related operations for template tracking.
    
    Handles all interactions with the Git repository, including
    initialization, commits, and version tracking.
    """
    def __init__(self, repo_path: Path):
        super().__init__({"service": "GitService"})
        self.repo_path = repo_path
        self.repo = self._initialize_repo()
    
    def _initialize_repo(self) -> git.Repo:
        """Initialize Git repository"""
        try:
            repo = git.Repo(self.repo_path)
            self.log_info(f"Git repository initialized at {self.repo_path}")
            return repo
        except git.InvalidGitRepositoryError:
            self.log_error(f"Invalid Git repository at {self.repo_path}")
            raise ConfigurationError(f"No Git repository found at {self.repo_path}")
    
    def commit_template(self, target_path: Path, template_type: str) -> None:
        """
        Commit a deployed template to the repository.
        
        Args:
            target_path (Path): Path to the deployed template
            template_type (str): Type of template being deployed
        
        Raises:
            TemplateDeploymentError: If commit fails
        """
        try:
            self.repo.index.add([str(target_path)])
            commit_message = f"Deploy {template_type} template to {target_path}"
            self.repo.index.commit(commit_message)
            self.log_info(f"Template {template_type} committed successfully")
        except Exception as e:
            self.log_error(f"Git commit failed: {e}")
            raise TemplateDeploymentError(f"Git commit error: {e}")


class TemplateService(BaseService):
    """
    Handles template processing and deployment logic.
    
    This service is responsible for processing templates, including
    metadata injection, relationship management, and content deployment.
    """
    def __init__(self, base_path: Path):
        super().__init__({"service": "TemplateService"})
        self.base_path = base_path
    
    def process_template(self, 
                         template_content: str, 
                         metadata: DocumentMetadataModel,
                         relationships: Optional[List[DocumentRelationshipModel]] = None) -> str:
        """
        Process template with metadata and relationship injection.
        
        Args:
            template_content (str): Raw template content
            metadata (DocumentMetadataModel): Metadata to inject
            relationships (Optional[List[DocumentRelationshipModel]]): Optional relationships
        
        Returns:
            str: Processed template content
        
        Raises:
            TemplateDeploymentError: If processing fails
        """
        try:
            # Replace metadata placeholders
            processed_content = self._replace_metadata(template_content, metadata)
            
            # Add relationships if provided
            if relationships:
                processed_content = self._add_relationships(processed_content, relationships)
            
            self.log_info("Template processed successfully")
            return processed_content
        except Exception as e:
            self.log_error(f"Template processing failed: {e}")
            raise TemplateDeploymentError(f"Template processing error: {e}")
    
    def _replace_metadata(self, content: str, metadata: DocumentMetadataModel) -> str:
        """Replace metadata placeholders in content"""
        replacements = {
            '[doc_id]': metadata.doc_id,
            '[version]': metadata.version,
            '[status]': metadata.status.value,
            '[created_date]': str(metadata.created_date),
            '[author]': metadata.author,
            '[department]': metadata.department or '',
            '[classification]': metadata.classification.value
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, str(value))
        
        return content
    
    def _add_relationships(self, content: str, relationships: List[DocumentRelationshipModel]) -> str:
        """Add relationships section to content"""
        if not relationships:
            return content
        
        rel_section = "\n## Relationships\n"
        for rel in relationships:
            rel_section += (
                f"- {rel.relationship_type.value.title()}: {rel.name} "
                f"(Doc ID: {rel.doc_id}, Version: {rel.version})\n"
                f"  Impact: {rel.impact}\n"
                f"  Direction: {rel.direction}\n"
                f"  Required: {rel.required}\n"
            )
        
        # Insert relationships section after metadata
        parts = content.split('---', 2)
        if len(parts) >= 2:
            return f"{parts[0]}---{parts[1]}{rel_section}\n{parts[2]}"
        
        return content


class DependencyService(BaseService):
    """
    Manages dependency and relationship validation.
    
    This service handles dependency checking, including circular
    dependency detection and relationship validation.
    """
    def __init__(self):
        super().__init__({"service": "DependencyService"})
    
    def check_circular_dependencies(self, 
                                    relationships: Dict[str, List[DocumentRelationshipModel]]) -> None:
        """
        Detect circular dependencies in document relationships.
        
        Uses depth-first search to detect cycles in the dependency graph.
        
        Args:
            relationships (Dict[str, List[DocumentRelationshipModel]]): 
                Mapping of document IDs to their relationships
        
        Raises:
            CircularDependencyError: If circular dependencies are detected
        """
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()
        
        def dfs(doc_id: str) -> None:
            visited.add(doc_id)
            recursion_stack.add(doc_id)
            
            for relationship in relationships.get(doc_id, []):
                dependent_doc = relationship.doc_id
                
                if dependent_doc in recursion_stack:
                    self.log_error(f"Circular dependency detected: {doc_id} -> {dependent_doc}")
                    raise CircularDependencyError(
                        f"Circular dependency detected between {doc_id} and {dependent_doc}"
                    )
                
                if dependent_doc not in visited:
                    dfs(dependent_doc)
            
            recursion_stack.remove(doc_id)
        
        try:
            for doc_id in relationships:
                if doc_id not in visited:
                    dfs(doc_id)
            self.log_info("Dependency check completed successfully")
        except CircularDependencyError:
            raise
        except Exception as e:
            self.log_error(f"Dependency checking failed: {e}")
            raise TemplateDeploymentError(f"Dependency checking error: {e}")


class DeploymentHistoryService(BaseService):
    """
    Manages deployment history tracking and rollback capabilities.
    
    This service handles recording deployment events and provides
    rollback functionality for failed deployments.
    """
    def __init__(self, history_file: Path, max_entries: int = 50):
        super().__init__({"service": "DeploymentHistoryService"})
        self.history_file = history_file
        self.max_entries = max_entries
        self.history: List[DeploymentRecord] = self._load_history()
    
    def _load_history(self) -> List[DeploymentRecord]:
        """Load deployment history from file"""
        try:
            if not self.history_file.exists():
                return []
            
            with self.history_file.open('r') as f:
                history_data = json.load(f)
            
            history = []
            for record in history_data:
                try:
                    history.append(DeploymentRecord(
                        template_type=record['template_type'],
                        target_path=record['target_path'],
                        timestamp=datetime.fromisoformat(record['timestamp']),
                        status=record['status'],
                        version=record['version'],
                        checksum=record['checksum'],
                        metadata=record['metadata'],
                        error=record.get('error')
                    ))
                except KeyError as e:
                    self.log_error(f"Invalid history record: {e}")
                    continue
            
            return history[-self.max_entries:]
        except Exception as e:
            self.log_error(f"Error loading deployment history: {e}")
            return []
    
    def record_deployment(self, record: DeploymentRecord) -> None:
        """Record a deployment event"""
        self.history.append(record)
        self.history = self.history[-self.max_entries:]
        
        try:
            with self.history_file.open('w') as f:
                json.dump([asdict(rec) for rec in self.history], f, default=str)
            self.log_info(f"Deployment record saved: {record.template_type}")
        except Exception as e:
            self.log_error(f"Failed to save deployment history: {e}")
    
    def rollback(self, target_path: str) -> Optional[Path]:
        """
        Rollback to previous deployment of a template.
        
        Args:
            target_path (str): Path to the template to rollback
        
        Returns:
            Optional[Path]: Path to backup file if rollback successful
        """
        matching_deployments = [
            rec for rec in reversed(self.history)
            if rec.target_path == target_path and rec.status == 'success'
        ]
        
        if not matching_deployments:
            self.log_warning(f"No successful previous deployment found for {target_path}")
            return None
        
        previous_deployment = matching_deployments[0]
        target_path = Path(target_path)
        
        try:
            # Create backup of current file
            backup_path = target_path.with_suffix('.backup')
            if target_path.exists():
                target_path.rename(backup_path)
            
            # Find the original template file
            template_path = Path(previous_deployment.metadata.get('template_path', ''))
            
            if not template_path.exists():
                raise TemplateDeploymentError(f"Original template not found: {template_path}")
            
            # Restore from template
            template_path.copy(target_path)
            
            self.log_info(f"Rolled back {target_path} to version {previous_deployment.version}")
            return backup_path
        except Exception as e:
            self.log_error(f"Rollback failed: {e}")
            return None
