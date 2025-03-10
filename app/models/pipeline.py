from app import db
from sqlalchemy import DateTime, Boolean


class Pipeline(db.Model):
    __tablename__ = 'metrics_pipeline'

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, unique=True)
    project = db.Column(db.String)
    duration = db.Column(db.Integer)
    duration_e2e = db.Column(db.Integer)
    created_at = db.Column(DateTime)
    is_master = db.Column(Boolean)
    has_restarts = db.Column(Boolean)
    project_id = db.Column("project_id", db.ForeignKey("project.id"), nullable=True)

    def __init__(self, pipeline_id, project, duration, duration_e2e, created_at, ref, has_restarts,
                 project_id):
        self.pipeline_id = pipeline_id
        self.project = project
        self.duration = duration
        self.duration_e2e = duration_e2e
        self.created_at = created_at
        self.is_master = True if ref == 'master' else False
        self.has_restarts = has_restarts
        self.project_id = project_id

    def __repr__(self):
        return '<id {}, pipeline_id {}>'.format(self.id)
