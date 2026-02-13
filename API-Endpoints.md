## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/` - Get all users (Admin only)
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/role/{role}` - Get users by role

### Courses
- `POST /api/courses/` - Create course (Teacher/Admin)
- `GET /api/courses/` - Get all courses
- `GET /api/courses/{course_id}` - Get course by ID
- `PUT /api/courses/{course_id}` - Update course (Teacher/Admin)
- `DELETE /api/courses/{course_id}` - Delete course (Teacher/Admin)
- `POST /api/courses/enroll` - Enroll student in course
- `GET /api/courses/student/{student_id}` - Get student's courses

### Attendance
- `POST /api/attendance/` - Mark attendance (Teacher/Admin)
- `GET /api/attendance/course/{course_id}` - Get course attendance
- `GET /api/attendance/student/{student_id}` - Get student attendance
- `GET /api/attendance/student/{student_id}/course/{course_id}` - Get student course attendance
- `PUT /api/attendance/{attendance_id}` - Update attendance (Teacher/Admin)
- `DELETE /api/attendance/{attendance_id}` - Delete attendance (Teacher/Admin)

### Events
- `POST /api/events/` - Create event (Teacher/Admin)
- `GET /api/events/` - Get all events
- `GET /api/events/{event_id}` - Get event by ID
- `PUT /api/events/{event_id}` - Update event (Teacher/Admin)
- `DELETE /api/events/{event_id}` - Delete event (Teacher/Admin)

### Announcements
- `POST /api/announcements/` - Create announcement (Teacher/Admin)
- `GET /api/announcements/` - Get all announcements
- `GET /api/announcements/{announcement_id}` - Get announcement by ID
- `PUT /api/announcements/{announcement_id}` - Update announcement (Teacher/Admin)
- `DELETE /api/announcements/{announcement_id}` - Delete announcement (Teacher/Admin)
