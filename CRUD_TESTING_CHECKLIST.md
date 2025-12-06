# CRUD Testing Checklist

## Testing Status Legend
- ✅ Completed and verified
- 🔄 In progress
- ❌ Failed/needs fix
- ⏸️ Pending

---

## Task 1: Student CRUD Operations

### 1.1 CREATE Student
- [ ] Form validation (required fields)
- [ ] Student ID format validation
- [ ] Profile photo upload (Cloudinary integration)
- [ ] Program dropdown populated correctly
- [ ] Year level dropdown (1st-4th Year)
- [ ] Gender selection (Male/Female)
- [ ] Success flash message appears
- [ ] Activity log records creation with all details
- [ ] New student appears in table immediately
- [ ] Student count increments on home page
- [ ] DataTables updates without page refresh

### 1.2 READ/VIEW Student
- [ ] View button displays correct student details
- [ ] Profile photo displays correctly (Cloudinary URL)
- [ ] All fields shown accurately (ID, name, program, year, gender)
- [ ] Activity log records view action
- [ ] Flash message appears
- [ ] Modal closes properly

### 1.3 UPDATE Student
- [ ] Edit button opens modal with pre-filled data
- [ ] Student ID field is read-only/disabled
- [ ] First name can be updated
- [ ] Last name can be updated
- [ ] Program can be changed (dropdown works)
- [ ] Year level can be changed
- [ ] Gender can be changed
- [ ] Profile photo upload works on edit
- [ ] Old photo removed from Cloudinary if replaced
- [ ] Success flash message appears
- [ ] Activity log records edit with before/after details
- [ ] Table updates immediately
- [ ] DataTables reflects changes

### 1.4 DELETE Student
- [ ] Delete button (trash icon) is clickable
- [ ] Confirmation dialog appears with student name
- [ ] Cancel button aborts deletion
- [ ] Confirm proceeds with deletion
- [ ] Student removed from database
- [ ] Profile photo deleted from Cloudinary
- [ ] Success flash message appears
- [ ] Activity log records deletion with student details
- [ ] Table updates immediately (student disappears)
- [ ] Student count decrements on home page
- [ ] No broken references to programs/colleges

### 1.5 SEARCH Student
- [ ] Search box filters by student ID
- [ ] Search box filters by name
- [ ] Search box filters by program
- [ ] Search results update in real-time
- [ ] DataTables search works correctly
- [ ] Clear search shows all students

### 1.6 Student-Program Relationship
- [ ] Cannot create student with non-existent program
- [ ] Deleting program doesn't orphan students (cascade/restrict)
- [ ] Program name displays correctly in student table
- [ ] Changing program updates student record

---

## Task 2: Program CRUD Operations

### 2.1 CREATE Program
- [ ] Form validation (required fields)
- [ ] Program code format validation
- [ ] Program name validation
- [ ] College dropdown populated correctly
- [ ] Cannot create duplicate program code
- [ ] Success flash message appears
- [ ] Activity log records creation
- [ ] New program appears in table immediately
- [ ] Program count increments on home page
- [ ] DataTables updates without refresh

### 2.2 READ/VIEW Program
- [ ] View button shows program details (if implemented)
- [ ] Program code displays correctly
- [ ] Program name displays correctly
- [ ] Associated college name shows
- [ ] Student count for program is accurate

### 2.3 UPDATE Program
- [ ] Edit button opens modal with pre-filled data
- [ ] Program code field is read-only/disabled
- [ ] Program name can be updated
- [ ] College can be changed (dropdown works)
- [ ] Success flash message appears
- [ ] Activity log records edit
- [ ] Table updates immediately
- [ ] Students associated with program see updated name
- [ ] DataTables reflects changes

### 2.4 DELETE Program
- [ ] Delete button (trash icon) is clickable
- [ ] Confirmation dialog appears with program name and code
- [ ] Cancel button aborts deletion
- [ ] Confirm proceeds with deletion
- [ ] Cannot delete program with enrolled students (or cascade)
- [ ] Program removed from database
- [ ] Success flash message appears
- [ ] Activity log records deletion
- [ ] Table updates immediately (program disappears)
- [ ] Program count decrements on home page
- [ ] College's program count updates

### 2.5 SEARCH Program
- [ ] Search box filters by program code
- [ ] Search box filters by program name
- [ ] Search box filters by college
- [ ] Search results update correctly
- [ ] DataTables search works

### 2.6 Program-College Relationship
- [ ] Cannot create program with non-existent college
- [ ] Deleting college doesn't orphan programs (cascade/restrict)
- [ ] College name displays correctly in program table
- [ ] Changing college updates program record

