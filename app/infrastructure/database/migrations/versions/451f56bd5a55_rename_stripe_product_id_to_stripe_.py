"""rename stripe product id to stripe subscription product id

Revision ID: 451f56bd5a55
Revises: b2930cf7aa1b
Create Date: 2026-07-31 15:15:22.139462

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "451f56bd5a55"
down_revision: str | Sequence[str] | None = "b2930cf7aa1b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "customer",
        "stripe_product_id",
        new_column_name="stripe_subscription_product_id",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "customer",
        "stripe_subscription_product_id",
        new_column_name="stripe_product_id",
    )
