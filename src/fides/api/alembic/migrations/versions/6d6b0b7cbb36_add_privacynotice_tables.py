"""add privacynotice tables

Revision ID: 6d6b0b7cbb36
Revises: 8615ac51e78b
Create Date: 2023-03-22 12:09:47.395190

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6d6b0b7cbb36"
down_revision = "8615ac51e78b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "privacynotice",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("origin", sa.String(), nullable=True),
        sa.Column("regions", sa.ARRAY(sa.String()), nullable=False),
        sa.Column(
            "consent_mechanism",
            sa.Enum("opt_in", "opt_out", "necessary", name="consentmechanism"),
            nullable=False,
        ),
        sa.Column("data_uses", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("version", sa.Float(), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("displayed_in_privacy_center", sa.Boolean(), nullable=False),
        sa.Column("displayed_in_banner", sa.Boolean(), nullable=False),
        sa.Column("displayed_in_privacy_modal", sa.Boolean(), nullable=False),
        sa.Column("enforcement_level", sa.String(), nullable=False),
        sa.Column("has_gpc_flag", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_privacynotice_id"), "privacynotice", ["id"], unique=False)
    op.create_index(
        op.f("ix_privacynotice_regions"), "privacynotice", ["regions"], unique=False
    )
    op.create_table(
        "privacynoticehistory",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("origin", sa.String(), nullable=True),
        sa.Column("regions", sa.ARRAY(sa.String()), nullable=False),
        sa.Column(
            "consent_mechanism",
            sa.Enum("opt_in", "opt_out", "necessary", name="consentmechanism"),
            nullable=False,
        ),
        sa.Column("data_uses", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("version", sa.Float(), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("displayed_in_privacy_center", sa.Boolean(), nullable=False),
        sa.Column("displayed_in_banner", sa.Boolean(), nullable=False),
        sa.Column("displayed_in_privacy_modal", sa.Boolean(), nullable=False),
        sa.Column("enforcement_level", sa.String(), nullable=False),
        sa.Column("has_gpc_flag", sa.Boolean(), nullable=False),
        sa.Column("privacy_notice_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["privacy_notice_id"],
            ["privacynotice.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_privacynoticehistory_id"), "privacynoticehistory", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_privacynoticehistory_regions"),
        "privacynoticehistory",
        ["regions"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_privacynoticehistory_regions"), table_name="privacynoticehistory"
    )
    op.drop_index(op.f("ix_privacynoticehistory_id"), table_name="privacynoticehistory")
    op.drop_table("privacynoticehistory")
    op.drop_index(op.f("ix_privacynotice_regions"), table_name="privacynotice")
    op.drop_index(op.f("ix_privacynotice_id"), table_name="privacynotice")
    op.drop_table("privacynotice")
    # ### end Alembic commands ###

    # specifically drop the enum type since it's not being deleted during table drop
    op.execute("""DROP TYPE consentmechanism""")
