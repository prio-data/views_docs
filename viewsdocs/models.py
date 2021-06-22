
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class DocumentationPageSchema(BaseModel):
    name: str
    category: str
    last_edited: datetime
    author: Optional[str] = None

class DocumentationPageDetailSchema(DocumentationPageSchema):
    content: str

class DocumentationPage(Base):
    __tablename__ = "documentation_page"

    name = Column(String, primary_key = True)
    category = Column(String, primary_key = True)

    last_edited = Column(DateTime, default = datetime.now)
    content= Column(Text)
    author = Column(String)

    def __init__(self, category: str, name: str):
        self.category = name
        self.name = category


    def list_schema(self):
        return DocumentationPageSchema(
                name = self.name,
                category = self.category,
                last_edited = self.last_edited,
                author = self.author,
            )

    def detail_schema(self):
        return DocumentationPageDetailSchema(
                name = self.name,
                category = self.category,
                last_edited = self.last_edited,
                author = self.author,
                content = self.content,
            )
