from app import db


class JobRunner(db.Model):
    __tablename__ = 'metrics_job_runner'

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, nullable=False)
    job_name = db.Column(db.String, nullable=False)
    system_id = db.Column(db.String)
    cpu_count = db.Column(db.Integer)
    cpu_model = db.Column(db.String)
    cores_per_socket = db.Column(db.Integer)
    threads_per_core = db.Column(db.Integer)
    ram_total_mb = db.Column(db.Integer)
    ram_available_mb = db.Column(db.Integer)
    queued_duration = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint('pipeline_id', 'job_name'),
    )

    def __init__(self, pipeline_id, job_name, system_id=None, cpu_count=None,
                 cpu_model=None, cores_per_socket=None, threads_per_core=None,
                 ram_total_mb=None, ram_available_mb=None, queued_duration=None):
        self.pipeline_id = pipeline_id
        self.job_name = job_name
        self.system_id = system_id
        self.cpu_count = cpu_count
        self.cpu_model = cpu_model
        self.cores_per_socket = cores_per_socket
        self.threads_per_core = threads_per_core
        self.ram_total_mb = ram_total_mb
        self.ram_available_mb = ram_available_mb
        self.queued_duration = queued_duration

    def __repr__(self):
        return '<JobRunner pipeline_id={} job_name={}>'.format(self.pipeline_id, self.job_name)
