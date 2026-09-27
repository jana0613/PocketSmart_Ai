import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from ..dependencies import get_current_user
from ..models.schemas import HomeRequest, PartyRequest, JewelryRequest
from ..services.recommender import Recommender
from ..db import save_recommendation
from ..config import get_settings

router = APIRouter(prefix="/api/planners", tags=["Planners"])
recommender = Recommender()

async def image_data(file: UploadFile | None):
    if not file:
        return None, None
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG and WEBP images are supported")
    data = await file.read()
    max_bytes = get_settings().max_upload_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Image is larger than {get_settings().max_upload_mb} MB")
    return data, file.content_type

@router.post("/home")
def home(data: HomeRequest, user=Depends(get_current_user)):
    payload = data.model_dump()
    result = recommender.recommend("home", payload)
    rec_id = save_recommendation(int(user["sub"]), "home", json.dumps(payload), json.dumps(result))
    result["history_id"] = rec_id
    return result

@router.post("/party")
def party(data: PartyRequest, user=Depends(get_current_user)):
    payload = data.model_dump()
    result = recommender.recommend("party", payload)
    rec_id = save_recommendation(int(user["sub"]), "party", json.dumps(payload), json.dumps(result))
    result["history_id"] = rec_id
    return result

@router.post("/jewelry")
async def jewelry(data: JewelryRequest, user=Depends(get_current_user), outfit_image: UploadFile | None = File(default=None)):
    payload = data.model_dump()
    image_bytes, mime = await image_data(outfit_image)
    result = recommender.recommend("jewelry", payload, image_bytes, mime)
    rec_id = save_recommendation(int(user["sub"]), "jewelry", json.dumps(payload), json.dumps(result))
    result["history_id"] = rec_id
    return result
