from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
from app.models.schemas import Attendance, AttendanceCreate, AttendanceUpdate, User
from app.core.supabase import supabase
from app.api.dependencies import get_current_user, get_current_teacher_user

router = APIRouter()

@router.post("/", response_model=Attendance, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    attendance: AttendanceCreate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Mark attendance for a student (Teacher/Admin only)"""
    try:
        attendance_data = attendance.model_dump()
        attendance_data["marked_by"] = current_user.id
        
        response = supabase.table("attendance").insert(attendance_data).execute()
        
        return Attendance(**response.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/course/{course_id}", response_model=List[Attendance])
async def get_course_attendance(
    course_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all attendance records for a course"""
    try:
        response = supabase.table("attendance").select("*").eq("course_id", course_id).execute()
        return [Attendance(**record) for record in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/student/{student_id}", response_model=List[Attendance])
async def get_student_attendance(
    student_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all attendance records for a student"""
    try:
        response = supabase.table("attendance").select("*").eq("student_id", student_id).execute()
        return [Attendance(**record) for record in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/student/{student_id}/course/{course_id}", response_model=List[Attendance])
async def get_student_course_attendance(
    student_id: str,
    course_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get attendance records for a student in a specific course"""
    try:
        response = supabase.table("attendance").select("*").eq("student_id", student_id).eq("course_id", course_id).execute()
        return [Attendance(**record) for record in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{attendance_id}", response_model=Attendance)
async def update_attendance(
    attendance_id: str,
    attendance_update: AttendanceUpdate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Update attendance record (Teacher/Admin only)"""
    try:
        update_data = attendance_update.model_dump(exclude_unset=True)
        
        response = supabase.table("attendance").update(update_data).eq("id", attendance_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance record not found"
            )
        
        return Attendance(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: str,
    current_user: User = Depends(get_current_teacher_user)
):
    """Delete attendance record (Teacher/Admin only)"""
    try:
        response = supabase.table("attendance").delete().eq("id", attendance_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance record not found"
            )
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
