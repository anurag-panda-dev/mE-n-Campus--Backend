from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, courses, attendance, events, announcements
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="mE n CAMPUS - Campus Management System API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["Announcements"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to mE n CAMPUS API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
