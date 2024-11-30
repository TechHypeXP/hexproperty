"""Audit logging implementation for security events."""

import json
import logging
import os
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict
from uuid import UUID, uuid4
import threading
from abc import ABC, abstractmethod
from pathlib import Path
import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditEventType(str, Enum):
    """Types of audit events."""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DEPLOYMENT = "deployment"
    CONFIGURATION = "configuration"
    SECURITY = "security"
    SYSTEM = "system"

class AuditEventSeverity(str, Enum):
    """Severity levels for audit events."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class SecurityError(Exception):
    """Security-related exception."""
    pass

class SecurityConfig:
    """Security configuration with safe defaults."""
    MIN_UID = 1000  # Minimum safe UID for non-root users
    DEFAULT_UID = 1000  # Default non-root UID
    READ_ONLY_FS = True  # Enable read-only root filesystem
    SECURE_PATHS = {
        'logs': '/var/log/hexproperty',
        'data': '/var/lib/hexproperty',
        'config': '/etc/hexproperty'
    }

def sanitize_path(path: str) -> str:
    """Sanitize and validate file paths to prevent path traversal."""
    import os
    from pathlib import Path
    
    # Normalize path and resolve symlinks
    safe_path = os.path.normpath(os.path.abspath(path))
    real_path = os.path.realpath(safe_path)
    
    # Validate against allowed paths
    allowed_paths = [Path(p).resolve() for p in SecurityConfig.SECURE_PATHS.values()]
    if not any(str(real_path).startswith(str(p)) for p in allowed_paths):
        raise SecurityError(f"Path {path} is outside allowed directories")
        
    return real_path

@dataclass
class AuditEvent:
    """Represents a security audit event."""
    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    event_type: AuditEventType = AuditEventType.SECURITY
    severity: AuditEventSeverity = AuditEventSeverity.INFO
    user_id: Optional[str] = None
    resource_id: Optional[str] = None
    action: str = ""
    status: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    source_ip: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        data = asdict(self)
        data['event_id'] = str(data['event_id'])
        data['timestamp'] = data['timestamp'].isoformat()
        return data

class AuditLogHandler(ABC):
    """Abstract base class for audit log handlers."""
    
    @abstractmethod
    def log_event(self, event: AuditEvent) -> None:
        """Log an audit event."""
        pass

class FileAuditLogHandler(AuditLogHandler):
    """Enhanced file audit log handler with security measures."""
    
    def __init__(self, filename: str):
        """Initialize with security checks."""
        self.filename = sanitize_path(filename)
        self._lock = threading.Lock()
        
        # Ensure proper file permissions
        if os.path.exists(self.filename):
            os.chmod(self.filename, 0o640)  # rw-r----- permissions
            
        # Ensure directory permissions
        os.makedirs(os.path.dirname(self.filename), mode=0o750, exist_ok=True)
    
    def log_event(self, event: AuditEvent) -> None:
        """Log event with enhanced security measures."""
        with self._lock:
            try:
                # Sanitize and validate all string inputs
                sanitized_event = self._sanitize_event(event)
                
                # Convert to JSON with proper escaping
                json_data = json.dumps(
                    sanitized_event.to_dict(),
                    default=str,
                    ensure_ascii=True
                )
                
                # Secure file writing with explicit utf8 encoding
                with open(self.filename, 'a', encoding='utf8') as f:
                    os.fchmod(f.fileno(), 0o640)  # Ensure file permissions
                    f.write(json_data + '\n')
                    f.flush()
                    os.fsync(f.fileno())  # Ensure data is written
                    
            except IOError as io_err:
                raise SecurityError("Failed to write to audit log") from io_err
            except json.JSONDecodeError as json_err:
                raise SecurityError("Failed to encode audit event") from json_err
            except Exception as e:
                raise SecurityError(f"Unexpected error in audit logging: {str(e)}") from e
    
    @staticmethod
    def _sanitize_event(event: AuditEvent) -> AuditEvent:
        """Sanitize event data to prevent XSS and injection."""
        try:
            def sanitize_value(value: Any) -> Any:
                if isinstance(value, str):
                    # Escape HTML and potentially dangerous characters
                    return html.escape(
                        re.sub(r'[<>&\'";()]', '', value)
                    )
                elif isinstance(value, dict):
                    return {k: sanitize_value(v) for k, v in value.items()}
                elif isinstance(value, (list, tuple)):
                    return [sanitize_value(v) for v in value]
                return value
            
            # Create a new event with sanitized values
            event_dict = event.to_dict()
            sanitized_dict = {
                k: sanitize_value(v) for k, v in event_dict.items()
            }
            
            return AuditEvent(**sanitized_dict)
            
        except Exception as e:
            raise SecurityError("Failed to sanitize audit event") from e

class DatabaseAuditLogHandler(AuditLogHandler):
    """Handles audit logging to database."""
    
    def __init__(self, db_connection: Any):
        self.db = db_connection
        self._lock = threading.Lock()
    
    def log_event(self, event: AuditEvent) -> None:
        """Log event to database."""
        # TODO: Implement database logging
        pass

class AuditLogger:
    """Main audit logging facility."""
    
    def __init__(self):
        self._handlers: list[AuditLogHandler] = []
        self._lock = threading.Lock()
    
    def add_handler(self, handler: AuditLogHandler) -> None:
        """Add a new audit log handler."""
        with self._lock:
            self._handlers.append(handler)
    
    def log_event(self, 
                  event_type: AuditEventType,
                  severity: AuditEventSeverity,
                  action: str,
                  status: str,
                  user_id: Optional[str] = None,
                  resource_id: Optional[str] = None,
                  details: Optional[Dict[str, Any]] = None,
                  source_ip: Optional[str] = None,
                  metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log an audit event to all handlers.
        
        Args:
            event_type: Type of the audit event
            severity: Severity level of the event
            action: Action being performed
            status: Status of the action
            user_id: Optional ID of the user performing the action
            resource_id: Optional ID of the resource being acted upon
            details: Optional detailed information about the event
            source_ip: Optional source IP address
            metadata: Optional additional metadata
        """
        event = AuditEvent(
            event_type=event_type,
            severity=severity,
            action=action,
            status=status,
            user_id=user_id,
            resource_id=resource_id,
            details=details or {},
            source_ip=source_ip,
            metadata=metadata or {}
        )
        
        for handler in self._handlers:
            try:
                handler.log_event(event)
            except Exception as e:
                logger.error(f"Failed to log audit event: {e}")

# Global audit logger instance
audit_logger = AuditLogger()

def setup_file_logging(filename: str = "audit.log") -> None:
    """Set up file-based audit logging."""
    handler = FileAuditLogHandler(filename)
    audit_logger.add_handler(handler)

def log_security_event(action: str,
                      status: str,
                      severity: AuditEventSeverity = AuditEventSeverity.INFO,
                      **kwargs) -> None:
    """Convenience function for logging security events."""
    audit_logger.log_event(
        event_type=AuditEventType.SECURITY,
        severity=severity,
        action=action,
        status=status,
        **kwargs
    )

def log_deployment_event(action: str,
                        status: str,
                        severity: AuditEventSeverity = AuditEventSeverity.INFO,
                        **kwargs) -> None:
    """Convenience function for logging deployment events."""
    audit_logger.log_event(
        event_type=AuditEventType.DEPLOYMENT,
        severity=severity,
        action=action,
        status=status,
        **kwargs
    )
