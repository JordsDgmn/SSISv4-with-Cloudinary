from flask import Blueprint, render_template, request, jsonify, redirect, url_for,flash

from website.models.collegeModels import CollegeModel
from website.models.programModels import ProgramModel
from website.models.studentModels import StudentModel
import os
from datetime import datetime

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

def log_activity(action, details):
    """Log all college-related activities"""
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}: {details}\n"
    try:
        with open('logs/activity.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log: {e}")

collegeRoute = Blueprint('college', __name__)
college_model = CollegeModel()
program_model = ProgramModel()
student_model = StudentModel()

@collegeRoute.route("/colleges", methods=["GET", "POST"])
def colleges():
    if request.method == "POST":
        print(f"\n{'='*80}")
        print(f"➕ CREATE COLLEGE REQUEST")
        print(f"{'='*80}")
        
        try:
            name = request.form.get("collegeName")
            code = request.form.get("collegeCode")
            
            print(f"📊 Form data received:")
            print(f"  College Code: {code}")
            print(f"  College Name: {name}")
            
            if not all([name, code]):
                print(f"❌ ERROR: Missing required fields")
                flash('All fields are required', 'danger')
            else:
                print(f"\n➕ Creating college in database...")
                result = college_model.create_college(name, code)
                print(f"📊 Create result: {result}")
                
                # Check if creation was successful
                if "success" in result.lower():
                    # Log the creation
                    log_activity("CREATE College", f"Code={code}, Name={name}")
                    flash('College created successfully', 'success')
                    print(f"✅ SUCCESS: College {code} created")
                else:
                    # Handle error (including duplicate key)
                    if "already exists" in result.lower() or "duplicate" in result.lower():
                        flash(f'Error: College with code "{code}" already exists', 'danger')
                        print(f"❌ ERROR: Duplicate college code {code}")
                    else:
                        flash(f'Error creating college: {result}', 'danger')
                        print(f"❌ ERROR: {result}")
            
            print(f"{'='*80}\n")
            
        except Exception as e:
            print(f"\n{'='*80}")
            print(f"❌ EXCEPTION OCCURRED")
            print(f"{'='*80}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Traceback:")
            import traceback
            traceback.print_exc()
            print(f"{'='*80}\n")
            flash(f'Error creating college: {str(e)}', 'danger')
    
    search_query = request.args.get("search")
    
    if search_query is None:
        search_query = ""  # Set a default value to an empty string if search_query is None
    
    colleges = college_model.search_colleges(search_query) if search_query else college_model.get_colleges()
    programs = program_model.get_programs()
    students_data = student_model.get_students(page_size=999999, page_number=1)
    students = students_data.get("results", []) if isinstance(students_data, dict) else []
    
    return render_template("colleges.html", colleges=colleges, programs=programs, students=students, search_query=search_query)

@collegeRoute.route("/colleges/delete/<int:college_id>", methods=["GET", "POST", "DELETE"])
def delete_college(college_id):
    print(f"\n{'='*80}")
    print(f"🗑️  DELETE COLLEGE REQUEST")
    print(f"{'='*80}")
    print(f"📋 College ID: {college_id}")
    print(f"📋 Request Method: {request.method}")
    print(f"📋 Request URL: {request.url}")
    print(f"📋 Referrer: {request.referrer}")
    print(f"{'='*80}\n")
    
    try:
        # Get college info first for logging
        print(f"🔍 Step 1: Fetching college details...")
        college = college_model.get_college_by_id(college_id)
        
        if not college:
            print(f"❌ ERROR: College ID {college_id} not found in database!")
            flash(f'College not found', 'danger')
            print(f"🔄 Redirecting to /colleges\n")
            return redirect(url_for('college.colleges'))
        
        college_name = college.get('name', 'Unknown')
        college_code = college.get('code', 'Unknown')
        print(f"✅ College found: {college_name} ({college_code})")
        print(f"📊 College data: {college}")
        
        # Perform deletion
        print(f"\n🗑️  Step 2: Executing deletion...")
        result = college_model.delete_college(college_id)
        print(f"📊 Delete result: {result}")
        
        if isinstance(result, dict) and result.get('success'):
            # Log the deletion
            log_activity("DELETE College", f"ID={college_id}, Code={college_code}, Name={college_name}")
            
            print(f"✅ SUCCESS: College {college_code} deleted")
            flash(f'College {college_name} ({college_code}) deleted successfully', 'success')
            message = result.get('message', 'College deleted')
        else:
            message = result.get('message', str(result)) if isinstance(result, dict) else str(result)
            print(f"❌ FAILED: {message}")
            flash(message, 'danger')
        
        if request.method == "DELETE" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print(f"📤 Returning JSON response")
            return jsonify(result if isinstance(result, dict) else {'success': False, 'message': str(result)})
        else:
            print(f"🔄 Redirecting to /colleges")
            print(f"{'='*80}\n")
            return redirect(url_for('college.colleges'))
            
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ EXCEPTION OCCURRED")
        print(f"{'='*80}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Traceback:")
        import traceback
        traceback.print_exc()
        print(f"{'='*80}\n")
        flash(f'Error deleting college: {str(e)}', 'danger')
        return redirect(url_for('college.colleges'))

@collegeRoute.route("/colleges/edit/<int:college_id>", methods=["POST"])
def edit_college(college_id):
    print(f"\n{'='*80}")
    print(f"✏️  EDIT COLLEGE REQUEST")
    print(f"{'='*80}")
    print(f"📋 College ID: {college_id}")
    print(f"📋 Request Method: {request.method}")
    print(f"{'='*80}\n")
    
    try:
        new_code = request.form.get("collegeCode")
        new_name = request.form.get("collegeName")
        
        print(f"📊 Form data received:")
        print(f"  College Code: {new_code}")
        print(f"  College Name: {new_name}")
        
        if not all([new_code, new_name]):
            print(f"❌ ERROR: Missing required fields")
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        print(f"\n✏️  Updating college in database...")
        result = college_model.update_college(college_id, new_code, new_name)
        print(f"📊 Update result: {result}")
        
        if isinstance(result, dict) and result.get('success'):
            # Log the edit
            log_activity("EDIT College", f"ID={college_id}, Code={new_code}, Name={new_name}")
            
            print(f"✅ SUCCESS: College {college_id} updated")
            print(f"{'='*80}\n")
            return jsonify(result)
        else:
            message = result.get('message', str(result)) if isinstance(result, dict) else str(result)
            print(f"❌ FAILED: {message}")
            print(f"{'='*80}\n")
            return jsonify({'success': False, 'message': message})
            
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ EXCEPTION OCCURRED")
        print(f"{'='*80}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Traceback:")
        import traceback
        traceback.print_exc()
        print(f"{'='*80}\n")
        return jsonify({'success': False, 'message': f'Error updating college: {str(e)}'})


@collegeRoute.route("/colleges/view/<string:college_code>", methods=["GET"])
def view_college(college_code):
    # Get college details
    college = college_model.get_college_with_details(college_code)
    
    if not college:
        flash(f'College with code "{college_code}" not found', 'danger')
        return redirect(url_for('college.colleges'))
    
    # Get all programs under this college
    programs = college_model.get_college_programs(college_code)
    
    # Get all students in this college (across all programs)
    students = student_model.get_students_by_college(college_code)
    
    # Group students by program for display
    students_by_program = {}
    for student in students:
        prog_code = student['program_code']
        if prog_code not in students_by_program:
            students_by_program[prog_code] = []
        students_by_program[prog_code].append(student)
    
    # Log the view
    log_activity("VIEW College", f"Code={college_code}, Name={college['name']}, Programs={len(programs)}, Students={len(students)}")
    
    return render_template('college_view.html', college=college, programs=programs, students_by_program=students_by_program)

