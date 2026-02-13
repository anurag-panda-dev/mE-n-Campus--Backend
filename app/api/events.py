from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.schemas import Event, EventCreate, EventUpdate, User
from app.core.supabase import supabase
from app.api.dependencies import get_current_user, get_current_teacher_user

router = APIRouter()

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Create a new event (Teacher/Admin only)"""
    try:
        event_data = event.model_dump()
        response = supabase.table("events").insert(event_data).execute()
        
        return Event(**response.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[Event])
async def get_all_events(current_user: User = Depends(get_current_user)):
    """Get all events"""
    try:
        response = supabase.table("events").select("*").order("event_date").execute()
        return [Event(**event) for event in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{event_id}", response_model=Event)
async def get_event(
    event_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get event by ID"""
    try:
        response = supabase.table("events").select("*").eq("id", event_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        return Event(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: str,
    event_update: EventUpdate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Update event (Teacher/Admin only)"""
    try:
        update_data = event_update.model_dump(exclude_unset=True)
        
        response = supabase.table("events").update(update_data).eq("id", event_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        return Event(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    current_user: User = Depends(get_current_teacher_user)
):
    """Delete event (Teacher/Admin only)"""
    try:
        response = supabase.table("events").delete().eq("id", event_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
