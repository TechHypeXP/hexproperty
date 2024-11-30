"""Rate limiting implementation for deployment operations."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from functools import wraps
import time
import logging
from threading import Lock
from .audit_log import audit_logger, AuditEventType, AuditEventSeverity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    max_requests: int
    time_window: int  # in seconds
    burst_limit: Optional[int] = None
    group_key: Optional[str] = None  # For grouping related limits

@dataclass
class RateLimitEntry:
    """Entry for tracking rate limit data."""
    requests: List[float] = field(default_factory=list)
    last_reset: datetime = field(default_factory=datetime.now)
    group_usage: Dict[str, int] = field(default_factory=dict)

class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str, remaining_time: float):
        self.remaining_time = remaining_time
        super().__init__(message)

class RateLimiter:
    """Thread-safe rate limiter implementation using sliding window."""
    
    def __init__(self, config: RateLimitConfig):
        """Initialize rate limiter with configuration."""
        if config.max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if config.time_window <= 0:
            raise ValueError("time_window must be positive")
        if config.burst_limit is not None and config.burst_limit <= 0:
            raise ValueError("burst_limit must be positive")
        
        self.config = config
        self.burst_limit = config.burst_limit or config.max_requests
        self._windows: Dict[str, RateLimitEntry] = {}
        self._lock = Lock()
    
    def check_rate_limit(self, key: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Check if the rate limit is exceeded for the given key."""
        with self._lock:
            now = time.time()
            window = self._get_or_create_window(key)
            
            # Clean up old requests
            cutoff = now - self.config.time_window
            window.requests = [t for t in window.requests if t > cutoff]
            
            # Check group limits if configured
            if self.config.group_key and context:
                group = context.get(self.config.group_key)
                if group:
                    group_count = window.group_usage.get(group, 0)
                    if group_count >= self.burst_limit:
                        self._log_limit_exceeded(key, group)
                        raise RateLimitExceeded(
                            f"Group rate limit exceeded for {group}",
                            self._get_reset_time(window)
                        )
            
            # Check if rate limit is exceeded
            if len(window.requests) >= self.burst_limit:
                self._log_limit_exceeded(key)
                raise RateLimitExceeded(
                    "Rate limit exceeded",
                    self._get_reset_time(window)
                )
            
            # Add new request
            window.requests.append(now)
            
            # Update group usage if applicable
            if self.config.group_key and context:
                group = context.get(self.config.group_key)
                if group:
                    window.group_usage[group] = window.group_usage.get(group, 0) + 1
            
            return True
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests for the given key."""
        with self._lock:
            now = time.time()
            window = self._get_or_create_window(key)
            
            # Clean up old requests
            cutoff = now - self.config.time_window
            window.requests = [t for t in window.requests if t > cutoff]
            
            return self.burst_limit - len(window.requests)
    
    def _get_or_create_window(self, key: str) -> RateLimitEntry:
        """Get or create a rate limit window for the given key."""
        if key not in self._windows:
            self._windows[key] = RateLimitEntry()
        return self._windows[key]
    
    def _get_reset_time(self, window: RateLimitEntry) -> float:
        """Calculate time until the rate limit resets."""
        if not window.requests:
            return 0
        oldest_request = min(window.requests)
        return max(0, oldest_request + self.config.time_window - time.time())
    
    def _log_limit_exceeded(self, key: str, group: Optional[str] = None) -> None:
        """Log rate limit exceeded event."""
        details = {
            "key": key,
            "limit": self.burst_limit,
            "window": self.config.time_window
        }
        if group:
            details["group"] = group
            
        audit_logger.log_event(
            event_type=AuditEventType.SECURITY,
            severity=AuditEventSeverity.WARNING,
            action="rate_limit_exceeded",
            status="blocked",
            details=details
        )
    
    def cleanup(self) -> None:
        """Clean up expired windows."""
        with self._lock:
            now = time.time()
            cutoff = now - self.config.time_window
            
            # Remove windows with all requests older than cutoff
            expired = []
            for key, window in self._windows.items():
                if all(t <= cutoff for t in window.requests):
                    expired.append(key)
            
            for key in expired:
                del self._windows[key]

def rate_limit(limiter: RateLimiter, key_func=None):
    """Decorator for rate limiting function calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs) if key_func else "default"
            context = kwargs.get("context", {})
            limiter.check_rate_limit(key, context)
            return func(*args, **kwargs)
        return wrapper
    return decorator
