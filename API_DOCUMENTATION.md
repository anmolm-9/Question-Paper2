# Question Papers API Documentation

This document describes the REST API endpoints available in the Question Papers Platform.

## Base URL
All API endpoints are prefixed with `/api/`

## Authentication
Most API endpoints require authentication. Use the login form on the frontend to authenticate, or send credentials to the login endpoint.

---

## Courses API

### GET /api/courses/
Get all courses
```json
Response:
{
  "success": true,
  "courses": [
    {
      "id": 1,
      "name": "Bachelor of Science in Computer Science",
      "code": "BSCCS",
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

### GET /api/courses/{course_id}
Get a specific course
```json
Response:
{
  "success": true,
  "course": {
    "id": 1,
    "name": "Bachelor of Science in Computer Science",
    "code": "BSCCS",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

### POST /api/courses/
Create a new course (Admin only)
```json
Request:
{
  "name": "Bachelor of Arts",
  "code": "BA"
}

Response:
{
  "success": true,
  "message": "Course created successfully",
  "course": { ... }
}
```

### PUT /api/courses/{course_id}
Update a course (Admin only)
```json
Request:
{
  "name": "Updated Course Name",
  "code": "UPDATED"
}
```

### DELETE /api/courses/{course_id}
Delete a course (Admin only)

---

## Papers API

### GET /api/papers/
Get question papers with optional filters
Query parameters:
- `course_id` - Filter by course ID
- `year` - Filter by year
- `semester` - Filter by semester

```json
Response:
{
  "success": true,
  "papers": [
    {
      "id": 1,
      "title": "Sample Question Paper",
      "course": {
        "id": 1,
        "name": "Bachelor of Science in Computer Science",
        "code": "BSCCS"
      },
      "year": 2024,
      "semester": 1,
      "subject": "Mathematics",
      "filename": "math_2024_s1.pdf",
      "uploaded_by": "admin",
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

### GET /api/papers/{paper_id}
Get a specific question paper

### POST /api/papers/
Upload a new question paper (Admin only)
Content-Type: multipart/form-data
```
Form fields:
- file: PDF/DOC/DOCX file
- title: Paper title
- course_id: Course ID
- year: Academic year
- semester: Semester number
- subject: Subject name
```

### PUT /api/papers/{paper_id}
Update paper metadata (Admin only)
```json
Request:
{
  "title": "Updated Title",
  "subject": "Updated Subject",
  "year": 2025,
  "semester": 2,
  "course_id": 2
}
```

### DELETE /api/papers/{paper_id}
Delete a question paper (Admin only)

### GET /api/papers/years
Get all available years
```json
Response:
{
  "success": true,
  "years": [2024, 2023, 2022]
}
```

### GET /api/papers/subjects
Get all subjects with optional filters
Query parameters same as papers endpoint

---

## Users API

### GET /api/users/profile
Get current user profile (Authenticated)
```json
Response:
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false,
    "created_at": "2025-01-01T00:00:00"
  }
}
```

### PUT /api/users/profile
Update current user profile (Authenticated)
```json
Request:
{
  "email": "newemail@example.com",
  "password": "newpassword" // optional
}
```

### GET /api/users/
Get all users (Admin only)

### POST /api/users/
Register a new user
```json
Request:
{
  "username": "new_user",
  "email": "user@example.com",
  "password": "password123",
  "is_admin": false // optional
}
```

### PUT /api/users/{user_id}
Update a user (Admin only)

### DELETE /api/users/{user_id}
Delete a user (Admin only)

---

## Error Responses

All endpoints return errors in the following format:
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 403: Forbidden (insufficient privileges)
- 404: Not Found
- 500: Internal Server Error

---

## Example Usage

### JavaScript Fetch Examples

```javascript
// Get all courses
fetch('/api/courses/')
  .then(response => response.json())
  .then(data => console.log(data.courses));

// Upload a paper (requires form data)
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('title', 'Math Paper 2024');
formData.append('course_id', '1');
formData.append('year', '2024');
formData.append('semester', '1');
formData.append('subject', 'Mathematics');

fetch('/api/papers/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Get papers for a specific course and year
fetch('/api/papers/?course_id=1&year=2024')
  .then(response => response.json())
  .then(data => console.log(data.papers));
```

---

## Frontend Integration

The frontend templates use these APIs internally through AJAX calls. You can extend the functionality by:

1. Adding new API endpoints
2. Creating frontend JavaScript to consume the APIs
3. Building single-page application features
4. Integrating with external services

The modular structure allows easy extension and maintenance of both backend logic and frontend presentation.