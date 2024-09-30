"""empty message

Revision ID: 2da9b84e3a49
Revises: 
Create Date: 2022-04-25 05:31:51.679804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2da9b84e3a49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metrics_job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('duration_e2e', sa.Integer(), nullable=True),
    sa.Column('duration_up', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metrics_job_failed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metrics_pipeline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=True),
    sa.Column('project', sa.String(), nullable=True),
    sa.Column('duration_build', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('duration_e2e', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_master', sa.Boolean(), nullable=True),
    sa.Column('has_restarts', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pipeline_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('metrics_pipeline')
    op.drop_table('metrics_job_failed')
    op.drop_table('metrics_job')
    # ### end Alembic commands ###
