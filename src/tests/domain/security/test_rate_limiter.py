"""Tests for rate limiting functionality."""

import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from src.domain.security.rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    RateLimitExceeded,
    rate_limit
)
from src.domain.security.audit_log import (
    AuditEventType,
    AuditEventSeverity,
    audit_logger
)

@pytest.fixture
def rate_limit_config():
    """Basic rate limit configuration."""
    return RateLimitConfig(
        max_requests=10,
        time_window=60,
        burst_limit=15
    )

@pytest.fixture
def group_rate_limit_config():
    """Rate limit configuration with group settings."""
    return RateLimitConfig(
        max_requests=10,
        time_window=60,
        burst_limit=15,
        group_key="tenant_id"
    )

@pytest.fixture
def limiter(rate_limit_config):
    """Rate limiter instance."""
    return RateLimiter(rate_limit_config)

@pytest.fixture
def group_limiter(group_rate_limit_config):
    """Rate limiter instance with group configuration."""
    return RateLimiter(group_rate_limit_config)

class TestRateLimiter:
    """Test suite for rate limiter functionality."""

    def test_init_validation(self):
        """Test initialization parameter validation."""
        # Test invalid max_requests
        with pytest.raises(ValueError, match="max_requests must be positive"):
            RateLimitConfig(max_requests=0, time_window=60)
        
        # Test invalid time_window
        with pytest.raises(ValueError, match="time_window must be positive"):
            RateLimitConfig(max_requests=10, time_window=0)
        
        # Test invalid burst_limit
        with pytest.raises(ValueError, match="burst_limit must be positive"):
            RateLimitConfig(max_requests=10, time_window=60, burst_limit=0)

    def test_basic_rate_limiting(self, limiter):
        """Test basic rate limiting functionality."""
        key = "test_user"
        
        # Should allow requests within limit
        for _ in range(10):
            assert limiter.check_rate_limit(key) is True
        
        # Should raise on exceeding limit
        with pytest.raises(RateLimitExceeded) as exc:
            limiter.check_rate_limit(key)
        assert exc.value.remaining_time > 0

    def test_burst_limit(self, limiter):
        """Test burst limit handling."""
        key = "test_user"
        
        # Should allow up to burst limit
        for _ in range(15):
            assert limiter.check_rate_limit(key) is True
        
        # Should raise on exceeding burst limit
        with pytest.raises(RateLimitExceeded) as exc:
            limiter.check_rate_limit(key)
        assert exc.value.remaining_time > 0

    def test_window_sliding(self, limiter):
        """Test sliding window behavior."""
        key = "test_user"
        
        # Fill up the window
        for _ in range(10):
            assert limiter.check_rate_limit(key) is True
        
        # Wait for half the window
        time.sleep(30)
        
        # Should allow more requests
        assert limiter.check_rate_limit(key) is True

    def test_group_rate_limiting(self, group_limiter):
        """Test group-based rate limiting."""
        key = "test_user"
        context = {"tenant_id": "tenant1"}
        
        # Should allow requests within group limit
        for _ in range(15):
            assert group_limiter.check_rate_limit(key, context) is True
        
        # Should raise on exceeding group limit
        with pytest.raises(RateLimitExceeded) as exc:
            group_limiter.check_rate_limit(key, context)
        assert "Group rate limit exceeded" in str(exc.value)

    def test_multiple_groups(self, group_limiter):
        """Test rate limiting across multiple groups."""
        key = "test_user"
        context1 = {"tenant_id": "tenant1"}
        context2 = {"tenant_id": "tenant2"}
        
        # Fill up first group
        for _ in range(15):
            assert group_limiter.check_rate_limit(key, context1) is True
        
        # Should still allow requests for second group
        assert group_limiter.check_rate_limit(key, context2) is True

    def test_remaining_requests(self, limiter):
        """Test remaining requests calculation."""
        key = "test_user"
        
        # Initial state
        assert limiter.get_remaining(key) == 15
        
        # After some requests
        for _ in range(5):
            limiter.check_rate_limit(key)
        assert limiter.get_remaining(key) == 10

    def test_cleanup(self, limiter):
        """Test cleanup of expired windows."""
        key = "test_user"
        
        # Add some requests
        for _ in range(5):
            limiter.check_rate_limit(key)
        
        # Wait for window to expire
        time.sleep(61)
        
        # Cleanup should remove expired window
        limiter.cleanup()
        assert limiter.get_remaining(key) == 15

    @patch('src.domain.security.audit_log.audit_logger.log_event')
    def test_audit_logging(self, mock_log_event, limiter):
        """Test audit logging of rate limit events."""
        key = "test_user"
        
        # Fill up the limit
        for _ in range(15):
            limiter.check_rate_limit(key)
        
        # Trigger rate limit exceeded
        with pytest.raises(RateLimitExceeded):
            limiter.check_rate_limit(key)
        
        # Verify audit log
        mock_log_event.assert_called_with(
            event_type=AuditEventType.SECURITY,
            severity=AuditEventSeverity.WARNING,
            action="rate_limit_exceeded",
            status="blocked",
            details={
                "key": key,
                "limit": 15,
                "window": 60
            }
        )

    def test_decorator(self, limiter):
        """Test rate limit decorator."""
        @rate_limit(limiter)
        def test_func():
            return True
        
        # Should work within limit
        for _ in range(15):
            assert test_func() is True
        
        # Should raise on exceeding limit
        with pytest.raises(RateLimitExceeded):
            test_func()

    def test_decorator_with_key_func(self, limiter):
        """Test rate limit decorator with custom key function."""
        def key_func(*args, **kwargs):
            return kwargs.get('user_id', 'default')
        
        @rate_limit(limiter, key_func)
        def test_func(user_id=None):
            return True
        
        # Different users should have separate limits
        for _ in range(15):
            assert test_func(user_id='user1') is True
        assert test_func(user_id='user2') is True
