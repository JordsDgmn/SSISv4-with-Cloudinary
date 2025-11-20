#!/usr/bin/env python3
"""
SSIS Setup Script
This script helps set up the Student Information System with PostgreSQL
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python 3.8+ is installed"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version} detected")
    return True

def check_postgresql():
    """Check if PostgreSQL is available"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL detected: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL not installed or not in PATH")
        return False

def install_dependencies():
    """Install Python dependencies using pipenv"""
    print("📦 Installing Python dependencies...")
    try:
        # Check if pipenv is installed
        subprocess.run(['pipenv', '--version'], check=True, capture_output=True)
        print("✅ Pipenv found")
        
        # Install dependencies
        subprocess.run(['pipenv', 'install'], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pipenv not found. Please install pipenv first:")
        print("   pip install pipenv")
        return False

def create_env_file():
    """Create .env file from .env.example"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_example.exists() and not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from .env.example")
        print("📋 Please edit .env file with your actual database and Cloudinary credentials")
        return True
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def setup_database():
    """Instructions for database setup"""
    print("\n🗄️  Database Setup Instructions:")
    print("1. Make sure PostgreSQL is running")
    print("2. Create a database named 'ssis':")
    print("   createdb ssis")
    print("3. Run the schema and initial data:")
    print("   psql -d ssis -f SSIS_postgres.sql")
    print("4. Generate and insert student data:")
    print("   python generate_student_data.py")
    print("   psql -d ssis -f student_data.sql")

def main():
    """Main setup function"""
    print("🚀 SSIS Setup Script")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_postgresql():
        print("Please install PostgreSQL and make sure it's in your PATH")
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create environment file
    if not create_env_file():
        return False
    
    # Database setup instructions
    setup_database()
    
    print("\n✅ Setup completed!")
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your database and Cloudinary credentials")
    print("2. Follow the database setup instructions above")
    print("3. Run the application with: pipenv run python app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)