# Simple Student Information System (SSIS v4) - Project Instructions

## Project Overview
Web Version of Simple Student Information System with full CRUD operations, image upload, and database management.

---

## Database Schema

### Tables Required

#### 1. **student** Table
| Column | Format/Type | Description |
|--------|-------------|-------------|
| `id` | `CHAR(9)` | Format: `YYYY-NNNN` (e.g., 2021-5724) |
| `firstname` | `VARCHAR(20)` | Student's first name |
| `lastname` | `VARCHAR(20)` | Student's last name |
| `course` | `VARCHAR(10)` FK | **Refers to `program` table** |
| `year` | `VARCHAR(20)` | Year level (1st Year, 2nd Year, etc.) |
| `gender` | `VARCHAR(10)` | Gender (Male/Female) |
| `photo` | `VARCHAR(255)` | **NOT REQUIRED** - Photo URL |

**Note:** The `course` column refers to the `program` table (code field).

---

#### 2. **program** Table
| Column | Format/Type | Description |
|--------|-------------|-------------|
| `code` | `VARCHAR(10)` PK | Program code (e.g., BSCS, BSIT) |
| `name` | `VARCHAR(100)` | Full program name (e.g., Bachelor of Science in Computer Science) |
| `college` | `VARCHAR(10)` FK | **Refers to `college` table** |

**Note:** The `college` column refers to the `college` table (code field).

---

#### 3. **college** Table
| Column | Format/Type | Description |
|--------|-------------|-------------|
| `code` | `VARCHAR(10)` PK | College code (e.g., CCS, COE) |
| `name` | `VARCHAR(100)` | Full college name (e.g., College of Computer Studies) |

---

## Functional Requirements

### Core Operations (CRUDL)
Implement **Create, Read, Update, Delete, List** operations for:
1. ✅ **student**
2. ✅ **program**
3. ✅ **college**

### Additional Features Required

#### 1. **Searching**
- ✅ Search functionality for all three entities
- ✅ Must allow searching across relevant fields

#### 2. **Sorting**
- ✅ Sort by any column in tables
- ✅ Ascending/descending order

#### 3. **Pagination**
- ✅ Display data in pages
- ✅ User can navigate between pages
- ✅ Configurable page size

#### 4. **Photo Upload**
- ✅ Upload student photos
- ⚠️ **IMPORTANT:** Photos must be uploaded to **Cloudinary** (changed from Supabase)
- Photo is **optional** (not required)

---

## Technical Requirements

### Database
- **PostgreSQL** must be used
- ✅ Database must be pre-populated with:
  - **At least 300 students**
  - **At least 30 programs**
  - Sufficient colleges to support programs

### Project Structure
- ✅ Follow the **Flask Demo Project** structure
- Use Blueprint architecture
- Separate models, routes, templates

---

## Data Integrity Rules

### Primary Keys (UNIQUE)
- ❗ **college.code** - Must be unique
- ❗ **program.code** - Must be unique
- ❗ **student.id** - Must be unique

### Foreign Key Constraints
- ❗ **program.college** → Must reference existing `college.code`
- ❗ **student.course** → Must reference existing `program.code`

### Cascade Rules
- ❗ Deleting a **college** → Cascades to delete all associated **programs**
- ❗ Deleting a **program** → Cascades to delete all enrolled **students**

### Validation Rules
- ❗ **NO DUPLICATES ALLOWED** for primary keys
- ❗ All required fields must be filled
- ❗ Foreign keys must reference existing records
- ❗ Student ID format must be `YYYY-NNNN`
- ❗ Error messages must be clear and informative

---

## Implementation Checklist

### Database Setup
- [x] PostgreSQL database created
- [x] All three tables created with proper constraints
- [x] Primary keys defined
- [x] Foreign keys defined with CASCADE
- [x] Pre-populated with 300+ students
- [x] Pre-populated with 30+ programs
- [x] Pre-populated with 10+ colleges

### Student Management
- [x] Create student (with validation)
- [x] View student list (with pagination)
- [x] View individual student details
- [x] Update student information
- [x] Delete student
- [x] Search students
- [x] Sort student table
- [x] Upload student photo to Cloudinary

### Program Management
- [x] Create program (with validation)
- [x] View program list (with pagination)
- [x] View program details
- [x] Update program information
- [x] Delete program
- [x] Search programs
- [x] Sort program table
- [x] Link programs to colleges

### College Management
- [x] Create college (with validation)
- [x] View college list (with pagination)
- [x] View college details
- [x] Update college information
- [x] Delete college
- [x] Search colleges
- [x] Sort college table

