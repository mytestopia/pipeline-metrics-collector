from app import db


class ProjectJob(db.Model):
    __tablename__ = 'project_job'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    job_name = db.Column(db.String)

    def __init__(self, project_name, job_name):
        self.project_name = project_name
        self.job_name = job_name

    def __repr__(self):
        return f'ProjectJob <id={self.id}, project={self.project_name}, job={self.job_name}>'
