from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime
import re
from typing import Optional, List, Dict, Any

# Email validation regex pattern
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# User schemas
class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v.lower()

class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v.lower()

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None

class RefreshTokenCreate(BaseModel):
    user_id: int
    token: str
    expires_at: datetime

class RefreshTokenDB(RefreshTokenCreate):
    id: int
    is_revoked: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Login response
class LoginResponse(BaseModel):
    id: int
    email: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Job schemas
class JobBase(BaseModel):
    title: str
    description: str
    company: str
    location: str
    salary_range: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobOut(JobBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class JobList(BaseModel):
    jobs: List[JobOut]
    total: int

# Skill schema
class Skill(BaseModel):
    name: str
    yearsExperience: float
    context: str
    confidence: float

# GitHub link schema
class GitHubLink(BaseModel):
    url: str
    username: str
    repositoryCount: int
    profileCreatedAt: datetime
    extractedFrom: str

# Candidate schemas
class CandidateBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    job_id: int
    skills: List[Skill] = []
    github_links: List[GitHubLink] = []

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v.lower()

class CandidateCreate(CandidateBase):
    pass

class CandidateOut(CandidateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CandidateList(BaseModel):
    candidates: List[CandidateOut]
    total: int
