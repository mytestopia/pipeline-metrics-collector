from app import db


class JobFailed(db.Model):
    __tablename__ = 'metrics_job_failed'

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer)
    name = db.Column(db.String)
    duration = db.Column(db.Integer)

    def __init__(self, pipeline_id, name, duration):
        self.pipeline_id = pipeline_id
        self.name = name
        self.duration = duration

    def __repr__(self):
        return '<id {}>'.format(self.id)
