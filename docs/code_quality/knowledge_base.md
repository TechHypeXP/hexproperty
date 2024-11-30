# Code Quality Knowledge Base

This document serves as a living knowledge base for code quality standards, best practices, and lessons learned from code reviews in the HexProperty project.

## Table of Contents
1. [Code Organization Patterns](#code-organization-patterns)
2. [Type Safety and Validation](#type-safety-and-validation)
3. [Error Handling](#error-handling)
4. [State Management](#state-management)
5. [Documentation Standards](#documentation-standards)
6. [Performance Optimization](#performance-optimization)
7. [Testing Best Practices](#testing-best-practices)

## Code Organization Patterns

### Three-Iterations Approach
Our codebase follows a three-iterations approach for comprehensive system development:

1. **Analysis & Understanding**
   - Focus on core domain models and relationships
   - Capture business requirements and constraints
   - Document assumptions and dependencies

2. **Solution & Implementation**
   - Implement core functionality
   - Add validation and error handling
   - Set up integration points

3. **Enhancement & Optimization**
   - Add performance metrics
   - Optimize critical paths
   - Handle edge cases
   - Plan for future improvements

### Code Review Insights

#### Pattern: Class-Level Constants Over Method-Level
**Problem:**
```python
def update_status(self, new_status: str):
    # Bad: Dictionary defined inside method
    valid_transitions = {
        'pending': ['in_progress', 'failed'],
        'in_progress': ['completed', 'failed']
    }
```

**Solution:**
```python
class DeploymentRecord:
    # Good: Class-level constant
    VALID_STATUS_TRANSITIONS = {
        DeploymentStatus.PENDING: [DeploymentStatus.IN_PROGRESS, DeploymentStatus.FAILED],
        DeploymentStatus.IN_PROGRESS: [DeploymentStatus.COMPLETED, DeploymentStatus.FAILED]
    }
```

**Benefits:**
- Improved memory efficiency
- Better code organization
- Single source of truth for constants
- Easier to maintain and update

#### Pattern: Simplified Validation Logic
**Problem:**
```python
def validate_deployment(self) -> bool:
    try:
        if not self.deployment_id:
            raise ValidationError("Missing ID")
        if not self.type:
            raise ValidationError("Missing type")
        return True
    except ValidationError as e:
        self.add_error("validation", str(e))
        return False
```

**Solution:**
```python
def validate_deployment(self) -> bool:
    if not all([self.deployment_id, self.deployment_type]):
        self.add_error("validation", "Missing required fields")
        return False
    return True
```

**Benefits:**
- More readable code
- Direct condition checks
- Clearer error messages
- Reduced complexity

#### Pattern: Async Resource Management
**Problem:**
```python
# Bad: No resource management or locking
with open(template_path, 'r') as f:
    template_data = json.load(f)
```

**Solution:**
```python
async def _load_template(self, template_name: str) -> Dict:
    """Loads and validates template existence"""
    template_path = self.template_dir / f"{template_name}.json"
    async with asyncio.Lock():
        with open(template_path, 'r') as f:
            return json.load(f)
```

**Benefits:**
- Proper resource management
- Thread-safe file operations
- Clear separation of concerns
- Reusable loading logic

#### Pattern: Decorator-Based Error Handling
**Problem:**
```python
# Bad: Repetitive try-except blocks
async def method1(self):
    try:
        # Logic
    except Exception as e:
        self.logger.error(f"Operation failed: {e}")
        raise
```

**Solution:**
```python
def async_error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            service = args[0]
            service.logger.error(f"{func.__name__} failed: {str(e)}", 
                               extra={"context": kwargs})
            raise TemplateError(str(e), context=kwargs)
    return wrapper

@async_error_handler
async def method1(self):
    # Logic without try-except
```

**Benefits:**
- Centralized error handling
- Consistent error logging
- Reduced code duplication
- Better error context

#### Pattern: List Comprehension for Data Transformation
**Problem:**
```python
# Bad: Imperative style with loops
def extract_data(self, data):
    results = []
    for item in data:
        if condition(item):
            results.append(transform(item))
    return results
```

**Solution:**
```python
def extract_data(self, data):
    return [
        transform(item)
        for item in data
        if condition(item)
    ]
```

**Benefits:**
- More readable and concise
- Functional programming style
- Better performance
- Clearer intent

## Type Safety and Validation

### Using Pydantic for Data Validation
- Leverage Pydantic's BaseModel for automatic validation
- Define clear field types and constraints
- Use validators for complex validation rules

```python
class DeploymentMetadata(BaseModel):
    version: str = "1.0.0"
    last_modified: datetime = Field(default_factory=datetime.now)
    
    @validator('version')
    def validate_version(cls, v):
        if not v.replace('.', '').isdigit():
            raise ValueError("Version must be in format X.Y.Z")
        return v
```

### Enum for Type-Safe Status
- Use Enum classes for predefined values
- Ensures type safety at compile time
- Provides better IDE support

```python
class DeploymentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
```

## Error Handling

### Custom Exception Hierarchy
- Create specific exception classes
- Include context in error messages
- Use proper exception inheritance

```python
class DeploymentError(Exception):
    """Base exception for deployment errors"""
    pass

class ValidationError(DeploymentError):
    """Raised when deployment validation fails"""
    pass
```

### Error Logging Best Practices
- Include timestamp and context
- Use structured logging
- Maintain error history

```python
def add_error(self, error_type: str, error_message: str) -> None:
    self.metadata.errors.append({
        "type": error_type,
        "message": error_message,
        "timestamp": datetime.now().isoformat()
    })
```

## State Management

### State Machine Pattern
- Define valid state transitions
- Validate state changes
- Document state flow

```python
VALID_STATUS_TRANSITIONS = {
    DeploymentStatus.PENDING: [DeploymentStatus.IN_PROGRESS, DeploymentStatus.FAILED],
    DeploymentStatus.IN_PROGRESS: [DeploymentStatus.COMPLETED, DeploymentStatus.FAILED],
    DeploymentStatus.COMPLETED: [DeploymentStatus.ROLLED_BACK],
    DeploymentStatus.FAILED: [DeploymentStatus.PENDING],
    DeploymentStatus.ROLLED_BACK: [DeploymentStatus.PENDING]
}
```

### Enum-Based Status Management
**Problem:**
```python
# Bad: String literals for status
status = "draft"
if status == "in_progress":
    # Logic
```

**Solution:**
```python
class TemplateStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

status = TemplateStatus.DRAFT
if status == TemplateStatus.IN_PROGRESS:
    # Logic
```

**Benefits:**
- Type safety
- IDE autocomplete
- Prevents typos
- Self-documenting code

## Documentation Standards

### Class and Method Documentation
- Include purpose and context
- Document parameters and return types
- Note exceptions and side effects

```python
def update_status(self, new_status: DeploymentStatus, modified_by: str) -> None:
    """Updates deployment status with proper state validation
    
    Args:
        new_status (DeploymentStatus): New status to set
        modified_by (str): User making the modification
        
    Raises:
        ValueError: If status transition is invalid
    """
```

## Testing Best Practices

### Test Organization
- Group related tests
- Use descriptive test names
- Include positive and negative cases

```python
@pytest.mark.asyncio
async def test_deployment_validation():
    """Test deployment validation with various scenarios"""
    # Arrange
    deployment = DeploymentRecord(...)
    
    # Act & Assert
    assert deployment.validate_deployment() is True
    
    # Test invalid cases
    deployment.deployment_id = ""
    assert deployment.validate_deployment() is False
```

### Mock Usage
- Mock external dependencies
- Use fixtures for common setup
- Test edge cases and error conditions

```python
@pytest.fixture
def mock_git_service():
    with patch('services.git_service.GitService') as mock:
        yield mock
```

## Performance Optimization

### Memory Efficiency
- Use class-level constants for shared data
- Implement proper cleanup in destructors
- Monitor memory usage in critical paths

### Async Operations
- Use async/await for I/O operations
- Implement proper error handling
- Consider connection pooling

### Normalized Metrics
**Problem:**
```python
# Bad: Raw metrics without normalization
def calculate_score(self, data):
    return len(json.dumps(data))  # Raw size
```

**Solution:**
```python
def calculate_complexity(self, data: Dict) -> float:
    """Calculates normalized complexity score"""
    return len(json.dumps(data)) / 1000.0  # Normalized score
```

**Benefits:**
- More meaningful metrics
- Easier comparison
- Better scaling
- Clearer interpretation

---

Note: This knowledge base is continuously updated based on code reviews and lessons learned. When implementing new features or refactoring existing code, please refer to these patterns and best practices.
