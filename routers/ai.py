from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_service import predict_status

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class TagRequest(BaseModel):
    note: str


@router.post("/tag-suggestion")
def tag_suggestion(request: TagRequest):
    prediction = predict_status(request.note)

    return {
    "success": True,
    "suggested_status": prediction,
    "message": "Prediction completed successfully."
}