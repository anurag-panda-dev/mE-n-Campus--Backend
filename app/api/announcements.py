from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.schemas import Announcement, AnnouncementCreate, AnnouncementUpdate, User
from app.core.supabase import supabase
from app.api.dependencies import get_current_user, get_current_teacher_user

router = APIRouter()

@router.post("/", response_model=Announcement, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    announcement: AnnouncementCreate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Create a new announcement (Teacher/Admin only)"""
    try:
        announcement_data = announcement.model_dump()
        response = supabase.table("announcements").insert(announcement_data).execute()
        
        return Announcement(**response.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[Announcement])
async def get_all_announcements(current_user: User = Depends(get_current_user)):
    """Get all announcements"""
    try:
        # Filter by target audience if user is student or teacher
        if current_user.role == "student":
            response = supabase.table("announcements").select("*").in_("target_audience", ["student", "all"]).order("created_at", desc=True).execute()
        elif current_user.role == "teacher":
            response = supabase.table("announcements").select("*").in_("target_audience", ["teacher", "all"]).order("created_at", desc=True).execute()
        else:
            response = supabase.table("announcements").select("*").order("created_at", desc=True).execute()
        
        return [Announcement(**announcement) for announcement in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{announcement_id}", response_model=Announcement)
async def get_announcement(
    announcement_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get announcement by ID"""
    try:
        response = supabase.table("announcements").select("*").eq("id", announcement_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Announcement not found"
            )
        
        return Announcement(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{announcement_id}", response_model=Announcement)
async def update_announcement(
    announcement_id: str,
    announcement_update: AnnouncementUpdate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Update announcement (Teacher/Admin only)"""
    try:
        update_data = announcement_update.model_dump(exclude_unset=True)
        
        response = supabase.table("announcements").update(update_data).eq("id", announcement_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Announcement not found"
            )
        
        return Announcement(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: str,
    current_user: User = Depends(get_current_teacher_user)
):
    """Delete announcement (Teacher/Admin only)"""
    try:
        response = supabase.table("announcements").delete().eq("id", announcement_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Announcement not found"
            )
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
