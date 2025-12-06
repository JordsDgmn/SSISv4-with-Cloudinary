# View Functionality Implementation Checklist

## Overview
Fix student counting and implement comprehensive view functionality for Students, Programs, and Colleges.

---

## Phase 1: Investigate Current Issues

### 1.1 Database Query Analysis
- [ ] Check `studentModels.py` - verify student queries include proper JOINs
- [ ] Check `programModels.py` - verify program queries
- [ ] Check `collegeModels.py` - verify college queries
- [ ] Identify why student counts show "0 students" in colleges/programs tables

### 1.2 Current State Analysis
- [ ] Review colleges.html - check how student count is calculated
- [ ] Review programs.html - check if student count column exists
- [ ] Review students.html - check current view functionality
- [ ] Review existing routes for `/view/` endpoints

---

## Phase 2: Fix Student Counting

### 2.1 Database Models - Add Count Methods
- [ ] Add `get_student_count_by_program(program_code)` to `studentModels.py`
- [ ] Add `get_student_count_by_college(college_code)` to `studentModels.py`
- [ ] Add `get_programs_with_student_counts()` to `programModels.py`
- [ ] Add `get_colleges_with_counts()` to `collegeModels.py`

### 2.2 Update Templates - Add Student Count Column
- [ ] Add "STUDENTS" column to programs.html table
- [ ] Update programs table to display student count per program
- [ ] Verify colleges.html shows accurate student counts
- [ ] Update route handlers to pass student counts to templates

### 2.3 Fix Count Display Logic
- [ ] Update `collegeRoute.py` - pass accurate counts to template
- [ ] Update `programRoute.py` - pass accurate counts to template
- [ ] Test that counts update when students are added/deleted
- [ ] Test that counts update when programs are added/deleted

---

## Phase 3: Implement View Routes

### 3.1 Student View Route (`/students/view/<id>`)
- [ ] Create route handler in `studentRoute.py`
- [ ] Query student details with program and college names
- [ ] Create `student_view.html` template
- [ ] Display student information:
  - [ ] Profile picture
  - [ ] Student ID
  - [ ] Full name (First + Last)
  - [ ] Program code and name
  - [ ] College name
  - [ ] Year level
  - [ ] Gender
- [ ] Add "Back to Students" button
- [ ] Add "Edit Student" button
- [ ] Add "Delete Student" button

### 3.2 Program View Route (`/programs/view/<code>`)
- [ ] Create route handler in `programRoute.py`
- [ ] Query program details with college info
- [ ] Query all students enrolled in this program
- [ ] Create `program_view.html` template
- [ ] Display program information:
  - [ ] Program code
  - [ ] Program name
  - [ ] College code and name
  - [ ] Total student count
- [ ] Display enrolled students table:
  - [ ] Student ID
  - [ ] Full name
  - [ ] Year level
  - [ ] Gender
  - [ ] Profile picture
  - [ ] Action buttons (View, Edit, Delete)
- [ ] Reuse table component styling
- [ ] Add DataTables for sorting/searching students
- [ ] Add "Back to Programs" button
- [ ] Add "Edit Program" button

### 3.3 College View Route (`/colleges/view/<code>`)
- [ ] Create route handler in `collegeRoute.py`
- [ ] Query college details
- [ ] Query all programs under this college
- [ ] Query all students in each program (grouped by program)
- [ ] Create `college_view.html` template
- [ ] Display college information:
  - [ ] College code
  - [ ] College name
  - [ ] Total programs count
  - [ ] Total students count (across all programs)
- [ ] Display programs section:
  - [ ] List each program with:
    - [ ] Program code
    - [ ] Program name
    - [ ] Student count per program
    - [ ] View/Edit buttons
- [ ] Display students by program section:
  - [ ] Group students by program
  - [ ] Show program name as section header
  - [ ] Display student table under each program:
    - [ ] Student ID
    - [ ] Full name
    - [ ] Year level
    - [ ] Gender
    - [ ] Action buttons
- [ ] Reuse table component styling
- [ ] Add "Back to Colleges" button
- [ ] Add "Edit College" button

---

## Phase 4: Update Action Buttons

### 4.1 Update View Button Links
- [ ] Students table - ensure View button links to `/students/view/<id>`
- [ ] Programs table - ensure View button links to `/programs/view/<code>`
- [ ] Colleges table - ensure View button links to `/colleges/view/<code>`

### 4.2 Test View Button Functionality
- [ ] Click View on any student - should show student details page
- [ ] Click View on any program - should show program with enrolled students
- [ ] Click View on any college - should show college with programs and students

---

## Phase 5: Template Creation

### 5.1 Create `student_view.html`
- [ ] Extend `layouts.html`
- [ ] Card layout for student details
- [ ] Display all student information
- [ ] Action buttons (Edit, Delete, Back)
- [ ] Responsive design
- [ ] Dark mode compatible

### 5.2 Create `program_view.html`
- [ ] Extend `layouts.html`
- [ ] Card layout for program details
- [ ] Card layout for enrolled students table
- [ ] DataTables integration
- [ ] Action buttons
- [ ] Responsive design
- [ ] Dark mode compatible

### 5.3 Create `college_view.html`
- [ ] Extend `layouts.html`
- [ ] Card layout for college details
- [ ] Card layout for programs list
- [ ] Expandable/collapsible sections per program
- [ ] Student tables under each program
- [ ] DataTables integration
- [ ] Action buttons
- [ ] Responsive design
- [ ] Dark mode compatible

