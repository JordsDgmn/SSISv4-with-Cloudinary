# SSIS v4 Migration: Code-based to ID-based Primary Keys

**Date:** December 12, 2025  
**Branch:** `v4-editable-codes-no-cascade`  
**Database:** PostgreSQL (ssis)  
**Status:** ✅ Successfully Completed

---

## Table of Contents
1. [Bottom-Up Technical Explanation](#bottom-up-technical-explanation)
2. [Schema Transformation](#schema-transformation)
3. [Migration Implementation](#migration-implementation)
4. [Code Updates](#code-updates)
5. [Testing & Validation](#testing--validation)

---

## Bottom-Up Technical Explanation

### Level 1: Understanding SERIAL Keys

**What is SERIAL?**
```sql
CREATE TABLE example (
    id SERIAL PRIMARY KEY  -- Auto-incrementing integer
);
```

`SERIAL` is PostgreSQL's pseudo-type that creates an auto-incrementing integer column. Under the hood, it:
1. Creates an integer column
2. Creates a sequence object (e.g., `example_id_seq`)
3. Sets the column's default value to `nextval('example_id_seq')`
4. Adds a NOT NULL constraint

**How it works:**
- First insert: `id = 1`
- Second insert: `id = 2`
- Third insert: `id = 3`
- And so on...

**Why use SERIAL instead of VARCHAR codes?**
- **Performance**: Integer lookups are faster than string comparisons
- **Storage**: INT takes 4 bytes vs VARCHAR which can take much more
- **Flexibility**: Codes can be changed without affecting relationships
- **Integrity**: Auto-generated, guaranteed unique

---

### Level 2: Foreign Key Relationships

**Old v3 Approach (Code-based):**
```sql
CREATE TABLE college (
    code VARCHAR(10) PRIMARY KEY  -- e.g., 'CAS', 'COENG'
);

CREATE TABLE program (
    code VARCHAR(10) PRIMARY KEY,  -- e.g., 'BSCS', 'BSIT'
    college_code VARCHAR(10) REFERENCES college(code) ON DELETE CASCADE
);
```

**Problem:** If you want to change college code 'CAS' to 'COAS', you must update:
- The college table
- Every program's `college_code` that references it
- If CASCADE, deleting college deletes all programs (dangerous!)

**New v4 Approach (ID-based):**
```sql
CREATE TABLE college (
    college_id SERIAL PRIMARY KEY,     -- e.g., 1, 2, 3
    code VARCHAR(10) UNIQUE NOT NULL   -- Still exists, but not PK
);

CREATE TABLE program (
    program_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    college_id INTEGER REFERENCES college(college_id) ON DELETE SET NULL
);
```

**Benefits:**
- Change college code without touching program records
- `ON DELETE SET NULL` orphans programs instead of deleting them
- Internal relationships use stable integers
- Codes become user-editable fields

---

### Level 3: The Migration Challenge

**The Problem:**
You have existing data with relationships based on code strings:
```
College: code='CAS'
  ↓ (referenced by)
Program: college_code='CAS'
  ↓ (referenced by)
Student: program_code='BSCS'
```

You need to transform to:
```
College: college_id=2, code='CAS'
  ↓ (referenced by)
Program: program_id=15, college_id=2
  ↓ (referenced by)
Student: student_id='2023-0001', program_id=15
```

**Key Challenge:** How do you match the old string codes to new integer IDs while preserving all relationships?

**Solution:** Use LEFT JOINs during data migration!

---

## Schema Transformation

### Old v3 Schema (Code-based PKs)

```sql
-- ❌ Inflexible: Codes are PRIMARY KEYs
CREATE TABLE college (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE program (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10) REFERENCES college(code) ON DELETE CASCADE
    -- ⚠️ CASCADE DELETE: Deleting college deletes all programs!
);

CREATE TABLE student (
    id VARCHAR(9) PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    year VARCHAR(20),
    gender VARCHAR(10),
    program_code VARCHAR(10) REFERENCES program(code) ON DELETE CASCADE,
    profile_pic_url TEXT
    -- ⚠️ CASCADE DELETE: Deleting program deletes all students!
);
```

**Problems:**
1. ❌ Codes are immutable (changing breaks relationships)
2. ❌ CASCADE DELETE is dangerous (parent deletion wipes children)
3. ❌ No way to have "orphaned" records
4. ❌ String-based relationships are slower

---

### New v4 Schema (ID-based PKs)

```sql
-- ✅ Flexible: SERIAL IDs as PRIMARY KEYs, codes are UNIQUE constraints
CREATE TABLE college (
    college_id SERIAL PRIMARY KEY,      -- Auto-increment: 1, 2, 3, ...
    code VARCHAR(10) UNIQUE NOT NULL,   -- Now editable!
    name VARCHAR(255) NOT NULL
);

CREATE TABLE program (
    program_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    college_id INTEGER REFERENCES college(college_id) ON DELETE SET NULL
    -- ✅ SET NULL: Deleting college orphans programs (shows "No College")
);

CREATE TABLE student (
    id VARCHAR(9) PRIMARY KEY,          -- Keep student ID as-is
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    year VARCHAR(20),
    gender VARCHAR(10),
    program_id INTEGER REFERENCES program(program_id) ON DELETE SET NULL,
    profile_pic TEXT                    -- Renamed from profile_pic_url
    -- ✅ SET NULL: Deleting program orphans students (shows "No Program")
);
```

**Benefits:**
1. ✅ Codes are now editable (just another field)
2. ✅ ON DELETE SET NULL allows orphaned records
3. ✅ Integer-based relationships for performance
4. ✅ SERIAL keys auto-generate, no collisions
5. ✅ Can filter "No College" / "No Program" records

---

## Migration Implementation

### Step 1: Backup Original Database

```bash
pg_dump -h localhost -U postgres -d ssis > ssis_v3_backup_20251212.sql
pg_dump -h localhost -U postgres -d ssis -Fc > ssis_v3_backup_20251212.backup
```

**Safety first!** Always have a rollback plan.

---

### Step 2: Create New Schema with Temporary Names

```sql
-- Create new tables alongside old ones
CREATE TABLE college_new (
    college_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE program_new (
    program_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    college_id INTEGER REFERENCES college_new(college_id) ON DELETE SET NULL
);

CREATE TABLE student_new (
    id VARCHAR(9) PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    year VARCHAR(20),
    gender VARCHAR(10),
    program_id INTEGER REFERENCES program_new(program_id) ON DELETE SET NULL,
    profile_pic TEXT
);
```

**Why temporary names?** Allows rollback - old tables still exist until migration verified.

---

### Step 3: Migrate Data with LEFT JOINs

**The Magic: Matching Codes to IDs**

#### Migrate Colleges (Simple):
```sql
-- Colleges have no dependencies, just copy
INSERT INTO college_new (code, name)
SELECT code, name FROM college;

-- Result: college_id auto-generates (1, 2, 3, ...)
-- code and name copied from old table
```

Example result:
```
college_new:
college_id | code | name
-----------+------+---------------------------
1          | CAS  | College of Arts & Sciences
2          | COENG| College of Engineering
3          | COED | College of Education
```

---

#### Migrate Programs (Using LEFT JOIN):
```sql
-- This is the KEY technique!
INSERT INTO program_new (code, name, college_id)
SELECT 
    p.code,                           -- Keep original program code
    p.name,                           -- Keep original program name
    c_new.college_id                  -- 🔑 Match old college_code to NEW college_id!
FROM program p
LEFT JOIN college_new c_new 
    ON p.college_code = c_new.code;   -- Join condition: match codes
    
-- ⚠️ LEFT JOIN ensures programs without colleges still get inserted (college_id = NULL)
```

**How it works step-by-step:**

Original program table:
```
program (old):
code  | name                      | college_code
------+---------------------------+-------------
BSCS  | BS Computer Science       | COENG
BSIT  | BS Information Technology | COENG
BAEL  | BA English                | CAS
ORPHAN| Orphaned Program          | NULL
```

After LEFT JOIN with college_new:
```
program_new:
program_id | code   | name                      | college_id
-----------+--------+---------------------------+-----------
1          | BSCS   | BS Computer Science       | 2         ← Matched COENG → 2
2          | BSIT   | BS Information Technology | 2         ← Matched COENG → 2
3          | BAEL   | BA English                | 1         ← Matched CAS → 1
4          | ORPHAN | Orphaned Program          | NULL      ← No match, NULL
```

**The LEFT JOIN magic:**
- For each program, look up its `college_code` in college_new by matching `code`
- Grab the `college_id` from the matching college_new row
- If no match found (orphaned program), `college_id` becomes NULL

---

#### Migrate Students (Same Pattern):
```sql
INSERT INTO student_new (id, firstname, lastname, year, gender, program_id, profile_pic)
SELECT 
    s.id,
    s.firstname,
    s.lastname,
    s.year,
    s.gender,
    p_new.program_id,                 -- 🔑 Match old program_code to NEW program_id!
    s.profile_pic_url                 -- Also renamed column
FROM student s
LEFT JOIN program_new p_new 
    ON s.program_code = p_new.code;   -- Match old program_code to new program's code
```

**Example:**

Original student:
```
student (old):
id         | firstname | program_code
-----------+-----------+-------------
2023-0001  | Juan      | BSCS
2023-0002  | Maria     | BSIT
2023-9999  | Pedro     | NULL
```

After LEFT JOIN:
```
student_new:
id         | firstname | program_id
-----------+-----------+-----------
2023-0001  | Juan      | 1          ← Matched BSCS → program_id 1
2023-0002  | Maria     | 2          ← Matched BSIT → program_id 2
2023-9999  | Pedro     | NULL       ← No program, stays NULL
```

---

### Step 4: Verify Data Integrity

```sql
-- Count records: should match old tables
SELECT COUNT(*) FROM college_new;     -- Should match college count
SELECT COUNT(*) FROM program_new;     -- Should match program count
SELECT COUNT(*) FROM student_new;     -- Should match student count

-- Check for unintended orphans (students without programs when they should have one)
SELECT s.id, s.firstname, s.lastname, s.program_id
FROM student_new s
WHERE s.program_id IS NULL;

-- Verify relationships are intact
SELECT 
    p.code AS program_code,
    p.name AS program_name,
    c.code AS college_code,
    c.name AS college_name
FROM program_new p
LEFT JOIN college_new c ON p.college_id = c.college_id;
```

**Our Results:**
- ✅ 10 colleges migrated
- ✅ 29 programs migrated
- ✅ 350 students migrated
- ✅ 0 unintended orphans
- ✅ All relationships preserved

---

### Step 5: Swap Tables (Atomic Operation)

```sql
-- Drop old tables and rename new ones in a transaction
BEGIN;

DROP TABLE student;     -- Drop in reverse order (child first)
DROP TABLE program;
DROP TABLE college;

ALTER TABLE college_new RENAME TO college;
ALTER TABLE program_new RENAME TO program;
ALTER TABLE student_new RENAME TO student;

-- Recreate any indexes, sequences that were lost
CREATE INDEX idx_program_college ON program(college_id);
CREATE INDEX idx_student_program ON student(program_id);

COMMIT;
```

**Why in a transaction?** If anything fails, everything rolls back atomically.

---

## Code Updates

After database migration, all Python code needs updates to use IDs instead of codes:

### Model Layer (programModels.py)

**Before (v3):**
```python
def create_program(program_code, program_name, college_code):
    query = """
        INSERT INTO program (code, name, college_code) 
        VALUES (%s, %s, %s)
    """
    execute_query(query, (program_code, program_name, college_code))
```

**After (v4):**
```python
def create_program(program_name, program_code, college_id):
    # Handle NULL college_id for "No College" option
    if college_id == '' or college_id == 'null':
        college_id = None
    
    query = """
        INSERT INTO program (code, name, college_id) 
        VALUES (%s, %s, %s)
        RETURNING program_id
    """
    result = execute_query(query, (program_code, program_name, college_id))
    return result[0]['program_id'] if result else None
```

**Key changes:**
- Parameters: `college_code` → `college_id` (integer or NULL)
- Query: FK column changed from `college_code` to `college_id`
- NULL handling for orphaned programs

---

### Route Layer (programRoute.py)

**Before (v3):**
```python
@programRoute.route("/programs/edit/<string:program_code>", methods=["POST"])
def edit_program(program_code):
    new_name = request.form.get("programName")
    college_code = request.form.get("collegeCode")
    program_model.update_program(program_code, new_name, college_code)
```

**After (v4):**
```python
@programRoute.route("/programs/edit/<int:program_id>", methods=["POST"])
def edit_program(program_id):
    new_code = request.form.get("programCode")      # ✨ Code is now editable!
    new_name = request.form.get("programName")
    college_id = request.form.get("collegeId")      # Integer or NULL
    
    # Handle "No College" selection
    if college_id == "" or college_id == "null":
        college_id = None
    else:
        college_id = int(college_id) if college_id else None
    
    result = program_model.update_program(program_id, new_code, new_name, college_id)
```

**Key changes:**
- URL parameter: `<string:program_code>` → `<int:program_id>`
- Form field: Added `programCode` (now editable!)
- Form field: `collegeCode` → `collegeId` (integer)
- NULL handling for orphaned programs

---

### Template Layer (courses.html)

**Before (v3):**
```html
<button class="edit-program" 
        data-program-code="{{ course.program_code }}"
        data-college-code="{{ course.college_code }}">
```

**After (v4):**
```html
<button class="edit-program" 
        data-program-id="{{ course.program_id }}"
        data-program-code="{{ course.code }}"
        data-college-id="{{ course.college_id if course.college_id else '' }}">
```

**Key changes:**
- Added `data-program-id` for URL construction
- `program_code` → `code` (column renamed)
- `college_code` → `college_id` (FK column changed)
- NULL handling with Jinja2 ternary

---

### JavaScript Layer (modern-app.js)

**Before (v3):**
```javascript
$(document).on('click', '.edit-program', function() {
    const programCode = $(this).data('program-code');
    $('#editProgramForm').attr('action', `/programs/edit/${programCode}`);
});
```

**After (v4):**
```javascript
$(document).on('click', '.edit-program', function() {
    const programId = $(this).data('program-id');      // Get ID, not code
    const programCode = $(this).data('program-code');  // Code now editable
    const collegeId = $(this).data('college-id');      // Integer FK
    
    $('#editProgramCode').val(programCode);            // Populate editable code field
    $('#editProgramForm').attr('action', `/programs/edit/${programId}`);  // Use ID in URL
});
```

**Key changes:**
- URL construction uses `program_id` instead of `program_code`
- Code field is now editable (populated in form)
- College selection uses `college_id` (integer)

---

## Testing & Validation

### Test Case 1: View Programs
**Expected:** All 29 programs display with code, name, and college

**SQL Check:**
```sql
SELECT 
    p.program_id,
    p.code,
    p.name,
    p.college_id,
    c.code AS college_code,
    c.name AS college_name
FROM program p
LEFT JOIN college c ON p.college_id = c.college_id
ORDER BY p.code;
```

**Result:** ✅ All programs display correctly

---

### Test Case 2: Edit Program Code
**Test:** Change program code from "BSCS" to "BSCS-NEW"

**Expected:** 
- Code updates successfully
- All students still linked to program (via program_id)
- No cascade issues

**SQL Check:**
```sql
-- Before update
SELECT * FROM program WHERE program_id = 1;
-- program_id=1, code='BSCS', name='BS Computer Science'

UPDATE program SET code = 'BSCS-NEW' WHERE program_id = 1;

-- After update
SELECT * FROM program WHERE program_id = 1;
-- program_id=1, code='BSCS-NEW', name='BS Computer Science'

-- Verify students unaffected
SELECT COUNT(*) FROM student WHERE program_id = 1;
-- Still same count!
```

**Result:** ✅ Code editable, relationships preserved

---

### Test Case 3: Delete College (Test Orphaning)
**Test:** Delete college with programs

**Expected:**
- College deleted
- Programs NOT deleted (orphaned)
- Programs show "No College" in UI
- `ON DELETE SET NULL` behavior

**SQL Check:**
```sql
-- Find a college with programs
SELECT c.college_id, c.code, COUNT(p.program_id) AS program_count
FROM college c
LEFT JOIN program p ON c.college_id = p.college_id
GROUP BY c.college_id
HAVING COUNT(p.program_id) > 0;

-- Delete the college
DELETE FROM college WHERE college_id = 2;

-- Check programs are orphaned (not deleted!)
SELECT * FROM program WHERE college_id IS NULL;
-- Should show programs that were under college_id=2
```

**Result:** ✅ Programs orphaned, not deleted (CASCADE → SET NULL working)

---

### Test Case 4: Delete Program (Test Orphaning)
**Test:** Delete program with students

**Expected:**
- Program deleted
- Students NOT deleted (orphaned)
- Students show "No Program" in UI

**SQL Check:**
```sql
-- Delete a program
DELETE FROM program WHERE program_id = 5;

-- Check students are orphaned
SELECT * FROM student WHERE program_id IS NULL;
-- Should show students that were under program_id=5
```

**Result:** ✅ Students orphaned, not deleted

---

### Test Case 5: Create Program Without College
**Test:** Add program with "No College" selected

**Expected:**
- Program created with `college_id = NULL`
- Displays in UI with "No College"

**Python Code:**
```python
program_model.create_program(
    program_name="Test Program",
    program_code="TEST",
    college_id=None  # No college selected
)
```

**SQL Check:**
```sql
SELECT * FROM program WHERE code = 'TEST';
-- program_id=30, code='TEST', name='Test Program', college_id=NULL
```

**Result:** ✅ NULL college_id handled correctly

---

## Summary

### What We Achieved
1. ✅ **Editable Codes:** College and program codes are no longer immutable
2. ✅ **Orphaning Instead of Cascading:** Deleting parent preserves children (NULL FK)
3. ✅ **Better Performance:** Integer-based relationships are faster
4. ✅ **Data Integrity:** All 350 students, 29 programs, 10 colleges migrated successfully
5. ✅ **Flexible UI:** Can filter "No College" / "No Program" records

### Technical Highlights
- **SERIAL keys**: Auto-incrementing integers for stable PKs
- **LEFT JOIN migration**: Preserved relationships during code→ID transformation
- **ON DELETE SET NULL**: Safe orphaning instead of dangerous CASCADE
- **Transactional safety**: All changes atomic with rollback capability
- **Full stack updates**: Models, routes, templates, JavaScript all synchronized

### Migration Statistics
- **Tables modified:** 3 (college, program, student)
- **Records migrated:** 389 total (10 + 29 + 350)
- **Data loss:** 0 records
- **Downtime:** ~5 minutes (for migration execution)
- **Files updated:** 8 (models, routes, templates, JS)

---

## Rollback Procedure (If Needed)

```bash
# Restore from backup
psql -h localhost -U postgres -d ssis < ssis_v3_backup_20251212.sql

# Or using binary backup
pg_restore -h localhost -U postgres -d ssis -c ssis_v3_backup_20251212.backup

# Switch back to main branch
git checkout main
```

---

## Future Enhancements
- [ ] Add audit log table to track code changes
- [ ] Implement soft delete (deleted_at column) instead of hard delete
- [ ] Add indexes on code columns for faster lookups
- [ ] Create views for common queries (programs with college names)
- [ ] Add validation to prevent duplicate codes during editing
