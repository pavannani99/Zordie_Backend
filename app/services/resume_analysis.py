from typing import Dict, Any
import httpx
from pathlib import Path
import os
from fastapi import HTTPException

class ResumeAnalysisService:
    def __init__(self):
        # TODO: Move to environment variables
        self.ds_service_url = "http://localhost:5000"
        
    async def analyze_resume(self, resume_path: Path, job_description: str) -> Dict[str, Any]:
        """
        Send resume and job description to data science service for analysis
        """
        try:
            # Prepare the data
            data = {
                "resume_path": str(resume_path),
                "job_description": job_description
            }
            
            # Make request to data science service
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ds_service_url}/analyze",
                    json=data,
                    timeout=30.0  # 30 second timeout
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Data science service error: {response.text}"
                    )
                
                return response.json()
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Data science service timeout"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error communicating with data science service: {str(e)}"
            )
            
    async def get_analysis_history(self) -> list[Dict[str, Any]]:
        """
        Get history of resume analyses
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.ds_service_url}/history",
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=500,
                        detail="Error fetching analysis history"
                    )
                    
                return response.json()
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching analysis history: {str(e)}"
            )
            
    async def get_analysis_by_id(self, analysis_id: str) -> Dict[str, Any]:
        """
        Get specific analysis result by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.ds_service_url}/analysis/{analysis_id}",
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=404,
                        detail="Analysis not found"
                    )
                    
                return response.json()
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching analysis: {str(e)}"
            ) 