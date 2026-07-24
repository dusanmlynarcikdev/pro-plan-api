"""replace email with external id

Revision ID: b7c31f04a9e2
Revises: dc08123bde2c
Create Date: 2026-07-17 10:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7c31f04a9e2"
down_revision: str | Sequence[str] | None = "dc08123bde2c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("customer", "email", new_column_name="external_id")
    op.execute("ALTER TABLE customer RENAME CONSTRAINT c_ui_email TO c_ui_external_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE customer RENAME CONSTRAINT c_ui_external_id TO c_ui_email")
    op.alter_column("customer", "external_id", new_column_name="email")
