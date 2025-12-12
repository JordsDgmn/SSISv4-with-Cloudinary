-- ============================================================================
-- SSIS v4 Database Migration Script
-- Migration from v3 (code-based PKs) to v4 (ID-based PKs, editable codes)
-- ============================================================================
-- 
-- CHANGES:
-- 1. Add auto-increment IDs as primary keys
-- 2. Make codes UNIQUE but editable
-- 3. Change foreign keys to reference IDs instead of codes
-- 4. Change CASCADE DELETE to SET NULL (allow orphans)
--
-- BEFORE RUNNING: 
-- - Backup your database: python backup_database_simple.py
-- - Review this script carefully
-- 
-- ============================================================================

\echo ''
\echo '============================================================================'
\echo 'SSIS v4 DATABASE MIGRATION'
\echo '============================================================================'
\echo ''

-- Start transaction (can rollback if something goes wrong)
BEGIN;

\echo '📦 Step 1: Creating backup tables...'

-- Backup existing tables
CREATE TABLE IF NOT EXISTS college_v3_backup AS SELECT * FROM college;
CREATE TABLE IF NOT EXISTS program_v3_backup AS SELECT * FROM program;
CREATE TABLE IF NOT EXISTS student_v3_backup AS SELECT * FROM student;

\echo '✅ Backup tables created'
\echo ''

\echo '🗑️  Step 2: Dropping old tables...'

-- Drop existing tables (CASCADE will drop all foreign key constraints)
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS program CASCADE;
DROP TABLE IF EXISTS college CASCADE;

\echo '✅ Old tables dropped'
\echo ''

\echo '🏗️  Step 3: Creating new schema...'

-- Create college table with ID-based primary key
CREATE TABLE college (
    college_id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

\echo '   ✅ college table created'

-- Create program table with ID-based primary key
CREATE TABLE program (
    program_id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    college_id INTEGER,
    FOREIGN KEY (college_id) REFERENCES college(college_id) ON DELETE SET NULL
);

\echo '   ✅ program table created'

-- Create student table with program_id foreign key
CREATE TABLE student (
    id VARCHAR(20) PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    year VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    program_id INTEGER,
    profile_pic TEXT,
    FOREIGN KEY (program_id) REFERENCES program(program_id) ON DELETE SET NULL
);

\echo '   ✅ student table created'
\echo ''

\echo '📥 Step 4: Migrating data...'

-- Migrate colleges (college_id will be auto-generated)
INSERT INTO college (code, name)
SELECT code, name 
FROM college_v3_backup
ORDER BY code;

\echo '   ✅ Migrated colleges'

-- Migrate programs (joining to get college_id from new college table)
INSERT INTO program (code, name, college_id)
SELECT 
    pb.code, 
    pb.name,
    c.college_id
FROM program_v3_backup pb
LEFT JOIN college c ON pb.collegecode = c.code
ORDER BY pb.code;

\echo '   ✅ Migrated programs'

-- Migrate students (joining to get program_id from new program table)
INSERT INTO student (id, firstname, lastname, year, gender, program_id, profile_pic)
SELECT 
    sb.id,
    sb.firstname,
    sb.lastname,
    sb.year,
    sb.gender,
    p.program_id,
    sb.profile_pic
FROM student_v3_backup sb
LEFT JOIN program p ON sb.coursecode = p.code
ORDER BY sb.id;

\echo '   ✅ Migrated students'
\echo ''

\echo '🔍 Step 5: Verifying migration...'
\echo ''

-- Verify record counts
\echo '   Record counts:'
SELECT 'Colleges' as table_name, COUNT(*) as count FROM college
UNION ALL
SELECT 'Programs', COUNT(*) FROM program
UNION ALL
SELECT 'Students', COUNT(*) FROM student;

\echo ''
\echo '   Checking for data integrity issues...'

-- Check for orphaned programs (college was deleted during migration)
WITH orphaned_programs AS (
    SELECT program_code, program_name 
    FROM program 
    WHERE college_id IS NULL
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '   ✅ No orphaned programs'
        ELSE '   ⚠️  ' || COUNT(*) || ' programs have no college'
    END as status
FROM orphaned_programs;

-- Check for orphaned students (program was deleted during migration)
WITH orphaned_students AS (
    SELECT id, firstname, lastname 
    FROM student 
    WHERE program_id IS NULL
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '   ✅ No orphaned students'
        ELSE '   ⚠️  ' || COUNT(*) || ' students have no program'
    END as status
FROM orphaned_students;

\echo ''
\echo '📊 Sample data from new tables:'
\echo ''
\echo '   Colleges (with IDs):'
SELECT college_id, college_code, college_name FROM college LIMIT 5;

\echo ''
\echo '   Programs (with IDs and college references):'
SELECT program_id, program_code, program_name, college_id FROM program LIMIT 5;

\echo ''
\echo '   Students (with program references):'
SELECT id, firstname, lastname, program_id FROM student LIMIT 5;

\echo ''
\echo '============================================================================'
\echo '✅ MIGRATION COMPLETED SUCCESSFULLY!'
\echo '============================================================================'
\echo ''
\echo 'Review the data above. If everything looks correct, type COMMIT to save.'
\echo 'If there are issues, type ROLLBACK to undo all changes.'
\echo ''
\echo 'IMPORTANT: Backup tables are preserved as:'
\echo '  - college_v3_backup'
\echo '  - program_v3_backup'
\echo '  - student_v3_backup'
\echo ''
\echo 'You can drop these after confirming the migration succeeded.'
\echo '============================================================================'
\echo ''

-- Don't auto-commit, let user review and decide
-- COMMIT;
