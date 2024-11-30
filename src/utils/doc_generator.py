"""Documentation generator module."""

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import jinja2
from .template_validator import TemplateValidator

class DocumentGenerator:
    """Generates documentation from templates."""
    
    def __init__(self, templates_dir: str = "docs/templates", output_dir: str = "docs/generated"):
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.validator = TemplateValidator(templates_dir)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )

    def generate_document(self, template_name: str, context: Dict, iteration: int = 1) -> Optional[str]:
        """Generate a document from a template.
        
        Args:
            template_name: Name of template to use
            context: Variables for template
            iteration: Current iteration (1-3)
            
        Returns:
            Generated document content or None if validation fails
        """
        # Validate template
        is_valid, errors = self.validator.validate_template(template_name)
        if not is_valid:
            print(f"Template validation failed: {errors}")
            return None

        # Get template config
        template_config = self.validator.config["templates"][template_name]
        template_file = template_config["file"]

        # Add iteration context
        context.update({
            "iteration": iteration,
            "iteration_phase": self._get_iteration_phase(iteration),
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "version": f"{iteration}.0.0"
        })

        # Generate document
        template = self.env.get_template(template_file)
        return template.render(**context)

    def save_document(self, content: str, template_name: str, iteration: int = 1) -> Path:
        """Save generated document to file.
        
        Args:
            content: Document content
            template_name: Name of template used
            iteration: Current iteration
            
        Returns:
            Path to saved file
        """
        if not content:
            raise ValueError("No content provided")
            
        # Create output directory if needed
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with iteration
        template_config = self.validator.config["templates"][template_name]
        base_name = Path(template_config["file"]).stem
        output_file = self.output_dir / f"{base_name}_iter{iteration}.md"
        
        # Save content
        output_file.write_text(content)
        return output_file

    def _get_iteration_phase(self, iteration: int) -> str:
        """Get phase description for iteration."""
        phases = {
            1: "Initial Draft",
            2: "Refinement",
            3: "Final Review"
        }
        return phases.get(iteration, "Unknown")

def generate_deployment_doc(
    deployment_name: str,
    output_path: str,
    variables: Dict,
    version: Optional[str] = None
) -> str:
    """Helper function to generate deployment documentation."""
    generator = DocumentGenerator()
    content = generator.generate_document(
        "Deployment Guide",
        {
            "deployment_name": deployment_name,
            **variables
        },
        version=version
    )
    if content is None:
        return ""
    return generator.save_document(content, "Deployment Guide").as_posix()

def generate_architecture_doc(
    component_name: str,
    output_path: str,
    variables: Dict,
    version: Optional[str] = None
) -> str:
    """Helper function to generate architecture documentation."""
    generator = DocumentGenerator()
    content = generator.generate_document(
        "Architecture Overview",
        {
            "component_name": component_name,
            **variables
        },
        version=version
    )
    if content is None:
        return ""
    return generator.save_document(content, "Architecture Overview").as_posix()

def generate_resource_doc(
    resource_name: str,
    output_path: str,
    variables: Dict,
    version: Optional[str] = None
) -> str:
    """Helper function to generate resource documentation."""
    generator = DocumentGenerator()
    content = generator.generate_document(
        "Resource Estimation",
        {
            "resource_name": resource_name,
            **variables
        },
        version=version
    )
    if content is None:
        return ""
    return generator.save_document(content, "Resource Estimation").as_posix()
