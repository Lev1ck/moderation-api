from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("verified", "images_qty", "expected"),
    [(True, 0, False), (True, 2, False), (False, 1, False), (False, 0, True)],
)
def test_prediction(ad_payload, verified, images_qty, expected):
    response = client.post(
        "/predict",
        json={**ad_payload, "is_verified_seller": verified, "images_qty": images_qty},
    )
    assert response.status_code == 200
    assert response.json() is expected


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seller_id", "10"),
        ("seller_id", True),
        ("is_verified_seller", "false"),
        ("item_id", 1.5),
        ("name", 123),
        ("description", None),
        ("category", False),
        ("images_qty", "1"),
        ("images_qty", -1),
    ],
)
def test_invalid_values(ad_payload, field, value):
    response = client.post("/predict", json={**ad_payload, field: value})
    assert response.status_code == 400
    assert response.json()["detail"]


@pytest.mark.parametrize(
    "field",
    ["seller_id", "is_verified_seller", "item_id", "name", "description", "category", "images_qty"],
)
def test_missing_required_field(ad_payload, field):
    ad_payload.pop(field)
    response = client.post("/predict", json=ad_payload)
    assert response.status_code == 400


def test_extra_field(ad_payload):
    response = client.post("/predict", json={**ad_payload, "unexpected": "value"})
    assert response.status_code == 400


def test_invalid_json():
    response = client.post(
        "/predict", content="{invalid", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400


def test_business_logic_error(ad_payload):
    with patch("routers.predict.ModerationService.predict", side_effect=RuntimeError("secret")):
        response = client.post("/predict", json=ad_payload)
    assert response.status_code == 500
    assert response.json() == {"detail": "Prediction failed"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
