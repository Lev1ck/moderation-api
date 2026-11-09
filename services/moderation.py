from repositories.moderation import ModerationRepository
from schemas.moderation import PredictionRequest


class ModerationService:
    def __init__(self, repository: ModerationRepository):
        self.repository = repository

    def predict(self, ad: PredictionRequest) -> bool:
        return not (
            ad.is_verified_seller
            or ad.images_qty >= self.repository.get_min_images_qty()
        )
