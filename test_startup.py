#!/usr/bin/env python
"""Test app startup and database connectivity"""

print("="*80)
print("Testing SSIS App Startup")
print("="*80)

try:
    print("\n1. Importing Flask app...")
    from website import create_app
    print("   ✅ Import successful!")
    
    print("\n2. Creating app instance...")
    app = create_app()
    print("   ✅ App created successfully!")
    
    print("\n3. Importing models...")
    from website.models.studentModels import StudentModel
    from website.models.programModels import ProgramModel
    from website.models.collegeModels import CollegeModel
    print("   ✅ Models imported successfully!")
    
    print("\n4. Testing database connection...")
    students = StudentModel.get_students(1, 1)
    print(f"   ✅ Database connection successful!")
    
    if isinstance(students, dict):
        student_count = len(students.get('results', []))
    else:
        student_count = len(students) if isinstance(students, list) else 0
    
    print(f"   📊 Found {student_count} student(s) in database")
    
    print("\n5. Testing server-side pagination method...")
    result = StudentModel.get_students_server_side(0, 25, '', 0, 'ASC')
    print(f"   ✅ Server-side method works!")
    print(f"   📊 Total students: {result.get('recordsTotal', 0)}")
    print(f"   📊 Data rows: {len(result.get('data', []))}")
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED! App is ready to run.")
    print("="*80)
    print("\n🚀 Starting Flask development server...")
    print("   Visit: http://127.0.0.1:5000")
    print("="*80 + "\n")
    
    # Start the app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    
except Exception as e:
    print("\n" + "="*80)
    print(f"❌ ERROR: {e}")
    print("="*80)
    import traceback
    traceback.print_exc()
    print("="*80)
