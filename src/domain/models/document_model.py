"""Document relationship model with enhanced security and validation.

This module implements a secure and validated document relationship management system
following the three-iterations approach with proper security measures and validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Protocol, Any
from enum import Enum
import re
from uuid import UUID, uuid4
from abc import ABC, abstractmethod

class SecurityLevel(str, Enum):
    """Security levels for document access"""
    PUBLIC = "public"      # Accessible to all users
    INTERNAL = "internal"  # Internal users only
    CONFIDENTIAL = "confidential"  # Limited access
    RESTRICTED = "restricted"      # Strictly controlled access

class WorkflowState(str, Enum):
    """Document workflow states"""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class DocumentError(Exception):
    """Base exception for document errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = datetime.now()

class ValidationError(DocumentError):
    """Validation specific error"""
    pass

class SecurityError(DocumentError):
    """Security specific error"""
    pass

class DocumentValidator(Protocol):
    """Protocol for document validators"""
    def validate(self, document: 'DocumentRelationshipModel') -> bool: ...

class BaseValidator(ABC):
    """Base validator implementation"""
    @abstractmethod
    def validate(self, document: 'DocumentRelationshipModel') -> bool:
        """Validates document according to specific rules"""
        pass

class RelationshipValidator(BaseValidator):
    """Validates document relationships"""
    def validate(self, document: 'DocumentRelationshipModel') -> bool:
        if not document.document_id or not document.document_type:
            return False
        return all(
            isinstance(doc_id, str) and doc_id.strip() 
            for rel_docs in document.relationships.values() 
            for doc_id in rel_docs
        )

@dataclass
class DocumentRelationshipModel:
    """Document relationship model with enhanced security and validation.
    
    This class implements a secure document relationship management system with:
    - Strong input validation
    - Access control
    - Workflow management
    - Performance optimization
    - Comprehensive error handling
    """
    
    # First Iteration - Analysis & Understanding
    document_id: str
    document_type: str
    title: str
    created_at: datetime = field(default_factory=datetime.now)
    stakeholder_access: Dict[str, List[str]] = field(default_factory=dict)
    workflow_state: WorkflowState = field(default=WorkflowState.DRAFT)
    current_location: str = field(default_factory=str)
    security_level: SecurityLevel = field(default=SecurityLevel.INTERNAL)
    
    # Second Iteration - Solution & Implementation
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    integration_points: Dict[str, Dict] = field(default_factory=dict)
    validation_status: Dict[str, bool] = field(default_factory=dict)
    
    # Third Iteration - Enhancement & Optimization
    performance_indicators: Dict[str, float] = field(default_factory=dict)
    optimization_history: List[Dict] = field(default_factory=list)
    cross_references: Dict[str, List[str]] = field(default_factory=dict)
    future_dependencies: List[Dict] = field(default_factory=list)
    
    # Metadata
    id: UUID = field(default_factory=uuid4)
    version: str = "1.0.0"
    last_modified: datetime = field(default_factory=datetime.now)
    modified_by: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validates model after initialization"""
        self._validate_fields()
        self._sanitize_inputs()
        
    def _validate_fields(self):
        """Validates required fields"""
        if not self.document_id or not isinstance(self.document_id, str):
            raise ValidationError("Invalid document_id")
        if not self.document_type or not isinstance(self.document_type, str):
            raise ValidationError("Invalid document_type")
        if not self.title or not isinstance(self.title, str):
            raise ValidationError("Invalid title")
            
    def _sanitize_inputs(self):
        """Sanitizes input fields"""
        self.document_id = self._sanitize_string(self.document_id)
        self.document_type = self._sanitize_string(self.document_type)
        self.title = self._sanitize_string(self.title)
        self.current_location = self._sanitize_string(self.current_location)
        
    @staticmethod
    def _sanitize_string(value: str) -> str:
        """Sanitizes string input"""
        return re.sub(r'[<>&\'";\(\)]', '', value)
            
    def add_relationship(self, related_doc_id: str, relationship_type: str):
        """Adds a new document relationship with validation"""
        # Validate inputs
        if not related_doc_id or not relationship_type:
            raise ValidationError("Invalid relationship parameters")
            
        # Sanitize inputs
        related_doc_id = self._sanitize_string(related_doc_id)
        relationship_type = self._sanitize_string(relationship_type)
        
        # Add relationship
        if relationship_type not in self.relationships:
            self.relationships[relationship_type] = []
        if related_doc_id not in self.relationships[relationship_type]:
            self.relationships[relationship_type].append(related_doc_id)
            self.last_modified = datetime.now()
            
    def update_workflow_state(self, new_state: WorkflowState, modified_by: str):
        """Updates workflow state with validation"""
        if not isinstance(new_state, WorkflowState):
            raise ValidationError(f"Invalid workflow state: {new_state}")
        if not modified_by:
            raise ValidationError("Modified by is required")
            
        self.workflow_state = new_state
        self.last_modified = datetime.now()
        self.modified_by = self._sanitize_string(modified_by)
        
    def check_access(self, user_id: str, required_level: SecurityLevel) -> bool:
        """Checks if user has required access level"""
        if not user_id or not required_level:
            return False
        if required_level.value > self.security_level.value:
            return False
        return user_id in self.stakeholder_access.get(required_level.value, [])
        
    def validate_relationships(self) -> bool:
        """Validates all document relationships"""
        validator = RelationshipValidator()
        return validator.validate(self)
        
    def to_dict(self) -> Dict[str, Any]:
        """Converts model to dictionary with proper type handling"""
        return {
            "id": str(self.id),
            "document_id": self.document_id,
            "document_type": self.document_type,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "workflow_state": self.workflow_state.value,
            "security_level": self.security_level.value,
            "relationships": self.relationships,
            "version": self.version,
            "last_modified": self.last_modified.isoformat(),
            "modified_by": self.modified_by
        }
