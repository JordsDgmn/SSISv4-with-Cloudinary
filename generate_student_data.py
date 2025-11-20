"""
Script to generate sample student data for the SSIS database.
This script generates 300+ students with realistic data.
"""
import random
from datetime import datetime

# Sample data
first_names = [
    'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jessica', 'William', 'Ashley',
    'James', 'Amanda', 'Christopher', 'Jennifer', 'Daniel', 'Lisa', 'Matthew', 'Michelle', 'Anthony', 'Kimberly',
    'Mark', 'Amy', 'Donald', 'Angela', 'Steven', 'Helen', 'Paul', 'Anna', 'Joshua', 'Brenda',
    'Kenneth', 'Emma', 'Kevin', 'Olivia', 'Brian', 'Sophia', 'George', 'Cynthia', 'Timothy', 'Marie',
    'Ronald', 'Janet', 'Jason', 'Catherine', 'Edward', 'Frances', 'Jeffrey', 'Samantha', 'Ryan', 'Deborah',
    'Jacob', 'Rachel', 'Gary', 'Carolyn', 'Nicholas', 'Janet', 'Eric', 'Virginia', 'Jonathan', 'Maria',
    'Stephen', 'Heather', 'Larry', 'Diane', 'Justin', 'Julie', 'Scott', 'Joyce', 'Brandon', 'Victoria',
    'Benjamin', 'Kelly', 'Samuel', 'Christina', 'Gregory', 'Joan', 'Alexander', 'Evelyn', 'Patrick', 'Lauren'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
    'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
    'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
    'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes',
    'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper',
    'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson'
]

course_codes = [
    'BSCS', 'BSIT', 'BSIS', 'BSCE', 'BSEE', 'BSME', 'BSIE', 'BSBA', 'BSAC', 'BSMA',
    'BSHRM', 'BEED', 'BSED', 'BPED', 'ABPS', 'BSMATH', 'BSPHY', 'BSBIO', 'BSN', 'BSMT',
    'BSAG', 'BSFOR', 'LLB', 'ABCOM', 'BSMarE', 'BSMT-MAR', 'BSDA', 'BSDS', 'BSCPE'
]

years = ['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year']
genders = ['Male', 'Female']

def generate_student_id():
    """Generate a 9-character student ID in format YYNNNNNNN"""
    year = random.randint(20, 25)  # 2020-2025 becomes 20-25
    number = random.randint(100000, 999999)  # 6 digits
    return f"{year}{number}"

def generate_student_data(num_students=350):
    """Generate student data"""
    students = []
    used_ids = set()
    
    for i in range(num_students):
        # Generate unique student ID
        while True:
            student_id = generate_student_id()
            if student_id not in used_ids:
                used_ids.add(student_id)
                break
        
        firstname = random.choice(first_names)
        lastname = random.choice(last_names)
        course_code = random.choice(course_codes)
        year = random.choice(years)
        gender = random.choice(genders)
        
        students.append({
            'id': student_id,
            'firstname': firstname,
            'lastname': lastname,
            'course_code': course_code,
            'year': year,
            'gender': gender
        })
    
    return students

def generate_sql_insert_statements(students):
    """Generate SQL INSERT statements for the student data"""
    sql_statements = []
    
    # Generate INSERT statements in batches for better performance
    batch_size = 50
    for i in range(0, len(students), batch_size):
        batch = students[i:i + batch_size]
        values = []
        
        for student in batch:
            values.append(f"('{student['id']}', '{student['firstname']}', '{student['lastname']}', '{student['course_code']}', '{student['year']}', '{student['gender']}')")
        
        sql = f"""
INSERT INTO student (id, firstname, lastname, course_code, year, gender) VALUES 
{', '.join(values)};
"""
        sql_statements.append(sql)
    
    return sql_statements

if __name__ == "__main__":
    print("Generating student data...")
    students = generate_student_data()
    sql_statements = generate_sql_insert_statements(students)
    
    # Write to file
    with open('student_data.sql', 'w') as f:
        f.write("-- Generated student data for SSIS database\n")
        f.write(f"-- Generated on: {datetime.now()}\n")
        f.write(f"-- Total students: {len(students)}\n\n")
        
        for sql in sql_statements:
            f.write(sql)
            f.write("\n")
    
    print(f"Generated {len(students)} student records in student_data.sql")
    print("Run this SQL file in your PostgreSQL database to insert the student data.")