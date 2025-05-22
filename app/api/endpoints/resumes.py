from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import os
from typing import Optional
import aiofiles
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import User
import requests
from app.config import settings

router = APIRouter()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx'}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

def is_valid_file_type(filename: str) -> bool:
    """
    Check if file extension is allowed
    """
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

async def scan_file_for_viruses(file_content: bytes) -> bool:
    """
    Scan file for viruses using ClamAV API
    Returns True if file is clean, False if infected
    """
    try:
        # You can replace this with your preferred virus scanning service
        # This is a placeholder for ClamAV API integration
        response = requests.post(
            "https://api.clamav.net/scan",
            files={"file": file_content},
            headers={"Authorization": f"Bearer {settings.CLAMAV_API_KEY}"}
        )
        return response.status_code == 200
    except Exception as e:
        # Log the error and fail safely
        print(f"Virus scanning error: {str(e)}")
        return False

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Validate file type
        if not is_valid_file_type(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOC, and DOCX files are allowed"
            )
        
        # Read file content
        content = await file.read()
        
        # Scan for viruses
        if not await scan_file_for_viruses(content):
            raise HTTPException(
                status_code=400,
                detail="File failed virus scan"
            )
        
        # Check file size
        file_size = len(content)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 10MB."
            )
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_id = str(uuid.uuid4())
        filename = f"{current_user.id}_{timestamp}_{file_id}{os.path.splitext(file.filename)[1]}"
        
        # Save file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Return success response with file details
        return JSONResponse(
            status_code=200,
            content={
                "message": "Resume uploaded successfully",
                "file_id": file_id,
                "filename": filename,
                "size": file_size,
                "uploaded_at": timestamp
            }
        )
        
    except Exception as e:
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        ) 