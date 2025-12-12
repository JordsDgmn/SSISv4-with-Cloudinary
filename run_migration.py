"""
Run Database Migration to v4
Executes the migration SQL script with safety checks
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

MIGRATION_FILE = 'migration_to_v4.sql'
BACKUP_DIR = 'database_backups'

def check_backup_exists():
    """Check if a backup was created"""
    if not os.path.exists(BACKUP_DIR):
        return False
    
    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith('ssis_v3_backup')]
    return len(backups) > 0

def run_migration():
    """Run the migration SQL script"""
    
    print("\n" + "="*80)
    print("🚀 SSIS v4 DATABASE MIGRATION")
    print("="*80)
    print("\nThis will:")
    print("  1. Create backup tables (_v3_backup)")
    print("  2. Drop current tables")
    print("  3. Create new schema with IDs as primary keys")
    print("  4. Migrate all data")
    print("  5. Verify integrity")
    print("\n" + "="*80 + "\n")
    
    # Check if backup exists
    if not check_backup_exists():
        print("⚠️  WARNING: No backup found in database_backups/")
        print("\nPlease run backup first:")
        print("   python backup_database_v3.py\n")
        response = input("Continue anyway? (yes/no): ").strip().lower()
        if response != 'yes':
            print("\n❌ Migration cancelled. Run backup first!\n")
            return False
    else:
        print("✅ Backup found in database_backups/")
    
    print("\n⚠️  WARNING: This is a MAJOR database change!")
    print("Make sure you have a backup before continuing.\n")
    
    response = input("Proceed with migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Migration cancelled.\n")
        return False
    
    # Set password environment variable
    os.environ['PGPASSWORD'] = DB_CONFIG['password']
    
    try:
        print(f"\n{'='*80}")
        print(f"🔄 Running migration script...")
        print(f"{'='*80}\n")
        
        # Run migration in psql with interactive mode
        psql_cmd = (
            f'psql -h {DB_CONFIG["host"]} '
            f'-U {DB_CONFIG["user"]} '
            f'-d {DB_CONFIG["database"]} '
            f'-f "{MIGRATION_FILE}"'
        )
        
        result = os.system(psql_cmd)
        
        if result == 0:
            print(f"\n{'='*80}")
            print(f"✅ Migration script executed!")
            print(f"{'='*80}\n")
            print("📋 NEXT STEPS:")
            print("   1. Review the output above")
            print("   2. Check if data looks correct")
            print("   3. If good: type COMMIT; in psql to save changes")
            print("   4. If bad: type ROLLBACK; in psql to undo everything")
            print(f"\n{'='*80}\n")
            return True
        else:
            print(f"\n❌ Migration failed! Error code: {result}\n")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        return False
    finally:
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']

if __name__ == "__main__":
    run_migration()