---

## Task 3: College CRUD Operations

### 3.1 CREATE College
- [ ] Form validation (required fields)
- [ ] College code format validation
- [ ] College name validation
- [ ] Cannot create duplicate college code
- [ ] Success flash message appears
- [ ] Activity log records creation
- [ ] New college appears in table immediately
- [ ] College count increments on home page
- [ ] DataTables updates without refresh

### 3.2 READ/VIEW College
- [ ] View button shows college details (if implemented)
- [ ] College code displays correctly
- [ ] College name displays correctly
- [ ] Program count for college is accurate
- [ ] Student count for college is accurate

### 3.3 UPDATE College
- [ ] Edit button opens modal with pre-filled data
- [ ] College code field is read-only/disabled
- [ ] College name can be updated
- [ ] Success flash message appears
- [ ] Activity log records edit
- [ ] Table updates immediately
- [ ] Programs associated with college see updated name
- [ ] DataTables reflects changes

### 3.4 DELETE College
- [ ] Delete button (trash icon) is clickable
- [ ] Confirmation dialog appears with college name and code
- [ ] Cancel button aborts deletion
- [ ] Confirm proceeds with deletion
- [ ] Cannot delete college with programs/students (or cascade)
- [ ] College removed from database
- [ ] Success flash message appears
- [ ] Activity log records deletion
- [ ] Table updates immediately (college disappears)
- [ ] College count decrements on home page

### 3.5 SEARCH College
- [ ] Search box filters by college code
- [ ] Search box filters by college name
- [ ] Search results update correctly
- [ ] DataTables search works

---

## Task 4: Cross-Cutting Concerns

### 4.1 Flash Messages
- [ ] Success messages show in green
- [ ] Error messages show in red
- [ ] Info messages show appropriately
- [ ] Messages auto-dismiss after timeout
- [ ] Messages are dismissible manually
- [ ] Messages display on correct page after redirect

### 4.2 Activity Logging
- [ ] All CREATE operations logged
- [ ] All READ/VIEW operations logged
- [ ] All UPDATE operations logged
- [ ] All DELETE operations logged
- [ ] Log entries have correct timestamps
- [ ] Log entries have operation type
- [ ] Log entries have entity details
- [ ] Logs page displays recent activities
- [ ] Download logs button works

### 4.3 JavaScript Event Handlers
- [ ] Delete buttons work after DataTables redraw
- [ ] Edit buttons work after DataTables redraw
- [ ] View buttons work after DataTables redraw
- [ ] Modal close/open works correctly
- [ ] Form submissions via AJAX work
- [ ] Confirmation dialogs work consistently

### 4.4 Dark Mode Compatibility
- [ ] All buttons visible in dark mode
- [ ] All text readable in dark mode
- [ ] Modals styled correctly in dark mode
- [ ] Flash messages visible in dark mode
- [ ] Tables styled correctly in dark mode
- [ ] Forms styled correctly in dark mode

### 4.5 DataTables Functionality
- [ ] Sorting works on all sortable columns
- [ ] Pagination works correctly
- [ ] Page size selection works
- [ ] Search filters entire dataset
- [ ] Table responsive on mobile
- [ ] Actions column not sortable

---

## Task 5: Edge Cases & Error Handling

### 5.1 Database Constraints
- [ ] Duplicate primary keys rejected
- [ ] Foreign key constraints enforced
- [ ] NULL constraints enforced
- [ ] Data type constraints enforced

### 5.2 User Input Validation
- [ ] Empty required fields rejected
- [ ] Invalid formats rejected (IDs, codes)
- [ ] SQL injection prevented
- [ ] XSS attacks prevented

### 5.3 File Upload (Cloudinary)
- [ ] Large files handled properly
- [ ] Invalid file types rejected
- [ ] Upload failures show error message
- [ ] Cloudinary URLs stored correctly
- [ ] Old images cleaned up on update/delete

### 5.4 Concurrent Operations
- [ ] Multiple users can create entities
- [ ] Race conditions handled
- [ ] Database locks work correctly

---

## Current Progress

**Task 1: Student CRUD** - 🔄 In Progress
- Fixed delete button class and data attributes
- Need to test all sub-tasks systematically

**Task 2: Program CRUD** - ⏸️ Pending
- Fixed delete button attributes and JS handler
- Awaiting systematic testing

**Task 3: College CRUD** - ⏸️ Pending
- Delete button already correct
- Awaiting systematic testing

**Task 4: Cross-Cutting** - ⏸️ Pending
**Task 5: Edge Cases** - ⏸️ Pending
