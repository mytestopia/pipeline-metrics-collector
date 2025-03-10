import datetime
from flask import Flask, request
from flask import Response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://e2e:e2e@db/e2e'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    from .models import (Pipeline, Job, JobFailed, JobBuild, ProjectJob, ProjectSchedule, ProjectPackage,
                         Project, Team, ProjectPriority, ProjectStatus)

    def is_pipeline_stats_exist(session, pipeline_id):
        return bool(session.query(Pipeline).filter_by(pipeline_id=pipeline_id).first())

    def save_items_to_db(model: db.Model, items_to_add: list, items_to_delete: list):
        if items_to_delete:
            ids = [item.id for item in items_to_delete]
            db.session.query(model).filter(model.id.in_(ids)).delete()

        if items_to_add:
            db.session.add_all(items_to_add)

        if items_to_add or items_to_delete:
            db.session.commit()

    def save_new_project_jobs_to_db(json_data: dict):
        jobs_in_db = ProjectJob.query.filter_by(project_id=json_data['project_id']).all()
        job_names_in_db = [job.name for job in jobs_in_db]

        jobs_to_delete = list()
        for job in jobs_in_db:
            if job.name not in json_data['all_e2e_jobs']:
                jobs_to_delete.append(job)

        jobs_to_add = list()
        for job_name in json_data['all_e2e_jobs']:
            if job_name not in job_names_in_db:
                new_job = ProjectJob(name=job_name, project_id=json_data['project_id'])
                jobs_to_add.append(new_job)

        save_items_to_db(ProjectJob, jobs_to_add, jobs_to_delete)

    def save_new_project_schedules_to_db(json_data: dict):
        schedules_in_db = ProjectSchedule.query.filter_by(project_id=json_data['project_id']).all()
        new_schedule_names = [schedule['name'] for schedule in json_data['schedules']]

        schedules_to_delete = list()
        for schedule in schedules_in_db:
            if schedule.name not in new_schedule_names:
                schedules_to_delete.append(schedule)

        schedules_to_add = list()
        is_existing_in_db = False

        for new_schedule in json_data['schedules']:
            for schedule_in_db in schedules_in_db:
                is_existing_in_db = new_schedule['name'] == schedule_in_db.name
                if is_existing_in_db:
                    if new_schedule['is_active'] != schedule_in_db.is_active:
                        schedule_in_db.is_active = new_schedule['is_active']
                        db.session.commit()
                    break

            if not is_existing_in_db:
                schedules_to_add.append(
                    ProjectSchedule(
                        name=new_schedule['name'],
                        is_active=new_schedule['is_active'],
                        project_id=json_data['project_id']
                    )
                )

        save_items_to_db(ProjectSchedule, schedules_to_add, schedules_to_delete)

    def save_new_project_packages_to_db(json_data: dict):
        packages_in_db = ProjectPackage.query.filter_by(project_id=json_data['project_id']).all()
        new_package_names = [package for package, _ in json_data['packages'].items()]

        packages_to_delete = list()
        for package in packages_in_db:
            if package.name not in new_package_names:
                packages_to_delete.append(package)

        packages_to_add = list()
        is_existing_in_db = False

        for new_package, new_version in json_data['packages'].items():
            for package_in_db in packages_in_db:
                is_existing_in_db = new_package == package_in_db.name
                if is_existing_in_db:
                    if new_version != package_in_db.version:
                        package_in_db.version = new_version
                        db.session.commit()
                    break

            if not is_existing_in_db:
                packages_to_add.append(
                    ProjectPackage(
                        name=new_package,
                        version=new_version,
                        project_id=json_data['project_id']
                    )
                )

        save_items_to_db(ProjectPackage, packages_to_add, packages_to_delete)

    def save_new_team_to_db(json_data: dict):
        team = Team.query.filter(Team.name == json_data['team']).first()
        if not team:
            new_team = Team(name=json_data['team'])
            db.session.add(new_team)
            db.session.commit()

    def save_new_project_to_db(json_data: dict):
        project = db.session.get(Project, json_data['project_id'])
        if not project:
            team = Team.query.filter(Team.name == json_data['team']).first()
            new_project = Project(
                id=json_data['project_id'],
                name=json_data['project_name'],
                status=ProjectStatus.ACTIVE,
                priority=ProjectPriority.P0,
                team_id=team.id
            )
            db.session.add(new_project)
            db.session.commit()

    @app.route("/save_metrics", methods=["POST"])
    def save_metrics():
        json_data = request.get_json()
        pipeline_id = json_data['pipeline_id']
        created_at = datetime.datetime.strptime(json_data['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")

        if 'project_id' in json_data and json_data['project_id']:
            project_id = json_data['project_id']
        else:
            project = Project.query.filter(Project.name == json_data['project']).first()
            project_id = project.id if project else None

        if not is_pipeline_stats_exist(db.session, pipeline_id):
            metrics_pipeline = Pipeline(
                pipeline_id=pipeline_id,
                project=json_data['project'],
                duration=json_data['duration'],
                duration_e2e=json_data['duration_e2e'],
                created_at=created_at,
                ref=json_data['ref'],
                has_restarts=json_data['has_restarts'],
                project_id=project_id
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

    @app.route("/save_project_info", methods=["POST"])
    def save_project_info():
        json_data = request.get_json()

        if 'team' not in json_data or not json_data['team']:
            return Response(status=HTTPStatus.BAD_REQUEST,
                            response="Field 'team' is required")

        save_new_team_to_db(json_data)

        if ('project_id' not in json_data or not json_data['project_id'] or
                'project_name' not in json_data or not json_data['project_name']):
            return Response(status=HTTPStatus.BAD_REQUEST,
                            response="Fields 'project_id' and 'project_name' are required")

        save_new_project_to_db(json_data)

        if 'all_e2e_jobs' in json_data and json_data['all_e2e_jobs']:
            save_new_project_jobs_to_db(json_data)

        if 'schedules' in json_data and json_data['schedules']:
            save_new_project_schedules_to_db(json_data)

        if 'packages' in json_data and json_data['packages']:
            save_new_project_packages_to_db(json_data)

        return Response(status=HTTPStatus.OK)

    return app
