"""Unit tests for document relationship model."""

import pytest
from datetime import datetime
from uuid import UUID
from src.domain.models.document_model import (
    DocumentRelationshipModel,
    SecurityLevel,
    WorkflowState,
    ValidationError,
    SecurityError,
    RelationshipValidator
)

@pytest.fixture
def valid_document():
    """Creates a valid document for testing."""
    return DocumentRelationshipModel(
        document_id="DOC-001",
        document_type="contract",
        title="Test Document"
    )

def test_document_initialization():
    """Tests basic document initialization."""
    doc = DocumentRelationshipModel(
        document_id="DOC-001",
        document_type="contract",
        title="Test Document"
    )
    assert isinstance(doc.id, UUID)
    assert doc.document_id == "DOC-001"
    assert doc.document_type == "contract"
    assert doc.title == "Test Document"
    assert doc.workflow_state == WorkflowState.DRAFT
    assert doc.security_level == SecurityLevel.INTERNAL

def test_invalid_document_initialization():
    """Tests initialization with invalid data."""
    with pytest.raises(ValidationError):
        DocumentRelationshipModel(
            document_id="",  # Invalid empty ID
            document_type="contract",
            title="Test Document"
        )

def test_input_sanitization():
    """Tests input sanitization."""
    doc = DocumentRelationshipModel(
        document_id="DOC-001<script>",
        document_type="contract';--",
        title="Test Document&lt;"
    )
    assert "<script>" not in doc.document_id
    assert "';--" not in doc.document_type
    assert "&lt;" not in doc.title

def test_add_relationship(valid_document):
    """Tests relationship addition."""
    valid_document.add_relationship("DOC-002", "references")
    assert "references" in valid_document.relationships
    assert "DOC-002" in valid_document.relationships["references"]

def test_add_invalid_relationship(valid_document):
    """Tests adding invalid relationship."""
    with pytest.raises(ValidationError):
        valid_document.add_relationship("", "references")

def test_update_workflow_state(valid_document):
    """Tests workflow state updates."""
    valid_document.update_workflow_state(WorkflowState.IN_REVIEW, "user123")
    assert valid_document.workflow_state == WorkflowState.IN_REVIEW
    assert valid_document.modified_by == "user123"

def test_invalid_workflow_state(valid_document):
    """Tests invalid workflow state update."""
    with pytest.raises(ValidationError):
        valid_document.update_workflow_state("invalid_state", "user123")

def test_access_control(valid_document):
    """Tests access control functionality."""
    valid_document.stakeholder_access = {
        SecurityLevel.INTERNAL.value: ["user123"]
    }
    assert valid_document.check_access("user123", SecurityLevel.INTERNAL)
    assert not valid_document.check_access("user456", SecurityLevel.INTERNAL)
    assert not valid_document.check_access("user123", SecurityLevel.RESTRICTED)

def test_relationship_validation(valid_document):
    """Tests relationship validation."""
    valid_document.add_relationship("DOC-002", "references")
    assert valid_document.validate_relationships()

    # Test with invalid relationship
    valid_document.relationships["invalid"] = [None]  # type: ignore
    assert not valid_document.validate_relationships()

def test_to_dict(valid_document):
    """Tests dictionary conversion."""
    data = valid_document.to_dict()
    assert isinstance(data["id"], str)
    assert data["document_id"] == "DOC-001"
    assert data["workflow_state"] == WorkflowState.DRAFT.value
    assert data["security_level"] == SecurityLevel.INTERNAL.value

def test_relationship_validator():
    """Tests the relationship validator."""
    validator = RelationshipValidator()
    doc = DocumentRelationshipModel(
        document_id="DOC-001",
        document_type="contract",
        title="Test Document"
    )
    assert validator.validate(doc)

    # Test with invalid document
    invalid_doc = DocumentRelationshipModel(
        document_id="",  # Invalid
        document_type="contract",
        title="Test Document"
    )
    assert not validator.validate(invalid_doc)

def test_security_levels():
    """Tests security level comparisons."""
    assert SecurityLevel.PUBLIC.value < SecurityLevel.RESTRICTED.value
    assert SecurityLevel.INTERNAL.value < SecurityLevel.CONFIDENTIAL.value
    assert SecurityLevel.CONFIDENTIAL.value < SecurityLevel.RESTRICTED.value
