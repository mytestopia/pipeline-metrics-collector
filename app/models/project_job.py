from app import db


class ProjectJob(db.Model):
    __tablename__ = 'project_job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    project_id = db.Column("project_id", db.ForeignKey("project.id"), nullable=False)

    def __init__(self, name, project_id):
        self.name = name
        self.project_id = project_id

    def __repr__(self):
        return f'ProjectJob <id={self.id}, name={self.name}, project_id={self.project_id}>'
