from typing import Dict, List, Optional, Any, Protocol, Callable
from datetime import datetime
import asyncio
import json
import logging
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from functools import wraps
from abc import ABC, abstractmethod

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.models.config_model import ConfigModel

class TemplateStatus(str, Enum):
    """Template status states"""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class TemplateError(Exception):
    """Base exception for template operations"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(message)
        self.context = context or {}

class LoggerProtocol(Protocol):
    """Protocol for logger interface"""
    def error(self, msg: str, *args, **kwargs): ...
    def info(self, msg: str, *args, **kwargs): ...
    def debug(self, msg: str, *args, **kwargs): ...

class OperationContext:
    """Context for template operations"""
    def __init__(self, operation: str, **kwargs):
        self.operation = operation
        self.start_time = datetime.now()
        self.context = kwargs
        self.error: Optional[Exception] = None
        
    def set_error(self, error: Exception) -> None:
        self.error = error
        self.context["error"] = str(error)
        self.context["error_type"] = error.__class__.__name__
        
    def get_duration(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()
        
    def to_dict(self) -> Dict:
        return {
            "operation": self.operation,
            "duration": self.get_duration(),
            "success": self.error is None,
            **self.context
        }

class ValidationStrategy(ABC):
    """Abstract base class for validation strategies"""
    @abstractmethod
    def validate(self, data: Dict) -> bool: ...
    
class TemplateValidator(ValidationStrategy):
    """Validates template structure and required fields"""
    def __init__(self, required_fields: List[str]):
        self.required_fields = required_fields
        
    def validate(self, data: Dict) -> bool:
        return all(field in data for field in self.required_fields)

class StrategiesValidator(ValidationStrategy):
    """Validates strategies section of template"""
    def validate(self, data: Dict) -> bool:
        return isinstance(data.get("strategies", {}), dict)

def with_operation_context(operation_name: str):
    """Decorator to add operation context"""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            context = OperationContext(operation_name, **kwargs)
            try:
                result = await func(self, *args, **kwargs, context=context)
                self.logger.info(f"{operation_name} completed", 
                               extra=context.to_dict())
                return result
            except Exception as e:
                context.set_error(e)
                self.logger.error(f"{operation_name} failed: {str(e)}", 
                                extra=context.to_dict())
                raise TemplateError(str(e), context=context.to_dict())
        return wrapper
    return decorator

@dataclass
class TemplateAnalysis:
    """Structured analysis results with metrics"""
    stakeholders: List[str]
    objectives: List[str]
    gaps: Dict[str, str]
    current_state: Dict[str, Any]
    complexity_score: float
    metrics: Dict[str, float]

class TemplateService:
    """Template service with enhanced error handling and validation"""
    
    # Class-level constants
    REQUIRED_FIELDS = ["name", "description", "created_at"]
    REQUIRED_SECTIONS = ["validation", "integration", "security"]
    
    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)
        self.logger = logging.getLogger(__name__)
        self.validators = [
            TemplateValidator(["name", "description", "created_at"]),
            StrategiesValidator()
        ]
        
    async def _load_template(self, template_name: str, context: OperationContext) -> Dict:
        """Loads and validates template existence with context"""
        template_path = self.template_dir / f"{template_name}.json"
        if not template_path.exists():
            raise TemplateError(f"Template {template_name} not found")
            
        async with asyncio.Lock():
            with open(template_path, 'r') as f:
                data = json.load(f)
                context.context["template_size"] = len(json.dumps(data))
                return data
                
    @with_operation_context("analyze_template")
    async def analyze_template(self, template_name: str, *, context: OperationContext) -> TemplateAnalysis:
        """Analyzes template with performance metrics"""
        template_data = await self._load_template(template_name, context)
        
        metrics = self._calculate_metrics(template_data)
        context.context["metrics"] = metrics
        
        return TemplateAnalysis(
            stakeholders=self._identify_stakeholders(template_data),
            objectives=self._extract_objectives(template_data),
            gaps=self._analyze_gaps(template_data),
            current_state=self._assess_current_state(template_data),
            complexity_score=metrics["complexity_score"],
            metrics=metrics
        )
    
    @with_operation_context("validate_template")    
    async def validate_template(self, template_name: str, *, context: OperationContext) -> bool:
        """Validates template using validation strategies"""
        template_data = await self._load_template(template_name, context)
        
        results = {
            validator.__class__.__name__: validator.validate(template_data)
            for validator in self.validators
        }
        
        context.context["validation_results"] = results
        return all(results.values())
    
    @with_operation_context("create_template")
    async def create_template(self, config: ConfigModel, *, context: OperationContext) -> str:
        """Creates a new template based on configuration"""
        template_data = {
            "name": config.name,
            "description": config.description,
            "created_at": datetime.now().isoformat(),
            "status": TemplateStatus.DRAFT,
            "strategies": config.strategies,
            "implementation": config.implementation_details,
            "validation": config.validation_rules
        }
        
        await self._save_template(config.name, template_data, context)
        return str(self.template_dir / f"{config.name}.json")
            
    async def _save_template(self, template_name: str, data: Dict, context: OperationContext) -> None:
        """Saves template with proper locking"""
        template_path = self.template_dir / f"{template_name}.json"
        async with asyncio.Lock():
            with open(template_path, 'w') as f:
                json.dump(data, f, indent=2)
                
    def _calculate_metrics(self, data: Dict) -> Dict[str, float]:
        """Calculates comprehensive template metrics"""
        return {
            "complexity_score": len(json.dumps(data)) / 1000.0,
            "field_count": sum(1 for _ in self._traverse_dict(data)),
            "depth": max(self._calculate_depth(data), default=0),
            "validation_coverage": self._calculate_validation_coverage(data)
        }
    
    def _calculate_depth(self, data: Dict, current_depth: int = 0) -> List[int]:
        """Calculates maximum nesting depth"""
        if not isinstance(data, dict):
            return [current_depth]
            
        if not data:
            return [current_depth + 1]
            
        depths = []
        for value in data.values():
            if isinstance(value, dict):
                depths.extend(self._calculate_depth(value, current_depth + 1))
            else:
                depths.append(current_depth + 1)
        return depths
    
    def _traverse_dict(self, data: Dict) -> Dict:
        """Traverses dictionary using generator expression"""
        return (
            key 
            for k, v in data.items() 
            for key in [k] + (list(self._traverse_dict(v)) if isinstance(v, dict) else [])
        )
        
    def _identify_stakeholders(self, template_data: Dict) -> List[str]:
        """Identifies stakeholders from template data"""
        stakeholders = set()
        if "access" in template_data:
            stakeholders.update(template_data["access"].keys())
        if "workflows" in template_data:
            for workflow in template_data["workflows"]:
                stakeholders.update(workflow.get("participants", []))
        return list(stakeholders)
        
    def _extract_objectives(self, template_data: Dict) -> List[str]:
        """Extracts objectives from template data"""
        return [
            *template_data.get("objectives", []),
            *template_data.get("goals", [])
        ]
        
    def _analyze_gaps(self, template_data: Dict) -> Dict[str, str]:
        """Analyzes gaps in template implementation"""
        return {
            section: "Missing implementation" if section not in template_data
            else "Empty implementation" if not template_data[section]
            else ""
            for section in self.REQUIRED_SECTIONS
            if section not in template_data or not template_data[section]
        }
        
    def _assess_current_state(self, template_data: Dict) -> Dict[str, Any]:
        """Assesses current state of template"""
        return {
            "version": template_data.get("version", "1.0.0"),
            "last_modified": template_data.get("last_modified", datetime.now().isoformat()),
            "status": template_data.get("status", TemplateStatus.DRAFT)
        }
        
    def _calculate_validation_coverage(self, template_data: Dict) -> float:
        """Calculates validation rule coverage"""
        total_fields = sum(1 for _ in self._traverse_dict(template_data))
        validated_fields = len(template_data.get("validation_rules", []))
        return validated_fields / total_fields if total_fields > 0 else 0.0
