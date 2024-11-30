"""Unit tests for deployment model."""

import pytest
from datetime import datetime
from uuid import UUID
from src.domain.models.deployment_model import (
    DeploymentRecord,
    DeploymentStatus,
    DeploymentType,
    SecurityLevel,
    ValidationError,
    SecurityError,
    DeploymentMetadata,
    StatusTransitionValidator
)

@pytest.fixture
def valid_deployment():
    """Creates a valid deployment for testing."""
    return DeploymentRecord(
        deployment_id="DEP-001",
        deployment_type=DeploymentType.TEMPLATE,
        deployment_strategy="blue-green",
        stakeholders=["user1", "user2"],
        objectives=["Improve performance"]
    )

def test_deployment_initialization():
    """Tests basic deployment initialization."""
    deployment = DeploymentRecord(
        deployment_id="DEP-001",
        deployment_type=DeploymentType.TEMPLATE,
        deployment_strategy="blue-green"
    )
    assert isinstance(deployment.metadata.id, UUID)
    assert deployment.deployment_id == "DEP-001"
    assert deployment.deployment_type == DeploymentType.TEMPLATE
    assert deployment.deployment_strategy == "blue-green"
    assert deployment.status == DeploymentStatus.PENDING
    assert deployment.metadata.security_level == SecurityLevel.READ_ONLY

def test_invalid_deployment_initialization():
    """Tests initialization with invalid data."""
    with pytest.raises(ValidationError):
        DeploymentRecord(
            deployment_id="",  # Invalid empty ID
            deployment_type=DeploymentType.TEMPLATE,
            deployment_strategy="blue-green"
        )

def test_input_sanitization():
    """Tests input sanitization."""
    deployment = DeploymentRecord(
        deployment_id="DEP-001<script>",
        deployment_type=DeploymentType.TEMPLATE,
        deployment_strategy="blue-green';--"
    )
    assert "<script>" not in deployment.deployment_id
    assert "';--" not in deployment.deployment_strategy

def test_status_transition(valid_deployment):
    """Tests status transitions."""
    valid_deployment.update_status(
        DeploymentStatus.IN_PROGRESS,
        "user123",
        SecurityLevel.EXECUTE
    )
    assert valid_deployment.status == DeploymentStatus.IN_PROGRESS
    assert valid_deployment.metadata.modified_by == "user123"

def test_invalid_status_transition(valid_deployment):
    """Tests invalid status transition."""
    with pytest.raises(ValidationError):
        valid_deployment.update_status(
            DeploymentStatus.ROLLED_BACK,
            "user123",
            SecurityLevel.EXECUTE
        )

def test_insufficient_permissions(valid_deployment):
    """Tests status update with insufficient permissions."""
    with pytest.raises(SecurityError):
        valid_deployment.update_status(
            DeploymentStatus.IN_PROGRESS,
            "user123",
            SecurityLevel.READ_ONLY
        )

def test_metadata_validation():
    """Tests metadata validation."""
    metadata = DeploymentMetadata(version="1.0.0")
    assert metadata.version == "1.0.0"
    
    with pytest.raises(ValueError):
        DeploymentMetadata(version="invalid")

def test_status_validator():
    """Tests status transition validator."""
    validator = StatusTransitionValidator()
    deployment = DeploymentRecord(
        deployment_id="DEP-001",
        deployment_type=DeploymentType.TEMPLATE,
        deployment_strategy="blue-green"
    )
    assert validator.validate(deployment)  # PENDING to IN_PROGRESS is valid
    deployment.status = DeploymentStatus.COMPLETED
    assert not validator.validate(deployment)  # COMPLETED to IN_PROGRESS is invalid

def test_system_deployment_security():
    """Tests system deployment security requirements."""
    deployment = DeploymentRecord(
        deployment_id="DEP-001",
        deployment_type=DeploymentType.SYSTEM,
        deployment_strategy="blue-green"
    )
    assert not deployment.validate_deployment()  # Should fail due to security level

def test_completed_deployment_validation(valid_deployment):
    """Tests validation of completed deployment."""
    valid_deployment.status = DeploymentStatus.COMPLETED
    assert not valid_deployment.validate_deployment()  # Missing metrics
    
    valid_deployment.performance_metrics = {"latency": 100}
    valid_deployment.validation_results = {"tests": True}
    assert valid_deployment.validate_deployment()

def test_access_control(valid_deployment):
    """Tests access control functionality."""
    assert valid_deployment.check_access("user123", SecurityLevel.READ_ONLY)
    assert not valid_deployment.check_access("user123", SecurityLevel.ADMIN)
    assert not valid_deployment.check_access("", SecurityLevel.READ_ONLY)

def test_to_dict(valid_deployment):
    """Tests dictionary conversion."""
    data = valid_deployment.to_dict()
    assert isinstance(data["id"], str)
    assert data["deployment_id"] == "DEP-001"
    assert data["deployment_type"] == DeploymentType.TEMPLATE.value
    assert data["status"] == DeploymentStatus.PENDING.value
    assert isinstance(data["created_at"], str)
    assert isinstance(data["last_modified"], str)

def test_error_handling(valid_deployment):
    """Tests error handling and recording."""
    valid_deployment.add_error("test", "Test error message")
    assert len(valid_deployment.metadata.errors) == 1
    error = valid_deployment.metadata.errors[0]
    assert error["type"] == "test"
    assert error["message"] == "Test error message"
    assert "timestamp" in error
