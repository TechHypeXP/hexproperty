import pytest
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.models.deployment_model import DeploymentRecord
from services.deployment_history_service import DeploymentHistoryService

@pytest.fixture
def history_dir(tmp_path):
    """Creates a temporary directory for deployment history tests"""
    return tmp_path / "deployments"

@pytest.fixture
def deployment_service(history_dir):
    """Creates a deployment history service instance"""
    history_dir.mkdir(exist_ok=True)
    return DeploymentHistoryService(str(history_dir))

@pytest.fixture
def sample_deployment():
    """Creates a sample deployment record"""
    return DeploymentRecord(
        deployment_id="test-deploy-001",
        deployment_type="test",
        stakeholders=["dev", "ops"],
        objectives=["test deployment"],
        deployment_strategy="blue-green",
        implementation_steps=[{"step": "deploy", "status": "completed"}]
    )

@pytest.mark.asyncio
async def test_analyze_deployment_history(deployment_service, history_dir):
    """Tests deployment history analysis functionality"""
    # Create test deployment records
    deployments = [
        {
            "id": "deploy1",
            "type": "test",
            "status": "completed",
            "stakeholders": ["dev"],
            "errors": []
        },
        {
            "id": "deploy2",
            "type": "prod",
            "status": "failed",
            "stakeholders": ["ops"],
            "errors": [{"type": "connection", "message": "timeout"}]
        }
    ]
    
    for dep in deployments:
        path = history_dir / f"{dep['id']}.json"
        with open(path, 'w') as f:
            json.dump(dep, f)
            
    analysis = await deployment_service.analyze_deployment_history()
    
    assert analysis["total_deployments"] == 2
    assert 0 <= analysis["success_rate"] <= 1
    assert "common_errors" in analysis
    assert "stakeholder_impact" in analysis

@pytest.mark.asyncio
async def test_record_deployment(deployment_service, sample_deployment):
    """Tests deployment recording functionality"""
    deployment_path = await deployment_service.record_deployment(sample_deployment)
    
    assert Path(deployment_path).exists()
    
    with open(deployment_path, 'r') as f:
        deployment_data = json.load(f)
        
    assert deployment_data["id"] == sample_deployment.deployment_id
    assert deployment_data["type"] == sample_deployment.deployment_type
    assert deployment_data["status"] == sample_deployment.status
    assert len(deployment_data["stakeholders"]) == len(sample_deployment.stakeholders)

@pytest.mark.asyncio
async def test_update_deployment_status(deployment_service, sample_deployment):
    """Tests deployment status update functionality"""
    # First record the deployment
    deployment_path = await deployment_service.record_deployment(sample_deployment)
    
    # Then update its status
    result = await deployment_service.update_deployment_status(
        sample_deployment.deployment_id,
        "completed",
        "test_user"
    )
    
    assert result is True
    
    with open(deployment_path, 'r') as f:
        deployment_data = json.load(f)
        assert deployment_data["status"] == "completed"
        assert "last_modified" in deployment_data
        assert deployment_data["modified_by"] == "test_user"

@pytest.mark.asyncio
async def test_generate_deployment_metrics(deployment_service, history_dir):
    """Tests deployment metrics generation functionality"""
    # Create test deployment records with various states
    deployments = [
        {
            "id": "deploy1",
            "type": "test",
            "status": "completed",
            "created_at": "2023-01-01T00:00:00",
            "errors": []
        },
        {
            "id": "deploy2",
            "type": "prod",
            "status": "failed",
            "created_at": "2023-01-02T00:00:00",
            "errors": [{"type": "error1"}]
        }
    ]
    
    for dep in deployments:
        path = history_dir / f"{dep['id']}.json"
        with open(path, 'w') as f:
            json.dump(dep, f)
            
    metrics = await deployment_service.generate_deployment_metrics()
    
    assert "performance" in metrics
    assert "reliability" in metrics
    assert "trends" in metrics
    assert "frequency" in metrics["trends"]
    assert "success_trend" in metrics["trends"]

@pytest.mark.asyncio
async def test_optimize_deployment_records(deployment_service, history_dir):
    """Tests deployment record optimization functionality"""
    # Create test deployment records
    for i in range(5):
        deployment = {
            "id": f"deploy{i}",
            "type": "test",
            "status": "completed"
        }
        path = history_dir / f"deploy{i}.json"
        with open(path, 'w') as f:
            json.dump(deployment, f)
            
    optimization_results = await deployment_service.optimize_deployment_records()
    
    assert "compressed" in optimization_results
    assert "indexed" in optimization_results
    assert "cleaned" in optimization_results
    assert isinstance(optimization_results["indexed"], dict)

@pytest.mark.asyncio
async def test_deployment_not_found(deployment_service):
    """Tests error handling for non-existent deployments"""
    result = await deployment_service.update_deployment_status(
        "nonexistent",
        "completed",
        "test_user"
    )
    assert result is False

@pytest.mark.asyncio
async def test_deployment_validation(deployment_service, sample_deployment):
    """Tests deployment validation functionality"""
    # Test with valid deployment
    deployment_path = await deployment_service.record_deployment(sample_deployment)
    assert Path(deployment_path).exists()
    
    # Test with invalid deployment (missing required fields)
    invalid_deployment = DeploymentRecord(
        deployment_id="",  # Invalid empty ID
        deployment_type="test",
        deployment_strategy="invalid"
    )
    
    assert not invalid_deployment.validate_deployment()

@pytest.mark.asyncio
async def test_deployment_error_handling(deployment_service, sample_deployment):
    """Tests deployment error handling functionality"""
    # Record initial deployment
    deployment_path = await deployment_service.record_deployment(sample_deployment)
    
    # Add an error
    sample_deployment.add_error("test_error", "Test error message")
    await deployment_service.record_deployment(sample_deployment)
    
    with open(deployment_path, 'r') as f:
        deployment_data = json.load(f)
        assert len(deployment_data["errors"]) > 0
        assert deployment_data["errors"][0]["type"] == "test_error"
