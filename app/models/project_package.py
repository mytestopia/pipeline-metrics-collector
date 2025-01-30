from app import db


class ProjectPackage(db.Model):
    __tablename__ = 'project_package'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    package_name = db.Column(db.String)
    version = db.Column(db.String)

    def __init__(self, project_name, package_name, version):
        self.project_name = project_name
        self.package_name = package_name
        self.version = version

    def __repr__(self):
        return (f'ProjectPackage <id={self.id}, project={self.project_name}, package={self.package_name}, '
                f'version={self.version}>')
