from fastapi import FastAPI
from app.routers import security_scan, database_scan


app = FastAPI(
    title="Enhanced Website Security Scanner",
    description="API for website security and database vulnerability scanning with authentication and improved error handling.",
    version="1.1.0",
)


app.include_router(security_scan.router, prefix="/security", tags=["Security Scan"])
app.include_router(database_scan.router, prefix="/database", tags=["Database Scan"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Enhanced Website Security Scanner API. Ensure you have proper authorization to scan any website."}
