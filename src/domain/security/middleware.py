"""Security middleware for the application."""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
import re
from pathlib import Path
from .audit_log import audit_logger, AuditEventType, AuditEventSeverity

class SecurityMiddleware:
    """Security middleware for request/response processing."""
    
    def __init__(self, app: FastAPI):
        self.app = app
        
        # Configure CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://hexproperty.com"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        # Security headers configuration
        self.security_headers = {
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "X-Content-Type-Options": "nosniff",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; img-src 'self' data:; script-src 'self'; frame-ancestors 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Process the request and apply security measures."""
        
        try:
            # Check for path traversal attempts
            if not self._is_safe_path(request.url.path):
                await self._log_security_event(
                    request,
                    "path_traversal_attempt",
                    "blocked",
                    {"path": request.url.path}
                )
                return Response(
                    content="Invalid path",
                    status_code=400
                )
            
            # Check for XSS attempts in headers
            if self._contains_xss(dict(request.headers)):
                await self._log_security_event(
                    request,
                    "xss_attempt",
                    "blocked",
                    {"headers": dict(request.headers)}
                )
                return Response(
                    content="Invalid headers",
                    status_code=400
                )
            
            # Process the request
            response = await call_next(request)
            
            # Apply security headers
            for header, value in self.security_headers.items():
                response.headers[header] = value
            
            return response
            
        except Exception as e:
            await self._log_security_event(
                request, "security_error", "error",
                details={"error": str(e)}
            )
            return Response(
                content="Internal server error",
                status_code=500
            )
    
    def _is_safe_path(self, path: str) -> bool:
        """Validate path for traversal attempts."""
        normalized = Path(path).resolve()
        return (
            ".." not in str(normalized) and
            not any(c in str(normalized) for c in '<>"|')
        )
    
    def _contains_xss(self, headers: dict) -> bool:
        """Check for XSS patterns in headers."""
        xss_patterns = [
            r'<script.*?>',
            r'javascript:',
            r'on\w+\s*=',
            r'data:text/html',
        ]
        
        return any(
            re.search(pattern, str(value), re.IGNORECASE)
            for value in headers.values()
            for pattern in xss_patterns
        )
    
    async def _log_security_event(
        self,
        request: Request,
        action: str,
        status: str,
        details: dict = None
    ) -> None:
        """Log security-related events."""
        audit_logger.log_event(
            event_type=AuditEventType.SECURITY,
            severity=AuditEventSeverity.WARNING,
            action=action,
            status=status,
            details={
                "path": str(request.url),
                "method": request.method,
                "client_host": request.client.host,
                **(details or {})
            }
        )
