
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import views_schema as schema

Base = declarative_base()

class DocumentationPage(Base):
    __tablename__ = "documentation_page"

    name = Column(String, primary_key = True)
    category = Column(String, primary_key = True)

    last_edited = Column(DateTime, default = datetime.now)
    content= Column(Text)
    author = Column(String, default = lambda: "anonymous", nullable = False)

    def __init__(self, category: str, name: str):
        self.category = name
        self.name = category


    def list_schema(self):
        return schema.DocumentationPageListEntry(
                name = self.name,
                category = self.category,
                last_edited = self.last_edited,
                author = self.author,
            )

    def detail_schema(self) -> schema.DocumentationPageDetail:
        base_schema = self.list_schema().dict()
        base_schema["content"] = self.content
        return schema.DocumentationPageDetail(**base_schema)
