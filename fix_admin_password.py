"""
Fix the admin user password hash
Generates a proper werkzeug password hash for admin123
"""
import psycopg2
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'ssis')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')

def fix_password():
    """Update admin user with properly hashed password"""
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
        print("="*60)
        
        # Generate proper password hash
        password = 'admin123'
        password_hash = generate_password_hash(password)
        
        print(f"Generated password hash for '{password}':")
        print(f"{password_hash[:50]}...")
        print()
        
        # Update admin user
        cur.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE email = %s
        """, (password_hash, 'admin@ssis.edu'))
        
        conn.commit()
        
        print(f"✅ Updated admin user password!")
        print("\nLogin credentials:")
        print("  Email: admin@ssis.edu")
        print("  Password: admin123")
        print("\n✅ You can now login!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\nSSIS v4 - Fix Admin Password")
    print("="*60)
    fix_password()
