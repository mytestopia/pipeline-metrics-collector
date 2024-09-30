"""empty message

Revision ID: 6cb8792ac0d6
Revises: 2da9b84e3a49
Create Date: 2022-08-31 03:21:22.771868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cb8792ac0d6'
down_revision = '2da9b84e3a49'
branch_labels = None
depends_on = None


def upgrade():
    new_table = op.create_table('metrics_build',
                                sa.Column('id', sa.Integer(), nullable=False),
                                sa.Column('pipeline_id', sa.Integer(), nullable=True),
                                sa.Column('name', sa.String(), nullable=True),
                                sa.Column('duration', sa.Integer(), nullable=True),
                                sa.PrimaryKeyConstraint('id')
                                )
    conn = op.get_bind()
    res = conn.execute("select pipeline_id, duration_build from metrics_pipeline")
    results = res.fetchall()

    old_info = [{'pipeline_id': r[0], 'duration': r[1], 'name': 'build-e2e'} for r in results]

    # Insert old_info into new table.
    op.bulk_insert(new_table, old_info)


def downgrade():
    op.drop_table('metrics_build')




