# Question Papers Platform

A Flask-based web application for managing and accessing previous year question papers. The platform allows administrators to upload question papers and users to browse and download them organized by courses, years, and semesters.

## Features

### Frontend Features
- **Home Page**: Clean, modern interface with course listings
- **Course-wise Navigation**: Browse papers by specific courses (BSCCS, BSCIT, BCOM)
- **Year-wise Navigation**: Browse papers organized by year, then course, then semester
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **User Authentication**: Login and registration system
- **Download Functionality**: Direct download of question papers

### Backend Features
- **Modular Architecture**: Separate routes and API endpoints
- **Flask-Login Authentication**: Secure user sessions
- **SQLite Database**: Lightweight, file-based database with SQLAlchemy ORM
- **RESTful APIs**: Complete API set for all operations
- **Admin Panel**: Upload and manage question papers
- **File Upload**: Support for PDF, DOC, and DOCX files

### Admin Panel Features
- **Add Courses**: Create new course offerings
- **Upload Papers**: Add question papers with metadata
- **Manage Papers**: View and delete uploaded papers
- **File Validation**: Size and format restrictions

### API Features
- **Courses API**: CRUD operations for courses
- **Papers API**: Upload, retrieve, update, delete question papers
- **Users API**: User management and profile operations
- **Filter Support**: Query papers by course, year, semester
- **JSON Responses**: All APIs return structured JSON data

## Project Structure

```
QP/
├── backend/
│   ├── routes/             # HTML rendering routes
│   │   ├── auth.py         # Authentication routes
│   │   ├── main.py         # Main page routes
│   │   └── admin.py        # Admin panel routes
│   ├── api/                # REST API endpoints
│   │   ├── courses.py      # Courses API
│   │   ├── papers.py       # Papers API
│   │   └── users.py        # Users API
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   └── models.py           # Database models
├── frontend/
│   ├── templates/          # Jinja2 templates
│   │   ├── base.html       # Base template
│   │   ├── home.html       # Home page
│   │   ├── login.html      # Login page
│   │   ├── register.html   # Registration page
│   │   ├── admin.html      # Admin panel
│   │   ├── course_papers.html  # Course-specific papers
│   │   └── year_papers.html    # Year-wise papers
│   └── static/
│       ├── css/
│       │   └── style.css   # Custom styles
│       ├── js/
│       │   └── main.js     # JavaScript functionality
│       └── uploads/        # Uploaded files storage
├── requirements.txt        # Python dependencies
├── init_db.py             # Database initialization
├── API_DOCUMENTATION.md   # API usage guide
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### 1. Clone and Setup
```bash
cd QP
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python init_db.py
```

### 5. Run the Application
```bash
python backend/app.py
```

The application will be available at `http://127.0.0.1:5000`

## Default Admin Credentials
- Username: `admin`
- Password: `admin123`

**Important**: Change these credentials in production!

## Usage

### For Users
1. **Register**: Create an account to access the platform
2. **Browse Courses**: Click on course buttons (BSCCS, BSCIT, BCOM) to view papers
3. **Year Papers**: Use the "Year Papers" link for chronological browsing
4. **Download**: Click download buttons to get question papers

### For Administrators
1. **Login**: Use admin credentials to access admin panel
2. **Add Courses**: Create new course offerings
3. **Upload Papers**: Add question papers with proper metadata:
   - Title and subject information
   - Course, year, and semester selection
   - File upload (PDF, DOC, DOCX)
4. **Manage**: View and delete existing papers

## File Upload Guidelines
- **Supported Formats**: PDF, DOC, DOCX
- **Maximum Size**: 16MB per file
- **Organization**: Files are automatically organized by year/semester/course

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: User email address
- `password_hash`: Hashed password
- `is_admin`: Admin privilege flag
- `created_at`: Registration timestamp

### Courses Table
- `id`: Primary key
- `name`: Course full name
- `code`: Course code (e.g., BSCCS)
- `created_at`: Creation timestamp

### Question Papers Table
- `id`: Primary key
- `title`: Paper title
- `course_id`: Foreign key to courses
- `year`: Academic year
- `semester`: Semester number
- `subject`: Subject name
- `filename`: Original filename
- `file_path`: Storage path
- `uploaded_by`: Foreign key to users
- `created_at`: Upload timestamp

## Security Features
- Password hashing using Werkzeug
- Session management with Flask-Login
- File upload validation
- Admin-only access controls
- SQL injection protection via SQLAlchemy ORM

## Customization

### Adding New Courses
1. Use the admin panel interface, or
2. Modify the `create_default_courses()` function in `app.py`

### Styling
- Modify `frontend/static/css/style.css` for custom styling
- Uses Bootstrap 5 classes for responsive design
- Font Awesome icons for visual elements

### Database Configuration
Update `backend/config.py` for different database configurations:
- Development: SQLite for testing
- Production: MySQL with proper credentials
- Environment variables for sensitive data

## Deployment Considerations

### Production Setup
1. **Environment Variables**: Use environment variables for sensitive data
2. **Database**: Configure production MySQL with proper credentials
3. **File Storage**: Consider cloud storage for uploaded files
4. **Security**: Change default admin credentials
5. **SSL**: Use HTTPS in production
6. **WSGI Server**: Use Gunicorn or uWSGI instead of Flask development server

### Sample Environment Variables
```bash
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="mysql://user:pass@localhost/question_papers"
```

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Check MySQL credentials and service status
2. **File Upload Issues**: Verify upload directory permissions
3. **Import Errors**: Ensure all dependencies are installed
4. **Admin Access**: Verify admin user creation in database

### Development Tips
- Use Flask debug mode for development
- Check console logs for JavaScript errors
- Verify file paths in templates match static structure
- Test with different file types and sizes

## Contributing
1. Follow PEP 8 for Python code
2. Use semantic HTML structure
3. Maintain responsive design principles
4. Add appropriate error handling
5. Document any new features

## License
This project is designed for educational purposes. Modify and distribute as needed for your institution's requirements.