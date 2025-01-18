import httpx
import re


async def analyze_headers(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.head(url, timeout=10.0)
        headers = response.headers
    return {
        "Content-Security-Policy": headers.get("Content-Security-Policy", "Missing"),
        "Strict-Transport-Security": headers.get("Strict-Transport-Security", "Missing"),
        "X-Content-Type-Options": headers.get("X-Content-Type-Options", "Missing"),
        "X-Frame-Options": headers.get("X-Frame-Options", "Missing"),
    }


async def check_cors(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.options(url, timeout=10.0)
    return {"CORS Policy": response.headers.get("Access-Control-Allow-Origin", "Missing")}


async def scan_database(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
    
    # Define precise patterns that focus on database connection details
    patterns = [
        r"\b(DB_|database|db)_\w+",  # Match DB-related constants like DB_HOST, DB_PASSWORD
        r"\b(host|user|password|port|db|connection)\s*=\s*['\"].*?['\"]",  # Match connection settings like host = 'localhost'
        r"\bDB_CONNECTION\s*=\s*['\"].*?['\"]",  # Match specific DB connection config (e.g., DB_CONNECTION)
        r"\b(\w*database\w*)\s*=\s*['\"].*?['\"]",  # Match database config (e.g., database_name)
        r"\burl\s*=\s*['\"].*?['\"]",  # Match URLs, might contain connection details (e.g., database URL)
    ]
    
    # Search for relevant patterns in the response content (skipping HTML)
    matched_content = ""
    for pattern in patterns:
        match = re.search(pattern, response.text, re.IGNORECASE)
        if match:
            # Extract surrounding content to give context
            matched_content = response.text[max(0, match.start() - 100):min(len(response.text), match.end() + 100)]
            break
    
    # If any sensitive patterns matched, return the match details
    if matched_content:
        return {"warning": "Potential database configuration or constants detected", "details": matched_content}
    
    # Return message if no vulnerabilities are detected
    return {"message": "No database vulnerabilities detected"}
