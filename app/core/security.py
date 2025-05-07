from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User, RefreshToken
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, db: Session):
    # Generate unique token
    token_value = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Store token in database
    refresh_token = RefreshToken(
        token=token_value,
        user_id=data["user_id"],
        expires_at=expires_at
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    
    # Create JWT with reference to this token
    to_encode = data.copy()
    to_encode.update({"exp": expires_at, "type": "refresh", "jti": token_value})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_refresh_token_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        jti: str = payload.get("jti")
        
        if email is None or token_type != "refresh" or jti is None:
            raise credentials_exception
        
        # Verify token exists in database and is not revoked
        db_token = db.query(RefreshToken).filter(RefreshToken.token == jti).first()
        if not db_token or db_token.is_revoked or db_token.expires_at < datetime.utcnow():
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return {"user": user, "token_jti": jti}

def revoke_refresh_token(jti: str, db: Session):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == jti).first()
    if db_token:
        db_token.is_revoked = True
        db.commit()
