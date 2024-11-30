"""Tests for security middleware functionality."""

import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.domain.security.middleware import SecurityMiddleware
from src.domain.security.rate_limiter import RateLimitExceeded

@pytest.fixture
def app():
    """Create test FastAPI application."""
    return FastAPI()

@pytest.fixture
def security_middleware(app):
    """Create security middleware instance."""
    return SecurityMiddleware(app)

@pytest.fixture
def client(app, security_middleware):
    """Create test client with security middleware."""
    app.middleware("http")(security_middleware.__call__)
    return TestClient(app)

class TestSecurityMiddleware:
    """Test suite for security middleware."""

    def test_security_headers(self, client):
        """Test security headers are properly set."""
        @client.app.get("/test-headers")
        async def test_endpoint():
            return {"message": "test"}

        response = client.get("/test-headers")
        assert response.status_code == 200
        
        # Verify security headers
        headers = response.headers
        assert headers["X-Frame-Options"] == "DENY"
        assert headers["X-XSS-Protection"] == "1; mode=block"
        assert headers["X-Content-Type-Options"] == "nosniff"
        assert "max-age=31536000" in headers["Strict-Transport-Security"]
        assert "default-src 'self'" in headers["Content-Security-Policy"]
        assert headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
        assert "geolocation=()" in headers["Permissions-Policy"]

    def test_path_traversal_prevention(self, client):
        """Test path traversal prevention."""
        @client.app.get("/test/../sensitive")
        async def test_endpoint():
            return {"message": "test"}

        response = client.get("/test/../sensitive")
        assert response.status_code == 400
        assert response.json() == "Invalid path"

    def test_xss_prevention(self, client):
        """Test XSS prevention in headers."""
        @client.app.get("/test-xss")
        async def test_endpoint():
            return {"message": "test"}

        headers = {
            "X-Custom": "<script>alert('xss')</script>"
        }
        response = client.get("/test-xss", headers=headers)
        assert response.status_code == 400
        assert response.json() == "Invalid headers"

    @pytest.mark.asyncio
    async def test_rate_limiting(self, app, client, security_middleware):
        """Test rate limiting functionality."""
        @app.get("/limited")
        async def limited_endpoint():
            return {"message": "test"}

        # Test within limit
        for _ in range(10):
            response = client.get("/limited")
            assert response.status_code == 200

        # Test exceeding limit
        response = client.get("/limited")
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()

    @patch('src.domain.security.audit_log.audit_logger.log_event')
    def test_security_event_logging(self, mock_log_event, client):
        """Test security event logging."""
        @client.app.get("/test-logging")
        async def test_endpoint():
            return {"message": "test"}

        # Test path traversal attempt
        client.get("/test-logging/../sensitive")
        mock_log_event.assert_called_with(
            event_type="SECURITY",
            severity="WARNING",
            action="path_traversal_attempt",
            status="blocked",
            details={"path": "/test-logging/../sensitive"}
        )

        # Test XSS attempt
        headers = {"X-Custom": "<script>alert('xss')</script>"}
        client.get("/test-logging", headers=headers)
        mock_log_event.assert_called_with(
            event_type="SECURITY",
            severity="WARNING",
            action="xss_attempt",
            status="blocked",
            details={"headers": headers}
        )

    def test_cors_configuration(self, client):
        """Test CORS configuration."""
        @client.app.get("/test-cors")
        async def test_endpoint():
            return {"message": "test"}

        headers = {
            "Origin": "https://hexproperty.com"
        }
        response = client.options("/test-cors", headers=headers)
        assert response.status_code == 200
        assert response.headers["Access-Control-Allow-Origin"] == "https://hexproperty.com"
        assert response.headers["Access-Control-Allow-Credentials"] == "true"

    def test_error_handling(self, client):
        """Test error handling in middleware."""
        @client.app.get("/test-error")
        async def test_endpoint():
            raise ValueError("Test error")

        response = client.get("/test-error")
        assert response.status_code == 500
        assert response.json() == "Internal server error"

    @pytest.mark.asyncio
    async def test_group_rate_limiting(self, app, client, security_middleware):
        """Test group-based rate limiting."""
        @app.get("/group-limited")
        async def group_limited_endpoint():
            return {"message": "test"}

        # Test within group limit
        headers = {"X-Tenant-ID": "tenant1"}
        for _ in range(10):
            response = client.get("/group-limited", headers=headers)
            assert response.status_code == 200

        # Test exceeding group limit
        response = client.get("/group-limited", headers=headers)
        assert response.status_code == 429
        assert "Group rate limit exceeded" in response.json()
