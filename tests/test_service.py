import pytest

from repositories.moderation import ModerationRepository
from schemas.moderation import PredictionRequest
from services.moderation import ModerationService


@pytest.mark.parametrize(
    ("verified", "images_qty", "expected"),
    [(True, 0, False), (True, 2, False), (False, 1, False), (False, 0, True)],
)
def test_predict(ad_payload, verified, images_qty, expected):
    ad = PredictionRequest(
        **{**ad_payload, "is_verified_seller": verified, "images_qty": images_qty}
    )
    assert ModerationService(ModerationRepository()).predict(ad) is expected
