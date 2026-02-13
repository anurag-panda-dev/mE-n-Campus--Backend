from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.schemas import Course, CourseCreate, CourseUpdate, User, EnrollmentCreate
from app.core.supabase import supabase
from app.api.dependencies import get_current_user, get_current_teacher_user

router = APIRouter()

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Create a new course (Teacher/Admin only)"""
    try:
        course_data = course.model_dump()
        response = supabase.table("courses").insert(course_data).execute()
        
        return Course(**response.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[Course])
async def get_all_courses(current_user: User = Depends(get_current_user)):
    """Get all courses"""
    try:
        response = supabase.table("courses").select("*").execute()
        return [Course(**course) for course in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get course by ID"""
    try:
        response = supabase.table("courses").select("*").eq("id", course_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return Course(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{course_id}", response_model=Course)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    current_user: User = Depends(get_current_teacher_user)
):
    """Update course (Teacher/Admin only)"""
    try:
        update_data = course_update.model_dump(exclude_unset=True)
        
        response = supabase.table("courses").update(update_data).eq("id", course_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return Course(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    current_user: User = Depends(get_current_teacher_user)
):
    """Delete course (Teacher/Admin only)"""
    try:
        response = supabase.table("courses").delete().eq("id", course_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/enroll", status_code=status.HTTP_201_CREATED)
async def enroll_student(
    enrollment: EnrollmentCreate,
    current_user: User = Depends(get_current_user)
):
    """Enroll a student in a course"""
    try:
        # Check if already enrolled
        existing = supabase.table("enrollments").select("*").eq("student_id", enrollment.student_id).eq("course_id", enrollment.course_id).execute()
        
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already enrolled in this course"
            )
        
        enrollment_data = enrollment.model_dump()
        response = supabase.table("enrollments").insert(enrollment_data).execute()
        
        return {"message": "Successfully enrolled", "data": response.data[0]}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/student/{student_id}", response_model=List[Course])
async def get_student_courses(
    student_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all courses for a student"""
    try:
        # Get enrollments
        enrollments = supabase.table("enrollments").select("course_id").eq("student_id", student_id).execute()
        
        if not enrollments.data:
            return []
        
        course_ids = [e["course_id"] for e in enrollments.data]
        
        # Get courses
        response = supabase.table("courses").select("*").in_("id", course_ids).execute()
        
        return [Course(**course) for course in response.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
