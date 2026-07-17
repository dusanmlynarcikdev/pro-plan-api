"""rename subscription table to customer

Revision ID: dc08123bde2c
Revises: e9edfee3741b
Create Date: 2026-07-17 08:46:32.889748

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc08123bde2c"
down_revision: str | Sequence[str] | None = "e9edfee3741b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("subscription", "customer")
    op.alter_column("customer", "is_active", new_column_name="has_pro")
    op.alter_column("customer", "stripe_customer_id", new_column_name="stripe_id")
    op.execute(
        "ALTER TABLE customer RENAME CONSTRAINT subscription_pkey TO customer_pkey"
    )
    op.execute(
        "ALTER TABLE customer RENAME CONSTRAINT uq_subscription_email TO c_ui_email"
    )
    op.execute(
        "ALTER TABLE customer RENAME CONSTRAINT uq_stripe_customer_id TO c_ui_stripe_id"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE customer RENAME CONSTRAINT c_ui_stripe_id TO uq_stripe_customer_id"
    )
    op.execute(
        "ALTER TABLE customer RENAME CONSTRAINT c_ui_email TO uq_subscription_email"
    )
    op.execute(
        "ALTER TABLE customer RENAME CONSTRAINT customer_pkey TO subscription_pkey"
    )
    op.alter_column("customer", "stripe_id", new_column_name="stripe_customer_id")
    op.alter_column("customer", "has_pro", new_column_name="is_active")
    op.rename_table("customer", "subscription")
