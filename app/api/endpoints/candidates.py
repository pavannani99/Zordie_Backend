from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Candidate, Job, User
from app.schemas import CandidateCreate, CandidateOut, CandidateList
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=CandidateOut)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):
    # Verify job exists
    job = db.query(Job).filter(Job.id == candidate.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

@router.get("/", response_model=CandidateList)
def read_candidates(
    skip: int = 0,
    limit: int = 100,
    job_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Candidate)
    
    if job_id:
        # Verify user has permission to view candidates for this job
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view candidates for this job")
        
        query = query.filter(Candidate.job_id == job_id)
    
    total = query.count()
    candidates = query.offset(skip).limit(limit).all()
    
    return {"candidates": candidates, "total": total}

@router.get("/{candidate_id}", response_model=CandidateOut)
def read_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Check if user has permission to view this candidate
    job = db.query(Job).filter(Job.id == db_candidate.job_id).first()
    if job and job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this candidate")
    
    return db_candidate

@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Check if user has permission to delete this candidate
    job = db.query(Job).filter(Job.id == db_candidate.job_id).first()
    if job and job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this candidate")
    
    db.delete(db_candidate)
    db.commit()
    
    return {"message": "Candidate deleted successfully"}
