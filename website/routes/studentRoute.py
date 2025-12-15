from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from website.models.studentModels import StudentModel
from website.models.programModels import ProgramModel
from website.models.collegeModels import CollegeModel
from website.utils.decorators import login_required
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import destroy as cloudinary_destroy
import cloudinary
import os
from datetime import datetime

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

def log_activity(action, details):
    """Log all student-related activities"""
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}: {details}\n"
    try:
        with open('logs/activity.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Logging error: {e}")

studentRoute = Blueprint('students', __name__)
student_model = StudentModel()
program_model = ProgramModel()
college_model = CollegeModel()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Restricted to PNG and JPEG only
MAX_FILE_SIZE_MB = 2  # Maximum allowed file size: 2 megabytes (2048 KB)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_public_id_from_url(cloudinary_url):
    """Extract Cloudinary public_id from URL"""
    try:
        # Extract the part after /upload/ and before the file extension
        # Example: https://res.cloudinary.com/demo/image/upload/v1234567890/sample.jpg
        # Result: v1234567890/sample
        parts = cloudinary_url.split('/upload/')
        if len(parts) > 1:
            # Get everything after /upload/ and remove file extension
            return parts[1].rsplit('.', 1)[0]
        else:
            # Fallback: just get the filename without extension
            return cloudinary_url.split('/')[-1].split('.')[0]
    except Exception as e:
        print(f"Error extracting public_id: {e}")
        # Fallback method
        return cloudinary_url.split('/')[-1].split('.')[0]

@studentRoute.route("/students", methods=["GET", "POST"])
def students():
    has_prev = False
    has_next = False

    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    if request.method == "POST":
        # Require authentication for creating students
        if 'user_id' not in session:
            flash('Please log in to add students', 'warning')
            return redirect(url_for('auth.login'))
        profile_file = request.files.get("file")

        if not profile_file:
            student_id = add_student()
            print(student_id)
        elif allowed_file(profile_file.filename):
            # Check file size before saving
            profile_file.seek(0, os.SEEK_END)  # Move to the end of the file
            file_size = profile_file.tell()  # Get the file size
            profile_file.seek(0)  # Move back to the beginning of the file

            print("length", file_size)
            if file_size > max_size_bytes:
                flash('File size exceeds the maximum allowed (5MB). Please upload a smaller file.', 'danger')
            else:
                print('prof', profile_file.filename)  # Adjusted to match FormData key
                student_id = add_student()
                print(student_id)
                upload_result = cloudinary.uploader.upload(profile_file)
                secure_url = upload_result['url']
                print(secure_url)
                student_model.update_student_profile_pic(student_id, secure_url)
        else:
            flash('Invalid file type. Please upload a valid file.', 'danger')

        # Redirect to prevent form resubmission
        return redirect(url_for('students.students'))

    search_query = request.args.get("search")

    programs = program_model.get_programs()
    students = []

    search_query = "" if search_query is None else search_query

    if search_query:
        students = student_model.search_students(search_query)
    else:
        # Fetch ALL students - let DataTables handle pagination on client side
        students = student_model.get_all_students()
    
    total_count = len(students)

    return render_template(
        "students.html",
        programs=programs,
        students=students,
        total_count=total_count,
        search_query=search_query,
    )

def add_student():
    print(f"\n{'='*80}")
    print(f"➕ CREATE STUDENT REQUEST")
    print(f"{'='*80}")
    
    try:
        # Remove ID from form - it's auto-generated now
        firstname = request.form.get("firstName")
        lastname = request.form.get("lastName")
        program_id = request.form.get("programId")
        year = request.form.get("year")
        gender = request.form.get("gender")
        
        # Handle "No Program" selection
        if program_id == "" or program_id == "null":
            program_id = None
        else:
            program_id = int(program_id) if program_id else None
        
        print(f"📊 Form data received:")
        print(f"  Name: {firstname} {lastname}")
        print(f"  Program ID: {program_id}")
        print(f"  Year: {year}")
        print(f"  Gender: {gender}")
        
        if not all([firstname, lastname, year, gender]):
            print(f"❌ ERROR: Missing required fields")
            flash('All fields are required', 'danger')
            return None
        
        print(f"\n➕ Creating student in database with auto-generated ID...")
        result = student_model.create_student(firstname, lastname, program_id, year, gender)
        print(f"📊 Create result: {result}")
        
        # Check if creation was successful
        if result.get('success'):
            student_id = result.get('student_id')
            # Log the creation
            log_activity("CREATE Student", f"ID={student_id}, Name={firstname} {lastname}, Program ID={program_id}, Year={year}, Gender={gender}")
            print(f"📝 Activity logged")
            flash(f'Student created successfully with ID: {student_id}', 'success')
            print(f"✅ SUCCESS: Student {student_id} created")
            print(f"{'='*80}\n")
            return student_id
        else:
            error_msg = result.get('message', 'Unknown error')
            flash(f'Error creating student: {error_msg}', 'danger')
            print(f"❌ ERROR: {error_msg}")
            print(f"{'='*80}\n")
            return None
        
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
        flash(f'Error creating student: {str(e)}', 'danger')
        return None


@studentRoute.route("/students/view/<string:student_id>", methods=["GET"])
@login_required
def view_student(student_id):
    # Get student with full details
    student = student_model.get_student_with_details(student_id)
    
    if not student:
        flash(f'Student with ID "{student_id}" not found', 'danger')
        return redirect(url_for('students.students'))
    
    # Get all programs for the edit modal dropdown
    programs = program_model.get_programs()
    
    # Log the view
    log_activity("VIEW Student", f"ID={student_id}, Name={student['firstname']} {student['lastname']}")
    
    return render_template('student_view.html', student=student, programs=programs)


@studentRoute.route("/students/delete/<string:student_id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_student(student_id):
    print(f"\n{'='*80}")
    print(f"🗑️  DELETE REQUEST RECEIVED")
    print(f"{'='*80}")
    print(f"📋 Student ID: {student_id}")
    print(f"📋 Request Method: {request.method}")
    print(f"📋 Request URL: {request.url}")
    print(f"📋 Referrer: {request.referrer}")
    print(f"{'='*80}\n")
    
    try:
        # Get student details before deletion for logging
        print(f"🔍 Step 1: Fetching student details...")
        student = student_model.get_student_by_id(student_id)
        
        if not student:
            print(f"❌ ERROR: Student {student_id} not found in database!")
            flash(f'Student {student_id} not found', 'danger')
            print(f"🔄 Redirecting to /students\n")
            return redirect(url_for('students.students'))
        
        student_name = f"{student.get('firstname', 'Unknown')} {student.get('lastname', 'Unknown')}"
        print(f"✅ Student found: {student_name}")
        print(f"📊 Student data: {student}")
        
        # Perform deletion
        print(f"\n🗑️  Step 2: Executing deletion...")
        result = student_model.delete_student(student_id)
        print(f"📊 Delete result: {result}")
        
        # Log the deletion with details
        if 'successfully' in result:
            log_activity("DELETE Student", f"ID={student_id}, Name={student_name}")
            print(f"✅ SUCCESS: Student deleted and activity logged")
            flash(result, 'success')
        else:
            print(f"❌ FAILED: {result}")
            flash(result, 'danger')
        
        if request.method == "DELETE" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print(f"📤 Returning JSON response")
            return jsonify({'success': result == 'Student deleted successfully', 'message': result})
        else:
            print(f"🔄 Redirecting to /students")
            print(f"{'='*80}\n")
            return redirect(url_for('students.students'))
            
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
        flash(f'Error deleting student: {str(e)}', 'danger')
        return redirect(url_for('students.students'))

@studentRoute.route("/students/edit/<string:student_id>", methods=["POST"])
@login_required
def edit_student(student_id):
    print(f"\n{'='*80}")
    print(f"✏️  EDIT STUDENT REQUEST")
    print(f"{'='*80}")
    print(f"📋 Student ID: {student_id}")
    print(f"📋 Request Method: {request.method}")
    print(f"{'='*80}\n")
    
    try:
        new_first_name = request.form.get("firstName")
        new_last_name = request.form.get("lastName")
        program_id = request.form.get("programId")
        new_year = request.form.get("year")
        new_gender = request.form.get("gender")
        
        # Handle "No Program" selection
        if program_id == "" or program_id == "null":
            program_id = None
        else:
            program_id = int(program_id) if program_id else None
        
        print(f"📊 Form data received:")
        print(f"  First Name: {new_first_name}")
        print(f"  Last Name: {new_last_name}")
        print(f"  Program ID: {program_id}")
        print(f"  Year: {new_year}")
        print(f"  Gender: {new_gender}")
        
        if not all([student_id, new_first_name, new_last_name, new_year, new_gender]):
            print(f"❌ ERROR: Missing required fields")
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Handle profile picture update
        profile_file = request.files.get("file")
        remove_profile_pic = request.form.get("removeProfilePic") == "true"
        
        # Get current profile picture URL for cleanup
        current_pic_url = student_model.get_student_profile_pic_url(student_id)
        
        if remove_profile_pic and current_pic_url:
            # User wants to remove the profile picture
            print(f"🗑️  Removing profile picture from Cloudinary...")
            try:
                public_id = get_public_id_from_url(current_pic_url)
                cloudinary_destroy(public_id)
                print(f"✅ Profile picture removed from Cloudinary")
            except Exception as e:
                print(f"⚠️  Warning: Could not delete from Cloudinary: {e}")
            
            # Remove from database
            student_model.update_student_profile_pic(student_id, None)
            print(f"✅ Profile picture removed from database")
            
        elif profile_file and allowed_file(profile_file.filename):
            # User is uploading a new profile picture
            print(f"📷 Processing new profile picture: {profile_file.filename}")
            
            # Check file size
            profile_file.seek(0, os.SEEK_END)
            file_size = profile_file.tell()
            profile_file.seek(0)
            
            max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
            
            if file_size > max_size_bytes:
                print(f"❌ File too large: {file_size} bytes")
                return jsonify({'success': False, 'message': f'File size exceeds {MAX_FILE_SIZE_MB}MB limit'})
            
            # Delete old picture from Cloudinary if exists
            if current_pic_url:
                print(f"🗑️  Deleting old profile picture from Cloudinary...")
                try:
                    public_id = get_public_id_from_url(current_pic_url)
                    cloudinary_destroy(public_id)
                    print(f"✅ Old profile picture deleted from Cloudinary")
                except Exception as e:
                    print(f"⚠️  Warning: Could not delete old picture: {e}")
            
            # Upload new picture to Cloudinary
            print(f"☁️  Uploading new profile picture to Cloudinary...")
            upload_result = cloudinary.uploader.upload(profile_file)
            new_pic_url = upload_result['url']
            print(f"✅ New profile picture uploaded: {new_pic_url}")
            
            # Update database with new URL
            student_model.update_student_profile_pic(student_id, new_pic_url)
            print(f"✅ Database updated with new profile picture URL")
        
        # Log the edit
        log_activity("EDIT Student", f"ID={student_id}, Name={new_first_name} {new_last_name}, Program ID={program_id}, Year={new_year}, Gender={new_gender}")
        print(f"📝 Activity logged")
        
        print(f"\n✏️  Updating student in database...")
        result = student_model.update_student(
            student_id, new_first_name, new_last_name, program_id, new_year, new_gender
        )
        print(f"📊 Update result: {result}")
        
        if isinstance(result, dict) and result.get('success'):
            print(f"✅ SUCCESS: Student {student_id} updated")
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
        return jsonify({'success': False, 'message': f'Error updating student: {str(e)}'})



def update_profile_pic():
    try:
        data = request.get_json()
        student_id = data.get('studentId')
        secure_url = data.get('secureUrl')

        # Check if the file size is greater than 5MB
        max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        if 'file' in request.files:
            file = request.files['file']
            if file and file.content_length and file.content_length > max_size_bytes:
                return jsonify({'error': f'File size exceeds the maximum allowed ({MAX_FILE_SIZE_MB}MB)'}), 400

        # Delete existing profile picture from Cloudinary
        existing_profile_pic_url = student_model.get_student_profile_pic_url(student_id)
        if existing_profile_pic_url:
            public_id = get_public_id_from_url(existing_profile_pic_url)
            deletion_response = cloudinary_destroy(public_id)
            print(deletion_response)

        upload_result = cloudinary.uploader.upload(file)
        secure_url = upload_result['url']
        student_model.update_student_profile_pic(student_id, secure_url)

        return jsonify({'secureUrl': secure_url, 'message': 'Profile picture updated successfully'})

    except Exception as e:
        return jsonify({'error': 'Failed to update profile picture'})

# Add this route to your Flask application
@studentRoute.route('/update_profile_pic', methods=['POST'])
def route_update_profile_pic():
    return update_profile_pic()