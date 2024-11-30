"""Helper functions for documentation generation."""

from pathlib import Path
from typing import Dict, List, Optional
from .doc_generator import DocumentGenerator

class DocSeriesGenerator:
    """Generates a series of documentation iterations."""
    
    def __init__(self, templates_dir: str = "docs/templates", output_dir: str = "docs/generated"):
        self.generator = DocumentGenerator(templates_dir, output_dir)
        self.output_dir = Path(output_dir)

    def generate_series(
        self,
        template_name: str,
        context: Dict,
        iterations: int = 3
    ) -> List[Path]:
        """Generate a series of documentation iterations.
        
        Args:
            template_name: Template to use
            context: Template variables
            iterations: Number of iterations (default 3)
            
        Returns:
            List of paths to generated documents
        """
        generated_files = []
        
        for i in range(1, iterations + 1):
            # Generate document for this iteration
            content = self.generator.generate_document(
                template_name,
                context,
                iteration=i
            )
            
            if content:
                # Save document
                output_file = self.generator.save_document(
                    content,
                    template_name,
                    iteration=i
                )
                generated_files.append(output_file)
            
        return generated_files

    def get_iteration_status(self, template_name: str) -> Dict[int, bool]:
        """Get status of iterations for a template.
        
        Returns:
            Dict mapping iteration number to whether it exists
        """
        status = {}
        template_config = self.generator.validator.config["templates"][template_name]
        base_name = Path(template_config["file"]).stem
        
        # Check each iteration
        for i in range(1, 4):
            expected_file = self.output_dir / f"{base_name}_iter{i}.md"
            status[i] = expected_file.exists()
            
        return status

def generate_deployment_series(
    deployment_name: str,
    variables: Dict,
    output_dir: str = "docs/generated"
) -> List[str]:
    """Generate deployment documentation series."""
    generator = DocSeriesGenerator(output_dir=output_dir)
    files = generator.generate_series(
        "Deployment Guide",
        {
            "deployment_name": deployment_name,
            **variables
        }
    )
    return [f.as_posix() for f in files]

def generate_architecture_series(
    component_name: str,
    variables: Dict,
    output_dir: str = "docs/generated"
) -> List[str]:
    """Generate architecture documentation series."""
    generator = DocSeriesGenerator(output_dir=output_dir)
    files = generator.generate_series(
        "Architecture Overview",
        {
            "component_name": component_name,
            **variables
        }
    )
    return [f.as_posix() for f in files]

def generate_resource_series(
    resource_name: str,
    variables: Dict,
    output_dir: str = "docs/generated"
) -> List[str]:
    """Generate resource documentation series."""
    generator = DocSeriesGenerator(output_dir=output_dir)
    files = generator.generate_series(
        "Resource Estimation",
        {
            "resource_name": resource_name,
            **variables
        }
    )
    return [f.as_posix() for f in files]
