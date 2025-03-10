from app import db


class ProjectPackage(db.Model):
    __tablename__ = 'project_package'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)
    project_id = db.Column("project_id", db.ForeignKey("project.id"), nullable=False)

    def __init__(self, name, version, project_id):
        self.name = name
        self.version = version
        self.project_id = project_id

    def __repr__(self):
        return (f'ProjectPackage <id={self.id}, name={self.name}, version={self.version}, '
                f'project_id={self.project_id}>')
