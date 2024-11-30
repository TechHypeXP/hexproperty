"""Security policy implementation for HexProperty."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
import re
from .audit_log import audit_logger, AuditEventType, AuditEventSeverity

class Permission(str, Enum):
    """Available permissions in the system."""
    DEPLOY = "deploy"
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    AUDIT = "audit"

class ResourceType(str, Enum):
    """Types of resources that can be protected."""
    DEPLOYMENT = "deployment"
    CONFIGURATION = "configuration"
    SECRET = "secret"
    POLICY = "policy"
    SYSTEM = "system"

@dataclass
class PolicyRule:
    """Individual policy rule."""
    permissions: Set[Permission]
    resource_types: Set[ResourceType]
    resource_patterns: List[str] = field(default_factory=list)
    conditions: Dict[str, str] = field(default_factory=dict)

@dataclass
class SecurityPolicy:
    """Security policy definition."""
    name: str
    rules: List[PolicyRule]
    priority: int = 0
    description: Optional[str] = None

class PolicyEnforcer:
    """Enforces security policies."""
    
    def __init__(self):
        self._policies: Dict[str, SecurityPolicy] = {}
        
    def add_policy(self, policy: SecurityPolicy) -> None:
        """Add a security policy."""
        if policy.name in self._policies:
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.WARNING,
                action="policy_update",
                status="success",
                details={"policy_name": policy.name}
            )
        self._policies[policy.name] = policy
        
    def remove_policy(self, policy_name: str) -> None:
        """Remove a security policy."""
        if policy_name in self._policies:
            del self._policies[policy_name]
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.WARNING,
                action="policy_remove",
                status="success",
                details={"policy_name": policy_name}
            )
    
    def check_permission(
        self,
        permission: Permission,
        resource_type: ResourceType,
        resource_name: str,
        context: Optional[Dict] = None
    ) -> bool:
        """Check if an operation is allowed by policy."""
        context = context or {}
        
        # Sort policies by priority
        sorted_policies = sorted(
            self._policies.values(),
            key=lambda p: p.priority,
            reverse=True
        )
        
        for policy in sorted_policies:
            for rule in policy.rules:
                if (permission in rule.permissions and
                    resource_type in rule.resource_types and
                    self._matches_resource_patterns(resource_name, rule.resource_patterns) and
                    self._check_conditions(context, rule.conditions)):
                    
                    audit_logger.log_event(
                        event_type=AuditEventType.SECURITY,
                        severity=AuditEventSeverity.INFO,
                        action="permission_check",
                        status="allowed",
                        details={
                            "permission": permission,
                            "resource_type": resource_type,
                            "resource_name": resource_name,
                            "policy_name": policy.name
                        }
                    )
                    return True
        
        # If no policy allows it, deny by default
        audit_logger.log_event(
            event_type=AuditEventType.SECURITY,
            severity=AuditEventSeverity.WARNING,
            action="permission_check",
            status="denied",
            details={
                "permission": permission,
                "resource_type": resource_type,
                "resource_name": resource_name
            }
        )
        return False
    
    def _matches_resource_patterns(self, resource_name: str, patterns: List[str]) -> bool:
        """Check if resource name matches any of the patterns."""
        if not patterns:  # Empty patterns list means match all
            return True
        return any(re.match(pattern, resource_name) for pattern in patterns)
    
    def _check_conditions(self, context: Dict, conditions: Dict[str, str]) -> bool:
        """Check if context matches all conditions."""
        for key, pattern in conditions.items():
            value = str(context.get(key, ""))
            if not re.match(pattern, value):
                return False
        return True

# Global policy enforcer instance
policy_enforcer = PolicyEnforcer()

def require_permission(
    permission: Permission,
    resource_type: ResourceType,
    resource_name_func=None
):
    """Decorator to enforce permissions on functions."""
    def decorator(func):
        from functools import wraps
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            resource_name = (
                resource_name_func(*args, **kwargs)
                if resource_name_func
                else "default"
            )
            
            if not policy_enforcer.check_permission(
                permission,
                resource_type,
                resource_name,
                kwargs.get("context", {})
            ):
                raise PermissionError(
                    f"Permission denied: {permission} on {resource_type}/{resource_name}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
