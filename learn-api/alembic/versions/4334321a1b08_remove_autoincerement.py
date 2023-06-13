"""Remove autoincerement

Revision ID: 4334321a1b08
Revises: 7380dae01035
Create Date: 2023-04-30 09:26:55.598664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4334321a1b08"
down_revision = "7380dae01035"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("course_ibfk_1", "course", type_="foreignkey")
    op.create_foreign_key(None, "course", "user", ["owner_id"], ["id"])
    op.drop_constraint("coursemembers_ibfk_2", "coursemembers", type_="foreignkey")
    op.create_foreign_key(None, "coursemembers", "user", ["user_id"], ["id"])
    op.drop_constraint("newtask_ibfk_2", "newtask", type_="foreignkey")
    op.create_foreign_key(None, "newtask", "user", ["user_id"], ["id"])
    op.drop_constraint(
        "questionnaireanswer_ibfk_2", "questionnaireanswer", type_="foreignkey"
    )
    op.create_foreign_key(None, "questionnaireanswer", "user", ["user_id"], ["id"])
    op.drop_constraint("taskstatistic_ibfk_3", "taskstatistic", type_="foreignkey")
    op.create_foreign_key(None, "taskstatistic", "user", ["user_id"], ["id"])
    op.drop_constraint("usersolution_ibfk_5", "usersolution", type_="foreignkey")
    op.create_foreign_key(None, "usersolution", "user", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "usersolution", type_="foreignkey")
    op.create_foreign_key(
        "usersolution_ibfk_5",
        "usersolution",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "taskstatistic", type_="foreignkey")
    op.create_foreign_key(
        "taskstatistic_ibfk_3",
        "taskstatistic",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "questionnaireanswer", type_="foreignkey")
    op.create_foreign_key(
        "questionnaireanswer_ibfk_2",
        "questionnaireanswer",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "newtask", type_="foreignkey")
    op.create_foreign_key(
        "newtask_ibfk_2", "newtask", "user", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint(None, "coursemembers", type_="foreignkey")
    op.create_foreign_key(
        "coursemembers_ibfk_2",
        "coursemembers",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "course", type_="foreignkey")
    op.create_foreign_key(
        "course_ibfk_1", "course", "user", ["owner_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###
