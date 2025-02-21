from app import db


class ProjectSchedule(db.Model):
    __tablename__ = 'project_schedule'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    project_id = db.Column("project_id", db.ForeignKey("project.id"), nullable=False)

    def __init__(self, name, is_active, project_id):
        self.name = name
        self.is_active = is_active
        self.project_id = project_id

    def __repr__(self):
        return (f'ProjectSchedule <id={self.id}, name={self.name}, is_active={self.is_active}'
                f'project_id={self.project_id}>')
