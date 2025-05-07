# Zordie Backend

FastAPI backend for the Zordie job portal application.

## Features

- User Authentication with JWT
- PostgreSQL Database Integration
- CRUD Operations for:
  - Users
  - Jobs
  - Candidates
- Token Refresh System
- Secure Password Hashing

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with:
```
DATABASE_URL=your_database_url
ACCESS_TOKEN_SECRET_KEY=your_secret_key
REFRESH_TOKEN_SECRET_KEY=your_refresh_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

4. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc` 