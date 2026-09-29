"""seed_categories

Revision ID: a7756283b8cd
Revises: 6de68b22c49e
Create Date: 2026-09-29 15:04:15.322815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7756283b8cd'
down_revision: Union[str, Sequence[str], None] = '6de68b22c49e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CATEGORIES = [
    "Food",
    "Transport",
    "Housing",
    "Utilities",
    "Entertainment",
    "Health",
    "Shopping",
    "Salary",
    "Other",
]

category_table = sa.table(
    "t_category",
    sa.column("category_name", sa.String)
)

def upgrade() -> None:
    op.bulk_insert(
        category_table,
        [{"category_name": name} for name in CATEGORIES]
    )


def downgrade() -> None:
    op.execute(
        category_table.delete().where(
            category_table.c.category_name.in_(CATEGORIES)
        )
    )
