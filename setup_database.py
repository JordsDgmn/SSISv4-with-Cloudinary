"""
Database setup script for SSIS
This script creates the database and initial schema
"""
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test different connection methods"""
    configs_to_try = [
        {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'geodgmn',  # Found in my-app .env file
            'database': 'postgres'
        },
        {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'postgres'
        },
        {
            'host': 'localhost',
            'port': '5432', 
            'user': 'postgres',
            'password': 'admin',
            'database': 'postgres'
        },
        {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres', 
            'password': 'password',
            'database': 'postgres'
        },
        {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': '123',
            'database': 'postgres'
        }
    ]
    
    for i, config in enumerate(configs_to_try):
        try:
            print(f"Trying connection {i+1}: user={config['user']}, password={config['password'][:3]}***")
            conn = psycopg2.connect(**config)
            conn.close()
            print(f"✅ Success! Working password is: {config['password']}")
            return config
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    return None

def create_database():
    """Create the SSIS database if it doesn't exist"""
    try:
        config = test_connection()
        if not config:
            print("❌ Could not establish database connection with any common passwords")
            print("Please check your PostgreSQL installation and password")
            return False
            
        # Connect using working config
        conn = psycopg2.connect(**config)
        
        # Enable autocommit to create database
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='ssis'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE ssis')
            print("✅ Database 'ssis' created successfully!")
        else:
            print("✅ Database 'ssis' already exists!")
        
        cursor.close()
        conn.close()
        
        # Update .env file with working password
        print(f"📝 Updating .env file with working password: {config['password']}")
        update_env_password(config['password'])
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def update_env_password(password):
    """Update the .env file with the correct password"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace the password line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('POSTGRES_PASSWORD='):
                lines[i] = f'POSTGRES_PASSWORD={password}'
                break
        
        with open('.env', 'w') as f:
            f.write('\n'.join(lines))
            
        print("✅ .env file updated with correct password")
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def setup_schema():
    """Set up the database schema"""
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
        
        # Read and execute the SQL schema file
        with open('SSIS_postgres.sql', 'r') as f:
            sql_commands = f.read()
            cursor.execute(sql_commands)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database schema created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up schema: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up SSIS Database...")
    print("Testing database connections...")
    
    if create_database():
        if setup_schema():
            print("🎉 Database setup completed successfully!")
            print("\nNext steps:")
            print("1. Generate sample data: python generate_student_data.py")
            print("2. Run the application: python app.py")
        else:
            print("❌ Database setup failed during schema creation")
    else:
        print("❌ Database setup failed during database creation")