---

## Phase 6: Database Query Optimization

### 6.1 Efficient Queries
- [ ] Optimize student count queries (use COUNT() instead of fetching all)
- [ ] Use JOIN queries to minimize database calls
- [ ] Cache counts where appropriate
- [ ] Test query performance with 300+ students

### 6.2 Query Methods to Implement
```python
# studentModels.py
- get_student_by_id(student_id) → returns single student with program/college info
- get_students_by_program(program_code) → returns all students in program
- get_students_by_college(college_code) → returns all students in college

# programModels.py
- get_program_by_code(program_code) → returns program with college info
- get_program_with_counts(program_code) → returns program + student count

# collegeModels.py
- get_college_by_code(college_code) → returns college with program/student counts
- get_college_programs_with_students(college_code) → returns programs with student lists
```

---

## Phase 7: Fix Data Relationships

### 7.1 Verify Foreign Key Relationships
- [ ] Confirm `student.program_code` → `program.code` relationship works
- [ ] Confirm `program.college_code` → `college.code` relationship works
- [ ] Test cascade deletes work properly
- [ ] Verify student belongs to exactly one program
- [ ] Verify program belongs to exactly one college

### 7.2 Test Data Integrity
- [ ] Add student to program → count should increase
- [ ] Delete student from program → count should decrease
- [ ] Move student to different program → counts should update in both programs
- [ ] Delete program → all students should be deleted (cascade)
- [ ] Delete college → all programs and students should be deleted (cascade)

---

## Phase 8: UI/UX Enhancements

### 8.1 Visual Design
- [ ] Consistent card styling across all view pages
- [ ] Clear hierarchy (College > Programs > Students)
- [ ] Proper spacing and padding
- [ ] Icons for different entity types
- [ ] Color coding (if needed)

### 8.2 Navigation
- [ ] Breadcrumbs (e.g., "Colleges > CCS > Programs > BSCS > Students")
- [ ] "Back" buttons that return to previous page
- [ ] Quick action buttons (Edit, Delete) on view pages
- [ ] Links between related entities

### 8.3 Empty States
- [ ] Message when program has no students
- [ ] Message when college has no programs
- [ ] Helpful text with "Add" buttons

---

## Phase 9: Testing

### 9.1 Functional Testing
- [ ] Test student view page loads correctly
- [ ] Test program view page shows all enrolled students
- [ ] Test college view page shows all programs and students
- [ ] Test counts are accurate across all pages
- [ ] Test view buttons work from all three main pages

### 9.2 Data Accuracy Testing
- [ ] Create new student → verify count increases
- [ ] Edit student's program → verify counts update in both programs
- [ ] Delete student → verify count decreases
- [ ] Verify student appears in correct program view
- [ ] Verify student appears in correct college view

### 9.3 Edge Cases
- [ ] View program with 0 students
- [ ] View college with 0 programs
- [ ] View college with programs but 0 students
- [ ] View student with very long name
- [ ] View program with 100+ students (test performance)

### 9.4 UI Testing
- [ ] Test responsive design on mobile
- [ ] Test dark mode on all view pages
- [ ] Test DataTables sorting/searching works
- [ ] Test pagination works correctly
- [ ] Test all action buttons work

---

## Phase 10: Activity Logging

### 10.1 Add Logging for View Operations
- [ ] Log student view: `VIEW Student: ID={id}, Name={name}`
- [ ] Log program view: `VIEW Program: Code={code}, Name={name}`
- [ ] Log college view: `VIEW College: Code={code}, Name={name}`

---

## Phase 11: Documentation Updates

### 11.1 Update Documentation Files
- [ ] Update `DATABASE_SCHEMA.md` with new query methods
- [ ] Update `PROJECT_INSTRUCTIONS.md` - mark view functionality as complete
- [ ] Document new routes in README (if exists)
- [ ] Add comments to complex queries

---

## Execution Order

1. **Start:** Phase 1 (Investigation)
2. **Fix Counts:** Phase 2 (Student Counting)
3. **Build Backend:** Phase 3 & 6 (Routes + Queries)
4. **Build Frontend:** Phase 5 (Templates)
5. **Connect:** Phase 4 (Update Buttons)
6. **Verify:** Phase 7 (Data Relationships)
7. **Polish:** Phase 8 (UI/UX)
8. **Test:** Phase 9 (Testing)
9. **Finalize:** Phase 10 & 11 (Logging + Docs)

---

## Current Status
- [ ] Phase 1: Investigation - NOT STARTED
- [ ] Phase 2: Fix Student Counting - NOT STARTED
- [ ] Phase 3: Implement View Routes - NOT STARTED
- [ ] Phase 4: Update Action Buttons - NOT STARTED
- [ ] Phase 5: Template Creation - NOT STARTED
- [ ] Phase 6: Query Optimization - NOT STARTED
- [ ] Phase 7: Fix Data Relationships - NOT STARTED
- [ ] Phase 8: UI/UX Enhancements - NOT STARTED
- [ ] Phase 9: Testing - NOT STARTED
- [ ] Phase 10: Activity Logging - NOT STARTED
- [ ] Phase 11: Documentation - NOT STARTED

---

**Last Updated:** December 7, 2025
**Status:** Ready to begin implementation
