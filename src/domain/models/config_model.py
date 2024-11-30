"""Configuration model module with enhanced validation and security.

This module implements a configuration management system following the three-iterations approach:
1. Analysis & Understanding - Basic configuration structure and validation
2. Solution & Implementation - Validation strategies and security measures  
3. Enhancement & Optimization - Performance improvements and advanced features

Key Features:
- Type-safe configuration management
- Comprehensive validation system
- Security and access control
- Performance optimization
- Detailed error tracking

Example:
    config = ConfigModel(
        name="deployment-config",
        description="Production deployment configuration"
    )
    config.validate()  # Validates the configuration
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Protocol, Any, TypeVar, Generic
from enum import Enum
from abc import ABC, abstractmethod
import re
from uuid import UUID, uuid4
from functools import lru_cache
from typing import Callable

T = TypeVar('T')

class ValidationMixin:
    """Mixin providing common validation functionality"""
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """Sanitizes input strings to prevent injection"""
        return re.sub(r'[<>&\'";\(\)]', '', value)
        
    @staticmethod
    def validate_length(value: str, max_length: int, field_name: str) -> List[str]:
        """Validates string length"""
        errors = []
        if len(value) > max_length:
            errors.append(f"{field_name} exceeds maximum length of {max_length}")
        return errors
        
    @staticmethod
    def validate_pattern(value: str, pattern: str, field_name: str) -> List[str]:
        """Validates string against regex pattern"""
        errors = []
        if not re.match(pattern, value):
            errors.append(f"Invalid {field_name} format: {value}")
        return errors

class ConfigStatus(str, Enum):
    """Configuration status enumeration"""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class SecurityLevel(str, Enum):
    """Security level enumeration defining access control levels.
    
    Levels:
        LOW: Basic access, no sensitive operations
        NORMAL: Standard operations, non-critical data
        HIGH: Sensitive operations, important data
        CRITICAL: Highest security, system-critical operations
    """
    LOW = "low"  # Basic access, no sensitive operations
    NORMAL = "normal"  # Standard operations, non-critical data
    HIGH = "high"  # Sensitive operations, important data
    CRITICAL = "critical"  # Highest security, system-critical operations

class ConfigError(Exception):
    """Base exception for configuration errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = datetime.now()

class ValidationError(ConfigError):
    """Validation specific error"""
    pass

class AuthorizationError(ConfigError):
    """Authorization specific error"""
    pass

class ValidationResult:
    """Structured validation result with security context"""
    def __init__(self, is_valid: bool, errors: List[str], security_level: SecurityLevel = SecurityLevel.NORMAL):
        self.is_valid = is_valid
        self.errors = errors
        self.timestamp = datetime.now()
        self.security_level = security_level
        self.validation_id = uuid4()

    def to_dict(self) -> Dict:
        """Converts validation result to dictionary"""
        return {
            "validation_id": str(self.validation_id),
            "is_valid": self.is_valid,
            "errors": self.errors,
            "timestamp": self.timestamp.isoformat(),
            "security_level": self.security_level.value
        }

    def __bool__(self) -> bool:
        """Allows direct boolean evaluation"""
        return self.is_valid

class ValidatorRegistry:
    """Registry for managing validators"""
    _validators: Dict[str, 'BaseConfigValidator'] = {}
    
    @classmethod
    def register(cls, name: str, validator: 'BaseConfigValidator') -> None:
        """Registers a validator"""
        cls._validators[name] = validator
        
    @classmethod
    def get_validator(cls, name: str) -> Optional['BaseConfigValidator']:
        """Retrieves a validator by name"""
        return cls._validators.get(name)
        
    @classmethod
    def get_all_validators(cls) -> List['BaseConfigValidator']:
        """Returns all registered validators"""
        return list(cls._validators.values())

class ConfigValidator(Protocol):
    """Protocol for configuration validators"""
    def validate(self, config: 'ConfigModel', context: Optional[Dict] = None) -> ValidationResult: ...

class BaseConfigValidator(ABC, ValidationMixin):
    """Base class for configuration validators"""
    def __init__(self, security_level: SecurityLevel = SecurityLevel.NORMAL):
        self.security_level = security_level
    
    @abstractmethod
    def validate(self, config: 'ConfigModel', context: Optional[Dict] = None) -> ValidationResult:
        """Validates configuration"""
        pass
    
    def _create_result(self, is_valid: bool, errors: List[str]) -> ValidationResult:
        """Creates validation result with proper security level"""
        return ValidationResult(is_valid, errors, self.security_level)

