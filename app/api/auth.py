from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.models.schemas import UserLogin, UserRegister, Token, UserRole
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.supabase import supabase, supabase_admin
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user"""
    try:
        # Check if user already exists
        existing = supabase.table("users").select("*").eq("email", user_data.email).execute()
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user in Supabase Auth
        auth_response = supabase_admin.auth.admin.create_user({
            "email": user_data.email,
            "password": user_data.password,
            "email_confirm": True
        })
        
        # Create user profile
        user_profile = {
            "id": auth_response.user.id,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "role": user_data.role.value,
            "phone": user_data.phone,
            "created_at": "now()"
        }
        
        profile_response = supabase.table("users").insert(user_profile).execute()
        
        # Create access token
        access_token = create_access_token(
            data={"sub": auth_response.user.id, "role": user_data.role.value},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": profile_response.data[0]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return access token"""
    try:
        # Sign in with Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": user_credentials.email,
            "password": user_credentials.password
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Get user profile
        profile_response = supabase.table("users").select("*").eq("id", auth_response.user.id).execute()
        
        if not profile_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        user_profile = profile_response.data[0]
        
        # Create access token
        access_token = create_access_token(
            data={"sub": auth_response.user.id, "role": user_profile["role"]},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_profile
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

@router.post("/logout")
async def logout():
    """Logout user"""
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
