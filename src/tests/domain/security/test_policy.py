"""Tests for security policy functionality."""

import pytest
from unittest.mock import patch
from src.domain.security.policy import (
    Permission,
    ResourceType,
    PolicyRule,
    SecurityPolicy,
    PolicyEnforcer,
    require_permission
)

@pytest.fixture
def policy_enforcer():
    """Create a policy enforcer instance."""
    return PolicyEnforcer()

@pytest.fixture
def basic_policy():
    """Create a basic security policy."""
    return SecurityPolicy(
        name="test-policy",
        rules=[
            PolicyRule(
                permissions={Permission.READ, Permission.WRITE},
                resource_types={ResourceType.DEPLOYMENT},
                resource_patterns=["test-.*"]
            )
        ],
        priority=1
    )

class TestSecurityPolicy:
    """Test suite for security policy functionality."""

    def test_basic_permission_check(self, policy_enforcer, basic_policy):
        """Test basic permission checking."""
        policy_enforcer.add_policy(basic_policy)
        
        # Test allowed permission
        assert policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "test-deployment"
        )
        
        # Test denied permission
        assert not policy_enforcer.check_permission(
            Permission.DELETE,
            ResourceType.DEPLOYMENT,
            "test-deployment"
        )

    def test_resource_pattern_matching(self, policy_enforcer):
        """Test resource pattern matching."""
        policy = SecurityPolicy(
            name="pattern-test",
            rules=[
                PolicyRule(
                    permissions={Permission.READ},
                    resource_types={ResourceType.DEPLOYMENT},
                    resource_patterns=["prod-.*", "staging-.*"]
                )
            ]
        )
        policy_enforcer.add_policy(policy)
        
        # Test matching patterns
        assert policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "prod-app1"
        )
        assert policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "staging-app1"
        )
        
        # Test non-matching pattern
        assert not policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "dev-app1"
        )

    def test_policy_priority(self, policy_enforcer):
        """Test policy priority handling."""
        deny_policy = SecurityPolicy(
            name="deny-all",
            rules=[
                PolicyRule(
                    permissions={Permission.READ},
                    resource_types={ResourceType.DEPLOYMENT},
                    resource_patterns=[".*"]
                )
            ],
            priority=1
        )
        
        allow_policy = SecurityPolicy(
            name="allow-specific",
            rules=[
                PolicyRule(
                    permissions={Permission.READ},
                    resource_types={ResourceType.DEPLOYMENT},
                    resource_patterns=["special-.*"]
                )
            ],
            priority=2
        )
        
        policy_enforcer.add_policy(deny_policy)
        policy_enforcer.add_policy(allow_policy)
        
        # Higher priority policy should take precedence
        assert policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "special-app"
        )

    def test_conditional_permissions(self, policy_enforcer):
        """Test conditional permissions."""
        policy = SecurityPolicy(
            name="conditional-test",
            rules=[
                PolicyRule(
                    permissions={Permission.DEPLOY},
                    resource_types={ResourceType.DEPLOYMENT},
                    conditions={"environment": "prod", "role": "admin"}
                )
            ]
        )
        policy_enforcer.add_policy(policy)
        
        # Test with matching conditions
        assert policy_enforcer.check_permission(
            Permission.DEPLOY,
            ResourceType.DEPLOYMENT,
            "app1",
            context={"environment": "prod", "role": "admin"}
        )
        
        # Test with non-matching conditions
        assert not policy_enforcer.check_permission(
            Permission.DEPLOY,
            ResourceType.DEPLOYMENT,
            "app1",
            context={"environment": "dev", "role": "admin"}
        )

    @patch('src.domain.security.audit_log.audit_logger.log_event')
    def test_audit_logging(self, mock_log_event, policy_enforcer, basic_policy):
        """Test audit logging of policy decisions."""
        policy_enforcer.add_policy(basic_policy)
        
        # Test allowed permission
        policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "test-deployment"
        )
        
        # Verify audit log for allowed permission
        mock_log_event.assert_called_with(
            event_type="SECURITY",
            severity="INFO",
            action="permission_check",
            status="allowed",
            details={
                "permission": Permission.READ,
                "resource_type": ResourceType.DEPLOYMENT,
                "resource_name": "test-deployment",
                "policy_name": "test-policy"
            }
        )
        
        # Test denied permission
        policy_enforcer.check_permission(
            Permission.DELETE,
            ResourceType.DEPLOYMENT,
            "test-deployment"
        )
        
        # Verify audit log for denied permission
        mock_log_event.assert_called_with(
            event_type="SECURITY",
            severity="WARNING",
            action="permission_check",
            status="denied",
            details={
                "permission": Permission.DELETE,
                "resource_type": ResourceType.DEPLOYMENT,
                "resource_name": "test-deployment"
            }
        )

    @pytest.mark.asyncio
    async def test_permission_decorator(self, policy_enforcer, basic_policy):
        """Test permission enforcement decorator."""
        policy_enforcer.add_policy(basic_policy)
        
        @require_permission(Permission.READ, ResourceType.DEPLOYMENT)
        async def test_func():
            return True
        
        # Test allowed operation
        assert await test_func()
        
        # Test denied operation
        with pytest.raises(PermissionError):
            @require_permission(Permission.DELETE, ResourceType.DEPLOYMENT)
            async def denied_func():
                return True
            await denied_func()

    def test_policy_updates(self, policy_enforcer, basic_policy):
        """Test policy addition and removal."""
        # Add policy
        policy_enforcer.add_policy(basic_policy)
        assert policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "test-deployment"
        )
        
        # Remove policy
        policy_enforcer.remove_policy(basic_policy.name)
        assert not policy_enforcer.check_permission(
            Permission.READ,
            ResourceType.DEPLOYMENT,
            "test-deployment"
        )
