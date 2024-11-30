"""Tests for audit logging functionality."""

import json
import os
import pytest
from datetime import datetime
from uuid import UUID
from src.domain.security.audit_log import (
    AuditLogger,
    AuditEvent,
    AuditEventType,
    AuditEventSeverity,
    FileAuditLogHandler,
    setup_file_logging,
    log_security_event,
    log_deployment_event
)

@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file."""
    return str(tmp_path / "test_audit.log")

@pytest.fixture
def audit_logger(temp_log_file):
    """Create an audit logger with file handler."""
    logger = AuditLogger()
    handler = FileAuditLogHandler(temp_log_file)
    logger.add_handler(handler)
    return logger

def test_audit_event_creation():
    """Test creating an audit event."""
    event = AuditEvent(
        event_type=AuditEventType.SECURITY,
        severity=AuditEventSeverity.INFO,
        action="test_action",
        status="success"
    )
    
    # Verify event fields using f-strings
    assert f"{event.event_type}" == "security", "Event type should be security"
    assert f"{event.severity}" == "info", "Severity should be info"
    assert event.action == "test_action", "Action should match"
    assert event.status == "success", "Status should match"
    assert event.event_id, "Event ID should be generated"

def test_audit_event_serialization():
    """Test audit event serialization."""
    event = AuditEvent(
        event_type=AuditEventType.SECURITY,
        severity=AuditEventSeverity.INFO,
        action="test_action",
        status="success",
        details={"key": "value"}
    )
    
    event_dict = event.to_dict()
    assert event_dict["event_type"] == AuditEventType.SECURITY
    assert event_dict["severity"] == AuditEventSeverity.INFO
    assert event_dict["action"] == "test_action"
    assert event_dict["details"] == {"key": "value"}

def test_file_logging(audit_logger, temp_log_file):
    """Test logging to file."""
    # Create and log test event
    event = AuditEvent(
        event_type=AuditEventType.SECURITY,
        severity=AuditEventSeverity.INFO,
        action="test_action",
        status="success"
    )
    audit_logger.log_event(event)
    
    # Verify log file content
    assert os.path.exists(temp_log_file), "Log file should exist"
    with open(temp_log_file, 'r') as f:
        log_entry = json.loads(f.readline().strip())
        assert log_entry["event_type"] == AuditEventType.SECURITY.value
        assert log_entry["severity"] == AuditEventSeverity.INFO.value
        assert log_entry["action"] == "test_action"

def test_multiple_handlers(temp_log_file):
    """Test using multiple handlers."""
    # Create logger with two handlers
    logger = AuditLogger()
    handler1 = FileAuditLogHandler(temp_log_file + "1")
    handler2 = FileAuditLogHandler(temp_log_file + "2")
    logger.add_handler(handler1)
    logger.add_handler(handler2)
    
    # Log test event
    logger.log_event(
        event_type=AuditEventType.SECURITY,
        severity=AuditEventSeverity.INFO,
        action="test_action",
        status="success"
    )
    
    # Verify both log files
    for suffix, filename in [("1", temp_log_file + "1"), ("2", temp_log_file + "2")]:
        assert os.path.exists(filename), f"Log file {suffix} should exist"
        with open(filename, 'r') as f:
            log_entry = json.loads(f.readline().strip())
            assert log_entry["event_type"] == AuditEventType.SECURITY.value
            assert log_entry["severity"] == AuditEventSeverity.INFO.value
            assert log_entry["action"] == "test_action"

def test_convenience_functions(audit_logger, temp_log_file):
    """Test convenience logging functions."""
    # Test security event logging
    log_security_event(
        action="test_security",
        status="success",
        user_id="test_user"
    )
    
    # Test deployment event logging
    log_deployment_event(
        action="test_deployment",
        status="success",
        resource_id="test_resource"
    )
    
    # Verify logs
    with open(temp_log_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2
        
        security_log = json.loads(lines[0])
        assert security_log["event_type"] == AuditEventType.SECURITY
        assert security_log["action"] == "test_security"
        
        deployment_log = json.loads(lines[1])
        assert deployment_log["event_type"] == AuditEventType.DEPLOYMENT
        assert deployment_log["action"] == "test_deployment"

def test_error_handling(audit_logger, temp_log_file):
    """Test error handling in audit logging."""
    # Make log file read-only
    os.chmod(temp_log_file, 0o444)
    
    try:
        # This should not raise an exception, but log an error
        audit_logger.log_event(
            event_type=AuditEventType.SECURITY,
            severity=AuditEventSeverity.INFO,
            action="test_action",
            status="success"
        )
    finally:
        # Restore permissions for cleanup
        os.chmod(temp_log_file, 0o666)
