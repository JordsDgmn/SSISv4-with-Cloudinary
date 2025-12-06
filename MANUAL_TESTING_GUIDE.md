# Manual Testing Guide - SSIS v4

## Server Status
✅ Flask server running at: **http://127.0.0.1:5000**  
✅ Students page open at: **http://127.0.0.1:5000/students**

---

## 📋 TASK 1: Test Student CRUD Operations

### ✅ Step 1: Test CREATE Student
1. **Navigate to Students page**: http://127.0.0.1:5000/students
2. **Click** the blue **"Add New Student"** button (top right)
3. **Fill in the form**:
   - Student ID: `20251234` (must be 9 digits)
   - First Name: `John`
   - Last Name: `Doe`
   - Program: Select any program from dropdown (e.g., BSCS)
   - Year Level: Select `1st Year`
   - Gender: Select `Male`
   - Profile Picture: (Optional) Upload an image
4. **Click** "Add Student" button
5. **Expected Results**:
   - ✅ Success message appears (green flash message)
   - ✅ New student appears in the table
   - ✅ Student count increments
   - ✅ Check logs: http://127.0.0.1:5000/logs
     - Should show: `[TIMESTAMP] CREATE Student: ID=20251234, Name=John Doe, Program=..., Year=1st Year, Gender=Male`

---

### ✅ Step 2: Test VIEW Student
1. **Find any student** in the table
2. **Click** the **eye icon** (👁️) in the Actions column
3. **Expected Results**:
   - ✅ Page redirects (view functionality may just redirect back)
   - ✅ Flash message appears saying "Student details viewed"
   - ✅ Check logs: http://127.0.0.1:5000/logs
     - Should show: `[TIMESTAMP] VIEW Student: ID=20251234`

---

### ✅ Step 3: Test EDIT Student
1. **Find the student** you just created (John Doe)
2. **Click** the **pencil icon** (✏️) in the Actions column
3. **Modal should open** with pre-filled data:
   - ✅ Student ID should be visible but read-only
   - ✅ All fields (name, program, year, gender) should show current values
4. **Make changes**:
   - Change First Name to: `Jane`
   - Change Year Level to: `2nd Year`
5. **Click** "Update Student" button
6. **Expected Results**:
   - ✅ Alert appears: "Student updated successfully!"
   - ✅ Page reloads automatically
   - ✅ Table shows updated information (Jane, 2nd Year)
   - ✅ Check logs: http://127.0.0.1:5000/logs
     - Should show: `[TIMESTAMP] EDIT Student: ID=20251234, Name=Jane Doe, Program=..., Year=2nd Year, Gender=Male`

**❌ If Edit Doesn't Work:**
- Open browser console (F12)
- Try clicking Edit again
- Check for JavaScript errors
- Verify the modal opens and fields populate

---

### ✅ Step 4: Test DELETE Student
1. **Find the student** you created (Jane Doe / ID: 20251234)
2. **Click** the **trash icon** (🗑️) in the Actions column
3. **Confirmation dialog should appear**:
   - Message: `Are you sure you want to delete Jane Doe (ID: 20251234)?`
   - Second line: `This action cannot be undone.`
4. **Click "Cancel"** first to test cancellation
   - ✅ Student should remain in table
5. **Click trash icon again**, then **Click "OK"** to confirm
6. **Expected Results**:
   - ✅ Page reloads
   - ✅ Student disappears from table
   - ✅ Student count decrements
   - ✅ Success message: "Student deleted successfully"
   - ✅ Check logs: http://127.0.0.1:5000/logs
     - Should show: `[TIMESTAMP] DELETE Student: ID=20251234, Name=Jane Doe`

**❌ If Delete Doesn't Work:**
- Check if confirmation dialog appears
- Check if page scrolls to top (should NOT happen)
- Open browser console (F12) for errors
- Try deleting a different student

---

### ✅ Step 5: Test SEARCH Student
1. **Use the search box** at the top of the table
2. **Type** part of a student name, ID, or program
3. **Expected Results**:
   - ✅ Table filters in real-time
   - ✅ Only matching students show
   - ✅ Clear search shows all students again

---

## 📋 TASK 2: Test Program CRUD Operations

### Navigate to Programs Page
**URL**: http://127.0.0.1:5000/programs

### ✅ Step 1: Test CREATE Program
1. **Click** "Add New Program" button
2. **Fill in the form**:
   - Program Code: `BSTEST` (uppercase letters)
   - Program Name: `BS in Testing`
   - College: Select any college
3. **Click** "Add Program"
4. **Expected Results**:
   - ✅ Success message
   - ✅ Program appears in table
   - ✅ Program count increments

### ✅ Step 2: Test EDIT Program
1. **Click** pencil icon on the program you created
2. **Change** Program Name to: `BS in Quality Assurance`
3. **Click** "Update"
4. **Expected Results**:
   - ✅ Table updates with new name
   - ✅ Success message appears

