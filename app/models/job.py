from app import db


class Job(db.Model):
    __tablename__ = 'metrics_job'

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer)
    name = db.Column(db.String)
    duration_e2e = db.Column(db.Integer)
    duration_up = db.Column(db.Integer)
    duration_up_without_pull = db.Column(db.Integer)
    duration_pull = db.Column(db.Integer)
    duration = db.Column(db.Integer)

    def __init__(self, pipeline_id, name,
                 duration_e2e, duration_up, duration_up_without_pull, duration_pull,
                 duration):
        self.pipeline_id = pipeline_id
        self.name = name
        self.duration = duration
        self.duration_e2e = duration_e2e
        self.duration_up = duration_up
        self.duration_pull = duration_pull
        self.duration_up_without_pull = duration_up_without_pull

    def __repr__(self):
        return '<id {}>'.format(self.id)
