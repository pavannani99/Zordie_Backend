from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.models import Job, User
from app.schemas import JobCreate, JobOut, JobList
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=JobOut)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_job = Job(**job.dict(), created_by=current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=JobList)
def read_jobs(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Job.title.ilike(search_term)) |
            (Job.company.ilike(search_term)) |
            (Job.description.ilike(search_term))
        )
    
    total = query.count()
    jobs = query.offset(skip).limit(limit).all()
    
    return {"jobs": jobs, "total": total}

@router.get("/{job_id}", response_model=JobOut)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if db_job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this job")
    
    for key, value in job.dict().items():
        setattr(db_job, key, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if db_job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    
    db.delete(db_job)
    db.commit()
    
    return {"message": "Job deleted successfully"}
