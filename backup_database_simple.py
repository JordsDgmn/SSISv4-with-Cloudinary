"""
Simple Database Backup Script - SSIS v3
Creates a complete Python-based backup of the current database
"""

import psycopg2
from datetime import datetime
import os
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ssis',
    'user': 'postgres',
    'password': 'geodgmn'
}

BACKUP_DIR = 'database_backups'

def create_backup_directory():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✅ Created backup directory: {BACKUP_DIR}")
    return BACKUP_DIR

def backup_table_to_json(cursor, table_name, columns):
    """Backup a table to JSON format"""
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY {columns[0]}")
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        record = {}
        for i, col in enumerate(columns):
            record[col] = row[i]
        data.append(record)
    
    return data

def create_backup():
    """Create complete database backup"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = create_backup_directory()
    
    print(f"\n{'='*80}")
    print(f"🔄 Starting database backup...")
    print(f"{'='*80}")
    print(f"📊 Database: {DB_CONFIG['database']}")
    print(f"📁 Backup directory: {backup_dir}")
    print(f"{'='*80}\n")
    
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        backup_data = {
            'version': 'v3',
            'timestamp': timestamp,
            'database': DB_CONFIG['database']
        }
        
        # Backup colleges
        print("📦 Backing up colleges...")
        colleges_data = backup_table_to_json(cur, 'college', ['code', 'name'])
        backup_data['colleges'] = colleges_data
        print(f"   ✅ Backed up {len(colleges_data)} colleges")
        
        # Backup programs
        print("📦 Backing up programs...")
        programs_data = backup_table_to_json(cur, 'program', ['code', 'name', 'collegecode'])
        backup_data['programs'] = programs_data
        print(f"   ✅ Backed up {len(programs_data)} programs")
        
        # Backup students
        print("📦 Backing up students...")
        students_data = backup_table_to_json(cur, 'student', ['id', 'firstname', 'lastname', 'year', 'gender', 'coursecode', 'profile_pic'])
        backup_data['students'] = students_data
        print(f"   ✅ Backed up {len(students_data)} students")
        
        # Save to JSON file
        backup_file = f'{backup_dir}/ssis_v3_backup_{timestamp}.json'
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        # Also create SQL insert statements
        sql_file = f'{backup_dir}/ssis_v3_backup_{timestamp}.sql'
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- SSIS v3 Database Backup\n")
            f.write(f"-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Colleges
            f.write("-- Colleges\n")
            for college in colleges_data:
                code = college['code'].replace("'", "''")
                name = college['name'].replace("'", "''")
                f.write(f"INSERT INTO college (code, name) VALUES ('{code}', '{name}');\n")
            
            f.write("\n-- Programs\n")
            for program in programs_data:
                p_code = program['code'].replace("'", "''")
                p_name = program['name'].replace("'", "''")
                c_code = program['collegecode'].replace("'", "''")
                f.write(f"INSERT INTO program (code, name, collegecode) VALUES ('{p_code}', '{p_name}', '{c_code}');\n")
            
            f.write("\n-- Students\n")
            for student in students_data:
                sid = student['id'].replace("'", "''")
                fname = student['firstname'].replace("'", "''")
                lname = student['lastname'].replace("'", "''")
                year = student['year'].replace("'", "''")
                gender = student['gender'].replace("'", "''")
                prog = student['coursecode'].replace("'", "''")
                pic = student['profile_pic'] or ''
                if pic:
                    pic = pic.replace("'", "''")
                f.write(f"INSERT INTO student (id, firstname, lastname, year, gender, coursecode, profile_pic) VALUES ('{sid}', '{fname}', '{lname}', '{year}', '{gender}', '{prog}', '{pic}');\n")
        
        cur.close()
        conn.close()
        
        # Calculate file sizes
        json_size = os.path.getsize(backup_file) / 1024
        sql_size = os.path.getsize(sql_file) / 1024
        
        print(f"\n{'='*80}")
        print(f"✅ BACKUP SUCCESSFUL!")
        print(f"{'='*80}")
        print(f"📁 JSON backup: {backup_file} ({json_size:.2f} KB)")
        print(f"📁 SQL backup:  {sql_file} ({sql_size:.2f} KB)")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        print("📊 Backup Summary:")
        print(f"   Colleges:  {len(colleges_data)}")
        print(f"   Programs:  {len(programs_data)}")
        print(f"   Students:  {len(students_data)}")
        print(f"\n{'='*80}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ BACKUP FAILED!")
        print(f"Error: {str(e)}\n")
        return False

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
        
        if success:
            print("✅ Backup completed successfully! Safe to proceed with migration.\n")
        else:
            print("\n❌ Backup failed. DO NOT proceed with migration!\n")
    else:
        print("\n❌ Backup cancelled.\n")
