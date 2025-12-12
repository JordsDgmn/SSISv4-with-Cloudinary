from flask import Blueprint, render_template, request, jsonify, flash
from website.models.programModels import ProgramModel
from website.models.collegeModels import CollegeModel

courseRoute = Blueprint('courses', __name__)
program_model = ProgramModel()
college_model = CollegeModel()

@courseRoute.route("/courses", methods=["GET", "POST"])
def courses():
    if request.method == "POST":
        name = request.form.get("courseName")
        code = request.form.get("courseCode")
        college_id = request.form.get("collegeId")
        
        # Handle "No College" selection (NULL)
        if college_id == "" or college_id == "null":
            college_id = None
        else:
            college_id = int(college_id) if college_id else None
        
        result = program_model.create_program(name, code, college_id)
        
        if isinstance(result, dict) and result.get('success'):
            flash('Program created successfully', 'success')
        else:
            message = result.get('message', str(result)) if isinstance(result, dict) else str(result)
            flash(f'Error creating program: {message}', 'danger')

    search_query = request.args.get("search", default="")  

    courses = program_model.search_programs(search_query) if search_query else program_model.get_programs()
    colleges = college_model.get_colleges()
    
    # Add orphaned programs for filter
    orphaned_programs = program_model.get_orphaned_programs()

    return render_template("courses.html", courses=courses, colleges=colleges, search_query=search_query, orphaned_programs=orphaned_programs)


@courseRoute.route("/courses/edit/<int:program_id>", methods=["POST"])
def edit_course(program_id):
    new_code = request.form.get("courseCode")
    new_name = request.form.get("courseName")
    college_id = request.form.get("collegeId")
    
    # Handle "No College" selection
    if college_id == "" or college_id == "null":
        college_id = None
    else:
        college_id = int(college_id) if college_id else None
    
    result = program_model.update_program(program_id, new_code, new_name, college_id)
    
    if isinstance(result, dict):
        return jsonify(result)
    else:
        return jsonify({'success': False, 'message': str(result)})

@courseRoute.route("/courses/delete/<int:program_id>", methods=["DELETE"])
def delete_course(program_id):
    result = program_model.delete_program(program_id)
    
    if isinstance(result, dict):
        return jsonify(result)
    else:
        return jsonify({'success': False, 'message': str(result)})
