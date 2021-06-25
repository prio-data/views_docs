from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel

class DocumentationPage(BaseModel):
    name: str
    category: str
    last_edited: Optional[datetime]
    author: Optional[str] = None

class DocumentationPageDetail(DocumentationPage):
    content: Optional[str] = None

class PostedDocumentation(BaseModel):
    content: str = ""

class AnnotatedProxiedDocumentation(BaseModel):
    proxied: Any
    documentation: Optional[DocumentationPageDetail] = {"content": ""}

class RemoteLocation(BaseModel):
    path: str
