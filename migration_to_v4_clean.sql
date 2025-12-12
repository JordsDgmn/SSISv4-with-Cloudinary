-- ============================================================================
-- SSIS v4 Database Migration Script (Python-compatible)
-- Migration from v3 (code-based PKs) to v4 (ID-based PKs, editable codes)
-- ============================================================================

-- Start transaction
BEGIN;

-- Step 1: Creating backup tables
CREATE TABLE IF NOT EXISTS college_v3_backup AS SELECT * FROM college;
CREATE TABLE IF NOT EXISTS program_v3_backup AS SELECT * FROM program;
CREATE TABLE IF NOT EXISTS student_v3_backup AS SELECT * FROM student;

-- Step 2: Dropping old tables
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS program CASCADE;
DROP TABLE IF EXISTS college CASCADE;

-- Step 3: Creating new schema

-- Create college table with ID-based primary key
CREATE TABLE college (
    college_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- Create program table with ID-based primary key
CREATE TABLE program (
    program_id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    college_id INTEGER,
    FOREIGN KEY (college_id) REFERENCES college(college_id) ON DELETE SET NULL
);

-- Create student table with program_id FK
CREATE TABLE student (
    id VARCHAR(9) PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    program_id INTEGER,
    year VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    profile_pic TEXT,
    FOREIGN KEY (program_id) REFERENCES program(program_id) ON DELETE SET NULL
);

-- Step 4: Migrating data

-- Migrate colleges (preserve IDs by inserting in order)
INSERT INTO college (code, name)
SELECT code, name
FROM college_v3_backup
ORDER BY code;

-- Migrate programs with college_id FK
INSERT INTO program (code, name, college_id)
SELECT 
    p.code,
    p.name,
    c.college_id
FROM program_v3_backup p
LEFT JOIN college c ON p.college_code = c.code
ORDER BY p.code;

-- Migrate students with program_id FK
INSERT INTO student (id, firstname, lastname, program_id, year, gender, profile_pic)
SELECT 
    s.id,
    s.firstname,
    s.lastname,
    p.program_id,
    s.year,
    s.gender,
    s.profile_pic_url
FROM student_v3_backup s
LEFT JOIN program p ON s.program_code = p.code
ORDER BY s.id;

-- Step 5: Verification queries
SELECT 'Colleges migrated: ' || COUNT(*) FROM college;
SELECT 'Programs migrated: ' || COUNT(*) FROM program;
SELECT 'Students migrated: ' || COUNT(*) FROM student;
SELECT 'Orphaned programs: ' || COUNT(*) FROM program WHERE college_id IS NULL;
SELECT 'Orphaned students: ' || COUNT(*) FROM student WHERE program_id IS NULL;

-- DO NOT COMMIT YET - Script will ask for confirmation
-- Type COMMIT or ROLLBACK after reviewing results
