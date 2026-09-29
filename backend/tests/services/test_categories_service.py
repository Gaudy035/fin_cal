from sqlalchemy.orm import Session
from models import Category
import services.categories as service
import pytest

@pytest.fixture
def seed_category(db_session: Session):
    def _seed(name: str = "Food"):
        category = Category(category_name = name)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        return category
    return _seed

def test_get_categories_returns_all_seeded(db_session, seed_category):
    seed_category()
    seed_category("Health")
    seed_category("Transport")

    result = service.get_categories(db_session)
    categories = {c.category_name for c in result}
    assert len(result) == 3
    assert "Food" in categories
    assert "Health" in categories
    assert "Transport" in categories
