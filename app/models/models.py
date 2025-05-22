from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    jobs = relationship("Job", back_populates="creator")
    refresh_tokens = relationship("RefreshToken", back_populates="user")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    company = Column(String)
    location = Column(String)
    salary_range = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("User", back_populates="jobs")
    candidates = relationship("Candidate", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Skills as JSON array
    skills = Column(JSON, default=list)  # Will store: [{"name": str, "yearsExperience": float, "context": str, "confidence": float}]
    
    # GitHub links as JSON array
    github_links = Column(JSON, default=list)  # Will store: [{"url": str, "username": str, "repositoryCount": int, "profileCreatedAt": str, "extractedFrom": str}]

    job = relationship("Job", back_populates="candidates")
