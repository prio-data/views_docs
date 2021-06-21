
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Path(Base):
    __tablename__ = "path"
    name = Column(String, primary_key = True)
    host_name = Column(ForeignKey("host.name"), primary_key = True)

    last_edited = Column(DateTime, default = datetime.now)
    annotation = Column(Text)
    author = Column(String)

class Host(Base):
    __tablename__ = "host"
    name = Column(String, primary_key = True)
    paths = relationship(Path, cascade = "all, delete-orphan")
