"""
Migration Script: Change Student ID Format from 8-digit to YYYY-XXXX

This script:
1. Creates the ID generation function
2. Alters the student table schema
3. Clears and repopulates student data with new format
"""

from website.database import DatabaseManager
from datetime import datetime
import random

def create_id_generation_function():
    """Create PostgreSQL function to generate next student ID"""
    print("\n" + "="*80)
    print("STEP 1: Creating ID Generation Function")
    print("="*80)
    
    sql = """
    CREATE OR REPLACE FUNCTION generate_student_id(year_param INT DEFAULT NULL) 
    RETURNS VARCHAR(10) AS $$
    DECLARE
        target_year INT;
        max_number INT;
        next_id VARCHAR(10);
    BEGIN
        -- Use provided year or current year
        IF year_param IS NULL THEN
            target_year := EXTRACT(YEAR FROM CURRENT_DATE);
        ELSE
            target_year := year_param;
        END IF;
        
        -- Find highest number for the year
        SELECT COALESCE(MAX(CAST(SPLIT_PART(id, '-', 2) AS INT)), 0)
        INTO max_number
        FROM student
        WHERE id LIKE target_year || '-%';
        
        -- Generate next ID
        next_id := target_year || '-' || LPAD((max_number + 1)::TEXT, 4, '0');
        
        RETURN next_id;
    END;
    $$ LANGUAGE plpgsql;
    """
    
    try:
        with DatabaseManager.get_cursor() as (cur, conn):
            cur.execute(sql)
            print("✅ Function 'generate_student_id()' created successfully")
            return True
    except Exception as e:
        print(f"❌ Error creating function: {e}")
        return False

def alter_student_table():
    """Alter student table to accept new ID format"""
    print("\n" + "="*80)
    print("STEP 2: Altering Student Table Schema")
    print("="*80)
    
    try:
        with DatabaseManager.get_cursor() as (cur, conn):
            # First, clear all existing students (they have old format)
            print("Clearing existing students with old format...")
            cur.execute("DELETE FROM student CASCADE;")
            
            # Drop existing constraint if any
            print("Dropping old constraints...")
            cur.execute("""
                ALTER TABLE student 
                DROP CONSTRAINT IF EXISTS student_id_check;
            """)
            
            # Change column type
            print("Changing id column type to VARCHAR(10)...")
            cur.execute("""
                ALTER TABLE student 
                ALTER COLUMN id TYPE VARCHAR(10);
            """)
            
            # Add new format constraint
            print("Adding format constraint (YYYY-XXXX)...")
            cur.execute("""
                ALTER TABLE student 
                ADD CONSTRAINT student_id_format_check 
                CHECK (id ~ '^[0-9]{4}-[0-9]{4}$');
            """)
            
            print("✅ Student table schema updated successfully")
            return True
    except Exception as e:
        print(f"❌ Error altering table: {e}")
        return False

def clear_existing_students():
    """Clear all existing student data - already done in alter step"""
    print("\n" + "="*80)
    print("STEP 3: Verifying Student Data is Clear")
    print("="*80)
    
    try:
        with DatabaseManager.get_cursor() as (cur, conn):
            cur.execute("SELECT COUNT(*) as count FROM student;")
            count = cur.fetchone()['count']
            print(f"✅ Current student count: {count}")
            return True
    except Exception as e:
        print(f"❌ Error checking data: {e}")
        return False

def generate_student_data():
    """Generate 346 students with new ID format distributed across 2021-2025"""
    print("\n" + "="*80)
    print("STEP 4: Generating New Student Data")
    print("="*80)
    
    # Get all programs
    try:
        with DatabaseManager.get_cursor() as (cur, conn):
            cur.execute("SELECT code FROM program ORDER BY code;")
            programs = [row['code'] for row in cur.fetchall()]
    except Exception as e:
        print(f"❌ Error fetching programs: {e}")
        return False
    
    if not programs:
        print("❌ No programs found in database")
        return False
    
    print(f"Found {len(programs)} programs")
    
    # First names and last names for generation
    first_names = [
        'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
        'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
        'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
        'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa',
        'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
        'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
        'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna',
        'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
        'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Raymond', 'Christine', 'Gregory', 'Debra',
        'Frank', 'Rachel', 'Alexander', 'Catherine', 'Patrick', 'Carolyn', 'Jack', 'Janet',
        'Dennis', 'Ruth', 'Jerry', 'Maria', 'Tyler', 'Heather', 'Aaron', 'Diane'
    ]
    
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
        'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
        'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
        'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
        'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
        'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
        'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson'
    ]
    
    year_levels = ['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year']
    genders = ['Male', 'Female']
    
    # Distribution: 346 students across 5 years (2021-2025)
    # 2021: 50, 2022: 70, 2023: 80, 2024: 76, 2025: 70
    year_distribution = {
        2021: 50,
        2022: 70,
        2023: 80,
        2024: 76,
        2025: 70
    }
    
    students = []
    student_counter = 0
    
    for year in [2021, 2022, 2023, 2024, 2025]:
        count = year_distribution[year]
        for i in range(1, count + 1):
            student_id = f"{year}-{i:04d}"
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            program_code = random.choice(programs)
            year_level = random.choice(year_levels)
            gender = random.choice(genders)
            
            students.append({
                'id': student_id,
                'firstname': first_name,
                'lastname': last_name,
                'program_code': program_code,
                'year': year_level,
                'gender': gender
            })
            student_counter += 1
    
    print(f"Generated {len(students)} students")
    
    # Insert into database
    print("Inserting students into database...")
    try:
        with DatabaseManager.get_cursor() as (cur, conn):
            for idx, student in enumerate(students, 1):
                cur.execute("""
                    INSERT INTO student (id, firstname, lastname, program_code, year, gender)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    student['id'],
                    student['firstname'],
                    student['lastname'],
                    student['program_code'],
                    student['year'],
                    student['gender']
                ))
                
                if idx % 50 == 0:
                    print(f"  Inserted {idx}/{len(students)} students...")
            
            print(f"✅ Successfully inserted all {len(students)} students")
            
            # Verify
            cur.execute("SELECT COUNT(*) as count FROM student;")
            final_count = cur.fetchone()['count']
            print(f"✅ Final student count: {final_count}")
            
            # Show sample IDs
            cur.execute("SELECT id FROM student ORDER BY id LIMIT 10;")
            samples = [row['id'] for row in cur.fetchall()]
            print(f"✅ Sample IDs: {', '.join(samples)}")
            
            return True
    except Exception as e:
        print(f"❌ Error inserting students: {e}")
        return False

def main():
    """Run all migration steps"""
    print("\n" + "="*80)
    print("STUDENT ID FORMAT MIGRATION")
    print("From: 8-digit (20168837) → To: YYYY-XXXX (2025-0001)")
    print("="*80)
    
    # Step 1: Create function
    if not create_id_generation_function():
        print("\n❌ Migration failed at step 1")
        return False
    
    # Step 2: Alter table
    if not alter_student_table():
        print("\n❌ Migration failed at step 2")
        return False
    
    # Step 3: Clear data
    if not clear_existing_students():
        print("\n❌ Migration failed at step 3")
        return False
    
    # Step 4: Repopulate
    if not generate_student_data():
        print("\n❌ Migration failed at step 4")
        return False
    
    print("\n" + "="*80)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("Summary:")
    print("  • ID Generation Function: Created")
    print("  • Student Table Schema: Updated")
    print("  • Old Data: Cleared")
    print("  • New Data: 346 students inserted")
    print("  • ID Format: YYYY-XXXX (2021-0001 to 2025-0070)")
    print("="*80)
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
