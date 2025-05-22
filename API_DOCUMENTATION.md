# Zordie API Documentation

## Base URLs
```
Development: http://127.0.0.1:8000/api
Production: https://api.zordie.com/api
```

## Docker Configuration
The API is containerized using Docker. Key environment variables for Docker deployment:
```
DATABASE_URL=postgresql://user:password@db:5432/dbname
ACCESS_TOKEN_SECRET_KEY=your_secret_key
REFRESH_TOKEN_SECRET_KEY=your_refresh_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://redis:6379
```

## CORS Configuration
The API supports CORS with the following configuration:
```
Allowed Origins: 
- http://localhost:3000 (Development)
- https://zordie.com (Production)

Allowed Methods: GET, POST, PUT, DELETE, OPTIONS
Allowed Headers: Content-Type, Authorization
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```
Response:
```json
{
    "id": 1,
    "email": "user@example.com",
    "access_token": "eyJhbGciOiJIUzI1...",
    "refresh_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```
Response: Same as register

#### Refresh Token
```http
POST /auth/refresh-token
Authorization: Bearer <refresh_token>
```
Response: New access and refresh tokens in the same format as login/register

#### Logout
```http
POST /auth/logout
Authorization: Bearer <refresh_token>
```
Response:
```json
{
    "message": "Successfully logged out"
}
```

## Resume Management

### Upload Resume
```http
POST /resumes/upload-resume
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <pdf_file>
```
Response:
```json
{
    "message": "Resume uploaded successfully",
    "file_id": "6c3df240-33f4-43f6-904e-b4ee067bce40",
    "filename": "3_20250508_035454_6c3df240-33f4-43f6-904e-b4ee067bce40.pdf",
    "size": 3610020,
    "uploaded_at": "20250508_035454"
}
```

### Check Parse Status
```http
GET /resumes/parsing-status/{file_id}
Authorization: Bearer <access_token>
```
Response:
```json
{
    "status": "processing|completed|failed",
    "progress": 75,
    "message": "Processing resume..."
}
```

### Get Parsed Results
```http
GET /resumes/parsed-results/{file_id}
Authorization: Bearer <access_token>
```
Response:
```json
{
    "candidate": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "skills": [
            {
                "name": "Python",
                "yearsExperience": 3.5,
                "context": "Work Experience",
                "confidence": 0.95
            }
        ],
        "github_links": [
            {
                "url": "https://github.com/johndoe",
                "username": "johndoe",
                "repositoryCount": 15,
                "profileCreatedAt": "2020-01-01T00:00:00Z",
                "extractedFrom": "Projects Section"
            }
        ]
    }
}
```

## Job Management

### Create Job
```http
POST /jobs/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Senior Python Developer",
    "description": "Job description...",
    "company": "Tech Corp",
    "location": "New York",
    "salary_range": "$100k - $150k"
}
```
Response:
```json
{
    "id": 1,
    "title": "Senior Python Developer",
    "description": "Job description...",
    "company": "Tech Corp",
    "location": "New York",
    "salary_range": "$100k - $150k",
    "created_by": 1,
    "created_at": "2024-05-08T03:54:54"
}
```

### List Jobs
```http
GET /jobs/
Authorization: Bearer <access_token>
Query Parameters:
- page: int (default: 1)
- limit: int (default: 10)
- search: string (optional)
- sort_by: string (optional, e.g., "created_at", "title")
- sort_order: string (optional, "asc" or "desc")
```
Response:
```json
{
    "jobs": [
        {
            "id": 1,
            "title": "Senior Python Developer",
            "description": "Job description...",
            "company": "Tech Corp",
            "location": "New York",
            "salary_range": "$100k - $150k",
            "created_by": 1,
            "created_at": "2024-05-08T03:54:54"
        }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "total_pages": 1
}
```

### Get Job Details
```http
GET /jobs/{job_id}
Authorization: Bearer <access_token>
```
Response: Single job object

### Update Job
```http
PUT /jobs/{job_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Updated Title",
    "description": "Updated description...",
    "company": "New Company",
    "location": "New Location",
    "salary_range": "New Range"
}
```
Response: Updated job object

### Delete Job
```http
DELETE /jobs/{job_id}
Authorization: Bearer <access_token>
```
Response:
```json
{
    "message": "Job deleted successfully"
}
```

## Candidate Management

### List Candidates
```http
GET /candidates/
Authorization: Bearer <access_token>
Query Parameters:
- page: int (default: 1)
- limit: int (default: 10)
- search: string (optional)
- sort_by: string (optional)
- sort_order: string (optional, "asc" or "desc")
```
Response:
```json
{
    "candidates": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "created_at": "2024-05-08T03:54:54"
        }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "total_pages": 1
}
```

### Get Candidate Details
```http
GET /candidates/{candidate_id}
Authorization: Bearer <access_token>
```
Response: Detailed candidate object with all parsed information

## User Management

### Get Current User
```http
GET /users/me
Authorization: Bearer <access_token>
```
Response:
```json
{
    "id": 1,
    "email": "user@example.com"
}
```

## Error Responses
All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
    "detail": "Not authenticated",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}
```

### 403 Forbidden
```json
{
    "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per user

## File Upload Limits
- Maximum file size: 10MB
- Allowed file types: PDF only
- Files are automatically deleted after 30 days

## Development Setup

### Local Development
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
ACCESS_TOKEN_SECRET_KEY=your_secret_key
REFRESH_TOKEN_SECRET_KEY=your_refresh_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. Run the server:
```bash
python -m uvicorn app.main:app --reload
```

### Docker Development
1. Build the Docker image:
```bash
docker build -t zordie-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env zordie-api
```

3. Access the API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Frontend Integration Guide

### Authentication Flow
1. Register/Login to get access and refresh tokens
2. Store tokens securely (e.g., in HttpOnly cookies)
3. Include access token in all API requests
4. Use refresh token to get new access token when expired

### Error Handling
- Implement proper error handling for all API responses
- Handle rate limiting errors with appropriate user feedback
- Implement retry logic for failed requests

### File Upload
- Implement proper file validation before upload
- Show upload progress using the parsing status endpoint
- Handle upload errors gracefully

### Pagination
- Implement pagination controls using the page and limit parameters
- Handle empty results and edge cases
- Implement proper loading states 