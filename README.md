# mE n CAMPUS - Backend API

A comprehensive Campus Management System API built with FastAPI and Supabase, providing robust endpoints for managing students, teachers, courses, attendance, events, and announcements.

## 🚀 Features

- **User Authentication** - Secure registration and login with JWT tokens
- **User Management** - Role-based access control (Student, Teacher, Admin)
- **Course Management** - Create, update, and manage courses with enrollment
- **Attendance Tracking** - Mark and monitor student attendance
- **Event Management** - Create and manage campus events
- **Announcements** - Broadcast important announcements to users
- **RESTful API** - Well-structured endpoints following REST principles
- **Interactive Documentation** - Automatic API docs with Swagger UI

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn (ASGI server)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with bcrypt
- **Data Validation**: Pydantic
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account and project
- pip (Python package manager)

## 📦 Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the backend directory with the following variables:

```env
# Project Settings
PROJECT_NAME=mE-n-CAMPUS-API
VERSION=1.0.0

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (Optional - defaults provided)
ALLOWED_ORIGINS=["http://localhost:8081","http://localhost:19006"]
```

### Getting Supabase Credentials

1. Go to your [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Navigate to Settings > API
4. Copy the following:
   - Project URL → `SUPABASE_URL`
   - anon/public key → `SUPABASE_KEY`
   - service_role key → `SUPABASE_SERVICE_KEY`

### Generating Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

For detailed endpoint information, see [API-Endpoints.md](API-Endpoints.md)

### Quick Endpoint Overview

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get access token
- `POST /api/auth/logout` - Logout user

#### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update profile
- `GET /api/users/` - List all users (Admin)
- `GET /api/users/role/{role}` - Get users by role

#### Courses
- `POST /api/courses/` - Create course
- `GET /api/courses/` - List all courses
- `GET /api/courses/{course_id}` - Get course details
- `PUT /api/courses/{course_id}` - Update course
- `DELETE /api/courses/{course_id}` - Delete course
- `POST /api/courses/enroll` - Enroll in course

#### Attendance
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/course/{course_id}` - Course attendance
- `GET /api/attendance/student/{student_id}` - Student attendance

#### Events
- `POST /api/events/` - Create event
- `GET /api/events/` - List all events
- `PUT /api/events/{event_id}` - Update event
- `DELETE /api/events/{event_id}` - Delete event

#### Announcements
- `POST /api/announcements/` - Create announcement
- `GET /api/announcements/` - List announcements
- `PUT /api/announcements/{announcement_id}` - Update announcement
- `DELETE /api/announcements/{announcement_id}` - Delete announcement

## 📁 Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
├── API-Endpoints.md       # Detailed API documentation
├── .env                   # Environment variables (create this)
├── app/
│   ├── __init__.py
│   ├── api/               # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User management endpoints
│   │   ├── courses.py     # Course management endpoints
│   │   ├── attendance.py  # Attendance tracking endpoints
│   │   ├── events.py      # Event management endpoints
│   │   ├── announcements.py  # Announcement endpoints
│   │   └── dependencies.py   # Shared dependencies
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration settings
│   │   ├── security.py    # Security utilities (JWT, hashing)
│   │   └── supabase.py    # Supabase client initialization
│   └── models/            # Data models
│       └── schemas.py     # Pydantic schemas
```

## 🔒 Security

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt algorithm for password security
- **CORS Configuration**: Configurable allowed origins
- **Role-Based Access**: Different permissions for Students, Teachers, and Admins

## 🔧 Development

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy"
}
```

### Testing Authentication Flow

1. **Register a new user**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password123","role":"student"}'
   ```

2. **Login**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password123"}'
   ```

3. **Use the token**
   ```bash
   curl http://localhost:8000/api/users/me \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## 📝 User Roles

- **Student**: Can view courses, events, announcements, and personal attendance
- **Teacher**: Can create courses, mark attendance, manage events and announcements
- **Admin**: Full access to all endpoints and user management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the mE n CAMPUS system.

## 📞 Support

For issues and questions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and Supabase**
