# Student ID Format Changes - Implementation Checklist

## Overview
Change student ID format from 8-digit (20168837) to **YYYY-XXXX** format (2025-0001) with auto-increment functionality.

---

## ✅ Phase 1: Database Schema Changes

### 1.1 Update Student Table
- [ ] Change `student.id` column type from `CHAR(9)` to `VARCHAR(10)` to accommodate dash
- [ ] Update constraint to validate format: `YYYY-XXXX` where YYYY is year and XXXX is 4-digit number
- [ ] Add check constraint: `CHECK (id ~ '^[0-9]{4}-[0-9]{4}$')`

### 1.2 Create Sequence/Function for Auto-Increment
- [ ] Create PostgreSQL function `generate_student_id()` that:
  - Gets current year (e.g., 2025)
  - Finds highest XXXX number for that year
  - Returns next ID (e.g., if 2025-0005 exists, return 2025-0006)
  - Handles year rollover (2025-9999 → 2026-0001)

---

## ✅ Phase 2: Database Migration & Data Repopulation

### 2.1 Backup Current Data
- [ ] Export current student data to backup file
- [ ] Save relationships (program_code, year, gender, etc.)

### 2.2 Clear & Repopulate
- [ ] Clear all students: `DELETE FROM student CASCADE;`
- [ ] Generate new student data with proper ID format
- [ ] Create `repopulate_students.py` script that:
  - Generates 346 students with IDs from 2021-0001 to 2025-XXXX
  - Distributes across years 2021-2025
  - Maintains proper foreign keys to programs/colleges

### 2.3 Update Sample Data
- [ ] Modify `generate_student_data.py` to use new format
- [ ] Update `insert_data.py` to use new format
- [ ] Ensure test data uses YYYY-XXXX format

---

## ✅ Phase 3: Backend Model Changes

### 3.1 Update Student Model (`studentModels.py`)
- [ ] Update `create_student()` method:
  - Remove manual ID input parameter
  - Call `generate_student_id()` function
  - Auto-assign ID before insert
- [ ] Update validation:
  - Remove 9-digit ID validation
  - Add YYYY-XXXX format validation for direct SQL inserts
  - Pattern: `^\d{4}-\d{4}$`
- [ ] Keep `update_student()` with ID as immutable (no changes needed)

### 3.2 Add ID Generation Function
```python
@classmethod
def generate_next_student_id(cls, year=None):
    """Generate next student ID in YYYY-XXXX format"""
    if year is None:
        year = datetime.now().year
    
    with DatabaseManager.get_cursor() as (cur, conn):
        cur.execute("""
            SELECT id FROM student 
            WHERE id LIKE %s 
            ORDER BY id DESC LIMIT 1
        """, (f"{year}-%",))
        
        result = cur.fetchone()
        if result:
            last_id = result['id']
            last_num = int(last_id.split('-')[1])
            next_num = last_num + 1
        else:
            next_num = 1
        
        return f"{year}-{next_num:04d}"
```

---

## ✅ Phase 4: Frontend Template Changes

### 4.1 Add Student Modal (`students.html`)
- [ ] **Remove** Student ID input field entirely from add modal
- [ ] Add hidden info text: "Student ID will be auto-generated (2025-XXXX)"
- [ ] Update form to not send `studentID` parameter
- [ ] Remove validation for 9-digit ID

### 4.2 Edit Student Modal (`students.html`)
- [ ] Keep Student ID field **visible** but **read-only** with lock icon
- [ ] Change input to: `<input type="text" class="form-control-plaintext bg-light" readonly>`
- [ ] Update label: "Student ID (Cannot be changed)"
- [ ] Add styling to show it's permanent/locked

### 4.3 Student Display
- [ ] Update table display to show YYYY-XXXX format
- [ ] Update student view page to show format with dash
- [ ] Ensure sorting works correctly with new format

---

## ✅ Phase 5: Route Handler Changes

### 5.1 Create Student Route (`studentRoute.py`)
- [ ] Remove `student_id` from `request.form.get()`
- [ ] Call `student_model.generate_next_student_id()` to get new ID
- [ ] Pass generated ID to `create_student()` method
- [ ] Update success message to show assigned ID

### 5.2 Update Validation
- [ ] Remove 9-digit ID validation in add route
- [ ] Keep ID immutable in edit route
- [ ] Add validation for direct database inserts (SQL)

---

## ✅ Phase 6: JavaScript Changes

### 6.1 Add Student Form (`modern-app.js`)
- [ ] Remove Student ID field validation
- [ ] Remove `studentID` from form data collection
- [ ] Update success message to show auto-generated ID
- [ ] Remove pattern validation for 9 digits

