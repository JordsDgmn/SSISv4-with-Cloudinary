# SSISv4 - Issues & Improvements To-Do List

## Current Issues to Fix

### 1. Home Page / Logo Navigation Issue
**Problem**: Clicking the home/legacy logo routes to the college page, which is confusing.

**Solution**: Create a dedicated home page that serves as a navigation hub
- Display all 3 main sections (Students, Programs/Courses, Colleges)
- Include descriptive cards/sections explaining what each page is for
- Make it intuitive for users to navigate without prior knowledge
- Add visual indicators or icons for each section

**Implementation**:
- [ ] Create new `home.html` template
- [ ] Add route handler in `__init__.py` or create `homeRoute.py`
- [ ] Update logo link in `layouts.html` to route to home page (`/`)
- [ ] Design homepage with cards for each section
- [ ] Add descriptions and call-to-action buttons

---

### 2. Remove Unnecessary Features
**Problem**: Features that don't serve the basic requirements are present (e.g., "Graduating Students", "New Students" stats)

**Features to Remove**:
- [ ] "Graduating Students" counter/card
- [ ] "New Students" counter/card
- [ ] Any other metrics not required by the specification

**Files to Update**:
- [ ] `templates/students.html` - Remove unnecessary stat cards
- [ ] `templates/colleges.html` - Keep only relevant stats
- [ ] `templates/courses.html` - Keep only relevant stats
- [ ] Backend routes if they have logic for these features

---

## Terminology Clarification

### Use Consistent Naming
The requirements use "program" but the codebase uses "course". Need to align terminology:

**Current**: 
- Course (in code)
- course_code, course_name (in database)

**Requirement**:
- Program (in specification)
- code, name (in schema)

**Decision**: Keep using "Course" in UI but note that it refers to academic programs.

---

## Additional Improvements (Nice to Have)

### UI/UX Enhancements
- [ ] Add loading states for AJAX operations
- [ ] Improve error messages and user feedback
- [ ] Add confirmation dialogs for delete operations
- [ ] Test and fix DataTables functionality on all pages

### Data Management
- [ ] Verify 300+ students are populated
- [ ] Verify 30+ programs/courses are populated
- [ ] Ensure proper foreign key relationships

### Code Quality
- [ ] Add comments to complex functions
- [ ] Remove duplicate code (old templates)
- [ ] Optimize database queries
- [ ] Add proper error handling

---

## Testing Checklist
- [ ] Test CRUD operations for Students
- [ ] Test CRUD operations for Courses/Programs
- [ ] Test CRUD operations for Colleges
- [ ] Test search functionality
- [ ] Test sorting functionality
- [ ] Test pagination
- [ ] Test photo upload to Cloudinary
- [ ] Test responsive design on mobile
- [ ] Test all navigation links
- [ ] Test form validation

---

## Status
- **Last Updated**: December 6, 2025
- **Current Phase**: Bug Fixes & UI Improvements
- **Next Steps**: 
  1. Remove unnecessary features
  2. Create proper home page
  3. Final testing
