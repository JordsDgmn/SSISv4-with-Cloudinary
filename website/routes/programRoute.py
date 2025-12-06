from flask import Blueprint, render_template, request, jsonify, flash
from website.models.programModels import ProgramModel
from website.models.collegeModels import CollegeModel
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

@programRoute.route("/programs", methods=["GET", "POST"])
def programs():
    if request.method == "POST":
        print(f"\n{'='*80}")
        print(f"➕ CREATE PROGRAM REQUEST")
        print(f"{'='*80}")
        
        try:
            name = request.form.get("programName")
            code = request.form.get("programCode")
            college_code = request.form.get("collegeCode")
            
            print(f"📊 Form data received:")
            print(f"  Program Code: {code}")
            print(f"  Program Name: {name}")
            print(f"  College Code: {college_code}")
            
            if not all([name, code, college_code]):
                print(f"❌ ERROR: Missing required fields")
                flash('All fields are required', 'danger')
            else:
                print(f"\n➕ Creating program in database...")
                result = program_model.create_program(name, code, college_code)
                print(f"📊 Create result: {result}")
                
                # Check if creation was successful
                if "success" in result.lower():
                    # Log the creation
                    log_activity("CREATE Program", f"Code={code}, Name={name}, College={college_code}")
                    flash('Program created successfully', 'success')
                    print(f"✅ SUCCESS: Program {code} created")
                else:
                    # Handle error (including duplicate key)
                    if "already exists" in result.lower() or "duplicate" in result.lower():
                        flash(f'Error: Program with code "{code}" already exists', 'danger')
                        print(f"❌ ERROR: Duplicate program code {code}")
                    else:
                        flash(f'Error creating program: {result}', 'danger')
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
            flash(f'Error creating program: {str(e)}', 'danger')

    search_query = request.args.get("search", default="")  

    programs = program_model.search_programs(search_query) if search_query else program_model.get_programs()
    colleges = college_model.get_colleges()

    return render_template("programs.html", programs=programs, colleges=colleges, search_query=search_query)


@programRoute.route("/programs/edit/<string:program_code>", methods=["POST"])
def edit_program(program_code):
    print(f"\n{'='*80}")
    print(f"✏️  EDIT PROGRAM REQUEST")
    print(f"{'='*80}")
    print(f"📋 Program Code: {program_code}")
    print(f"📋 Request Method: {request.method}")
    print(f"{'='*80}\n")
    
    try:
        new_name = request.form.get("programName")
        college_code = request.form.get("collegeCode")
        
        print(f"📊 Form data received:")
        print(f"  Program Name: {new_name}")
        print(f"  College Code: {college_code}")
        
        if not all([program_code, new_name, college_code]):
            print(f"❌ ERROR: Missing required fields")
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        print(f"\n✏️  Updating program in database...")
        result = program_model.update_program(program_code, new_name, college_code)
        print(f"📊 Update result: {result}")
        
        if 'successfully' in result.lower():
            # Log the edit
            log_activity("EDIT Program", f"Code={program_code}, Name={new_name}, College={college_code}")
            
            print(f"✅ SUCCESS: Program {program_code} updated")
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
        return jsonify({'success': False, 'message': f'Error updating program: {str(e)}'})

@programRoute.route("/programs/delete/<string:program_code>", methods=["GET", "POST", "DELETE"])
def delete_program(program_code):
    from flask import redirect, url_for
    
    print(f"\n{'='*80}")
    print(f"🗑️  DELETE PROGRAM REQUEST")
    print(f"{'='*80}")
    print(f"📋 Program Code: {program_code}")
    print(f"📋 Request Method: {request.method}")
    print(f"📋 Request URL: {request.url}")
    print(f"📋 Referrer: {request.referrer}")
    print(f"{'='*80}\n")
    
    try:
        # Get program info first for logging
        print(f"🔍 Step 1: Fetching program details...")
        programs = program_model.get_programs()
        print(f"📊 Total programs fetched: {len(programs)}")
        if programs:
            print(f"📊 Sample program keys: {programs[0].keys()}")
        
        # Use program_code key (not 'code') because get_programs() returns it as program_code
        program = next((p for p in programs if p.get('program_code') == program_code), None)
        
        if not program:
            print(f"❌ ERROR: Program {program_code} not found in database!")
            print(f"📊 Available program codes: {[p.get('program_code') for p in programs]}")
            flash(f'Program {program_code} not found', 'danger')
            print(f"🔄 Redirecting to /programs\n")
            return redirect(url_for('programs.programs'))
        
        program_name = program.get('program_name', 'Unknown')
        print(f"✅ Program found: {program_name}")
        print(f"📊 Program data: {program}")
        
        # Perform deletion
        print(f"\n🗑️  Step 2: Executing deletion...")
        result = program_model.delete_program(program_code)
        print(f"📊 Delete result: {result}")
        
        if 'successfully' in result.lower():
            # Log the deletion
            log_activity("DELETE Program", f"Code={program_code}, Name={program_name}")
            
            print(f"✅ SUCCESS: Program {program_code} deleted")
            flash(f'Program {program_name} ({program_code}) deleted successfully', 'success')
        else:
            print(f"❌ FAILED: {result}")
            flash(result, 'danger')
        
        if request.method == "DELETE" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print(f"📤 Returning JSON response")
            return jsonify({'success': 'successfully' in result.lower(), 'message': result})
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
