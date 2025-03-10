from app import db
from sqlalchemy import Enum
import enum


class ProjectPriority(enum.Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(Enum(ProjectStatus, name="project_status"), nullable=False)
    priority = db.Column(Enum(ProjectPriority, name="project_priority"), nullable=False)
    team_id = db.Column("team_id", db.ForeignKey("team.id"), nullable=False)

    def __init__(self, id, name, status, priority, team_id):
        self.id = id
        self.name = name
        self.status = status
        self.priority = priority
        self.team_id = team_id

    def __repr__(self):
        return f'Project <id={self.id}, name={self.name}, team_id={self.team_id}>'
