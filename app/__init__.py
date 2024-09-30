from http import HTTPStatus
import datetime

from flask import Flask, request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://e2e:e2e@db/e2e'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    from .models import Pipeline, Job, JobFailed, JobBuild

    def is_pipeline_stats_exist(session, pipeline_id):
        return bool(session.query(Pipeline).filter_by(pipeline_id=pipeline_id).first())

    @app.route("/save_metrics", methods=["POST"])
    def save_metrics():
        json_data = request.get_json()

        pipeline_id = json_data['pipeline_id']
        created_at = datetime.datetime.strptime(json_data['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")

        if not is_pipeline_stats_exist(db.session, pipeline_id):
            metrics_pipeline = Pipeline(
                pipeline_id=pipeline_id,
                project=json_data['project'],
                duration=json_data['duration'],
                duration_e2e=json_data['duration_e2e'],
                created_at=created_at,
                ref=json_data['ref'],
                has_restarts=json_data['has_restarts']
            )
            db.session.add(metrics_pipeline)

            if 'builds' in json_data.keys():
                for build in json_data['builds']:
                    name = list(build.keys())[0]
                    metrics_build = JobBuild(
                        pipeline_id=pipeline_id,
                        name=name,
                        duration=build[name]
                    )
                    db.session.add(metrics_build)
            else:
                metrics_build = JobBuild(
                    pipeline_id=pipeline_id,
                    name='build-e2e',
                    duration=json_data['build']
                )
                db.session.add(metrics_build)

            for job in json_data['jobs']:
                metrics_job = Job(
                    name=job['name'],
                    pipeline_id=pipeline_id,
                    duration=job['duration'],
                    duration_up=job.get('up'),
                    duration_e2e=job.get('e2e'),
                    duration_pull=job.get('pull'),
                    duration_up_without_pull=job.get('up_without_pull'),
                )
                db.session.add(metrics_job)

            for job in json_data['jobs_failed']:
                metrics_job_failed = JobFailed(
                    name=job['name'],
                    pipeline_id=pipeline_id,
                    duration=job['duration']
                )
                db.session.add(metrics_job_failed)

            db.session.commit()
            return Response(status=HTTPStatus.OK)

        return Response(status=HTTPStatus.ALREADY_REPORTED)

    return app
