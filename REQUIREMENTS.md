# Simple Student Information System - Requirements

## Project Overview
Web Version of Simple Student Information System

## Database Schema

### Tables

#### student
- **id** (format: YYYY-NNNN)
- **firstname**
- **lastname**
- **course** → refers to the *program* table
- **year**
- **gender**
- **photo** (not required)

#### program
- **code** (e.g., BSCS)
- **name** (e.g., Bachelor of Science in Computer Science)
- **college** → refers to the *college* table

#### college
- **code** (e.g., CCS)
- **name** (e.g., College of Computer Studies)

## Core Requirements

1. **Implement CRUDL** (Create, Read, Update, Delete, List) for:
   - student
   - program
   - college

2. **Features**:
   - Searching
   - Sorting
   - Pagination

3. **Photo Upload**:
   - Uploading of student photo
   - Photo should be uploaded to Cloudinary (not supabase as originally specified)

4. **Database**:
   - Use PostgreSQL
   - Must be pre-populated with at least **300 students** and **30 programs**

5. **Project Structure**:
   - Follow the project structure from the Flask Demo Project
   - Use Blueprint-based modular architecture
   - Implement MVC design pattern

## Technology Stack

### Backend
- Flask 3.x
- Python 3.10+
- PostgreSQL with psycopg2

### Frontend
- Bootstrap 5
- Jinja2 templates
- DataTables for advanced table features

### Forms & Authentication
- Flask-WTF
- WTForms
- Form validation

### Image Upload
- Cloudinary integration

### Environment
- Pipenv for dependency management
- .env for configuration

## Project Structure
```
SSISv4-with-Cloudinary/
├── app.py                     # Application entry point
├── config.py                  # Configuration settings
├── website/                   # Main application package
│   ├── __init__.py           # Application factory
│   ├── database.py           # Database connection management
│   ├── models/               # Database models (M in MVC)
│   │   ├── collegeModels.py
│   │   ├── courseModels.py
│   │   └── studentModels.py
│   ├── routes/               # Route controllers (C in MVC)
│   │   ├── collegeRoute.py
│   │   ├── courseRoute.py
│   │   └── studentRoute.py
│   ├── templates/            # Jinja2 templates (V in MVC)
│   │   ├── layouts.html      # Base template
│   │   ├── colleges.html
│   │   ├── courses.html
│   │   └── students.html
│   └── static/               # CSS, JS, images
│       ├── modern-style.css
│       ├── modern-app.js
│       └── app.js
├── SSIS_postgres.sql         # Database schema
├── generate_student_data.py  # Sample data generator
├── student_data.sql          # Generated student data
├── .env                      # Environment variables
└── Pipfile                   # Dependencies
```

## Security Features
- CSRF Protection
- SQL Injection Prevention (parameterized queries)
- Environment Variables for sensitive data
- Form validation

## Development Guidelines
1. Follow MVC pattern for organization
2. Use Blueprints for modular design
3. Implement proper error handling
4. Use Bootstrap 5 for responsive design
5. Maintain clean, readable code structure
