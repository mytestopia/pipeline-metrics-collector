from app import db


class ProjectSchedule(db.Model):
    __tablename__ = 'project_schedule'

    id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String)
    project_name = db.Column(db.String)
    is_active = db.Column(db.Boolean)

    def __init__(self, schedule_name, project_name, is_active):
        self.schedule_name = schedule_name
        self.project_name = project_name
        self.is_active = is_active

    def __repr__(self):
        return (f'ProjectSchedule <id={self.id}, schedule_name={self.schedule_name}, project={self.project_name}, '
                f'is_active={self.is_active}>')
