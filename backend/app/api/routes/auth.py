from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from bson import ObjectId
from datetime import datetime, timedelta
import secrets

from ...schemas.auth import RegisterRequest, UserResponse, LoginRequest
from ...core.security import hash_password, verify_password
from ...core.email import send_verification_email
from ...core.config import BACKEND_BASE_URL
from ...db.mongo import db


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest, background_tasks: BackgroundTasks):
    
    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long. Please use atmost 72 characters"
        )
    
    # Check existing user
    existing = await db.users.find_one({"email": payload.email})
    
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate random verification link
    verification_token = secrets.token_urlsafe(32)
    verification_expiry = datetime.utcnow() + timedelta(hours=24)
    
    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "role": payload.role,
        "is_verified": False,
        "verification_token":verification_token,
        "verification_expiry": verification_expiry,
        "created_at" : datetime.utcnow(),
    }
    
    # Add role specific data
    
    if payload.role == "student" :
        user_doc["branch"] = payload.branch
    elif payload.role == "teacher" :
        user_doc["employee_id"] = payload.employee_id
        user_doc["phone"] = payload.phone
        
    result = await db.users.insert_one(user_doc)
    
    # Build Verification link
    verify_link = f"{BACKEND_BASE_URL}/auth/verify-email?token={verification_token}"
    
    # Background tasks
    background_tasks.add_task(
        send_verification_email,
        to_email=payload.email,
        verification_link=verify_link,
    )
    
    return {
        "id": str(result.inserted_id),
        "email": payload.email,
        "role": payload.role,
        "name": payload.name,
    }
        


@router.post("/login", response_model=UserResponse)
async def login(payload: LoginRequest):
    email = payload.email
    password = payload.password
    
    user = await db.users.find_one({"email": payload.email})

    # 1. Find user with this email
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 2. Verify the password of the user
    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Wrong Password")

    # 3. Check if user is verified or not
    if not user.get("is_verified", False):
        raise HTTPException(status_code=403, detail="Please verify your email first..")

    return UserResponse(
        email=email,
        role=user["role"],
        name=user["name"],
    )
    
    
# Verify email route

@router.get("/verify-email")
async def verify_email(token: str = Query(...)):
    user = await db.users.find_one({"verification_token":token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Check expiry
    expires_at = user.get("verification_expiry")
    if expires_at and expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification link expired")
    
    await db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"is_verified": True},
            "$unset": {"verification_token": "", "verification_expiry": ""},
        },
    )
    
    return {"message": "Email verified successfully. You can now log in.."}