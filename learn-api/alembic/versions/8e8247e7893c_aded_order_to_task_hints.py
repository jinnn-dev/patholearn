"""Aded order to task hints

Revision ID: 8e8247e7893c
Revises: e321bbcdb4ec
Create Date: 2021-09-22 16:54:37.151818

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8e8247e7893c"
down_revision = "e321bbcdb4ec"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.add_column(
            "taskhint", sa.Column("needed_mistakes", sa.Integer(), nullable=True)
        )
        op.add_column(
            "taskhint", sa.Column("order_position", sa.Integer(), nullable=False)
        )
    except Exception as e:
        print(e)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("taskhint", "order_position")
    op.drop_column("taskhint", "needed_mistakes")
    # ### end Alembic commands ###