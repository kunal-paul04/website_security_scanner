### README.md

# Enhanced Website Security Scanner

This is a FastAPI application that scans websites for security headers, CORS policy, and potential database vulnerabilities.

## Features
- Security header analysis
- CORS policy validation
- Database vulnerability detection
- API key authentication
- Dockerized for easy deployment

## Setup

### Prerequisites
- Docker
- Python 3.10+

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fastapi_security_scanner
   ```

2. Build and run with Docker:
   ```bash
   docker build -t security-scanner .
   docker run -d -p 8000:8000 --env-file .env security-scanner
   ```

3. Access the API:
   - Open a browser or use `curl` to navigate to `http://localhost:8000`

## API Endpoints

### `POST /security/scan`
Scan a website for security headers and CORS policy.

**Request Body:**
```json
{
    "url": "https://example.com"
}
```

### `POST /database/scan`
Check a website for potential database vulnerabilities.

**Request Body:**
```json
{
    "url": "https://example.com"
}
```

### Notes
Use responsibly and ensure you have authorization to scan any website.
