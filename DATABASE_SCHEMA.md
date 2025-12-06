# SSIS v4 Database Schema Documentation

## Overview
This document provides a comprehensive specification of the Student Information System (SSIS v4) database schema, including all tables, relationships, constraints, and data integrity rules.

## Database: `ssis` (PostgreSQL)

---

## Table Schemas

### 1. `college` Table
**Purpose:** Stores information about academic colleges/departments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `code` | `VARCHAR(10)` | **PRIMARY KEY** | Unique college code identifier (e.g., 'CCS', 'COE') |
| `name` | `VARCHAR(100)` | **NOT NULL** | Full name of the college |

**Constraints:**
- **Primary Key:** `code` - Ensures each college has a unique identifier
- **NOT NULL:** `name` - College name is required

**Indexes:**
- Primary key automatically creates an index on `code`

**Business Rules:**
- College codes should be uppercase acronyms (3-10 characters)
- College names must be unique in practice (not enforced at DB level currently)

**Relationships:**
- **One-to-Many** with `program` table (one college can have multiple programs)
- **Cascading Delete:** Deleting a college will delete all associated programs

---

### 2. `program` Table
**Purpose:** Stores academic programs/courses offered by colleges

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `code` | `VARCHAR(10)` | **PRIMARY KEY** | Unique program code identifier (e.g., 'BSCS', 'BSIT') |
| `name` | `VARCHAR(100)` | **NOT NULL** | Full name of the program |
| `college_code` | `VARCHAR(10)` | **NOT NULL**, **FOREIGN KEY** → `college(code)` | Reference to parent college |

**Constraints:**
- **Primary Key:** `code` - Ensures each program has a unique identifier
- **Foreign Key:** `college_code` REFERENCES `college(code)` ON DELETE CASCADE
  - Ensures referential integrity (program must belong to existing college)
  - Cascading delete: If college is deleted, all its programs are deleted
- **NOT NULL:** `name`, `college_code` - Required fields

**Indexes:**
- Primary key automatically creates an index on `code`
- Foreign key automatically creates an index on `college_code`

**Business Rules:**
- Program codes should be uppercase abbreviations (2-10 characters)
- Program names should be descriptive (e.g., "Bachelor of Science in Computer Science")
- Each program must be assigned to exactly one college

**Relationships:**
- **Many-to-One** with `college` table (many programs belong to one college)
- **One-to-Many** with `student` table (one program can have multiple students)
- **Cascading Delete:** Deleting a program will delete all enrolled students

---

### 3. `student` Table
**Purpose:** Stores student records and profile information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `CHAR(9)` | **PRIMARY KEY** | Unique 9-character student ID |
| `firstname` | `VARCHAR(20)` | **NOT NULL** | Student's first name |
| `lastname` | `VARCHAR(20)` | **NOT NULL** | Student's last name |
| `program_code` | `VARCHAR(10)` | **NOT NULL**, **FOREIGN KEY** → `program(code)` | Enrolled program |
| `year` | `VARCHAR(20)` | **NOT NULL** | Year level (e.g., '1st Year', '2nd Year') |
| `gender` | `VARCHAR(10)` | **NOT NULL** | Gender ('Male' or 'Female') |
| `profile_pic_url` | `VARCHAR(255)` | **NULLABLE** | Cloudinary URL for profile picture |

**Constraints:**
- **Primary Key:** `id` - Ensures each student has a unique identifier
- **Foreign Key:** `program_code` REFERENCES `program(code)` ON DELETE CASCADE
  - Ensures referential integrity (student must be enrolled in existing program)
  - Cascading delete: If program is deleted, all enrolled students are deleted
- **NOT NULL:** `id`, `firstname`, `lastname`, `program_code`, `year`, `gender` - Required fields
- **NULLABLE:** `profile_pic_url` - Optional profile picture

**Indexes:**
- Primary key automatically creates an index on `id`
- Foreign key automatically creates an index on `program_code`

**Business Rules:**
- Student ID must be exactly 9 characters (format: YYYY-NNNN, e.g., 2021-5724)
- First name and last name limited to 20 characters each
- Year values: '1st Year', '2nd Year', '3rd Year', '4th Year'
- Gender values: 'Male', 'Female'
- Profile picture URL stores Cloudinary CDN links

**Relationships:**
- **Many-to-One** with `program` table (many students belong to one program)
- **Indirect relationship** to `college` through `program` table

---

## Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│    college      │
│─────────────────│
│ code (PK)       │◄─────┐
│ name            │      │
└─────────────────┘      │
                         │ 1:N
                         │
                  ┌──────┴────────┐
                  │    program     │
                  │────────────────│
                  │ code (PK)      │◄─────┐
                  │ name           │      │
                  │ college_code(FK)      │ 1:N
                  └────────────────┘      │
                                          │
                                   ┌──────┴────────┐
                                   │    student     │
                                   │────────────────│
                                   │ id (PK)        │
                                   │ firstname      │
                                   │ lastname       │
                                   │ program_code(FK)
                                   │ year           │
                                   │ gender         │
                                   │ profile_pic_url│
                                   └────────────────┘
```

---

## Referential Integrity & Cascading Rules

### Cascade Chain
```
DELETE college → CASCADE deletes programs → CASCADE deletes students
```

**Example:**
1. Delete `College of Computer Studies (CCS)`
2. Automatically deletes all programs: `BSCS`, `BSIT`, `BSIS`
3. Automatically deletes all students enrolled in those programs

### Foreign Key Constraints Summary

| Child Table | Foreign Key Column | Parent Table | Parent Column | On Delete Action |
|-------------|-------------------|--------------|---------------|------------------|
| `program` | `college_code` | `college` | `code` | **CASCADE** |
| `student` | `program_code` | `program` | `code` | **CASCADE** |

---

## Data Integrity Constraints

### Primary Keys (Uniqueness)
- ✅ `college.code` - Unique college identifier
- ✅ `program.code` - Unique program identifier  
- ✅ `student.id` - Unique student identifier

### Foreign Keys (Referential Integrity)
- ✅ `program.college_code` → `college.code`
- ✅ `student.program_code` → `program.code`

### NOT NULL Constraints
- ✅ `college.name`
- ✅ `program.name`, `program.college_code`
- ✅ `student.id`, `student.firstname`, `student.lastname`, `student.program_code`, `student.year`, `student.gender`

### Missing Constraints (Recommendations)

⚠️ **UNIQUE Constraints** (currently missing, should consider adding):
- `college.name` - Prevent duplicate college names
- `program.name` - Prevent duplicate program names within same college

⚠️ **CHECK Constraints** (currently missing, should consider adding):
```sql
-- Recommended additions:
ALTER TABLE student ADD CONSTRAINT check_year 
  CHECK (year IN ('1st Year', '2nd Year', '3rd Year', '4th Year'));

ALTER TABLE student ADD CONSTRAINT check_gender 
  CHECK (gender IN ('Male', 'Female'));

ALTER TABLE student ADD CONSTRAINT check_id_format 
  CHECK (id ~ '^[0-9]{4}-[0-9]{4}$');

ALTER TABLE college ADD CONSTRAINT check_code_uppercase 
  CHECK (code = UPPER(code));

ALTER TABLE program ADD CONSTRAINT check_code_uppercase 
  CHECK (code = UPPER(code));
```

---

## Data Types & Size Limits

| Table | Column | Type | Max Length | Purpose |
|-------|--------|------|------------|---------|
| `college` | `code` | `VARCHAR(10)` | 10 chars | Short acronym |
| `college` | `name` | `VARCHAR(100)` | 100 chars | Full college name |
| `program` | `code` | `VARCHAR(10)` | 10 chars | Program acronym |
| `program` | `name` | `VARCHAR(100)` | 100 chars | Full program name |
| `program` | `college_code` | `VARCHAR(10)` | 10 chars | Foreign key reference |
| `student` | `id` | `CHAR(9)` | **9 chars** | Fixed-length ID (YYYY-NNNN) |
| `student` | `firstname` | `VARCHAR(20)` | 20 chars | First name |
| `student` | `lastname` | `VARCHAR(20)` | 20 chars | Last name |
| `student` | `program_code` | `VARCHAR(10)` | 10 chars | Foreign key reference |
| `student` | `year` | `VARCHAR(20)` | 20 chars | Year level string |
| `student` | `gender` | `VARCHAR(10)` | 10 chars | Gender value |
| `student` | `profile_pic_url` | `VARCHAR(255)` | 255 chars | Cloudinary URL |

---

## Indexes

### Automatically Created Indexes
1. **Primary Key Indexes** (B-tree, unique):
   - `college_pkey` on `college(code)`
   - `program_pkey` on `program(code)`
   - `student_pkey` on `student(id)`

2. **Foreign Key Indexes** (B-tree):
   - Index on `program(college_code)` for joins
   - Index on `student(program_code)` for joins

### Recommended Additional Indexes
```sql
-- For faster name searches:
CREATE INDEX idx_college_name ON college(name);
CREATE INDEX idx_program_name ON program(name);
CREATE INDEX idx_student_name ON student(lastname, firstname);

