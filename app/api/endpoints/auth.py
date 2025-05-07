from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schemas import UserCreate, LoginResponse, LoginRequest
from app.core.security import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, get_refresh_token_user, revoke_refresh_token
)

router = APIRouter()

@router.post("/register", response_model=LoginResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email, "user_id": db_user.id}, db=db)
    
    return {
        "id": db_user.id,
        "email": db_user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Authenticate user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email, "user_id": user.id}, db=db)
    
    return {
        "id": user.id,
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh-token", response_model=LoginResponse)
def refresh_token(refresh_data = Depends(get_refresh_token_user), db: Session = Depends(get_db)):
    user = refresh_data["user"]
    token_jti = refresh_data["token_jti"]
    
    # Revoke the current refresh token
    revoke_refresh_token(token_jti, db)
    
    # Generate new tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email, "user_id": user.id}, db=db)
    
    return {
        "id": user.id,
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(refresh_data = Depends(get_refresh_token_user), db: Session = Depends(get_db)):
    # Revoke the refresh token
    revoke_refresh_token(refresh_data["token_jti"], db)
    return {"message": "Successfully logged out"}