### UI/UX Requirements
- [x] Clean, modern interface
- [x] Responsive design
- [x] Dark mode support
- [x] Flash messages for operations
- [x] Confirmation dialogs for deletions
- [x] Form validation (client & server-side)
- [x] Loading indicators

### Error Handling
- [ ] **ISSUE:** Duplicate key errors not properly displayed
- [x] Database connection errors handled
- [x] Invalid foreign key references prevented
- [x] Empty form submissions prevented
- [x] File upload errors handled
- [x] User-friendly error messages

---

## Known Issues to Fix

### 1. Duplicate Key Validation ❌
**Problem:** When trying to create a college/program with existing code, the system shows "Successfully created" even though the database rejected it due to UNIQUE constraint.

**Current Behavior:**
```
Console: "Create result: failed to create college: duplicate key violates unique constraint"
UI: "✅ College created successfully"
```

**Expected Behavior:**
```
Console: "ERROR: Duplicate key detected"
UI: "❌ Error: College with code 'CCS' already exists"
```

**Fix Required:**
- Check the return value from `create_college()` and `create_program()`
- Only show success message if operation actually succeeded
- Show error message with duplicate details if it failed

### 2. Validation Before Database Operation
**Enhancement:** Check if code exists BEFORE attempting database insert to provide better error messages.

---

## File Structure
```
SSISv3-with-Cloudinary/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── DATABASE_SCHEMA.md              # Database documentation
├── PROJECT_INSTRUCTIONS.md         # This file
├── SSIS.sql                        # MySQL schema (legacy)
├── SSIS_postgres.sql              # PostgreSQL schema
├── website/
│   ├── __init__.py                # App factory
│   ├── database.py                # Database connection
│   ├── models/
│   │   ├── collegeModels.py       # College CRUD operations
│   │   ├── programModels.py       # Program CRUD operations
│   │   └── studentModels.py       # Student CRUD operations
│   ├── routes/
│   │   ├── collegeRoute.py        # College routes
│   │   ├── programRoute.py        # Program routes
│   │   └── studentRoute.py        # Student routes
│   ├── static/
│   │   ├── modern-app.js          # Frontend JavaScript
│   │   ├── modern-style.css       # Main stylesheet
│   │   └── ...
│   └── templates/
│       ├── layouts.html           # Base template
│       ├── students.html          # Student management UI
│       ├── programs.html          # Program management UI
│       └── colleges.html          # College management UI
└── logs/
    └── activity.log               # Activity logging
```

---

## Development Notes

### Technologies Used
- **Backend:** Flask 3.x (Python)
- **Database:** PostgreSQL 12+
- **ORM:** psycopg2 (direct SQL queries)
- **Frontend:** Bootstrap 5, jQuery 3.7.1, DataTables
- **File Storage:** Cloudinary CDN
- **Environment:** Python venv

### Key Features Implemented
1. ✅ Full CRUD operations for all entities
2. ✅ Advanced search with ILIKE (case-insensitive)
3. ✅ DataTables integration (sorting, pagination, search)
4. ✅ Image upload to Cloudinary with transformation
5. ✅ Activity logging system
6. ✅ Dark mode toggle
7. ✅ Responsive design
8. ✅ Form validation (client and server)
9. ✅ Flash message system
10. ✅ Cascading deletes with confirmations

---

## Testing Checklist

### Duplicate Prevention Testing
- [ ] Try creating college with existing code → Should show error
- [ ] Try creating program with existing code → Should show error
- [ ] Try creating student with existing ID → Should show error

### Foreign Key Testing
- [ ] Try creating program with non-existent college → Should show error
- [ ] Try creating student with non-existent program → Should show error

### Cascade Delete Testing
- [ ] Delete college → Should delete all programs and their students
- [ ] Delete program → Should delete all enrolled students
- [ ] Proper confirmation dialogs shown

### Search/Sort/Pagination Testing
- [ ] Search works across all fields
- [ ] Sort works on all sortable columns
- [ ] Pagination displays correct number of items
- [ ] Page navigation works correctly

---

## Version History
- **v1:** Initial MySQL implementation
- **v2:** Added profile picture support
- **v3:** Terminology change (course → program)
- **v4:** PostgreSQL migration + comprehensive features + bug fixes needed

---

## Next Steps
1. ✅ Fix duplicate key validation in routes
2. ✅ Add pre-validation before database operations
3. ✅ Improve error messages
4. Test all CRUD operations thoroughly
5. Performance optimization
6. Final code review

---

**Last Updated:** December 7, 2025
**Status:** 95% Complete - Fixing duplicate validation
