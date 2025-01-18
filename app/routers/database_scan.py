from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.utils.scanner_utils import scan_database
from app.utils.security import get_api_key


router = APIRouter()

class DatabaseScanRequest(BaseModel):
    url: str


@router.post("/scan", dependencies=[Depends(get_api_key)])
async def check_database(payload: DatabaseScanRequest):
    url = payload.url
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    db_info = await scan_database(url)
    return db_info 
