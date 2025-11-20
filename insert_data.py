"""
Insert student data into the database
"""
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def insert_student_data():
    """Insert generated student data into the database"""
    try:
        # Connect to the ssis database
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='ssis'
        )
        
        cursor = conn.cursor()
        
        # Read and execute the student data SQL file
        with open('student_data.sql', 'r') as f:
            sql_commands = f.read()
            # Execute the SQL commands
            cursor.execute(sql_commands)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Student data inserted successfully!")
        
        # Count students to verify
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='ssis'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM student")
        count = cursor.fetchone()[0]
        print(f"📊 Total students in database: {count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error inserting student data: {e}")
        return False

if __name__ == "__main__":
    print("📥 Inserting student data into database...")
    if insert_student_data():
        print("🎉 Database is ready with sample data!")
        print("\n🚀 Ready to run the web application!")
        print("Run: python app.py")
    else:
        print("❌ Failed to insert student data")