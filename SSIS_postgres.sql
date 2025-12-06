-- PostgreSQL Database Schema for SSIS
-- Create database (run this separately if needed)
-- CREATE DATABASE ssis;

-- Connect to the ssis database before running the following commands

-- Create tables
CREATE TABLE IF NOT EXISTS college (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS program (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    college_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (college_code) REFERENCES college(code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student (
    id CHAR(9) PRIMARY KEY,
    firstname VARCHAR(20) NOT NULL,
    lastname VARCHAR(20) NOT NULL,
    program_code VARCHAR(10) NOT NULL,
    year VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    profile_pic_url VARCHAR(255),
    FOREIGN KEY (program_code) REFERENCES program(code) ON DELETE CASCADE
);

-- Insert sample data for colleges
INSERT INTO college (code, name) VALUES 
('CCS', 'College of Computer Studies'),
('COE', 'College of Engineering'),
('CBA', 'College of Business Administration'),
('COED', 'College of Education'),
('CAS', 'College of Arts and Sciences'),
('CNHS', 'College of Nursing and Health Sciences'),
('CAF', 'College of Agriculture and Forestry'),
('CLAL', 'College of Law and Liberal Arts'),
('CME', 'College of Marine Engineering'),
('CITC', 'College of Information Technology and Computing')
ON CONFLICT (code) DO NOTHING;

-- Insert sample data for courses (programs)
INSERT INTO course (code, name, college_code) VALUES 
-- CCS Courses
('BSCS', 'Bachelor of Science in Computer Science', 'CCS'),
('BSIT', 'Bachelor of Science in Information Technology', 'CCS'),
('BSIS', 'Bachelor of Science in Information Systems', 'CCS'),

-- COE Courses
('BSCE', 'Bachelor of Science in Civil Engineering', 'COE'),
('BSEE', 'Bachelor of Science in Electrical Engineering', 'COE'),
('BSME', 'Bachelor of Science in Mechanical Engineering', 'COE'),
('BSIE', 'Bachelor of Science in Industrial Engineering', 'COE'),

-- CBA Courses
('BSBA', 'Bachelor of Science in Business Administration', 'CBA'),
('BSAC', 'Bachelor of Science in Accountancy', 'CBA'),
('BSMA', 'Bachelor of Science in Management Accounting', 'CBA'),
('BSHRM', 'Bachelor of Science in Hotel and Restaurant Management', 'CBA'),

-- COED Courses
('BEED', 'Bachelor of Elementary Education', 'COED'),
('BSED', 'Bachelor of Secondary Education', 'COED'),
('BPED', 'Bachelor of Physical Education', 'COED'),

-- CAS Courses
('ABPS', 'Bachelor of Arts in Psychology', 'CAS'),
('BSMATH', 'Bachelor of Science in Mathematics', 'CAS'),
('BSPHY', 'Bachelor of Science in Physics', 'CAS'),
('BSBIO', 'Bachelor of Science in Biology', 'CAS'),

-- CNHS Courses
('BSN', 'Bachelor of Science in Nursing', 'CNHS'),
('BSMT', 'Bachelor of Science in Medical Technology', 'CNHS'),

-- CAF Courses
('BSAG', 'Bachelor of Science in Agriculture', 'CAF'),
('BSFOR', 'Bachelor of Science in Forestry', 'CAF'),

-- CLAL Courses
('LLB', 'Bachelor of Laws', 'CLAL'),
('ABCOM', 'Bachelor of Arts in Communication', 'CLAL'),

-- CME Courses
('BSMarE', 'Bachelor of Science in Marine Engineering', 'CME'),
('BSMT-MAR', 'Bachelor of Science in Marine Transportation', 'CME'),

-- CITC Courses
('BSDA', 'Bachelor of Science in Data Analytics', 'CITC'),
('BSDS', 'Bachelor of Science in Data Science', 'CITC'),
('BSCPE', 'Bachelor of Science in Computer Engineering', 'CITC')
ON CONFLICT (code) DO NOTHING;