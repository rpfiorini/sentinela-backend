from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.models.models import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    return TokenResponse(access_token=create_access_token(user.username))

@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        return {"message": "admin já existe"}
    user = User(username="admin", password_hash=hash_password("admin123"), role="ADMIN", active=1)
    db.add(user)
    db.commit()
    return {"message": "admin criado", "username": "admin", "password": "admin123"}
