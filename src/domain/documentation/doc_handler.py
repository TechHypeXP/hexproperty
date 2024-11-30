"""Documentation automation handler with security measures."""

import os
import yaml
import jinja2
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

from ..security.audit_log import audit_logger
from ..security.rate_limiter import RateLimiter
from ..security.middleware import SecurityMiddleware

@dataclass
class DocumentMetadata:
    """Metadata for documentation."""
    doc_id: str
    version: str
    status: str
    timestamp: str
    author: str
    reviewers: List[str]
    doctype: str

class DocumentationHandler:
    """Handles automated documentation generation and updates."""
    
    def __init__(self, templates_dir: str, output_dir: str):
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.config = self._load_config()
        self.env = self._setup_jinja()
        self.rate_limiter = RateLimiter(
            max_requests=100,
            time_window=3600,
            group_id="documentation"
        )
    
    def _load_config(self) -> Dict:
        """Load templates configuration."""
        config_path = self.templates_dir / "templates_config.yaml"
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    
    def _setup_jinja(self) -> jinja2.Environment:
        """Setup Jinja2 environment."""
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def _generate_doc_id(self, doctype: str) -> str:
        """Generate unique document ID."""
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M")
        return f"{doctype}-{timestamp}"
    
    def _validate_template(self, template_name: str) -> bool:
        """Validate template exists and has required sections."""
        if template_name not in self.config["templates"]:
            return False
        
        template_config = self.config["templates"][template_name]
        template_path = self.templates_dir / template_config["file"]
        
        if not template_path.exists():
            return False
            
        required_sections = self.config["validation_rules"]["required_sections"]
        template_content = template_path.read_text()
        
        return all(section in template_content for section in required_sections)
    
    def _validate_metadata(self, metadata: DocumentMetadata) -> bool:
        """Validate document metadata."""
        rules = self.config["metadata"]
        
        # Validate status
        if metadata.status not in rules["status_values"]:
            return False
        
        # Validate version format
        version_parts = metadata.version.split(".")
        if len(version_parts) != 3 or not all(p.isdigit() for p in version_parts):
            return False
        
        # Validate doctype
        if metadata.doctype not in rules["document_id"]["doctypes"]:
            return False
        
        return True
    
    async def create_document(
        self,
        template_name: str,
        metadata: DocumentMetadata,
        content_vars: Dict,
        user_id: str
    ) -> str:
        """Create a new document from template."""
        # Check rate limit
        if not await self.rate_limiter.check_rate_limit(user_id):
            raise Exception("Rate limit exceeded for document creation")
        
        # Validate template and metadata
        if not self._validate_template(template_name):
            raise ValueError(f"Invalid template: {template_name}")
        
        if not self._validate_metadata(metadata):
            raise ValueError("Invalid document metadata")
        
        try:
            # Load template
            template = self.env.get_template(
                self.config["templates"][template_name]["file"]
            )
            
            # Generate document
            doc_content = template.render(
                metadata=metadata,
                **content_vars
            )
            
            # Create output file
            output_path = self.output_dir / f"{metadata.doc_id}.md"
            output_path.write_text(doc_content)
            
            # Log document creation
            audit_logger.log_event(
                event_type="DOCUMENTATION",
                severity="INFO",
                action="create_document",
                status="success",
                details={
                    "doc_id": metadata.doc_id,
                    "template": template_name,
                    "author": metadata.author,
                    "user_id": user_id
                }
            )
            
            return str(output_path)
            
        except Exception as e:
            audit_logger.log_event(
                event_type="DOCUMENTATION",
                severity="ERROR",
                action="create_document",
                status="failed",
                details={
                    "error": str(e),
                    "template": template_name,
                    "user_id": user_id
                }
            )
            raise
    
    async def update_document(
        self,
        doc_id: str,
        metadata: DocumentMetadata,
        content_vars: Dict,
        user_id: str
    ) -> str:
        """Update an existing document."""
        # Check rate limit
        if not await self.rate_limiter.check_rate_limit(user_id):
            raise Exception("Rate limit exceeded for document update")
        
        doc_path = self.output_dir / f"{doc_id}.md"
        if not doc_path.exists():
            raise FileNotFoundError(f"Document not found: {doc_id}")
        
        try:
            # Get original metadata
            original_content = doc_path.read_text()
            original_metadata = self._extract_metadata(original_content)
            
            # Validate version increment
            if not self._validate_version_increment(
                original_metadata.version,
                metadata.version
            ):
                raise ValueError("Invalid version increment")
            
            # Update document
            template_name = self._get_template_from_doctype(metadata.doctype)
            template = self.env.get_template(
                self.config["templates"][template_name]["file"]
            )
            
            doc_content = template.render(
                metadata=metadata,
                **content_vars
            )
            
            # Save updated document
            doc_path.write_text(doc_content)
            
            # Log document update
            audit_logger.log_event(
                event_type="DOCUMENTATION",
                severity="INFO",
                action="update_document",
                status="success",
                details={
                    "doc_id": doc_id,
                    "old_version": original_metadata.version,
                    "new_version": metadata.version,
                    "user_id": user_id
                }
            )
            
            return str(doc_path)
            
        except Exception as e:
            audit_logger.log_event(
                event_type="DOCUMENTATION",
                severity="ERROR",
                action="update_document",
                status="failed",
                details={
                    "error": str(e),
                    "doc_id": doc_id,
                    "user_id": user_id
                }
            )
            raise
    
    def _extract_metadata(self, content: str) -> DocumentMetadata:
        """Extract metadata from document content."""
        # Implementation depends on document format
        # For now, assume YAML frontmatter
        pass
    
    def _validate_version_increment(
        self,
        old_version: str,
        new_version: str
    ) -> bool:
        """Validate version increment follows rules."""
        old_parts = [int(p) for p in old_version.split(".")]
        new_parts = [int(p) for p in new_version.split(".")]
        
        # Must increment at least one part
        if old_parts >= new_parts:
            return False
        
        # Only one part should be incremented
        diff_count = sum(1 for o, n in zip(old_parts, new_parts) if o != n)
        return diff_count == 1
    
    def _get_template_from_doctype(self, doctype: str) -> str:
        """Get template name from document type."""
        for name, config in self.config["templates"].items():
            if config["doctype"] == doctype:
                return name
        raise ValueError(f"No template found for doctype: {doctype}")