class BaseData(Generic[T], ABC):
    """Base class for data containers with validation.
    
    This class provides a common validation framework that all data classes
    should inherit from. It enforces a consistent validation approach and
    reduces code duplication.
    """
    data: T
    
    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validates data according to specific rules.
        
        Returns:
            ValidationResult containing validation status and errors.
        """
        pass
    
    def __post_init__(self):
        """Validates data after initialization"""
        result = self.validate()
        if not result.is_valid:
            raise ValidationError(f"Validation failed: {', '.join(result.errors)}")
            
    @staticmethod
    def validate_field(value: Any, field_name: str, validators: List[Callable]) -> List[str]:
        """Common field validation framework.
        
        Args:
            value: Field value to validate
            field_name: Name of the field
            validators: List of validator functions
            
        Returns:
            List of validation error messages
        """
        errors = []
        for validator in validators:
            error = validator(value, field_name)
            if error:
                errors.append(error)
        return errors

@dataclass
class AnalysisData(BaseData[Dict]):
    """First iteration - Analysis data with validation"""
    stakeholders: List[str] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    current_state: Dict = field(default_factory=dict)
    gap_analysis: Dict = field(default_factory=dict)
    
    def validate(self) -> ValidationResult:
        """Validates analysis data using common validation framework"""
        errors = []
        errors.extend(self.validate_field(self.stakeholders, "stakeholders", 
                     [self._validate_stakeholders]))
        errors.extend(self.validate_field(self.objectives, "objectives",
                     [self._validate_objectives]))
        return ValidationResult(len(errors) == 0, errors)
        
    @staticmethod
    def _validate_stakeholders(value: List[str], field_name: str) -> Optional[str]:
        if not all(isinstance(s, str) and s.strip() for s in value):
            return f"{field_name} must be non-empty strings"
        return None
        
    @staticmethod
    def _validate_objectives(value: List[str], field_name: str) -> Optional[str]:
        if not all(isinstance(o, str) and len(o) > 10 for o in value):
            return f"{field_name} must be strings with length > 10"
        return None

@dataclass
class ImplementationData(BaseData[Dict]):
    """Second iteration - Implementation data with validation"""
    strategies: Dict[str, str] = field(default_factory=dict)
    implementation_details: Dict = field(default_factory=dict)
    validation_rules: List[Dict] = field(default_factory=list)
    integration_paths: List[str] = field(default_factory=list)

    def validate(self) -> ValidationResult:
        """Validates implementation data"""
        errors = []
        if not isinstance(self.strategies, dict):
            errors.append("strategies must be a dictionary")
        if not isinstance(self.validation_rules, list):
            errors.append("validation_rules must be a list")
        return ValidationResult(len(errors) == 0, errors)

@dataclass
class OptimizationData(BaseData[Dict]):
    """Third iteration - Optimization data with validation"""
    performance_metrics: Dict = field(default_factory=dict)
    optimization_rules: List[Dict] = field(default_factory=list)
    cross_system_dependencies: List[str] = field(default_factory=list)
    future_scenarios: List[Dict] = field(default_factory=list)
    edge_cases: List[Dict] = field(default_factory=list)

    def validate(self) -> ValidationResult:
        """Validates optimization data"""
        errors = []
        if not isinstance(self.performance_metrics, dict):
            errors.append("performance_metrics must be a dictionary")
        if not isinstance(self.optimization_rules, list):
            errors.append("optimization_rules must be a list")
        return ValidationResult(len(errors) == 0, errors)

@dataclass
class ValidationContext:
    """Context for validation operations"""
    user_id: Optional[str] = None
    security_level: SecurityLevel = SecurityLevel.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    extra: Dict[str, Any] = field(default_factory=dict)

    def has_permission(self, required_level: SecurityLevel) -> bool:
        """Checks if context has required security level"""
        return self.security_level.value >= required_level.value

@dataclass
class Metadata:
    """Configuration metadata with security tracking"""
    id: UUID = field(default_factory=uuid4)
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    modified_by: Optional[str] = None
    status: ConfigStatus = field(default=ConfigStatus.DRAFT)
    security_level: SecurityLevel = field(default=SecurityLevel.NORMAL)
    access_control: Dict[str, List[str]] = field(default_factory=dict)

    def update_modification(self, modified_by: str, context: Optional[ValidationContext] = None):
        """Updates modification metadata with validation"""
        if context and not context.has_permission(self.security_level):
            raise AuthorizationError("Insufficient permissions")
            
        if not modified_by or not isinstance(modified_by, str):
            raise ValidationError("Invalid modified_by value")
            
        self.last_modified = datetime.now()
        self.modified_by = ValidationMixin.sanitize_input(modified_by)

    def check_access(self, user_id: str, required_level: str) -> bool:
        """Checks if user has required access level"""
        return user_id in self.access_control and required_level in self.access_control[user_id]

@dataclass
class ConfigModel:
    """Configuration model with enhanced security and validation.
    
    This class implements a comprehensive configuration management system
    with validation, security, and optimization features. It uses dependency
    injection for validators and follows the Strategy pattern for validation.
    
    The @lru_cache decorator is used on the validate method to cache validation
    results for repeated calls with the same context, improving performance
    for frequent validation checks.
    """
    name: str
    description: str
    metadata: Metadata = field(default_factory=Metadata)
    analysis: AnalysisData = field(default_factory=AnalysisData)
    implementation: ImplementationData = field(default_factory=ImplementationData)
    optimization: OptimizationData = field(default_factory=OptimizationData)
    _validator_registry: ValidatorRegistry = field(default_factory=ValidatorRegistry)
    
    def __post_init__(self):
        """Validates model after initialization with enhanced security checks"""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValidationError("name must be a non-empty string")
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValidationError("description must be a non-empty string")
        # Sanitize inputs
        self.name = ValidationMixin.sanitize_input(self.name)
        self.description = ValidationMixin.sanitize_input(self.description)

    @lru_cache(maxsize=128)
    def validate(self, context: Optional[ValidationContext] = None) -> ValidationResult:
        """Validates the configuration model with caching.
        
        The validation results are cached for performance optimization when
        the same configuration is validated multiple times with the same context.
        The cache size is limited to 128 entries to prevent memory issues.
        
        Args:
            context: Optional validation context for security checks
            
        Returns:
            ValidationResult object containing validation status
            
        Raises:
            ValidationError: If validation fails
            AuthorizationError: If user lacks permissions
        """
        if context:
            if not context.user_id:
                raise AuthorizationError("User ID required for validation")
            if not context.has_permission(self.metadata.security_level):
                raise AuthorizationError(
                    f"Insufficient permissions: required {self.metadata.security_level.value}"
                )
            
        validators = self._validator_registry.get_all_validators()
        all_errors = []
        security_level = SecurityLevel.NORMAL
        
        for validator in validators:
            result = validator.validate(self, context)
            if not result.is_valid:
                all_errors.extend(result.errors)
            if result.security_level.value > security_level.value:
                security_level = result.security_level
                
        return ValidationResult(len(all_errors) == 0, all_errors, security_level)

    def update_modification(self, modified_by: str, context: Optional[ValidationContext] = None):
        """Updates modification metadata with access control"""
        self.metadata.update_modification(modified_by, context)

    def to_dict(self) -> Dict:
        """Converts config model to dictionary with security metadata"""
        return {
            "name": self.name,
            "description": self.description,
            "metadata": {
                "id": str(self.metadata.id),
                "version": self.metadata.version,
                "created_at": self.metadata.created_at.isoformat(),
                "last_modified": self.metadata.last_modified.isoformat(),
                "modified_by": self.metadata.modified_by,
                "status": self.metadata.status.value,
                "security_level": self.metadata.security_level.value
            },
            "analysis": {
                "stakeholders": self.analysis.stakeholders,
                "objectives": self.analysis.objectives,
                "current_state": self.analysis.current_state,
                "gap_analysis": self.analysis.gap_analysis
            },
            "implementation": {
                "strategies": self.implementation.strategies,
                "implementation_details": self.implementation.implementation_details,
                "validation_rules": self.implementation.validation_rules,
                "integration_paths": self.implementation.integration_paths
            },
            "optimization": {
                "performance_metrics": self.optimization.performance_metrics,
                "optimization_rules": self.optimization.optimization_rules,
                "cross_system_dependencies": self.optimization.cross_system_dependencies,
                "future_scenarios": self.optimization.future_scenarios,
                "edge_cases": self.optimization.edge_cases
            }
        }
