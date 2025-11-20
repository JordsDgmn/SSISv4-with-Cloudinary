# Student Information System (SSIS)

A comprehensive web-based Student Information System built with Flask and PostgreSQL, featuring student profile management with Cloudinary image uploads.

## Features

### Core Functionality
- **Student Management**: Complete CRUD operations for student records
- **Course Management**: Manage academic courses and their relationships with colleges
- **College Management**: Administer college/department information
- **Advanced Search**: Search across all entities with intelligent filtering
- **Pagination**: Efficient data loading with page navigation
- **Profile Pictures**: Upload and manage student profile photos via Cloudinary

### Technical Features
- **PostgreSQL Database**: Robust relational database with foreign key constraints
- **Responsive Design**: Bootstrap-based UI that works on all devices
- **File Upload Validation**: Image type and size validation (5MB limit)
- **Error Handling**: Comprehensive error handling and user feedback
- **Environment Configuration**: Secure configuration management with .env files

## Quick Setup

1. **Install dependencies**
   ```bash
   pipenv install
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Configure .env file with your credentials**
   ```env
   # Database Configuration
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=ssis

   # Cloudinary Configuration
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb ssis
   
   # Run schema and initial data
   psql -d ssis -f SSIS_postgres.sql
   
   # Generate and insert sample student data (300+ students)
   python generate_student_data.py
   psql -d ssis -f student_data.sql
   ```

5. **Run the application**
   ```bash
   pipenv shell
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Database Schema

- **college** - College/Department information (10 sample colleges)
- **course** - Academic programs/courses (29 sample programs)  
- **student** - Student records with profile pictures (300+ generated students)

## Project Structure

```
SSISv3-with-Cloudinary/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── SSIS_postgres.sql       # Database schema
├── generate_student_data.py # Sample data generator
├── website/                # Application package
│   ├── models/             # Database models
│   ├── routes/             # Route controllers
│   ├── templates/          # HTML templates
│   └── static/             # CSS and JS files
```

## Requirements Met

✅ **CRUD Operations**: Create, Read, Update, Delete for students, courses, and colleges  
✅ **Search Functionality**: Advanced search across all entities  
✅ **Sorting**: Data sorted by ID/code  
✅ **Photo Upload**: Student profile pictures via Cloudinary  
✅ **Database**: PostgreSQL with proper relationships  
✅ **300+ Students**: Sample data generator creates 350 students  
✅ **30+ Programs**: 29 courses across 10 colleges  

## Navigation

- **Home (/)**: Redirects to Students page
- **/students**: Student management with photos
- **/courses**: Course/program management  
- **/colleges**: College/department management

---

**Built with Flask, PostgreSQL, and Cloudinary for CCS Student Information System**
