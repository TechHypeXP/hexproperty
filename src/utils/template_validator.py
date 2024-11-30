"""Template validation for documentation system."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class TemplateValidator:
    """Validates documentation templates."""
    
    def __init__(self, templates_dir: str = "docs/templates"):
        self.templates_dir = Path(templates_dir)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load templates configuration."""
        config_path = self.templates_dir / "templates_config.yaml"
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def validate_template(self, template_name: str) -> Tuple[bool, List[str]]:
        """Validate a template against configuration rules.
        
        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []
        template_config = self.config["templates"].get(template_name)
        
        if not template_config:
            return False, [f"Template '{template_name}' not found in config"]
            
        template_path = self.templates_dir / template_config["file"]
        
        # Check template file exists
        if not template_path.exists():
            return False, [f"Template file not found: {template_path}"]
            
        # Check required sections
        required_sections = self.config["validation_rules"]["required_sections"]
        template_content = template_path.read_text()
        
        for section in required_sections:
            if section not in template_content:
                errors.append(f"Missing required section: {section}")

        # Check template variables - only warn about missing variables
        if "variables" in template_config:
            missing_vars = []
            for var in template_config["variables"]:
                if f"{{{{ {var} }}}}" not in template_content:
                    missing_vars.append(f"Template missing variable: {var}")
            if missing_vars:
                errors.extend(missing_vars)

        # Template is valid if it has all required sections
        # Variable warnings don't make it invalid
        is_valid = all(not "Missing required section" in err for err in errors)
        return is_valid, errors

    def get_template_requirements(self, template_name: str) -> Dict:
        """Get requirements for a template."""
        template_config = self.config["templates"].get(template_name, {})
        return {
            "required_sections": self.config["validation_rules"]["required_sections"],
            "variables": template_config.get("variables", []),
            "doctype": template_config.get("doctype", "")
        }