-- For faster college-based queries:
CREATE INDEX idx_program_college_code ON program(college_code);

-- For faster program-based queries:
CREATE INDEX idx_student_program_code ON student(program_code);
```

---

## Sample Data Counts

Based on initial database setup:

| Table | Sample Count | Examples |
|-------|--------------|----------|
| `college` | 10 colleges | CCS, COE, CBA, COED, CAS, CNHS, CAF, CLAL, CME, CITC |
| `program` | 30 programs | BSCS, BSIT, BSCE, BSBA, BEED, BSN, etc. |
| `student` | Variable | Depends on user data entry |

---

## Schema Validation Checklist

### ✅ Properly Configured
- [x] Primary keys defined on all tables
- [x] Foreign key relationships established
- [x] Cascading deletes configured (college → program → student)
- [x] NOT NULL constraints on required fields
- [x] Automatic indexing on PKs and FKs

### ⚠️ Recommended Improvements
- [ ] Add UNIQUE constraints on college.name and program.name
- [ ] Add CHECK constraints for year, gender, and ID format validation
- [ ] Add CHECK constraints for uppercase code fields
- [ ] Consider adding composite unique constraint: (program.name, program.college_code)
- [ ] Add default values where applicable
- [ ] Consider adding created_at/updated_at timestamps
- [ ] Consider adding soft delete flag instead of hard deletes

---

## Migration Notes

### From MySQL to PostgreSQL
The schema was migrated from MySQL (`SSIS.sql`) to PostgreSQL (`SSIS_postgres.sql`). Key differences:
- MySQL: Uses `AUTO_INCREMENT`
- PostgreSQL: Uses `SERIAL` or sequences (not applicable here as all PKs are manually assigned)
- PostgreSQL requires explicit `IF NOT EXISTS` in CREATE TABLE statements
- PostgreSQL uses `ON CONFLICT` instead of `ON DUPLICATE KEY UPDATE`

### Schema Evolution
1. **v1:** Basic college/course/student structure
2. **v2:** Added profile picture support (`profile_pic_url` column)
3. **v3:** Terminology change: "course" → "program" (database still references old table name in some SQL files)
4. **v4:** PostgreSQL migration with proper constraints

---

## Application-Level Constraints

Beyond database constraints, the application enforces:

1. **Frontend Validation:**
   - Required field validation
   - Format validation for student ID (YYYY-NNNN pattern)
   - Dropdown selections for year and gender

2. **Backend Validation:**
   - Duplicate code detection
   - Referential integrity checks before operations
   - File upload validation for profile pictures (Cloudinary integration)

3. **Activity Logging:**
   - All CRUD operations logged to `logs/activity.log`
   - Timestamp format: `[YYYY-MM-DD HH:MM:SS] ACTION: Details`

---

## Security Considerations

1. **SQL Injection Prevention:**
   - All queries use parameterized statements (`%s` placeholders)
   - No string concatenation for query building

2. **Connection Management:**
   - Database connections managed through `DatabaseManager` class
   - Automatic connection pooling via psycopg2

3. **Credentials:**
   - Database credentials stored in `.env` file (not committed to version control)
   - Environment variables: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`

---

## Maintenance Queries

### Check Referential Integrity
```sql
-- Find orphaned programs (should return nothing):
SELECT * FROM program WHERE college_code NOT IN (SELECT code FROM college);

-- Find orphaned students (should return nothing):
SELECT * FROM student WHERE program_code NOT IN (SELECT code FROM program);
```

### Get Statistics
```sql
-- Count by college:
SELECT c.code, c.name, COUNT(DISTINCT p.code) AS programs, COUNT(s.id) AS students
FROM college c
LEFT JOIN program p ON c.code = p.college_code
LEFT JOIN student s ON p.code = s.program_code
GROUP BY c.code, c.name
ORDER BY c.code;

-- Count by program:
SELECT p.code, p.name, COUNT(s.id) AS student_count
FROM program p
LEFT JOIN student s ON p.code = s.program_code
GROUP BY p.code, p.name
ORDER BY student_count DESC;
```

### Backup Recommendations
```bash
# Backup entire database:
pg_dump -U postgres ssis > ssis_backup_$(date +%Y%m%d).sql

# Backup with inserts (portable):
pg_dump -U postgres --column-inserts ssis > ssis_backup_inserts_$(date +%Y%m%d).sql
```

---

## Document Version
- **Version:** 1.0
- **Last Updated:** December 7, 2025
- **Database Version:** PostgreSQL 12+
- **Application Version:** SSIS v4
- **Author:** System Documentation

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-07 | 1.0 | Initial comprehensive schema documentation |
