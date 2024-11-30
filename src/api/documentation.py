"""Documentation API endpoints with security measures."""

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, List, Optional
from pydantic import BaseModel

from ..domain.documentation.doc_handler import (
    DocumentationHandler,
    DocumentMetadata
)
from ..domain.security.middleware import SecurityMiddleware
from ..domain.security.rate_limiter import RateLimiter

router = APIRouter(prefix="/docs", tags=["documentation"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_middleware = SecurityMiddleware()

# Initialize doc handler with configured paths
doc_handler = DocumentationHandler(
    templates_dir="docs/templates",
    output_dir="docs/generated"
)

class DocumentRequest(BaseModel):
    """Request model for document creation/update."""
    template_name: str
    metadata: Dict
    content_vars: Dict

@router.post("/create")
async def create_document(
    request: DocumentRequest,
    token: str = Depends(oauth2_scheme)
):
    """Create a new document from template."""
    # Validate token and get user info
    user_id = await security_middleware.validate_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        # Convert request metadata to DocumentMetadata
        metadata = DocumentMetadata(**request.metadata)
        
        # Create document
        doc_path = await doc_handler.create_document(
            template_name=request.template_name,
            metadata=metadata,
            content_vars=request.content_vars,
            user_id=user_id
        )
        
        return {"status": "success", "doc_path": doc_path}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update/{doc_id}")
async def update_document(
    doc_id: str,
    request: DocumentRequest,
    token: str = Depends(oauth2_scheme)
):
    """Update an existing document."""
    # Validate token and get user info
    user_id = await security_middleware.validate_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        # Convert request metadata to DocumentMetadata
        metadata = DocumentMetadata(**request.metadata)
        
        # Update document
        doc_path = await doc_handler.update_document(
            doc_id=doc_id,
            metadata=metadata,
            content_vars=request.content_vars,
            user_id=user_id
        )
        
        return {"status": "success", "doc_path": doc_path}
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def list_templates(token: str = Depends(oauth2_scheme)):
    """List available document templates."""
    # Validate token
    if not await security_middleware.validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {
        "templates": list(doc_handler.config["templates"].keys())
    }

@router.get("/validate/{template_name}")
async def validate_template(
    template_name: str,
    token: str = Depends(oauth2_scheme)
):
    """Validate a template."""
    # Validate token
    if not await security_middleware.validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    is_valid = doc_handler._validate_template(template_name)
    return {
        "template": template_name,
        "valid": is_valid
    }
