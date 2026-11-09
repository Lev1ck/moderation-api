from fastapi import APIRouter, Depends, HTTPException

from repositories.moderation import ModerationRepository
from schemas.moderation import PredictionRequest
from services.moderation import ModerationService

router = APIRouter()


def get_service() -> ModerationService:
    return ModerationService(ModerationRepository())


@router.post(
    "/predict",
    response_model=bool,
    responses={400: {"description": "Invalid request"}, 500: {"description": "Prediction failed"}},
)
async def predict(ad: PredictionRequest, service: ModerationService = Depends(get_service)) -> bool:
    try:
        return service.predict(ad)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
