from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel

class DocumentationPageSchema(BaseModel):
    name: str
    category: str
    last_edited: datetime
    author: Optional[str] = None

class DocumentationPageDetailSchema(DocumentationPageSchema):
    content: str

class PostedDocumentation(BaseModel):
    content: str

class Documentation(BaseModel):
    proxied: Any
    documentation: Optional[DocumentationPageDetailSchema]