### ✅ Step 3: Test DELETE Program
1. **Click** trash icon on BSTEST program
2. **Confirmation dialog should appear**:
   - Message should include program name and code
3. **Click OK**
4. **Expected Results**:
   - ✅ Program deleted from table
   - ✅ Success message
   - ✅ **Note**: If program has students enrolled, deletion should be prevented

**❌ If Delete Shows "Are you sure you want to delete course...":**
- This is a bug - should say "program" not "course"
- But functionality should still work

---

## 📋 TASK 3: Test College CRUD Operations

### Navigate to Colleges Page
**URL**: http://127.0.0.1:5000/colleges

### ✅ Step 1: Test CREATE College
1. **Click** "Add New College" button
2. **Fill in**:
   - College Code: `CTEST`
   - College Name: `College of Testing`
3. **Click** "Add College"
4. **Expected Results**:
   - ✅ Success message
   - ✅ College appears in table

### ✅ Step 2: Test EDIT College
1. **Click** pencil icon
2. **Change** name
3. **Expected Results**:
   - ✅ Updates successfully

### ✅ Step 3: Test DELETE College
1. **Click** trash icon
2. **Confirm deletion**
3. **Expected Results**:
   - ✅ College deleted
   - ✅ **Note**: If college has programs, deletion should be prevented

---

## 📋 TASK 4: Verify Activity Logs

### Check All Operations Were Logged
**URL**: http://127.0.0.1:5000/logs

**What to verify**:
- ✅ CREATE operations logged with all details (ID, Name, Program, Year, Gender)
- ✅ EDIT operations logged with updated values
- ✅ DELETE operations logged with student name (not just ID)
- ✅ VIEW operations logged with timestamp
- ✅ Timestamps are correct format: `[2025-12-06 HH:MM:SS]`
- ✅ All operations have proper action type (CREATE, EDIT, DELETE, VIEW)

---

## 🐛 Common Issues to Check

### Issue: Page Scrolls to Top
- **Cause**: Delete link has `href="#"`
- **Fix Applied**: Should now use `href="javascript:void(0)"`
- **Test**: Click delete - page should NOT scroll

### Issue: Edit Submits Wrong ID
- **Symptom**: Logs show `ID=students` instead of actual ID
- **Fix Applied**: Hidden input field stores ID
- **Test**: Edit a student, check logs for correct ID

### Issue: Delete Not Working
- **Symptom**: Nothing happens when clicking trash icon
- **Fix Applied**: JavaScript handler properly binds to `.delete-student` class
- **Test**: Click trash icon - confirmation should appear

### Issue: Edit Modal Empty
- **Symptom**: Modal opens but fields are blank
- **Fix Applied**: jQuery handler populates both visible and hidden ID fields
- **Test**: Click edit - all fields should be filled

---

## ✅ Testing Checklist

Copy this checklist and check off as you test:

**Students:**
- [ ] CREATE: Add new student with all fields
- [ ] CREATE: Verify appears in table immediately
- [ ] VIEW: Click eye icon, check logs
- [ ] EDIT: Click pencil, modal opens with data
- [ ] EDIT: Change fields, save, verify updates
- [ ] EDIT: Check logs show correct ID (not "students")
- [ ] DELETE: Click trash, confirmation appears
- [ ] DELETE: Confirm shows student name and ID
- [ ] DELETE: Cancel works (student stays)
- [ ] DELETE: Confirm works (student removed)
- [ ] DELETE: Check logs show student name
- [ ] SEARCH: Filter by name/ID/program

**Programs:**
- [ ] CREATE: Add new program
- [ ] EDIT: Modify program name
- [ ] DELETE: Confirmation appears (should say "program" not "course")
- [ ] DELETE: Deletes successfully

**Colleges:**
- [ ] CREATE: Add new college
- [ ] EDIT: Modify college name
- [ ] DELETE: Deletes successfully

**Logs:**
- [ ] All CREATE operations logged with details
- [ ] All EDIT operations logged with new values
- [ ] All DELETE operations logged with names
- [ ] All VIEW operations logged
- [ ] Timestamps accurate

**Dark Mode:**
- [ ] Toggle dark mode (moon icon top right)
- [ ] All text readable in dark mode
- [ ] Tables have dark background in dark mode
- [ ] Modals styled correctly in dark mode
- [ ] Buttons visible in dark mode

---

## 📝 Report Issues

If any test fails, note:
1. **What you did** (exact steps)
2. **What happened** (actual behavior)
3. **What should happen** (expected behavior)
4. **Console errors** (F12 → Console tab)
5. **Screenshot** if helpful

---

## 🎯 Priority Tests

**Test these FIRST** (most critical):
1. ✅ Student DELETE (was broken - should show confirmation)
2. ✅ Student EDIT (was broken - should save correct ID)
3. ✅ Activity logs (should show details, not just IDs)
4. ✅ No page scrolling when clicking delete

**Test these NEXT**:
5. Student CREATE with photo upload
6. Program DELETE (check confirmation text)
7. Search/filter functionality

---

Good luck testing! 🚀
