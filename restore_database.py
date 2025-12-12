"""
Database Restore Script - SSIS v3
Restores a database backup created by backup_database_v3.py
"""

import os
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ssis',
    'user': 'postgres',
    'password': 'geodgmn'
}

def restore_backup(backup_file):
    """Restore database from backup file"""
    
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return False
    
    print(f"\n{'='*80}")
    print(f"🔄 Starting database restore...")
    print(f"{'='*80}")
    print(f"📁 Backup file: {backup_file}")
    print(f"📊 Database: {DB_CONFIG['database']}")
    print(f"{'='*80}\n")
    
    print("⚠️  WARNING: This will OVERWRITE the current database!")
    response = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Restore cancelled.\n")
        return False
    
    # Set password environment variable
    os.environ['PGPASSWORD'] = DB_CONFIG['password']
    
    try:
        # Drop and recreate database
        print("\n🗑️  Dropping current database...")
        drop_cmd = f'psql -h {DB_CONFIG["host"]} -U {DB_CONFIG["user"]} -d postgres -c "DROP DATABASE IF EXISTS {DB_CONFIG["database"]}"'
        os.system(drop_cmd)
        
        print("📦 Creating fresh database...")
        create_cmd = f'psql -h {DB_CONFIG["host"]} -U {DB_CONFIG["user"]} -d postgres -c "CREATE DATABASE {DB_CONFIG["database"]}"'
        os.system(create_cmd)
        
        # Restore from backup
        print(f"📥 Restoring from backup...\n")
        restore_cmd = f'psql -h {DB_CONFIG["host"]} -U {DB_CONFIG["user"]} -d {DB_CONFIG["database"]} -f "{backup_file}"'
        result = os.system(restore_cmd)
        
        if result == 0:
            print(f"\n{'='*80}")
            print(f"✅ RESTORE SUCCESSFUL!")
            print(f"{'='*80}\n")
            return True
        else:
            print(f"\n❌ RESTORE FAILED! Error code: {result}\n")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        return False
    finally:
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n❌ Usage: python restore_database.py <backup_file>")
        print("\nExample:")
        print("   python restore_database.py database_backups/ssis_v3_backup_20251212_150000.sql\n")
        sys.exit(1)
    
    backup_file = sys.argv[1]
    restore_backup(backup_file)
