
from datetime import datetime
from typing import Dict,Optional
from sqlalchemy.orm import Session
from . import models

def annotate_path(session: Session,
        host_name: str, path_name: str,
        annotation: str, author: Optional[str] = None)-> None:
    """
    Annotate a host_name/path_name, adding the annotation to the database.
    """

    path = get_or_create_path(session, host_name, path_name)
    path.annotation = annotation
    path.last_edited = datetime.now()
    if author:
        path.annotation_author = author

def get_annotation(session: Session, host_name: str, path_name: str) -> str:
    """
    Get the annotation registered for host_name/path_name.
    If no annotation exists, returns an empty string.
    """

    try:
        assert (path := session.query(models.Path).get((path_name, host_name))) is not None
    except AssertionError:
        return ""
    else:
        return path.annotation

def get_or_create_path(session: Session, host_name: str, path_name: str)-> models.Path:
    try:
        assert (host := session.query(models.Host).get(host_name)) is not None
    except AssertionError:
        host = models.Host(name = host_name)
        session.add(host)
    try:
        path,*_ = [p for p in host.paths if p.name == path_name]
    except ValueError:
        path = models.Path(name = path_name)
        session.add(path)
        host.paths.append(path)
    return path

def list_annotations(session: Session, host_name: str) -> Dict[str,str]:
    try:
        assert (host := session.query(models.Host).get(host_name)) is not None
    except AssertionError:
        return {}
    else:
        return {path.name: path.annotation for path in host.paths}

def delete_action(model):
    def delete(session: Session, id) -> None:
        instance = session.query(model).get(id)
        session.delete(instance)
    return delete

delete_host = delete_action(models.Host)
delete_path = delete_action(models.Path)
