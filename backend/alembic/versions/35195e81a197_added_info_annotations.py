"""Added info annotations

Revision ID: 35195e81a197
Revises: 1b342ac080d3
Create Date: 2021-12-16 22:16:10.685002

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "35195e81a197"
down_revision = "1b342ac080d3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.add_column("task", sa.Column("info_annotations", sa.JSON(), nullable=True))
    except Exception as e:
        print(e)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("task", "info_annotations")
    # ### end Alembic commands ###
