from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from website.models.programModels import ProgramModel
from website.models.collegeModels import CollegeModel
from website.models.studentModels import StudentModel
import os
from datetime import datetime

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

def log_activity(action, details):
    """Log all program-related activities"""
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}: {details}\n"
    try:
        with open('logs/activity.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log: {e}")

programRoute = Blueprint('programs', __name__)
program_model = ProgramModel()
college_model = CollegeModel()
student_model = StudentModel()

@programRoute.route("/programs", methods=["GET", "POST"])
def programs():
    if request.method == "POST":
        print(f"\n{'='*80}")
        print(f"➕ CREATE PROGRAM REQUEST")
        print(f"{'='*80}")
        
        try:
            name = request.form.get("programName")
            code = request.form.get("programCode")
            college_id = request.form.get("collegeId")
            
            # Handle "No College" selection
            if college_id == "" or college_id == "null":
                college_id = None
            else:
                college_id = int(college_id) if college_id else None
            
            print(f"📊 Form data received:")
            print(f"  Program Code: {code}")
            print(f"  Program Name: {name}")
            print(f"  College ID: {college_id}")
            
            if not all([name, code]):
                print(f"❌ ERROR: Missing required fields")
                flash('Program name and code are required', 'danger')
            else:
                print(f"\n➕ Creating program in database...")
                result = program_model.create_program(name, code, college_id)
                print(f"📊 Create result: {result}")
                
                # Check if creation was successful
                if isinstance(result, dict) and result.get('success'):
                    # Log the creation
                    log_activity("CREATE Program", f"Code={code}, Name={name}, College ID={college_id}")
                    flash('Program created successfully', 'success')
                    print(f"✅ SUCCESS: Program {code} created")
                else:
                    message = result.get('message', str(result)) if isinstance(result, dict) else str(result)
                    flash(f'Error creating program: {message}', 'danger')
                    print(f"❌ ERROR: {message}")
            
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
            flash(f'Error creating program: {str(e)}', 'danger')

    search_query = request.args.get("search", default="")  

    programs = program_model.search_programs(search_query) if search_query else program_model.get_programs()
    colleges = college_model.get_colleges()
    students_data = student_model.get_students(page_size=999999, page_number=1)
    students = students_data.get("results", []) if isinstance(students_data, dict) else []

    return render_template("programs.html", programs=programs, colleges=colleges, students=students, search_query=search_query)


@programRoute.route("/programs/edit/<int:program_id>", methods=["POST"])
def edit_program(program_id):
    print(f"\n{'='*80}")
    print(f"✏️  EDIT PROGRAM REQUEST")
    print(f"{'='*80}")
    print(f"📋 Program ID: {program_id}")
    print(f"📋 Request Method: {request.method}")
    print(f"{'='*80}\n")
    
    try:
        new_code = request.form.get("programCode")
        new_name = request.form.get("programName")
        college_id = request.form.get("collegeId")
        
        # Handle "No College" selection
        if college_id == "" or college_id == "null":
            college_id = None
        else:
            college_id = int(college_id) if college_id else None
        
        print(f"📊 Form data received:")
        print(f"  Program Code: {new_code}")
        print(f"  Program Name: {new_name}")
        print(f"  College ID: {college_id}")
        
        if not all([new_code, new_name]):
            print(f"❌ ERROR: Missing required fields")
            return jsonify({'success': False, 'message': 'Program code and name are required'})
        
        print(f"\n✏️  Updating program in database...")
        result = program_model.update_program(program_id, new_code, new_name, college_id)
        print(f"📊 Update result: {result}")
        
        if isinstance(result, dict) and result.get('success'):
            # Log the edit
            log_activity("EDIT Program", f"ID={program_id}, Code={new_code}, Name={new_name}, College ID={college_id}")
            
            print(f"✅ SUCCESS: Program {program_id} updated")
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
        return jsonify({'success': False, 'message': f'Error updating program: {str(e)}'})

@programRoute.route("/programs/delete/<int:program_id>", methods=["GET", "POST", "DELETE"])
def delete_program(program_id):
    print(f"\n{'='*80}")
    print(f"🗑️  DELETE PROGRAM REQUEST")
    print(f"{'='*80}")
    print(f"📋 Program ID: {program_id}")
    print(f"📋 Request Method: {request.method}")
    print(f"📋 Request URL: {request.url}")
    print(f"📋 Referrer: {request.referrer}")
    print(f"{'='*80}\n")
    
    try:
        # Get program info first for logging
        print(f"🔍 Step 1: Fetching program details...")
        program = program_model.get_program_by_id(program_id)
        
        if not program:
            print(f"❌ ERROR: Program ID {program_id} not found in database!")
            flash(f'Program not found', 'danger')
            print(f"🔄 Redirecting to /programs\n")
            return redirect(url_for('programs.programs'))
        
        program_name = program.get('name', 'Unknown')
        program_code = program.get('code', 'Unknown')
        print(f"✅ Program found: {program_name} ({program_code})")
        print(f"📊 Program data: {program}")
        
        # Perform deletion
        print(f"\n🗑️  Step 2: Executing deletion...")
        result = program_model.delete_program(program_id)
        print(f"📊 Delete result: {result}")
        
        if isinstance(result, dict) and result.get('success'):
            # Log the deletion
            log_activity("DELETE Program", f"ID={program_id}, Code={program_code}, Name={program_name}")
            
            print(f"✅ SUCCESS: Program {program_code} deleted")
            flash(f'Program {program_name} ({program_code}) deleted successfully', 'success')
            message = result.get('message', 'Program deleted')
        else:
            message = result.get('message', str(result)) if isinstance(result, dict) else str(result)
            print(f"❌ FAILED: {message}")
            flash(message, 'danger')
        
        if request.method == "DELETE" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print(f"📤 Returning JSON response")
            return jsonify(result if isinstance(result, dict) else {'success': False, 'message': str(result)})
        else:
            print(f"🔄 Redirecting to /programs")
            print(f"{'='*80}\n")
            return redirect(url_for('programs.programs'))
            
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
        flash(f'Error deleting program: {str(e)}', 'danger')
        return redirect(url_for('programs.programs'))


@programRoute.route("/programs/view/<int:program_id>", methods=["GET"])
def view_program(program_id):
    # Get program with details
    program = program_model.get_program_by_id(program_id)
    
    if not program:
        flash(f'Program not found', 'danger')
        return redirect(url_for('programs.programs'))
    
    # Get all students enrolled in this program
    students = student_model.get_students_by_program(program_id)
    
    # Log the view
    log_activity("VIEW Program", f"ID={program_id}, Code={program['code']}, Name={program['name']}, Students={len(students)}")
    
    return render_template('program_view.html', program=program, students=students)
