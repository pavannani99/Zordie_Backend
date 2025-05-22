# Zordie Backend

Hey there! 👋 This is the backend for Zordie, a job portal application.

## What's Inside? 🚀

- User login and registration
- Job posting and management
- Candidate applications
- Secure authentication
- PostgreSQL database

## Getting Started 🛠️

1. **Setup your environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   ```

2. **Install stuff**
   ```bash
   pip install -r requirements.txt
   ```
cd Zordie_Backend
3. **Set up your .env file**
   ```
   DATABASE_URL=your_database_url
   ACCESS_TOKEN_SECRET_KEY=your_secret_key
   REFRESH_TOKEN_SECRET_KEY=your_refresh_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

4. **Run it!**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## Check it out! 🔍

Once it's running, visit:
- `http://127.0.0.1:8000/docs` - See all the cool stuff you can do
- `http://127.0.0.1:8000/redoc` - For a prettier view

## Need Help? 🤝

Feel free to reach out if you need any help or have questions! 