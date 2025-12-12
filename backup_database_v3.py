"""
Database Backup Script - SSIS v3
Creates a complete backup of the current database before v4 migration
"""

import psycopg2
from datetime import datetime
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ssis',
    'user': 'postgres',
    'password': 'geodgmn'
}

BACKUP_DIR = 'database_backups'
BACKUP_FILE = f'{BACKUP_DIR}/ssis_v3_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'

def create_backup():
    """Create a complete database backup using pg_dump"""
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✅ Created backup directory: {BACKUP_DIR}")
    
    # Construct pg_dump command
    pg_dump_cmd = (
        f'pg_dump -h {DB_CONFIG["host"]} '
        f'-U {DB_CONFIG["user"]} '
        f'-d {DB_CONFIG["database"]} '
        f'-F p '  # Plain text format
        f'-f "{BACKUP_FILE}"'
    )
    
    # Set password environment variable to avoid prompt
    os.environ['PGPASSWORD'] = DB_CONFIG['password']
    
    print(f"\n{'='*80}")
    print(f"🔄 Starting database backup...")
    print(f"{'='*80}")
    print(f"📊 Database: {DB_CONFIG['database']}")
    print(f"📁 Backup file: {BACKUP_FILE}")
    print(f"{'='*80}\n")
    
    try:
        # Execute pg_dump
        result = os.system(pg_dump_cmd)
        
        if result == 0:
            # Get file size
            file_size = os.path.getsize(BACKUP_FILE) / 1024  # KB
            
            print(f"\n{'='*80}")
            print(f"✅ BACKUP SUCCESSFUL!")
            print(f"{'='*80}")
            print(f"📁 File: {BACKUP_FILE}")
            print(f"📊 Size: {file_size:.2f} KB")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*80}\n")
            
            # Also create a Python backup of data (as fallback)
            create_python_backup()
            
            return True
        else:
            print(f"\n❌ BACKUP FAILED!")
            print(f"Error code: {result}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False
    finally:
        # Clear password from environment
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']


def create_python_backup():
    """Create a Python-based backup (CSV exports) as additional safety"""
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Backup colleges
        cur.execute("SELECT * FROM colleges ORDER BY college_code")
        colleges = cur.fetchall()
        with open(f'{BACKUP_DIR}/colleges_backup_{timestamp}.csv', 'w', encoding='utf-8') as f:
            f.write("college_code,college_name\n")
            for row in colleges:
                f.write(f'"{row[0]}","{row[1]}"\n')
        print(f"   ✅ Exported {len(colleges)} colleges")
        
        # Backup programs
        cur.execute("SELECT * FROM programs ORDER BY program_code")
        programs = cur.fetchall()
        with open(f'{BACKUP_DIR}/programs_backup_{timestamp}.csv', 'w', encoding='utf-8') as f:
            f.write("program_code,program_name,college_code\n")
            for row in programs:
                f.write(f'"{row[0]}","{row[1]}","{row[2]}"\n')
        print(f"   ✅ Exported {len(programs)} programs")
        
        # Backup students
        cur.execute("SELECT * FROM students ORDER BY id")
        students = cur.fetchall()
        with open(f'{BACKUP_DIR}/students_backup_{timestamp}.csv', 'w', encoding='utf-8') as f:
            f.write("id,firstname,lastname,year,gender,program_code,profile_pic_url\n")
            for row in students:
                profile_url = row[6] if row[6] else ""
                f.write(f'"{row[0]}","{row[1]}","{row[2]}","{row[3]}","{row[4]}","{row[5]}","{profile_url}"\n')
        print(f"   ✅ Exported {len(students)} students")
        
        cur.close()
        conn.close()
        
        print(f"\n   📦 Additional CSV backups created in {BACKUP_DIR}/")
        
    except Exception as e:
        print(f"   ⚠️  CSV backup warning: {str(e)}")


def verify_backup():
    """Verify the backup file was created and contains data"""
    
    if not os.path.exists(BACKUP_FILE):
        print("❌ Backup file not found!")
        return False
    
    file_size = os.path.getsize(BACKUP_FILE)
    if file_size < 1000:  # Less than 1KB is suspicious
        print(f"⚠️  Warning: Backup file seems too small ({file_size} bytes)")
        return False
    
    return True


def show_restore_instructions():
    """Show instructions for restoring the backup"""
    
    print("\n" + "="*80)
    print("📖 RESTORE INSTRUCTIONS")
    print("="*80)
    print("\nTo restore this backup, run:")
    print(f'\n   psql -U postgres -d ssis < "{BACKUP_FILE}"')
    print("\nOr use the restore script:")
    print(f'\n   python restore_database.py "{BACKUP_FILE}"')
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🗄️  SSIS v3 DATABASE BACKUP UTILITY")
    print("="*80)
    print("\nThis will create a complete backup of your current database")
    print("before migrating to v4 (editable codes, no cascade delete).")
    print("\n" + "="*80 + "\n")
    
    response = input("Proceed with backup? (yes/no): ").strip().lower()
    
    if response == 'yes':
        success = create_backup()
        
        if success and verify_backup():
            show_restore_instructions()
            print("✅ Backup completed successfully! Safe to proceed with migration.\n")
        else:
            print("\n❌ Backup verification failed. DO NOT proceed with migration!\n")
    else:
        print("\n❌ Backup cancelled.\n")
