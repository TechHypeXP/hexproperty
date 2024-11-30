# HexProperty Template Management System

A comprehensive solution for managing enterprise documentation templates with advanced deployment, versioning, and dependency tracking capabilities.

## Features

- **Template Processing**: Deploy templates with metadata injection and relationship management
- **Dependency Management**: Validate and track document dependencies
- **Version Control**: Git integration for template version tracking
- **Deployment History**: Track and manage template deployments
- **Rollback Support**: Easily rollback to previous template versions
- **Command-line Interface**: User-friendly CLI for system interaction

## Installation

1. Ensure Python 3.8+ is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `config.yaml` file with the following settings:

```yaml
templates_dir: "templates"
deployment_history_path: "deployment_history.json"
git_repo_path: "."
default_hooks:
  pre_deploy: "scripts/hooks/pre_deploy.py"
  post_deploy: "scripts/hooks/post_deploy.py"
max_history_entries: 100
default_department: "Engineering"
default_classification: "internal"
```

## Usage

### Command-line Interface

1. Deploy a template:
   ```bash
   python -m template_system.cli deploy architecture docs/auth-service.md \
       --doc-id AUTH-001 \
       --title "Authentication Service Architecture" \
       --author "John Doe" \
       --department "Engineering"
   ```

2. View deployment history:
   ```bash
   python -m template_system.cli history
   ```

3. Rollback a deployment:
   ```bash
   python -m template_system.cli rollback docs/auth-service.md
   ```

### Python API

```python
from pathlib import Path
from template_system.core import TemplateManager
from template_system.models import DocumentMetadataModel, DocumentStatus

# Initialize template manager
manager = TemplateManager(Path("config.yaml"))

# Create metadata
metadata = DocumentMetadataModel(
    doc_id="AUTH-001",
    version="1.0.0",
    status=DocumentStatus.DRAFT,
    author="John Doe",
    department="Engineering"
)

# Deploy template
record = manager.deploy_template(
    template_type="architecture",
    target_path=Path("docs/auth-service.md"),
    metadata=metadata
)
```

## Template Format

Templates use a YAML front matter for metadata and support relationship definitions:

```markdown
---
doc_id: [doc_id]
version: [version]
status: [status]
created_date: [created_date]
author: [author]
department: [department]
classification: [classification]
---

# [Title]

## Overview
[Content goes here]

## Dependencies
[Dependencies section will be automatically populated]

## References
[References will be automatically populated]
```

## Development

### Project Structure

```
template_system/
├── __init__.py
├── cli.py
├── core.py
├── models.py
├── services.py
├── config.yaml
└── templates/
    └── architecture.md
```

### Adding New Features

1. Define models in `models.py`
2. Implement service logic in `services.py`
3. Update core functionality in `core.py`
4. Add CLI commands in `cli.py`

### Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
