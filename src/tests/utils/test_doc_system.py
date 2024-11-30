"""Tests for documentation generation system."""

import pytest
from pathlib import Path
import tempfile
import shutil
import yaml
from src.utils.template_validator import TemplateValidator
from src.utils.doc_generator import DocumentGenerator
from src.utils.doc_helpers import DocSeriesGenerator

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def templates_dir(temp_dir):
    """Create test templates directory with config."""
    templates = temp_dir / "templates"
    templates.mkdir()
    
    # Create config
    config = {
        "templates": {
            "Test Template": {
                "file": "test_template.md",
                "variables": ["title", "description", "iteration_phase"]
            }
        },
        "validation_rules": {
            "required_sections": ["# Overview", "## Details"]
        }
    }
    
    with open(templates / "templates_config.yaml", "w") as f:
        yaml.dump(config, f)
        
    # Create template file
    template_content = """# Overview
Title: {{ title }}
Iteration Phase: {{ iteration_phase }}

## Details
Description: {{ description }}

## Optional
Some optional content
"""
    
    with open(templates / "test_template.md", "w") as f:
        f.write(template_content)
        
    return templates

@pytest.fixture
def output_dir(temp_dir):
    """Create test output directory."""
    output = temp_dir / "output"
    output.mkdir()
    return output

class TestTemplateValidator:
    """Test template validation functionality."""
    
    def test_validate_valid_template(self, templates_dir):
        validator = TemplateValidator(str(templates_dir))
        is_valid, errors = validator.validate_template("Test Template")
        assert is_valid
        assert len(errors) == 0
        
    def test_validate_missing_template(self, templates_dir):
        validator = TemplateValidator(str(templates_dir))
        is_valid, errors = validator.validate_template("Missing Template")
        assert not is_valid
        assert "not found in config" in errors[0]
        
    def test_validate_missing_section(self, templates_dir):
        # Create template missing required section
        bad_template = templates_dir / "bad_template.md"
        bad_template.write_text("Some content without required sections")
        
        # Update config
        config_path = templates_dir / "templates_config.yaml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        config["templates"]["Bad Template"] = {"file": "bad_template.md"}
        
        with open(config_path, "w") as f:
            yaml.dump(config, f)
            
        validator = TemplateValidator(str(templates_dir))
        is_valid, errors = validator.validate_template("Bad Template")
        assert not is_valid
        assert any("Missing required section" in err for err in errors)

class TestDocumentGenerator:
    """Test document generation functionality."""
    
    def test_generate_document(self, templates_dir, output_dir):
        generator = DocumentGenerator(str(templates_dir), str(output_dir))
        content = generator.generate_document(
            "Test Template",
            {
                "title": "Test Title",
                "description": "Test Description",
                "iteration_phase": "Initial Draft"
            },
            iteration=1
        )
        
        assert content is not None
        assert "Test Title" in content
        assert "Test Description" in content
        assert "Initial Draft" in content
        
    def test_save_document(self, templates_dir, output_dir):
        generator = DocumentGenerator(str(templates_dir), str(output_dir))
        content = "Test content"
        output_file = generator.save_document(content, "Test Template", iteration=1)
        
        assert output_file.exists()
        assert output_file.read_text() == content
        assert output_file.name == "test_template_iter1.md"

class TestDocSeriesGenerator:
    """Test documentation series generation."""
    
    def test_generate_series(self, templates_dir, output_dir):
        generator = DocSeriesGenerator(str(templates_dir), str(output_dir))
        files = generator.generate_series(
            "Test Template",
            {
                "title": "Series Test",
                "description": "Testing series generation",
                "iteration_phase": "Initial Draft"
            }
        )
        
        assert len(files) == 3
        for i, file in enumerate(files, 1):
            assert file.exists()
            assert f"iter{i}" in file.name
            content = file.read_text()
            assert "Series Test" in content
            
    def test_get_iteration_status(self, templates_dir, output_dir):
        generator = DocSeriesGenerator(str(templates_dir), str(output_dir))
        
        # Generate first two iterations
        generator.generate_series(
            "Test Template",
            {"title": "Status Test", "description": "Testing status", "iteration_phase": "Initial Draft"},
            iterations=2
        )
        
        status = generator.get_iteration_status("Test Template")
        assert status[1] is True
        assert status[2] is True
        assert status[3] is False

def test_end_to_end(templates_dir, output_dir):
    """Test complete documentation workflow."""
    
    # 1. Validate template
    validator = TemplateValidator(str(templates_dir))
    is_valid, errors = validator.validate_template("Test Template")
    assert is_valid
    
    # 2. Generate single document
    generator = DocumentGenerator(str(templates_dir), str(output_dir))
    content = generator.generate_document(
        "Test Template",
        {"title": "E2E Test", "description": "End to end testing", "iteration_phase": "Initial Draft"},
        iteration=1
    )
    assert content is not None
    
    # 3. Save document
    output_file = generator.save_document(content, "Test Template", iteration=1)
    assert output_file.exists()
    
    # 4. Generate series
    series_gen = DocSeriesGenerator(str(templates_dir), str(output_dir))
    files = series_gen.generate_series(
        "Test Template",
        {"title": "Series E2E", "description": "Testing full series", "iteration_phase": "Initial Draft"}
    )
    assert len(files) == 3
    
    # 5. Check status
    status = series_gen.get_iteration_status("Test Template")
    assert all(status[i] for i in range(1, 4))
