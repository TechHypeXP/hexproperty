import pytest
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.models.config_model import ConfigModel
from services.template_service import TemplateService

@pytest.fixture
def template_dir(tmp_path):
    """Creates a temporary directory for template tests"""
    return tmp_path / "templates"

@pytest.fixture
def template_service(template_dir):
    """Creates a template service instance"""
    template_dir.mkdir(exist_ok=True)
    return TemplateService(str(template_dir))

@pytest.fixture
def sample_config():
    """Creates a sample configuration"""
    return ConfigModel(
        name="test_template",
        description="Test template description",
        stakeholders=["dev", "qa"],
        objectives=["test", "validate"],
        strategies={"deployment": "blue-green"},
        implementation_details={"steps": ["plan", "execute"]},
        validation_rules=[{"rule": "test_coverage", "threshold": 80}]
    )

@pytest.mark.asyncio
async def test_analyze_template(template_service, template_dir):
    """Tests template analysis functionality"""
    # Create test template
    template_data = {
        "name": "test",
        "description": "Test template",
        "access": {"dev": "write", "qa": "read"},
        "workflows": [
            {"name": "test", "participants": ["dev", "qa"]}
        ],
        "objectives": ["test", "validate"],
        "validation": {"rules": ["coverage"]}
    }
    
    template_path = template_dir / "test.json"
    template_path.parent.mkdir(exist_ok=True)
    with open(template_path, 'w') as f:
        json.dump(template_data, f)
        
    analysis = await template_service.analyze_template("test")
    
    assert "stakeholders" in analysis
    assert "objectives" in analysis
    assert "gaps" in analysis
    assert "current_state" in analysis
    assert "dev" in analysis["stakeholders"]
    assert "qa" in analysis["stakeholders"]

@pytest.mark.asyncio
async def test_create_template(template_service, sample_config):
    """Tests template creation functionality"""
    template_path = await template_service.create_template(sample_config)
    
    assert Path(template_path).exists()
    
    with open(template_path, 'r') as f:
        template_data = json.load(f)
        
    assert template_data["name"] == sample_config.name
    assert template_data["description"] == sample_config.description
    assert "strategies" in template_data
    assert "implementation" in template_data
    assert "validation" in template_data

@pytest.mark.asyncio
async def test_validate_template(template_service, template_dir):
    """Tests template validation functionality"""
    # Valid template
    valid_template = {
        "name": "valid",
        "description": "Valid template",
        "created_at": datetime.now().isoformat(),
        "strategies": {}
    }
    
    valid_path = template_dir / "valid.json"
    with open(valid_path, 'w') as f:
        json.dump(valid_template, f)
        
    assert await template_service.validate_template("valid") is True
    
    # Invalid template
    invalid_template = {
        "description": "Invalid template",
        "strategies": "invalid"  # Should be dict
    }
    
    invalid_path = template_dir / "invalid.json"
    with open(invalid_path, 'w') as f:
        json.dump(invalid_template, f)
        
    assert await template_service.validate_template("invalid") is False

@pytest.mark.asyncio
async def test_optimize_template(template_service, template_dir):
    """Tests template optimization functionality"""
    template_data = {
        "name": "test",
        "description": "Test template",
        "validation_rules": [
            {"rule": "coverage", "edge_case": {"scenario": "low_coverage"}}
        ]
    }
    
    template_path = template_dir / "test.json"
    with open(template_path, 'w') as f:
        json.dump(template_data, f)
        
    optimized = await template_service.optimize_template("test")
    
    assert "performance_metrics" in optimized
    assert "cross_system_interactions" in optimized
    assert "edge_cases" in optimized
    assert len(optimized["edge_cases"]) > 0

@pytest.mark.asyncio
async def test_template_not_found(template_service):
    """Tests error handling for non-existent templates"""
    with pytest.raises(FileNotFoundError):
        await template_service.analyze_template("nonexistent")

@pytest.mark.asyncio
async def test_template_metrics(template_service, template_dir):
    """Tests template metrics calculation"""
    template_data = {
        "name": "test",
        "description": "Test template",
        "validation_rules": [{"rule": "test"}],
        "integrations": [
            {"system": "test", "dependencies": ["dep1", "dep2"]}
        ]
    }
    
    template_path = template_dir / "test.json"
    with open(template_path, 'w') as f:
        json.dump(template_data, f)
        
    optimized = await template_service.optimize_template("test")
    metrics = optimized["performance_metrics"]
    
    assert "complexity_score" in metrics
    assert "field_count" in metrics
    assert "validation_coverage" in metrics
    assert 0 <= metrics["validation_coverage"] <= 1.0
