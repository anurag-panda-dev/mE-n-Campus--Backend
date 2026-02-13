from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

#Enums
class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    STW = "stw"  # Seminar, Training, Workshop

# Auth Schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
    phone: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class User(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    credits: int
    teacher_id: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None

class Course(CourseBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Enrollment Schema
class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str

class Enrollment(BaseModel):
    id: str
    student_id: str
    course_id: str
    enrolled_at: datetime
    
    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceCreate(BaseModel):
    student_id: str
    course_id: str
    date: datetime
    status: AttendanceStatus
    notes: Optional[str] = None

class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None

class Attendance(BaseModel):
    id: str
    student_id: str
    course_id: str
    date: datetime
    status: AttendanceStatus
    notes: Optional[str] = None
    marked_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: datetime
    location: Optional[str] = None
    organizer_id: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None

class Event(EventBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Announcement Schemas
class AnnouncementBase(BaseModel):
    title: str
    content: str
    author_id: str
    target_audience: Optional[str] = None  # student, teacher, all

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    target_audience: Optional[str] = None

class Announcement(AnnouncementBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
