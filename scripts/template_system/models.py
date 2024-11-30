"""
Data models for the template management system.

This module contains all the Pydantic models and data classes used
throughout the template management system.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from pydantic.config import ConfigDict
from dataclasses import dataclass, field
from enum import Enum, auto


class RelationshipType(str, Enum):
    """Valid relationship types between documents"""
    DEPENDENCY = "dependency"
    REFERENCE = "reference"
    DERIVED = "derived"
    RELATED = "related"


class DocumentStatus(str, Enum):
    """Valid document statuses"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    ARCHIVED = "archived"


class DocumentClassification(str, Enum):
    """Valid document classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class DocumentMetadataModel(BaseModel):
    """
    Represents the metadata for a document in the template management system.

    This model captures essential information about a document, including:
    - Unique identification
    - Versioning
    - Status
    - Authorship
    - Classification
    - Temporal information

    Attributes:
        doc_id (str): Unique identifier for the document
        version (str): Semantic version of the document
        status (DocumentStatus): Current status of the document
        created_date (datetime): Timestamp of document creation
        updated_date (datetime, optional): Timestamp of last update
        author (str): Name of the document's author
        department (str, optional): Department responsible for the document
        classification (DocumentClassification): Document security classification
        template_version (str): Version of the template used
        checksum (str, optional): Cryptographic hash for document integrity
    """
    doc_id: str
    version: str = Field(default="1.0.0")
    status: DocumentStatus = Field(default=DocumentStatus.DRAFT)
    created_date: datetime = Field(default_factory=datetime.now)
    updated_date: Optional[datetime] = None
    author: str = Field(default="Unknown")
    department: Optional[str] = None
    classification: DocumentClassification = Field(default=DocumentClassification.INTERNAL)
    template_version: str = Field(default="1.0.0")
    checksum: Optional[str] = None

    model_config = ConfigDict(
        validate_assignment=True,
        extra='ignore',
        arbitrary_types_allowed=True
    )

    @validator('version', 'template_version')
    def validate_version(cls, value: str) -> str:
        """
        Validate version format to ensure it follows semantic versioning.

        Args:
            value (str): Version string to validate

        Returns:
            str: Validated version string

        Raises:
            ValueError: If version format is invalid
        """
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', value):
            raise ValueError("Version must follow semantic versioning (X.Y.Z)")
        return value


class DocumentRelationshipModel(BaseModel):
    """
    Defines the relationship between documents in the documentation system.

    Represents how documents are interconnected, including:
    - Dependency tracking
    - Reference management
    - Hierarchical relationships

    Attributes:
        doc_id (str): Unique identifier of the related document
        name (str): Human-readable name of the relationship
        version (str): Version of the related document
        relationship_type (RelationshipType): Type of relationship
        impact (str): Significance of the relationship
        direction (str, optional): Direction of the relationship
        required (bool, optional): Whether the relationship is mandatory
    """
    doc_id: str
    name: str
    version: str
    relationship_type: RelationshipType
    impact: str
    direction: str = "outbound"
    required: bool = True


class ConfigModel(BaseModel):
    """
    Manages configuration settings for the template deployment system.

    Provides a structured and validated approach to loading system configurations,
    including paths, default settings, and deployment parameters.

    Attributes:
        templates_dir (Path): Base directory for document templates
        deployment_history_path (Path): Location for storing deployment history
        git_repo_path (Optional[Path]): Path to the Git repository
        default_hooks (Dict[str, Optional[str]]): Default deployment hooks
        max_history_entries (int): Maximum number of deployment history entries
        default_department (str): Default department for new documents
        default_classification (DocumentClassification): Default security classification
    """
    templates_dir: str
    deployment_history_path: str
    git_repo_path: Optional[str] = None
    default_hooks: Dict[str, Optional[str]] = Field(default_factory=dict)
    max_history_entries: int = Field(default=50, ge=1, le=1000)
    default_department: str = Field(default="Engineering")
    default_classification: DocumentClassification = Field(default=DocumentClassification.INTERNAL)

    @validator('max_history_entries')
    def validate_max_history(cls, value: int) -> int:
        """Validate maximum history entries"""
        if not 1 <= value <= 1000:
            raise ValueError("max_history_entries must be between 1 and 1000")
        return value


@dataclass
class DeploymentRecord:
    """
    Record of a template deployment operation.

    Captures all relevant information about a template deployment,
    including success/failure status and any error information.

    Attributes:
        template_type (str): Type of template deployed
        target_path (str): Path where template was deployed
        timestamp (datetime): When the deployment occurred
        status (str): Deployment status (success/failed)
        version (str): Version of the deployed template
        checksum (str): Content checksum for verification
        metadata (Dict[str, Any]): Additional deployment metadata
        error (Optional[str]): Error message if deployment failed
    """
    template_type: str
    target_path: str
    timestamp: datetime
    status: str
    version: str
    checksum: str
    metadata: Dict[str, Any]
    error: Optional[str] = None
