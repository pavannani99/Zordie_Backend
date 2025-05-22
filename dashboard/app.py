from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import httpx
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel

# Create necessary directories
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Resume Analysis Dashboard",
    description="Dashboard for analyzing resumes against job descriptions",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

class AnalysisResponse(BaseModel):
    overall_score: float
    skills_match: Dict[str, Any]
    experience_match: Dict[str, Any]
    education_match: Dict[str, Any]
    recommendations: list[str]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the dashboard home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Analyze a resume against a job description"""
    try:
        # Save the uploaded resume
        resume_path = UPLOAD_DIR / resume.filename
        with open(resume_path, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        # Save job description to a temporary file
        jd_path = UPLOAD_DIR / "temp_jd.txt"
        with open(jd_path, "w", encoding="utf-8") as f:
            f.write(job_description)
        
        # Prepare data for data science service
        data = {
            "resume_path": str(resume_path),
            "jd_path": str(jd_path)
        }
        
        # Call data science service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:5000/analyze",  # Data science service endpoint
                json=data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail="Error from data science service"
                )
            
            analysis_result = response.json()
            
            # Save individual components as JSON files
            # Save overall score
            with open(OUTPUT_DIR / "overall_score.json", "w") as f:
                json.dump({"overall_score": analysis_result["overall_score"]}, f)
            
            # Save skills match
            with open(OUTPUT_DIR / "skills_match.json", "w") as f:
                json.dump(analysis_result["skills_match"], f)
            
            # Save experience match
            with open(OUTPUT_DIR / "experience_match.json", "w") as f:
                json.dump(analysis_result["experience_match"], f)
            
            # Save education match
            with open(OUTPUT_DIR / "education_match.json", "w") as f:
                json.dump(analysis_result["education_match"], f)
            
            # Save recommendations
            with open(OUTPUT_DIR / "recommendations.json", "w") as f:
                json.dump({"recommendations": analysis_result["recommendations"]}, f)
        
        # Clean up the uploaded files
        os.remove(resume_path)
        os.remove(jd_path)
        
        return analysis_result
        
    except Exception as e:
        # Clean up files if they exist
        if os.path.exists(resume_path):
            os.remove(resume_path)
        if os.path.exists(jd_path):
            os.remove(jd_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis-history")
async def get_analysis_history():
    """Get history of resume analyses"""
    try:
        if not OUTPUT_DIR.exists():
            return {"analyses": []}
            
        analyses = []
        for file in OUTPUT_DIR.glob("*.json"):
            with open(file, "r") as f:
                analyses.append({
                    "file": file.name,
                    "data": json.load(f)
                })
        return {"analyses": analyses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get specific analysis result by ID"""
    try:
        file_path = OUTPUT_DIR / f"{analysis_id}.json"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8080, reload=True) 