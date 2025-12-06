-- Migration Script: Rename 'course' table to 'program' and related columns
-- Run this script to migrate existing database to match official requirements

-- Step 1: Drop the foreign key constraint on student table
ALTER TABLE student DROP CONSTRAINT IF EXISTS student_course_code_fkey;

-- Step 2: Rename the course table to program
ALTER TABLE course RENAME TO program;

-- Step 3: Rename course_code column to program_code in student table
ALTER TABLE student RENAME COLUMN course_code TO program_code;

-- Step 4: Add the foreign key constraint back with new names
ALTER TABLE student 
ADD CONSTRAINT student_program_code_fkey 
FOREIGN KEY (program_code) REFERENCES program(code) ON DELETE CASCADE;

-- Verify the changes
SELECT 'Migration completed successfully!' AS status;
