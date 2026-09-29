import services.categories as service

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
