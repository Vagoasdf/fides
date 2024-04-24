"""migrate to usage of evaluation violations

Revision ID: 312aff72b275
Revises: 45c7a349db68
Create Date: 2021-12-15 15:53:46.484775

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "312aff72b275"
down_revision = "45c7a349db68"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("evaluations", sa.Column("violations", sa.JSON(), nullable=True))
    op.drop_column("evaluations", "details")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "evaluations",
        sa.Column(
            "details",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("evaluations", "violations")
    # ### end Alembic commands ###
