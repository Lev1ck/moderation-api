import pytest


@pytest.fixture
def ad_payload():
    return {
        "seller_id": 10,
        "is_verified_seller": False,
        "item_id": 42,
        "name": "Bicycle",
        "description": "Used bicycle",
        "category": 3,
        "images_qty": 1,
    }
