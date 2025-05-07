# Zordie API Documentation

## Base URL
```
http://127.0.0.1:8000/api
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
Response: New access and refresh tokens

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
GET /parsing-status/{file_id}
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
GET /parsed-results/{file_id}
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
    "total": 1
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

### Create Candidate
```http
POST /candidates/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "resume_url": "https://storage.example.com/resumes/123.pdf",
    "job_id": 1,
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
```
Response: Created candidate object

### List Candidates
```http
GET /candidates/
Authorization: Bearer <access_token>
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
            "resume_url": "https://storage.example.com/resumes/123.pdf",
            "job_id": 1,
            "skills": [...],
            "github_links": [...],
            "created_at": "2024-05-08T03:54:54"
        }
    ],
    "total": 1
}
```

### Get Candidate Details
```http
GET /candidates/{candidate_id}
Authorization: Bearer <access_token>
```
Response: Single candidate object

### Delete Candidate
```http
DELETE /candidates/{candidate_id}
Authorization: Bearer <access_token>
```
Response:
```json
{
    "message": "Candidate deleted successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}
```

### 403 Forbidden
```json
{
    "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
    "detail": [
        {
            "loc": ["field_name"],
            "msg": "error message",
            "type": "error_type"
        }
    ]
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

4. Access the API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc 