from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.schemas import User, UserUpdate
from app.core.supabase import supabase
from app.api.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=User)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update current user profile"""
    try:
        update_data = user_update.model_dump(exclude_unset=True)
        
        response = supabase.table("users").update(update_data).eq("id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return User(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[User])
async def get_all_users(current_user: User = Depends(get_current_admin_user)):
    """Get all users (Admin only)"""
    try:
        response = supabase.table("users").select("*").execute()
        return [User(**user) for user in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get user by ID"""
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return User(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/role/{role}", response_model=List[User])
async def get_users_by_role(
    role: str,
    current_user: User = Depends(get_current_user)
):
    """Get users by role"""
    try:
        response = supabase.table("users").select("*").eq("role", role).execute()
        return [User(**user) for user in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
