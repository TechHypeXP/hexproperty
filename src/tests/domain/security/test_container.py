"""Tests for container security functionality."""

import pytest
from unittest.mock import patch, Mock
from src.domain.security.container import (
    SecurityLevel,
    ContainerStatus,
    SecurityScan,
    ContainerPolicy,
    ContainerSecurity,
    container_security
)
from src.domain.security.policy import Permission, ResourceType

@pytest.fixture
def container_security_instance():
    """Create a container security instance."""
    return ContainerSecurity()

@pytest.fixture
def basic_policy():
    """Create a basic container policy."""
    return ContainerPolicy(
        allowed_registries={"gcr.io/hexproperty"},
        required_labels={"maintainer", "version"},
        blocked_packages={"vulnerable-pkg"},
        min_security_score=0.8,
        security_level=SecurityLevel.HIGH
    )

class TestContainerSecurity:
    """Test suite for container security functionality."""

    @pytest.mark.asyncio
    async def test_container_scan(self, container_security_instance):
        """Test container scanning."""
        image_name = "gcr.io/hexproperty/test-app:latest"
        
        with patch('src.domain.security.policy.policy_enforcer.check_permission', return_value=True):
            scan_result = await container_security_instance.scan_container(image_name)
            
            assert isinstance(scan_result, SecurityScan)
            assert hasattr(scan_result, 'vulnerabilities')
            assert hasattr(scan_result, 'security_score')

    @pytest.mark.asyncio
    async def test_container_validation(self, container_security_instance, basic_policy):
        """Test container validation against policy."""
        image_name = "gcr.io/hexproperty/test-app:latest"
        policy_name = "test-policy"
        
        container_security_instance.add_policy(policy_name, basic_policy)
        
        with patch('src.domain.security.policy.policy_enforcer.check_permission', return_value=True):
            with patch.object(
                container_security_instance,
                '_perform_security_scan',
                return_value=SecurityScan(security_score=0.9)
            ):
                status = await container_security_instance.validate_container(
                    image_name,
                    policy_name
                )
                assert status == ContainerStatus.APPROVED

    def test_policy_management(self, container_security_instance, basic_policy):
        """Test policy addition and removal."""
        policy_name = "test-policy"
        
        # Add policy
        container_security_instance.add_policy(policy_name, basic_policy)
        assert policy_name in container_security_instance._policies
        
        # Remove policy
        container_security_instance.remove_policy(policy_name)
        assert policy_name not in container_security_instance._policies

    @pytest.mark.asyncio
    async def test_permission_checking(self, container_security_instance):
        """Test permission checking for container operations."""
        image_name = "gcr.io/hexproperty/test-app:latest"
        
        # Test with no permission
        with patch('src.domain.security.policy.policy_enforcer.check_permission', return_value=False):
            with pytest.raises(PermissionError):
                await container_security_instance.scan_container(image_name)

    @pytest.mark.asyncio
    async def test_security_levels(self, container_security_instance):
        """Test different security levels."""
        policies = {
            "high": ContainerPolicy(security_level=SecurityLevel.HIGH),
            "medium": ContainerPolicy(security_level=SecurityLevel.MEDIUM),
            "low": ContainerPolicy(security_level=SecurityLevel.LOW)
        }
        
        for name, policy in policies.items():
            container_security_instance.add_policy(name, policy)
            assert container_security_instance._policies[name].security_level == policy.security_level

    @pytest.mark.asyncio
    async def test_vulnerability_handling(self, container_security_instance, basic_policy):
        """Test handling of vulnerabilities."""
        image_name = "gcr.io/hexproperty/test-app:latest"
        policy_name = "test-policy"
        
        container_security_instance.add_policy(policy_name, basic_policy)
        
        # Test with critical vulnerability
        scan_result = SecurityScan(
            vulnerabilities=[{"severity": "CRITICAL"}],
            security_score=0.9
        )
        
        with patch('src.domain.security.policy.policy_enforcer.check_permission', return_value=True):
            with patch.object(
                container_security_instance,
                '_perform_security_scan',
                return_value=scan_result
            ):
                status = await container_security_instance.validate_container(
                    image_name,
                    policy_name
                )
                assert status == ContainerStatus.VULNERABLE

    @patch('src.domain.security.audit_log.audit_logger.log_event')
    @pytest.mark.asyncio
    async def test_audit_logging(self, mock_log_event, container_security_instance):
        """Test audit logging of container security events."""
        image_name = "gcr.io/hexproperty/test-app:latest"
        
        with patch('src.domain.security.policy.policy_enforcer.check_permission', return_value=True):
            await container_security_instance.scan_container(image_name)
            
            # Verify scan audit log
            mock_log_event.assert_called_with(
                event_type="SECURITY",
                severity="INFO",
                action="container_scan",
                status="completed",
                details={
                    "image": image_name,
                    "score": 0.0,
                    "vulnerabilities": 0
                }
            )
