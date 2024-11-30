"""Configuration models for the template management system.

First Iteration - Analysis & Understanding:
-------------------------------------
Day-in-the-Life Analysis:
* Template developers need consistent configuration
* Deployment teams require environment-specific settings
* Security teams need policy enforcement
* Operations teams manage infrastructure settings

Objectives:
* Centralize configuration management
* Enable environment-specific configurations
* Enforce security policies
* Support infrastructure automation

Gap Analysis:
* No standardized configuration structure
* Manual environment configuration
* Limited security policy enforcement
* Inconsistent deployment settings

Second Iteration - Solution & Implementation:
---------------------------------------
Gap Management:
* Structured configuration models
* Environment-aware settings
* Security policy integration
* Deployment automation support

Problem-Solving Approach:
* Hierarchical configuration
* Environment inheritance
* Policy validation
* Automation hooks

Third Iteration - Enhancement & Optimization:
---------------------------------------
Solution Refinement:
* Performance optimization
* Cross-system integration
* Dependency management
* Resource optimization

Future Scenarios:
* Multi-region deployment
* Dynamic configuration
* Policy evolution
* Infrastructure scaling

Integration Touchpoints:
* Version control systems
* CI/CD pipelines
* Security frameworks
* Monitoring systems
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator, root_validator
import yaml

# First Iteration - Core Settings
# ----------------------------
# Basic configuration structures
class PathConfig(BaseModel):
    """Path configuration settings.
    
    First Iteration:
    * Basic paths
    
    Second Iteration:
    * Path validation
    * Access checks
    
    Third Iteration:
    * Dynamic paths
    * Environment vars
    * Path templates
    """
    template_root: Path = Field(..., description="Root directory for templates")
    deployment_root: Path = Field(..., description="Root directory for deployments")
    backup_root: Optional[Path] = Field(None, description="Root directory for backups")
    
    @validator('*')
    def validate_path(cls, v: Optional[Path]) -> Optional[Path]:
        """Validate path configuration.
        
        First Iteration:
        * Path format
        
        Second Iteration:
        * Permissions
        * Existence
        
        Third Iteration:
        * Environment
        * Templates
        * Variables
        """
        if v is None:
            return v
        return Path(str(v)).resolve()

class SecurityConfig(BaseModel):
    """Security configuration settings.
    
    First Iteration:
    * Basic security
    
    Second Iteration:
    * Access control
    * Encryption
    
    Third Iteration:
    * Compliance
    * Auditing
    * Monitoring
    """
    enable_encryption: bool = Field(False, description="Enable content encryption")
    allowed_classifications: List[str] = Field(
        default=["public", "internal", "confidential", "restricted"],
        description="Allowed classification levels"
    )
    require_auth: bool = Field(True, description="Require authentication")
    
class VersionControlConfig(BaseModel):
    """Version control configuration.
    
    First Iteration:
    * Basic VCS
    
    Second Iteration:
    * Repository
    * Branches
    
    Third Iteration:
    * Workflows
    * Integration
    * Automation
    """
    enabled: bool = Field(False, description="Enable version control")
    provider: str = Field("git", description="Version control provider")
    repository_url: Optional[str] = Field(None, description="Repository URL")
    branch: str = Field("main", description="Default branch")

class HookConfig(BaseModel):
    """Hook system configuration.
    
    First Iteration:
    * Basic hooks
    
    Second Iteration:
    * Hook paths
    * Validation
    
    Third Iteration:
    * Sandboxing
    * Resources
    * Monitoring
    """
    enabled: bool = Field(True, description="Enable hook system")
    hook_path: Optional[Path] = Field(None, description="Path to hook scripts")
    timeout: int = Field(30, description="Hook execution timeout in seconds")
    max_retries: int = Field(3, description="Maximum hook retry attempts")

# Second Iteration - Main Config
# ---------------------------
# Complete configuration model
class ConfigModel(BaseModel):
    """System configuration model.
    
    First Iteration - Analysis & Understanding:
    -------------------------------------
    Day-in-the-Life:
    * Developers need to manage multiple environments
    * Operations teams handle infrastructure changes
    * Security teams enforce compliance
    * Users require consistent deployments
    
    Objectives:
    * Centralize configuration
    * Enable environment management
    * Enforce security policies
    * Support automation
    
    Gaps:
    * No standard configuration
    * Manual environment handling
    * Limited policy enforcement
    * Inconsistent deployments
    
    Second Iteration - Solution & Implementation:
    --------------------------------------
    Gap Management:
    * Structured configuration models
    * Environment inheritance
    * Policy validation
    * Deployment automation
    
    Problem-Solving:
    * Configuration hierarchy
    * Environment mapping
    * Security integration
    * Automation support
    
    Implementation:
    * Model structure
    * Validation rules
    * Integration points
    * Automation hooks
    
    Third Iteration - Enhancement & Optimization:
    --------------------------------------
    Solution Refinement:
    * Performance tuning
    * Resource optimization
    * Integration enhancement
    * Security hardening
    
    Future Scenarios:
    * Multi-region support
    * Dynamic configuration
    * Policy evolution
    * Scale handling
    
    Integration Analysis:
    * VCS integration
    * CI/CD pipeline
    * Security framework
    * Monitoring system
    """
    # First Iteration - Essential Settings
    paths: PathConfig = Field(..., description="Path configuration")
    security: SecurityConfig = Field(
        default_factory=SecurityConfig,
        description="Security settings"
    )
    
    # Second Iteration - Extended Settings
    version_control: VersionControlConfig = Field(
        default_factory=VersionControlConfig,
        description="Version control configuration"
    )
    hooks: HookConfig = Field(
        default_factory=HookConfig,
        description="Hook system configuration"
    )
    
    # Third Iteration - Advanced Settings
    environment: str = Field("production", description="Deployment environment")
    debug: bool = Field(False, description="Enable debug mode")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional configuration metadata"
    )

    # First Iteration - Basic Validation
    @root_validator(pre=True)
    def validate_config(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete configuration.
        
        First Iteration:
        * Basic validation
        
        Second Iteration:
        * Cross-field validation
        * Dependency checks
        
        Third Iteration:
        * Environment checks
        * Resource validation
        * Security audit
        """
        # Validate paths exist
        paths = values.get('paths', {})
        if isinstance(paths, dict):
            for key, path in paths.items():
                if path and not Path(path).parent.exists():
                    raise ValueError(f"Parent directory for {key} does not exist: {path}")
        
        return values

    # Second Iteration - Configuration Loading
    @classmethod
    def from_yaml(cls, path: Path) -> 'ConfigModel':
        """Load configuration from YAML file.
        
        First Iteration:
        * Basic loading
        
        Second Iteration:
        * Validation
        * Defaults
        
        Third Iteration:
        * Environment
        * Inheritance
        * Overrides
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
            
        with open(path) as f:
            config_data = yaml.safe_load(f)
            
        return cls(**config_data)

    # Third Iteration - Advanced Features
    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration.
        
        First Iteration:
        * Basic config
        
        Second Iteration:
        * Environment vars
        * Overrides
        
        Third Iteration:
        * Dynamic config
        * Service discovery
        * Resource limits
        """
        return {
            "environment": self.environment,
            "debug": self.debug,
            "paths": {
                k: str(v) for k, v in self.paths.dict().items() if v is not None
            },
            "security": self.security.dict(),
            "version_control": self.version_control.dict(),
            "hooks": self.hooks.dict(),
            "metadata": self.metadata
        }

    class Config:
        """Model configuration.
        
        First Iteration:
        * Basic settings
        
        Second Iteration:
        * Validation rules
        * Type handling
        
        Third Iteration:
        * Custom settings
        * Performance
        * Integration
        """
        validate_assignment = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
