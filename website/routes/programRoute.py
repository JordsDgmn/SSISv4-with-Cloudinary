from flask import Blueprint, render_template, request, jsonify, flash
from website.models.programModels import ProgramModel
from website.models.collegeModels import CollegeModel

programRoute = Blueprint('programs', __name__)
program_model = ProgramModel()
college_model = CollegeModel()

@programRoute.route("/programs", methods=["GET", "POST"])
def programs():
    if request.method == "POST":
        name = request.form.get("programName")
        code = request.form.get("programCode")
        college_code = request.form.get("collegeCode")
        program_model.create_program(name, code, college_code)
        flash('Program created successfully', 'success')

    search_query = request.args.get("search", default="")  

    programs = program_model.search_programs(search_query) if search_query else program_model.get_programs()
    colleges = college_model.get_colleges()

    return render_template("programs.html", programs=programs, colleges=colleges, search_query=search_query)


@programRoute.route("/programs/edit/<string:program_code>", methods=["POST"])
def edit_program(program_code):
    new_name = request.form.get("programName")
    college_code = request.form.get("collegeCode")
    result = program_model.update_program(program_code, new_name, college_code)
    return jsonify({'success': result == 'Program updated successfully'})

@programRoute.route("/programs/delete/<string:program_code>", methods=["DELETE"])
def delete_program(program_code):
    result = program_model.delete_program(program_code)
    return jsonify({'success': result == 'Program and its students deleted successfully'})
