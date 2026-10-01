"""add metrics_job_runner table

Revision ID: a1b2c3d4e5f6
Revises: 43eff8f33449
Create Date: 2026-10-01 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '43eff8f33449'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('metrics_job_runner',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pipeline_id', sa.Integer(), nullable=False),
        sa.Column('job_name', sa.String(), nullable=False),
        sa.Column('system_id', sa.String(), nullable=True),
        sa.Column('cpu_count', sa.Integer(), nullable=True),
        sa.Column('cpu_model', sa.String(), nullable=True),
        sa.Column('cores_per_socket', sa.Integer(), nullable=True),
        sa.Column('threads_per_core', sa.Integer(), nullable=True),
        sa.Column('ram_total_mb', sa.Integer(), nullable=True),
        sa.Column('ram_available_mb', sa.Integer(), nullable=True),
        sa.Column('queued_duration', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pipeline_id', 'job_name'),
    )
    op.create_index('idx_metrics_job_runner_pipeline', 'metrics_job_runner', ['pipeline_id'])
    op.create_index('idx_metrics_job_runner_system', 'metrics_job_runner', ['system_id'])


def downgrade():
    op.drop_index('idx_metrics_job_runner_system', table_name='metrics_job_runner')
    op.drop_index('idx_metrics_job_runner_pipeline', table_name='metrics_job_runner')
    op.drop_table('metrics_job_runner')
