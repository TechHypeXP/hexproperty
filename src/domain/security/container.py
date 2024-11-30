"""Container security implementation for HexProperty."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
import json
import re
from .audit_log import audit_logger, AuditEventType, AuditEventSeverity
from .policy import Permission, ResourceType, policy_enforcer

class SecurityLevel(str, Enum):
    """Container security levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ContainerStatus(str, Enum):
    """Container security status."""
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    VULNERABLE = "vulnerable"

@dataclass
class SecurityScan:
    """Container security scan results."""
    vulnerabilities: List[Dict] = field(default_factory=list)
    policy_violations: List[Dict] = field(default_factory=list)
    security_score: float = 0.0
    scan_timestamp: str = ""
    scan_status: str = ""

@dataclass
class ContainerPolicy:
    """Container security policy."""
    allowed_registries: Set[str] = field(default_factory=set)
    required_labels: Set[str] = field(default_factory=set)
    blocked_packages: Set[str] = field(default_factory=set)
    min_security_score: float = 0.0
    security_level: SecurityLevel = SecurityLevel.MEDIUM

class ContainerSecurity:
    """Container security management."""
    
    def __init__(self):
        self._policies: Dict[str, ContainerPolicy] = {}
        self._scan_results: Dict[str, SecurityScan] = {}
        
    async def scan_container(self, image_name: str, context: Optional[Dict] = None) -> SecurityScan:
        """Scan a container image for security issues."""
        # Ensure permission
        if not policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            image_name,
            context
        ):
            raise PermissionError(f"No permission to scan {image_name}")
        
        try:
            # Perform security scan
            scan_result = await self._perform_security_scan(image_name)
            
            # Store scan results
            self._scan_results[image_name] = scan_result
            
            # Log scan completion
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.INFO,
                action="container_scan",
                status="completed",
                details={
                    "image": image_name,
                    "score": scan_result.security_score,
                    "vulnerabilities": len(scan_result.vulnerabilities)
                }
            )
            
            return scan_result
            
        except Exception as e:
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.ERROR,
                action="container_scan",
                status="failed",
                details={
                    "image": image_name,
                    "error": str(e)
                }
            )
            raise
    
    async def validate_container(
        self,
        image_name: str,
        policy_name: str,
        context: Optional[Dict] = None
    ) -> ContainerStatus:
        """Validate a container against security policy."""
        if not policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            image_name,
            context
        ):
            raise PermissionError(f"No permission to validate {image_name}")
        
        try:
            policy = self._policies.get(policy_name)
            if not policy:
                raise ValueError(f"Policy {policy_name} not found")
            
            # Get or perform scan
            scan_result = self._scan_results.get(image_name)
            if not scan_result:
                scan_result = await self.scan_container(image_name, context)
            
            # Validate against policy
            status = await self._validate_against_policy(image_name, scan_result, policy)
            
            # Log validation result
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.INFO,
                action="container_validation",
                status=status,
                details={
                    "image": image_name,
                    "policy": policy_name,
                    "score": scan_result.security_score
                }
            )
            
            return status
            
        except Exception as e:
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.ERROR,
                action="container_validation",
                status="failed",
                details={
                    "image": image_name,
                    "policy": policy_name,
                    "error": str(e)
                }
            )
            raise
    
    async def _perform_security_scan(self, image_name: str) -> SecurityScan:
        """Perform security scan on container image."""
        # TODO: Implement actual container scanning
        # This would integrate with tools like Trivy, Clair, or Anchore
        return SecurityScan(
            vulnerabilities=[],
            policy_violations=[],
            security_score=0.0,
            scan_timestamp="",
            scan_status="pending"
        )
    
    async def _validate_against_policy(
        self,
        image_name: str,
        scan_result: SecurityScan,
        policy: ContainerPolicy
    ) -> ContainerStatus:
        """Validate scan results against policy."""
        # Check security score
        if scan_result.security_score < policy.min_security_score:
            return ContainerStatus.REJECTED
        
        # Check for critical vulnerabilities
        if any(v.get("severity") == "CRITICAL" for v in scan_result.vulnerabilities):
            return ContainerStatus.VULNERABLE
        
        # Check registry
        registry = image_name.split("/")[0]
        if registry not in policy.allowed_registries:
            return ContainerStatus.REJECTED
        
        # All checks passed
        return ContainerStatus.APPROVED
    
    def add_policy(self, name: str, policy: ContainerPolicy) -> None:
        """Add or update a container security policy."""
        self._policies[name] = policy
        audit_logger.log_event(
            event_type=AuditEventType.SECURITY,
            severity=AuditEventSeverity.INFO,
            action="container_policy_update",
            status="success",
            details={"policy_name": name}
        )
    
    def remove_policy(self, name: str) -> None:
        """Remove a container security policy."""
        if name in self._policies:
            del self._policies[name]
            audit_logger.log_event(
                event_type=AuditEventType.SECURITY,
                severity=AuditEventSeverity.WARNING,
                action="container_policy_remove",
                status="success",
                details={"policy_name": name}
            )

# Global container security instance
container_security = ContainerSecurity()
