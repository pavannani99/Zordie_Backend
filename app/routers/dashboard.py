from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import json
import os
from pathlib import Path
import httpx
from pydantic import BaseModel

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)

UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class ResumeAnalysisResponse(BaseModel):
    overall_score: float
    skills_match: Dict[str, Any]
    experience_match: Dict[str, Any]
    education_match: Dict[str, Any]
    recommendations: list[str]
    detailed_scores: Dict[str, Any]  # For additional scoring components

@router.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyze a resume against a job description and return scoring results.
    """
    try:
        # Save the uploaded resume
        resume_path = UPLOAD_DIR / resume.filename
        with open(resume_path, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        # Prepare data for data science service
        data = {
            "resume_path": str(resume_path),
            "job_description": job_description
        }
        
        # Call data science service
        async with httpx.AsyncClient() as client:
            # Using the data science service from the provided repo
            response = await client.post(
                "http://localhost:5000/analyze",  # Update this URL to match your data science service
                json=data,
                timeout=30.0  # Increased timeout for processing
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail="Error from data science service"
                )
            
            analysis_result = response.json()
            
            # Save individual scoring components as JSON files
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            
            # Save overall score
            with open(output_dir / "overall_score.json", "w") as f:
                json.dump({"overall_score": analysis_result["overall_score"]}, f)
            
            # Save skills match
            with open(output_dir / "skills_match.json", "w") as f:
                json.dump(analysis_result["skills_match"], f)
            
            # Save experience match
            with open(output_dir / "experience_match.json", "w") as f:
                json.dump(analysis_result["experience_match"], f)
            
            # Save education match
            with open(output_dir / "education_match.json", "w") as f:
                json.dump(analysis_result["education_match"], f)
            
            # Save recommendations
            with open(output_dir / "recommendations.json", "w") as f:
                json.dump({"recommendations": analysis_result["recommendations"]}, f)
            
            # Save detailed scores if available
            if "detailed_scores" in analysis_result:
                with open(output_dir / "detailed_scores.json", "w") as f:
                    json.dump(analysis_result["detailed_scores"], f)
        
        # Clean up the uploaded file
        os.remove(resume_path)
        
        return analysis_result
        
    except Exception as e:
        # Clean up file if it exists
        if os.path.exists(resume_path):
            os.remove(resume_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis-history")
async def get_analysis_history():
    """
    Get history of resume analyses
    """
    try:
        output_dir = Path("outputs")
        if not output_dir.exists():
            return {"analyses": []}
            
        analyses = []
        for file in output_dir.glob("*.json"):
            with open(file, "r") as f:
                analyses.append({
                    "file": file.name,
                    "data": json.load(f)
                })
        return {"analyses": analyses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get specific analysis result by ID
    """
    try:
        output_dir = Path("outputs")
        file_path = output_dir / f"{analysis_id}.json"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 