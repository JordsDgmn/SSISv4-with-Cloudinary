"""
Database migration script to create users table
Run this before starting the application with authentication
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'ssis')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')

def run_migration():
    """Run the users table migration"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        print("Connected to database successfully!")
        print(f"Database: {DB_NAME}@{DB_HOST}")
        print("\nRunning migration: create_users_table")
        print("="*60)
        
        # Read migration SQL
        with open('database/migrations/create_users_table.sql', 'r') as f:
            sql = f.read()
        
        # Execute migration
        cur.execute(sql)
        conn.commit()
        
        print("✅ Users table created successfully!")
        print("✅ Default admin user created")
        print("\nDefault credentials:")
        print("  Email: admin@ssis.edu")
        print("  Password: admin123")
        print("\n⚠️  Please change the default password after first login!")
        
        # Verify table was created
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """)
        columns = cur.fetchall()
        
        print("\nUsers table structure:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        cur.close()
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        print("You can now start the Flask application with authentication enabled.")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except FileNotFoundError:
        print("❌ Migration file not found: database/migrations/create_users_table.sql")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("SSIS v4 - User Authentication Migration")
    print("="*60)
    run_migration()
