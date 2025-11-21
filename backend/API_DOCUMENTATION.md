# University Resource App - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All endpoints except `/api/auth/login` require authentication. Include session cookies in requests.

## Test Users
- **Student**: username=`student1`, password=`student123`
- **Lecturer**: username=`lecturer1`, password=`lecturer123`

---

## Authentication Endpoints

### POST /api/auth/login
Login to the application.

**Request Body:**
```json
{
    "username": "student1",
    "password": "student123"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful!",
    "user": {
        "id": 1,
        "username": "student1",
        "email": "student1@university.edu",
        "role": "student"
    }
}
```

### POST /api/auth/logout
Logout from the application.

**Response:**
```json
{
    "success": true,
    "message": "You have been logged out."
}
```

### GET /api/auth/me
Get current authenticated user information.

**Response:**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "student1",
        "email": "student1@university.edu",
        "role": "student",
        "student_profile": {
            "id": 1,
            "full_name": "John Student",
            "registration_number": "STU2023001",
            "academic_year": 3,
            "faculty": "Engineering",
            "department": "Computer Science",
            "can_upload": true
        }
    }
}
```

---

## Student Endpoints

### GET /api/student/dashboard
Get student dashboard data.

**Response:**
```json
{
    "success": true,
    "data": {
        "uploaded_resources": [...],
        "recent_resources": [...],
        "student_info": {
            "full_name": "John Student",
            "registration_number": "STU2023001",
            "can_upload": true
        }
    }
}
```

### GET /api/student/browse
Browse approved resources with pagination and filtering.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 12)
- `category` (optional): Category ID filter
- `search` (optional): Search term

**Response:**
```json
{
    "success": true,
    "data": {
        "resources": [...],
        "categories": [...],
        "pagination": {
            "page": 1,
            "pages": 5,
            "per_page": 12,
            "total": 60,
            "has_next": true,
            "has_prev": false
        }
    }
}
```

### GET /api/student/profile
Get student profile information.

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "full_name": "John Student",
        "registration_number": "STU2023001",
        "academic_year": 3,
        "faculty": "Engineering",
        "department": "Computer Science",
        "contact_number": "123-456-7890",
        "enrolled_date": "2023-01-15",
        "can_upload": true
    }
}
```

---

## Lecturer Endpoints

### GET /api/lecturer/dashboard
Get lecturer dashboard data.

**Response:**
```json
{
    "success": true,
    "data": {
        "pending_resources": [...],
        "reviewed_resources": [...],
        "lecturer_info": {
            "full_name": "Dr. Jane Lecturer",
            "employee_id": "LEC2023001",
            "position": "Professor",
            "department": "Computer Science"
        }
    }
}
```

### GET /api/lecturer/review/{id}
Get resource details for review.

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Introduction to Algorithms",
        "description": "Basic algorithm concepts",
        "file_name": "algorithms.pdf",
        "file_type": "pdf",
        "file_size": 2048576,
        "upload_date": "2023-11-20T10:30:00",
        "status": "pending",
        "category": {
            "id": 1,
            "name": "Lecture Notes"
        },
        "uploader": {
            "full_name": "John Student",
            "registration_number": "STU2023001",
            "faculty": "Engineering",
            "department": "Computer Science"
        }
    }
}
```

### POST /api/lecturer/review/{id}
Review a resource (approve or reject).

**Request Body:**
```json
{
    "action": "approve",
    "comments": "Good resource, approved for publication."
}
```

**Response:**
```json
{
    "success": true,
    "message": "Resource approved successfully!",
    "data": {
        "id": 1,
        "status": "approved",
        "review_date": "2023-11-20T15:45:00"
    }
}
```

### GET /api/lecturer/profile
Get lecturer profile information.

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "full_name": "Dr. Jane Lecturer",
        "employee_id": "LEC2023001",
        "department": "Computer Science",
        "position": "Professor",
        "office_location": "Building A, Room 101",
        "contact_number": "098-765-4321",
        "joined_date": "2020-08-01"
    }
}
```

---

## Resources Endpoints

### POST /api/resources/upload
Upload a new resource (requires upload permission).

**Request:** Multipart form data
- `title`: Resource title (required)
- `description`: Resource description (optional)
- `category`: Category ID (required)
- `file`: File to upload (required)

**Response:**
```json
{
    "success": true,
    "message": "Resource uploaded successfully!",
    "data": {
        "id": 1,
        "title": "Introduction to Algorithms",
        "description": "Basic algorithm concepts",
        "file_name": "algorithms.pdf",
        "file_type": "pdf",
        "file_size": 2048576,
        "upload_date": "2023-11-20T10:30:00",
        "status": "pending",
        "category": {
            "id": 1,
            "name": "Lecture Notes"
        }
    }
}
```

### GET /api/resources/download/{id}
Download a resource file (only approved resources).

**Response:** File download

### GET /api/resources/categories
Get all active categories.

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Lecture Notes",
            "description": "Class lecture materials and notes",
            "created_at": "2023-11-20T09:00:00"
        },
        ...
    ]
}
```

### GET /api/resources/my-uploads
Get current student's uploaded resources.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)
- `status` (optional): Filter by status (pending/approved/rejected)

**Response:**
```json
{
    "success": true,
    "data": {
        "resources": [...],
        "pagination": {
            "page": 1,
            "pages": 2,
            "per_page": 10,
            "total": 15,
            "has_next": true,
            "has_prev": false
        }
    }
}
```

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
    "success": false,
    "message": "Error description"
}
```

Common HTTP Status Codes:
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

---

## Testing with cURL

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username":"student1","password":"student123"}'
```

### Get Dashboard
```bash
curl -X GET http://localhost:5000/api/student/dashboard \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### Upload File
```bash
curl -X POST http://localhost:5000/api/resources/upload \
  -F "title=Test Resource" \
  -F "description=Test description" \
  -F "category=1" \
  -F "file=@/path/to/file.pdf" \
  -b cookies.txt
```
