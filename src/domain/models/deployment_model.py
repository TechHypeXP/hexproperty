"""Deployment model with enhanced security and validation.

This module implements a secure and validated deployment management system
following the three-iterations approach with proper security measures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Protocol, Any
from uuid import UUID, uuid4
import re
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator
from src.domain.security.rate_limiter import RateLimiter, RateLimitConfig, rate_limit
from src.domain.security.audit_log import (
    audit_logger,
    AuditEventType,
    AuditEventSeverity,
    log_deployment_event
)

class SecurityLevel(str, Enum):
    """Security levels for deployment operations"""
    READ_ONLY = "read_only"      # Can only view deployments
    EXECUTE = "execute"          # Can execute deployments
    MODIFY = "modify"           # Can modify deployment configs
    ADMIN = "admin"            # Full deployment control

class DeploymentStatus(str, Enum):
    """Deployment status states with validation rules"""
    PENDING = "pending"          # Initial state
    IN_PROGRESS = "in_progress"  # Deployment running
    COMPLETED = "completed"      # Successfully completed
    FAILED = "failed"           # Failed to complete
    ROLLED_BACK = "rolled_back" # Reverted to previous state

class DeploymentType(str, Enum):
    """Types of deployments with security implications"""
    TEMPLATE = "template"        # Template-based deployment
    CONFIG = "config"           # Configuration deployment
    SYSTEM = "system"           # System-level deployment
    INFRASTRUCTURE = "infrastructure"  # Infrastructure deployment

class DeploymentError(Exception):
    """Base exception for deployment errors with context"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = datetime.now()

class ValidationError(DeploymentError):
    """Validation specific error"""
    pass

class SecurityError(DeploymentError):
    """Security specific error"""
    pass

class DeploymentValidator(Protocol):
    """Protocol for deployment validators"""
    def validate(self, deployment: 'DeploymentRecord') -> bool: ...

class BaseValidator(ABC):
    """Base validator implementation"""
    @abstractmethod
    def validate(self, deployment: 'DeploymentRecord') -> bool:
        """Validates deployment according to specific rules"""
        pass

class StatusTransitionValidator(BaseValidator):
    """Validates deployment status transitions"""
    def validate(self, deployment: 'DeploymentRecord') -> bool:
        valid_transitions = {
            DeploymentStatus.PENDING: {DeploymentStatus.IN_PROGRESS, DeploymentStatus.FAILED},
            DeploymentStatus.IN_PROGRESS: {DeploymentStatus.COMPLETED, DeploymentStatus.FAILED},
            DeploymentStatus.COMPLETED: {DeploymentStatus.ROLLED_BACK},
            DeploymentStatus.FAILED: {DeploymentStatus.PENDING},
            DeploymentStatus.ROLLED_BACK: {DeploymentStatus.PENDING}
        }
        return deployment.status in valid_transitions.get(deployment.status, set())

class DeploymentMetadata(BaseModel):
    """Metadata model for deployment records with enhanced validation"""
    id: UUID = Field(default_factory=uuid4)
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    modified_by: Optional[str] = None
    security_level: SecurityLevel = Field(default=SecurityLevel.READ_ONLY)
    errors: List[Dict] = Field(default_factory=list)

    @validator('version')
    def validate_version(cls, v: str) -> str:
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError("Version must be in format X.Y.Z")
        return v

    def add_error(self, error_type: str, error_message: str) -> None:
        """Adds an error with proper sanitization"""
        self.errors.append({
            "type": self._sanitize_string(error_type),
            "message": self._sanitize_string(error_message),
            "timestamp": datetime.now().isoformat()
        })

    @staticmethod
    def _sanitize_string(value: str) -> str:
        """Sanitizes string input"""
        return re.sub(r'[<>&\'";\(\)]', '', value)

