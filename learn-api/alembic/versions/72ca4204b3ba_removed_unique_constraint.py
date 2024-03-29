"""Removed unique constraint

Revision ID: 72ca4204b3ba
Revises: 2b7444861dd9
Create Date: 2022-12-14 21:02:33.044972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "72ca4204b3ba"
down_revision = "2b7444861dd9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("order", table_name="questionnairequestionoption")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("order", "questionnairequestionoption", ["order"], unique=False)
    # ### end Alembic commands ###