### 6.2 Edit Student Form
- [ ] Keep Student ID display-only logic
- [ ] Ensure ID is not sent in edit request body
- [ ] Keep visual lock indication

---

## ✅ Phase 7: Database Function Creation

### 7.1 Create PostgreSQL Function
```sql
CREATE OR REPLACE FUNCTION generate_student_id() 
RETURNS VARCHAR(10) AS $$
DECLARE
    current_year INT;
    max_number INT;
    next_id VARCHAR(10);
BEGIN
    current_year := EXTRACT(YEAR FROM CURRENT_DATE);
    
    SELECT COALESCE(MAX(CAST(SPLIT_PART(id, '-', 2) AS INT)), 0)
    INTO max_number
    FROM student
    WHERE id LIKE current_year || '-%';
    
    next_id := current_year || '-' || LPAD((max_number + 1)::TEXT, 4, '0');
    
    RETURN next_id;
END;
$$ LANGUAGE plpgsql;
```

### 7.2 Test Function
- [ ] Test generating first ID: 2025-0001
- [ ] Test incrementing: 2025-0001 → 2025-0002
- [ ] Test year boundary: 2024-9999 → 2025-0001
- [ ] Test with gaps: 2025-0001, 2025-0010 → 2025-0011

---

## ✅ Phase 8: Testing & Validation

### 8.1 Unit Tests
- [ ] Test ID generation function
- [ ] Test ID format validation
- [ ] Test create student without manual ID
- [ ] Test edit student with immutable ID
- [ ] Test direct SQL insert with custom ID (2023-0011)

### 8.2 Integration Tests
- [ ] Test adding student through UI
- [ ] Test editing student through UI
- [ ] Test student display in tables
- [ ] Test search with new ID format
- [ ] Test sorting by ID

### 8.3 Edge Cases
- [ ] Test year rollover (Dec 31 → Jan 1)
- [ ] Test max increment (9999)
- [ ] Test concurrent ID generation
- [ ] Test foreign key constraints with new format
- [ ] Test bulk insert with mixed years

---

## ✅ Phase 9: Documentation Updates

### 9.1 Update Schema Documentation
- [ ] Update `DATABASE_SCHEMA.md` with new ID format
- [ ] Document `generate_student_id()` function
- [ ] Add examples of valid IDs

### 9.2 Update Instructions
- [ ] Update `PROJECT_INSTRUCTIONS.md`
- [ ] Document ID format rules
- [ ] Explain auto-generation vs manual SQL insert

---

## ✅ Phase 10: Migration Script

### 10.1 Create Migration Script (`migrate_student_ids.py`)
```python
# Script to migrate existing IDs to new format
# - Maps old 8-digit IDs to new YYYY-XXXX format
# - Preserves all relationships
# - Updates foreign key references if any
```

### 10.2 Rollback Plan
- [ ] Create rollback script to revert if needed
- [ ] Test rollback on copy of database

---

## Implementation Order

1. **First**: Create database function (Phase 7)
2. **Second**: Update database schema (Phase 1)
3. **Third**: Create repopulation script (Phase 2)
4. **Fourth**: Update models (Phase 3)
5. **Fifth**: Update routes (Phase 5)
6. **Sixth**: Update templates (Phase 4)
7. **Seventh**: Update JavaScript (Phase 6)
8. **Eighth**: Test thoroughly (Phase 8)
9. **Ninth**: Update documentation (Phase 9)

---

## Key Rules Summary

✅ **Adding Student:**
- ID is **auto-generated** in format `2025-XXXX`
- User **cannot input** ID manually via UI
- ID field **hidden** or shown as "Auto-generated"

✅ **Editing Student:**
- ID is **visible** but **read-only**
- Shown with lock icon and "Cannot be changed" text
- ID is **never** sent in update request

✅ **Direct SQL Insert:**
- Allows custom IDs like `2023-0011` or `2027-9923`
- Must follow `YYYY-XXXX` format
- No UI for this - database admin only

✅ **Format:**
- Pattern: `YYYY-XXXX` (e.g., 2025-0001)
- YYYY = 4-digit year
- XXXX = 4-digit incrementing number (0001-9999)
- **Dash is mandatory**

---

## Status Tracking

- [ ] Phase 1: Database Schema
- [ ] Phase 2: Data Migration
- [ ] Phase 3: Backend Models
- [ ] Phase 4: Frontend Templates
- [ ] Phase 5: Route Handlers
- [ ] Phase 6: JavaScript
- [ ] Phase 7: Database Function
- [ ] Phase 8: Testing
- [ ] Phase 9: Documentation
- [ ] Phase 10: Migration Script

**Last Updated:** December 7, 2025
**Status:** Planning Phase
