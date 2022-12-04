"""TaskStatistic

Revision ID: 5365d581e37c
Revises: 88baa0b43fe1
Create Date: 2021-11-10 19:20:11.211943

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy.engine import Inspector

revision = "5365d581e37c"
down_revision = "88baa0b43fe1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    if not "taskstatistic" in tables:
        op.create_table(
            "taskstatistic",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("task_id", sa.Integer(), nullable=False),
            sa.Column("base_task_id", sa.Integer(), nullable=True),
            sa.Column("solved_date", sa.DateTime(), nullable=False),
            sa.Column(
                "percentage_solved",
                sa.Numeric(precision=5, scale=2),
                server_default=sa.text("0"),
                nullable=True,
            ),
            sa.Column("solution_data", sa.JSON(), nullable=False),
            sa.Column("task_result", sa.JSON(), nullable=True),
            sa.ForeignKeyConstraint(
                ["base_task_id"],
                ["basetask.id"],
            ),
            sa.ForeignKeyConstraint(
                ["task_id"],
                ["task.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("taskstatistic")
    # ### end Alembic commands ###