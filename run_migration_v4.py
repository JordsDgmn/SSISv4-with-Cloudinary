"""
SSIS v4 Migration Runner
Executes the migration from code-based PKs to ID-based PKs with editable codes
"""

import psycopg2
from config import Config

def run_migration():
    print("\n" + "="*80)
    print("SSIS v4 DATABASE MIGRATION")
    print("="*80)
    print("\n⚠️  WARNING: This migration will:")
    print("  1. Create backup tables (_v3_backup)")
    print("  2. DROP existing college, program, student tables")
    print("  3. CREATE new tables with SERIAL IDs and UNIQUE codes")
    print("  4. Migrate all data (preserving relationships via LEFT JOINs)")
    print("  5. Change ON DELETE CASCADE → ON DELETE SET NULL")
    print("\n" + "="*80)
    
    confirm = input("\n📝 Type 'MIGRATE' to proceed (or anything else to cancel): ")
    
    if confirm != "MIGRATE":
        print("\n❌ Migration cancelled. No changes made.")
        return
    
    print("\n🔄 Connecting to database...")
    
    try:
        conn = psycopg2.connect(
            host=Config.POSTGRES_HOST,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            port=Config.POSTGRES_PORT
        )
        conn.autocommit = False  # Start transaction mode
        cur = conn.cursor()
        
        print("✅ Connected successfully")
        print("\n📖 Reading migration script...")
        
        with open('migration_to_v4_clean.sql', 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        print("✅ Migration script loaded")
        print("\n🚀 Executing migration...")
        print("="*80)
        
        # Execute the migration
        cur.execute(migration_sql)
        
        # Get verification counts
        print("\n📊 Verifying migration results:")
        print("-"*80)
        
        cur.execute("SELECT COUNT(*) FROM college")
        college_count = cur.fetchone()[0]
        print(f"✓ Colleges: {college_count}")
        
        cur.execute("SELECT COUNT(*) FROM program")
        program_count = cur.fetchone()[0]
        print(f"✓ Programs: {program_count}")
        
        cur.execute("SELECT COUNT(*) FROM student")
        student_count = cur.fetchone()[0]
        print(f"✓ Students: {student_count}")
        
        cur.execute("SELECT COUNT(*) FROM program WHERE college_id IS NULL")
        orphaned_programs = cur.fetchone()[0]
        print(f"✓ Orphaned programs: {orphaned_programs}")
        
        cur.execute("SELECT COUNT(*) FROM student WHERE program_id IS NULL")
        orphaned_students = cur.fetchone()[0]
        print(f"✓ Orphaned students: {orphaned_students}")
        
        print("-"*80)
        print("\n✅ Migration executed successfully!")
        print("\n⚠️  IMPORTANT: Transaction is NOT YET COMMITTED!")
        print("="*80)
        
        final_confirm = input("\n💾 Type 'COMMIT' to save changes (or anything else to ROLLBACK): ")
        
        if final_confirm == "COMMIT":
            conn.commit()
            print("\n✅ MIGRATION COMMITTED - Changes saved to database")
            print("✅ Backup tables preserved: college_v3_backup, program_v3_backup, student_v3_backup")
        else:
            conn.rollback()
            print("\n❌ MIGRATION ROLLED BACK - No changes made to database")
        
        cur.close()
        conn.close()
        
        print("="*80)
        print("✅ Migration process complete")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR during migration:")
        print(f"   {type(e).__name__}: {str(e)}")
        print("\n🔄 Rolling back transaction...")
        try:
            conn.rollback()
            print("✅ Rollback successful - database unchanged")
        except:
            print("❌ Rollback failed - database may be in inconsistent state!")
        print("="*80 + "\n")
        raise

if __name__ == "__main__":
    run_migration()
