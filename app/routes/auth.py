from fastapi import APIRouter, Depends, HTTPException
from ..db import create_user, get_user_by_email
from ..models.schemas import RegisterRequest, LoginRequest
from ..security import hash_password, verify_password, create_access_token
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register")
def register(data: RegisterRequest):
    email = data.email.lower()
    if get_user_by_email(email):
        raise HTTPException(status_code=409, detail="Email already registered")
    uid = create_user(email, hash_password(data.password))
    return {"message": "Registration successful", "user": {"id": uid, "email": email}}

@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email.lower())
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": create_access_token(user["id"], user["email"]), "token_type": "bearer", "user": {"id": user["id"], "email": user["email"]}}

@router.post("/logout")
def logout(user=Depends(get_current_user)):
    return {"message": "Logout acknowledged. Remove the token from the browser."}

@router.get("/session-info")
def session_info(user=Depends(get_current_user)):
    return {"authenticated": True, "user_id": int(user["sub"]), "email": user["email"]}

@router.get("/session-data")
def session_data(user=Depends(get_current_user)):
    return {"user_id": int(user["sub"]), "email": user["email"], "personalization": {"planner_history_enabled": True}}
