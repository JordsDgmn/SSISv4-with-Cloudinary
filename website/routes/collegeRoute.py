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

@collegeRoute.route("/colleges/delete/<string:college_code>", methods=["GET", "POST", "DELETE"])
def delete_college(college_code):
    print(f"\n{'='*80}")
    print(f"🗑️  DELETE COLLEGE REQUEST")
    print(f"{'='*80}")
    print(f"📋 College Code: {college_code}")
    print(f"📋 Request Method: {request.method}")
    print(f"📋 Request URL: {request.url}")
    print(f"📋 Referrer: {request.referrer}")
    print(f"{'='*80}\n")
    
    try:
        # Get college info first for logging
        print(f"🔍 Step 1: Fetching college details...")
        colleges = college_model.get_colleges()
        college = next((c for c in colleges if c.get('code') == college_code), None)
        
        if not college:
            print(f"❌ ERROR: College {college_code} not found in database!")
            flash(f'College {college_code} not found', 'danger')
            print(f"🔄 Redirecting to /colleges\n")
            return redirect(url_for('college.colleges'))
        
        college_name = college.get('name', 'Unknown')
        print(f"✅ College found: {college_name}")
        print(f"📊 College data: {college}")
        
        # Perform deletion
        print(f"\n🗑️  Step 2: Executing deletion...")
        result = college_model.delete_college(college_code)
        print(f"📊 Delete result: {result}")
        
        if 'successfully' in result.lower():
            # Log the deletion
            log_activity("DELETE College", f"Code={college_code}, Name={college_name}")
            
            print(f"✅ SUCCESS: College {college_code} deleted")
            flash(f'College {college_name} ({college_code}) deleted successfully', 'success')
        else:
            print(f"❌ FAILED: {result}")
            flash(result, 'danger')
        
        if request.method == "DELETE" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print(f"📤 Returning JSON response")
            return jsonify({'success': 'successfully' in result.lower(), 'message': result})
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

@collegeRoute.route("/colleges/edit/<string:college_code>", methods=["POST"])
def edit_college(college_code):
    print(f"\n{'='*80}")
    print(f"✏️  EDIT COLLEGE REQUEST")
    print(f"{'='*80}")
    print(f"📋 College Code: {college_code}")
    print(f"📋 Request Method: {request.method}")
    print(f"{'='*80}\n")
    
    try:
        new_name = request.form.get("collegeName")
        
        print(f"📊 Form data received:")
        print(f"  College Name: {new_name}")
        
        if not all([college_code, new_name]):
            print(f"❌ ERROR: Missing required fields")
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        print(f"\n✏️  Updating college in database...")
        result = college_model.update_college(college_code, new_name)
        print(f"📊 Update result: {result}")
        
        if 'successfully' in result.lower():
            # Log the edit
            log_activity("EDIT College", f"Code={college_code}, Name={new_name}")
            
            print(f"✅ SUCCESS: College {college_code} updated")
            print(f"{'='*80}\n")
            return jsonify({'success': True, 'message': result})
        else:
            print(f"❌ FAILED: {result}")
            print(f"{'='*80}\n")
            return jsonify({'success': False, 'message': result})
            
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
