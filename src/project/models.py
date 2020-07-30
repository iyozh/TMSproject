import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from path import PROJECTS
from project.settings import REPO_DIR


@dataclass
class Model:
    project_id:Optional[str] = None

    __json_file__ = None


    __storage__ = REPO_DIR / "storage"

    @classmethod
    def load(cls):
        try:
            with PROJECTS.open("r", encoding="utf-8") as fp:
             return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}


    @classmethod
    def all(cls):
        projects_content = cls.load()
        projects = []

        for id in projects_content:
            project = {
                "project_id": id,
                "project_name": projects_content[id]["project_name"],
                "started": projects_content[id]["started"],
                "ended": projects_content[id]["ended"],
                "project_description": projects_content[id]["project_description"],
            }
            projects.append(project)

        return projects

    # @classmethod
    # def source(cls) -> Path:
    #     if not cls.__json_file__:
    #         raise TypeError(f"unbound source for {cls}")
    #     src = (cls.__storage__ / cls.__json_file__).resolve()
    #     return src

