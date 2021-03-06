"""First commit

Revision ID: 9586bf705fdf
Revises: 7047f90165ed
Create Date: 2021-09-15 14:57:38.094475

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "9586bf705fdf"
down_revision = "7047f90165ed"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if "user" not in tables:
        op.create_table(
            "user",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("firstname", sa.String(length=255), nullable=True),
            sa.Column("middlename", sa.String(length=255), nullable=True),
            sa.Column("lastname", sa.String(length=255), nullable=True),
            sa.Column("hashed_password", sa.String(length=255), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=True),
            sa.Column("is_superuser", sa.Boolean(), nullable=True),
            sa.Column("last_login", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
        op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)

    if "course" not in tables:
        op.create_table(
            "course",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("short_name", sa.String(length=255), nullable=True),
            sa.Column("created", sa.DateTime(), nullable=True),
            sa.Column("owner_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["owner_id"],
                ["user.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )
        op.create_index(op.f("ix_course_id"), "course", ["id"], unique=False)
        op.create_index(
            op.f("ix_course_short_name"), "course", ["short_name"], unique=False
        )

    if "coursemembers" not in tables:
        op.create_table(
            "coursemembers",
            sa.Column("course_id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ["course_id"],
                ["course.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.id"],
            ),
            sa.PrimaryKeyConstraint("course_id", "user_id"),
        )
    if "taskgroup" not in tables:
        op.create_table(
            "taskgroup",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("short_name", sa.String(length=255), nullable=True),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("course_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["course_id"],
                ["course.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_taskgroup_id"), "taskgroup", ["id"], unique=False)
        op.create_index(
            op.f("ix_taskgroup_short_name"), "taskgroup", ["short_name"], unique=False
        )

    if "basetask" not in tables:
        op.create_table(
            "basetask",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("course_id", sa.Integer(), nullable=True),
            sa.Column("task_group_id", sa.Integer(), nullable=True),
            sa.Column("enabled", sa.Boolean(), nullable=True),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("short_name", sa.String(length=255), nullable=True),
            sa.Column("slide_id", sa.String(length=255), nullable=True),
            sa.ForeignKeyConstraint(
                ["course_id"],
                ["course.id"],
            ),
            sa.ForeignKeyConstraint(
                ["task_group_id"],
                ["taskgroup.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_basetask_id"), "basetask", ["id"], unique=False)
        op.create_index(op.f("ix_basetask_name"), "basetask", ["name"], unique=False)
        op.create_index(
            op.f("ix_basetask_short_name"), "basetask", ["short_name"], unique=False
        )
        op.create_index(
            op.f("ix_basetask_slide_id"), "basetask", ["slide_id"], unique=False
        )

    if "newtask" not in tables:
        op.create_table(
            "newtask",
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("base_task_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ["base_task_id"],
                ["basetask.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.id"],
            ),
            sa.PrimaryKeyConstraint("user_id", "base_task_id"),
        )

    if "task" not in tables:
        op.create_table(
            "task",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("layer", sa.Integer(), nullable=False),
            sa.Column("base_task_id", sa.Integer(), nullable=True),
            sa.Column("task_type", sa.Integer(), nullable=True),
            sa.Column("annotation_type", sa.Integer(), nullable=False),
            sa.Column("min_correct", sa.Integer(), nullable=False),
            sa.Column("task_question", sa.String(length=255), nullable=True),
            sa.Column("knowledge_level", sa.Integer(), nullable=True),
            sa.Column("solution", sa.JSON(), nullable=True),
            sa.Column("task_data", sa.JSON(), nullable=True),
            sa.Column("annotation_groups", sa.JSON(), nullable=True),
            sa.ForeignKeyConstraint(
                ["base_task_id"],
                ["basetask.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_task_id"), "task", ["id"], unique=False)

    if "usersolution" not in tables:
        op.create_table(
            "usersolution",
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("task_id", sa.Integer(), nullable=False),
            sa.Column(
                "percentage_solved", sa.Numeric(precision=5, scale=2), nullable=True
            ),
            sa.Column("base_task_id", sa.Integer(), nullable=True),
            sa.Column("task_group_id", sa.Integer(), nullable=True),
            sa.Column("course_id", sa.Integer(), nullable=True),
            sa.Column("solution_data", sa.JSON(), nullable=False),
            sa.Column("task_result", sa.JSON(), nullable=True),
            sa.ForeignKeyConstraint(
                ["base_task_id"],
                ["basetask.id"],
            ),
            sa.ForeignKeyConstraint(
                ["course_id"],
                ["course.id"],
            ),
            sa.ForeignKeyConstraint(
                ["task_group_id"],
                ["taskgroup.id"],
            ),
            sa.ForeignKeyConstraint(
                ["task_id"],
                ["task.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.id"],
            ),
            sa.PrimaryKeyConstraint("user_id", "task_id"),
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("usersolution")
    op.drop_index(op.f("ix_task_id"), table_name="task")
    op.drop_table("task")
    op.drop_table("newtask")
    op.drop_index(op.f("ix_basetask_slide_id"), table_name="basetask")
    op.drop_index(op.f("ix_basetask_short_name"), table_name="basetask")
    op.drop_index(op.f("ix_basetask_name"), table_name="basetask")
    op.drop_index(op.f("ix_basetask_id"), table_name="basetask")
    op.drop_table("basetask")
    op.drop_index(op.f("ix_taskgroup_short_name"), table_name="taskgroup")
    op.drop_index(op.f("ix_taskgroup_id"), table_name="taskgroup")
    op.drop_table("taskgroup")
    op.drop_table("coursemembers")
    op.drop_index(op.f("ix_course_short_name"), table_name="course")
    op.drop_index(op.f("ix_course_id"), table_name="course")
    op.drop_table("course")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
