from dataclasses import dataclass
from datetime import date
from typing import Optional

from django.db import models

# Create your models here.
from project.models import Model
from project.settings import REPO_DIR


@dataclass
class Project(Model):
    project_name: Optional[str] = None
    started: Optional[str] = None
    ended: Optional[str] = None
    project_description: Optional[str] = None

    __json_file__ = REPO_DIR / "data" / "projects.json"