@dataclass
class DeploymentRecord:
    """Deployment record model with enhanced security and validation.
    
    This class implements a secure deployment management system with:
    - Strong input validation
    - Access control
    - Status management
    - Performance tracking
    - Comprehensive error handling
    - Rate limiting
    - Audit logging
    """
    
    # First Iteration - Analysis & Understanding
    deployment_id: str
    deployment_type: DeploymentType
    deployment_strategy: str
    created_at: datetime = field(default_factory=datetime.now)
    stakeholders: List[str] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    initial_state: Dict = field(default_factory=dict)
    
    # Second Iteration - Solution & Implementation
    implementation_steps: List[Dict] = field(default_factory=list)
    validation_results: Dict[str, bool] = field(default_factory=dict)
    integration_status: Dict[str, str] = field(default_factory=dict)
    rollback_plan: Dict = field(default_factory=dict)
    
    # Third Iteration - Enhancement & Optimization
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    optimization_attempts: List[Dict] = field(default_factory=list)
    system_interactions: Dict[str, List[str]] = field(default_factory=dict)
    future_improvements: List[Dict] = field(default_factory=list)
    edge_case_handling: Dict[str, str] = field(default_factory=dict)
    
    # Status and Metadata
    status: DeploymentStatus = field(default=DeploymentStatus.PENDING)
    metadata: DeploymentMetadata = field(default_factory=DeploymentMetadata)
    
    # Rate limiter for deployment operations
    _rate_limiter = RateLimiter(RateLimitConfig(
        max_requests=10,
        time_window=60  # 10 requests per minute
    ))
    
    def __post_init__(self):
        """Validates model after initialization"""
        self._validate_fields()
        self._sanitize_inputs()
        
    def _validate_fields(self) -> None:
        """Validates required fields with simplified checks."""
        required_fields = {
            'deployment_id': str,
            'deployment_type': DeploymentType,
            'deployment_strategy': str
        }
        
        if errors := [
            f"Missing or invalid {field}: {type_}" 
            for field, type_ in required_fields.items()
            if not isinstance(getattr(self, field), type_)
        ]:
            raise ValidationError("\n".join(errors))

    def _sanitize_inputs(self) -> None:
        """Sanitizes input fields using list comprehension."""
        self.stakeholders = [
            self._sanitize_string(s) for s in self.stakeholders
            if (sanitized := self._sanitize_string(s))
        ]
        self.objectives = [
            self._sanitize_string(obj) for obj in self.objectives
            if (sanitized := self._sanitize_string(obj))
        ]
        
        # Use dictionary comprehension for nested structures
        self.implementation_steps = [
            {k: self._sanitize_string(v) if isinstance(v, str) else v 
             for k, v in step.items()}
            for step in self.implementation_steps
        ]

    def update_status(self, new_status: DeploymentStatus, modified_by: str, 
                     security_level: SecurityLevel = SecurityLevel.EXECUTE) -> None:
        """Updates deployment status with enhanced validation."""
        if not (access_granted := self.check_access(modified_by, security_level)):
            raise SecurityError(f"User {modified_by} lacks {security_level} access")
            
        validator = StatusTransitionValidator()
        if not (is_valid := validator.validate(self)):
            raise ValidationError(f"Invalid status transition from {self.status} to {new_status}")
            
        self.status = new_status
        self.metadata.last_modified = datetime.now()
        self.metadata.modified_by = modified_by
        
        # Log the status update
        log_deployment_event(
            action=f"status_update_{new_status}",
            status="success",
            severity=AuditEventSeverity.INFO,
            details={
                "deployment_id": self.deployment_id,
                "old_status": self.status,
                "new_status": new_status,
                "modified_by": modified_by
            }
        )

    @rate_limit
    def validate_deployment(self) -> bool:
        """Validates deployment with simplified checks."""
        try:
            if not (all_fields_valid := self._validate_fields()):
                return False
                
            if not (status_valid := StatusTransitionValidator().validate(self)):
                self.add_error("status", f"Invalid status: {self.status}")
                return False
                
            return True
            
        except Exception as e:
            self.add_error("validation", f"Validation failed: {str(e)}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Converts deployment record to dictionary with f-strings."""
        return {
            "deployment_id": self.deployment_id,
            "type": f"{self.deployment_type.value}",
            "strategy": self.deployment_strategy,
            "status": f"{self.status.value}",
            "created_at": f"{self.created_at.isoformat()}",
            "metadata": self.metadata.dict(),
            "stakeholders": self.stakeholders,
            "objectives": self.objectives,
            "implementation": self.implementation_steps,
            "validation": self.validation_results,
            "integration": self.integration_status,
            "performance": self.performance_metrics
        }

    def check_access(self, user_id: str, required_level: SecurityLevel) -> bool:
        """Checks if user has required access level with audit logging
        
        Args:
            user_id: User ID to check
            required_level: Required security level
            
        Returns:
            bool: True if access is allowed
        """
        if not user_id or not required_level:
            log_deployment_event(
                action="check_access",
                status="failed",
                severity=AuditEventSeverity.WARNING,
                user_id=user_id,
                resource_id=str(self.metadata.id),
                details={
                    "required_level": required_level.value if required_level else None,
                    "reason": "Missing user_id or required_level"
                }
            )
            return False
            
        if required_level.value > self.metadata.security_level.value:
            log_deployment_event(
                action="check_access",
                status="denied",
                severity=AuditEventSeverity.WARNING,
                user_id=user_id,
                resource_id=str(self.metadata.id),
                details={
                    "required_level": required_level.value,
                    "actual_level": self.metadata.security_level.value
                }
            )
            return False
            
        log_deployment_event(
            action="check_access",
            status="granted",
            user_id=user_id,
            resource_id=str(self.metadata.id),
            details={
                "required_level": required_level.value,
                "actual_level": self.metadata.security_level.value
            }
        )
        return True  # TODO: Implement actual user permission check
        
    def add_error(self, error_type: str, error_message: str) -> None:
        """Adds an error with proper sanitization"""
        self.metadata.add_error(error_type, error_message)
        
    @staticmethod
    def _sanitize_string(value: str) -> str:
        """Sanitizes string input"""
        return re.sub(r'[<>&\'";\(\)]', '', value)
