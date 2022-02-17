"""Initial schema

Revision ID: 6fbf772f0f35
Revises: 
Create Date: 2022-02-17 20:04:01.137024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6fbf772f0f35"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "character",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("species", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "episode",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("air_date", sa.Date(), nullable=False),
        sa.Column("episode", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "association",
        sa.Column("episode_id", sa.Integer(), nullable=False),
        sa.Column("character_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["character_id"],
            ["character.id"],
        ),
        sa.ForeignKeyConstraint(
            ["episode_id"],
            ["episode.id"],
        ),
        sa.PrimaryKeyConstraint("episode_id", "character_id"),
    )


def downgrade():
    op.drop_table("association")
    op.drop_table("episode")
    op.drop_table("character")
