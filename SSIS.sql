	CREATE DATABASE SSIS;
		USE SSIS;
		
		CREATE TABLE college (
		    code VARCHAR(10) PRIMARY KEY,
		    name VARCHAR(100)
		);
		
		CREATE TABLE course (
		    code VARCHAR(10) PRIMARY KEY,
		    name VARCHAR(100),
		    college_code VARCHAR(10),
		    FOREIGN KEY (college_code) REFERENCES college(code) ON DELETE CASCADE
		);
		
		CREATE TABLE student (
		    id CHAR(9) PRIMARY KEY,
		    firstname VARCHAR(20),
		    lastname VARCHAR(20),
		    course_code VARCHAR(10),
		    year VARCHAR(20),
		    gender VARCHAR(10),
		    profile_pic_url VARCHAR(255), -- Add a new field for profile picture URL
		    FOREIGN KEY (course_code) REFERENCES course(code) ON DELETE CASCADE
		);