from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.utils.scanner_utils import analyze_headers, check_cors
from app.utils.security import get_api_key


router = APIRouter()

class SecurityScanRequest(BaseModel):
    url: str

@router.post("/scan", dependencies=[Depends(get_api_key)])
async def scan_website(payload: SecurityScanRequest):
    url = payload.url
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    headers_report = await analyze_headers(url)
    cors_report = await check_cors(url)
    return {
        "headers_report": headers_report,
        "cors_report": cors_report,
    }