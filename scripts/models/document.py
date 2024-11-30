"""Document models for the template management system.

First Iteration - Core Purpose:
---------------------------
Define the core data structures for document metadata and relationships,
ensuring proper data validation and type safety.

Second Iteration - Technical Details:
--------------------------------
Implementation Components:
1. Data Models
2. Validation Rules
3. Type Definitions
4. Relationship Mappings
5. State Management

Third Iteration - Implementation Context:
------------------------------------
System Integration:
* Pydantic integration
* JSON serialization
* Database mapping
* API compatibility
* Version control
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator

# First Iteration - Core Enums
# --------------------------
# Basic status and classification types
class DocumentStatus(str, Enum):
    """Document workflow status.
    
    First Iteration:
    * Basic status tracking
    
    Second Iteration:
    * Workflow states
    * State transitions
    * Validation rules
    
    Third Iteration:
    * State machine
    * Transition hooks
    * Audit logging
    """
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    ARCHIVED = "archived"

class DocumentClassification(str, Enum):
    """Document security classification.
    
    First Iteration:
    * Basic classification levels
    
    Second Iteration:
    * Access control
    * Visibility rules
    * Security policies
    
    Third Iteration:
    * Compliance rules
    * Audit requirements
    * Encryption levels
    """
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

# First Iteration - Relationship Types
# ---------------------------------
# Basic relationship classifications
class RelationshipType(str, Enum):
    """Document relationship types.
    
    First Iteration:
    * Basic relationships
    
    Second Iteration:
    * Relationship rules
    * Validation logic
    
    Third Iteration:
    * Custom types
    * Workflow integration
    * Graph traversal
    """
    PARENT = "parent"
    CHILD = "child"
    REFERENCE = "reference"
    DEPENDENCY = "dependency"
    SUPERSEDES = "supersedes"

# First Iteration - Core Models
# ---------------------------
# Essential document metadata
class DocumentMetadataModel(BaseModel):
    """Document metadata model.
    
    First Iteration - Core Purpose:
    ---------------------------
    Define essential document metadata fields with basic validation.
    
    Second Iteration - Technical Details:
    --------------------------------
    Validation Rules:
    1. Required Fields:
       * doc_id
       * version
       * status
    2. Optional Fields:
       * author
       * department
       * classification
    3. Auto-generated:
       * created_date
       * checksum
    
    Third Iteration - Implementation Context:
    ------------------------------------
    Implementation Features:
    1. Data Validation:
       * Format checking
       * Type conversion
       * Default values
       * Custom validators
    
    2. Integration:
       * Database mapping
       * API serialization
       * Version control
       * Audit logging
    
    3. Performance:
       * Lazy loading
       * Caching
       * Batch processing
    """
    # First Iteration - Essential Fields
    doc_id: str = Field(..., description="Unique document identifier")
    version: str = Field(..., description="Document version")
    status: DocumentStatus = Field(
        default=DocumentStatus.DRAFT,
        description="Document workflow status"
    )
    
    # Second Iteration - Extended Fields
    created_date: datetime = Field(
        default_factory=datetime.utcnow,
        description="Document creation timestamp"
    )
    author: Optional[str] = Field(
        default=None,
        description="Document author"
    )
    department: Optional[str] = Field(
        default=None,
        description="Owning department"
    )
    classification: DocumentClassification = Field(
        default=DocumentClassification.INTERNAL,
        description="Security classification"
    )
    
    # Third Iteration - Technical Fields
    template_version: Optional[str] = Field(
        default=None,
        description="Version of template used"
    )
    checksum: Optional[str] = Field(
        default=None,
        description="Content checksum"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )

    # First Iteration - Basic Validation
    @validator('doc_id')
    def validate_doc_id(cls, v: str) -> str:
        """Validate document ID format.
        
        First Iteration:
        * Basic format check
        
        Second Iteration:
        * Pattern matching
        * Reserved words
        
        Third Iteration:
        * Custom patterns
        * Department prefixes
        * Classification rules
        """
        if not v or not v.strip():
            raise ValueError("Document ID cannot be empty")
        return v.strip().upper()

    # Second Iteration - Extended Validation
    @validator('version')
    def validate_version(cls, v: str) -> str:
        """Validate version format.
        
        First Iteration:
        * Basic format
        
        Second Iteration:
        * Semantic versioning
        * Version comparison
        
        Third Iteration:
        * Custom formats
        * Branch versions
        * Release tracking
        """
        if not v or not v.strip():
            raise ValueError("Version cannot be empty")
        # Could add semantic version validation here
        return v.strip()

    # Third Iteration - Advanced Features
    def get_security_context(self) -> Dict[str, Any]:
        """Get security context for access control.
        
        First Iteration:
        * Basic context
        
        Second Iteration:
        * Access levels
        * Permissions
        
        Third Iteration:
        * Role-based access
        * Time-based rules
        * Location rules
        """
        return {
            "classification": self.classification,
            "department": self.department,
            "status": self.status
        }

    class Config:
        """Model configuration.
        
        First Iteration:
        * Basic settings
        
        Second Iteration:
        * Validation rules
        * Schema options
        
        Third Iteration:
        * Custom settings
        * Performance options
        * Integration config
        """
        validate_assignment = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Second Iteration - Relationship Model
# ----------------------------------
# Document relationship tracking
class DocumentRelationshipModel(BaseModel):
    """Document relationship model.
    
    First Iteration - Analysis & Understanding:
    -------------------------------------
    Day-in-the-Life:
    * Users need to track document dependencies
    * Teams collaborate on related documents
    * Managers oversee document hierarchies
    * Systems process document relationships
    
    Objectives:
    * Track document relationships
    * Manage dependencies
    * Enable collaboration
    * Support automation
    
    Gaps:
    * No relationship tracking
    * Manual dependency management
    * Limited collaboration support
    * Inconsistent versioning
    
    Second Iteration - Solution & Implementation:
    --------------------------------------
    Gap Management:
    * Relationship tracking system
    * Dependency resolution
    * Collaboration features
    * Version control integration
    
    Problem-Solving:
    * Graph-based relationships
    * Dependency validation
    * Change propagation
    * Version synchronization
    
    Implementation:
    * Model structure
    * Validation rules
    * Graph operations
    * Event handling
    
    Third Iteration - Enhancement & Optimization:
    --------------------------------------
    Solution Refinement:
    * Performance tuning
    * Graph optimization
    * Memory management
    * Query efficiency
    
    Future Scenarios:
    * Complex relationships
    * Large-scale graphs
    * Real-time collaboration
    * AI-powered insights
    
    Integration Analysis:
    * Version control
    * Collaboration tools
    * Search systems
    * Analytics platforms
    """
    # First Iteration - Essential Fields
    source_doc_id: str = Field(..., description="Source document ID")
    target_doc_id: str = Field(..., description="Target document ID")
    relationship_type: RelationshipType = Field(
        ...,
        description="Type of relationship"
    )
    
    # Second Iteration - Extended Fields
    created_date: datetime = Field(
        default_factory=datetime.utcnow,
        description="Relationship creation date"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional relationship metadata"
    )
    
    # Third Iteration - Technical Fields
    bidirectional: bool = Field(
        default=False,
        description="Whether relationship is bidirectional"
    )
    weight: float = Field(
        default=1.0,
        description="Relationship strength or importance"
    )
    
    # First Iteration - Basic Validation
    @validator('source_doc_id', 'target_doc_id')
    def validate_doc_ids(cls, v: str) -> str:
        """Validate document IDs.
        
        First Iteration:
        * Format check
        
        Second Iteration:
        * Existence check
        * Access check
        
        Third Iteration:
        * Graph validation
        * Cycle detection
        * Impact analysis
        """
        if not v or not v.strip():
            raise ValueError("Document ID cannot be empty")
        return v.strip().upper()
    
    # Second Iteration - Relationship Validation
    @validator('target_doc_id')
    def validate_relationship(cls, v: str, values: Dict[str, Any]) -> str:
        """Validate relationship constraints.
        
        First Iteration:
        * Self-reference check
        
        Second Iteration:
        * Type constraints
        * Access rules
        
        Third Iteration:
        * Graph constraints
        * Business rules
        * Workflow rules
        """
        if 'source_doc_id' in values and v == values['source_doc_id']:
            raise ValueError("Document cannot have relationship with itself")
        return v
    
    # Third Iteration - Advanced Features
    def get_graph_data(self) -> Dict[str, Any]:
        """Get data for graph operations.
        
        First Iteration:
        * Basic node data
        
        Second Iteration:
        * Edge properties
        * Traversal info
        
        Third Iteration:
        * Cache data
        * Index hints
        * Performance data
        """
        return {
            "source": self.source_doc_id,
            "target": self.target_doc_id,
            "type": self.relationship_type,
            "weight": self.weight,
            "bidirectional": self.bidirectional,
            "metadata": self.metadata
        }

    class Config:
        """Model configuration.
        
        First Iteration:
        * Basic config
        
        Second Iteration:
        * Validation rules
        * Schema settings
        
        Third Iteration:
        * Custom settings
        * Cache config
        * Index settings
        """
        validate_assignment = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
