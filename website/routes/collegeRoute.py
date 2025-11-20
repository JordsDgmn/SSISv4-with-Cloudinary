from flask import Blueprint, render_template, request, jsonify, redirect, url_for,flash

from website.models.collegeModels import CollegeModel

collegeRoute = Blueprint('college', __name__)
college_model = CollegeModel()

@collegeRoute.route("/", methods=["GET"])
def redirect_to_colleges():
    return redirect(url_for("college.colleges"))

@collegeRoute.route("/colleges", methods=["GET", "POST"])
def colleges():
    if request.method == "POST":
        name = request.form.get("collegeName")
        code = request.form.get("collegeCode")
        college_model.create_college(name, code)
        flash('College created successfully', 'success')
    search_query = request.args.get("search")
    
    if search_query is None:
        search_query = ""  # Set a default value to an empty string if search_query is None
    
    colleges = college_model.search_colleges(search_query) if search_query else college_model.get_colleges()
    
    return render_template("colleges.html", colleges=colleges, search_query=search_query)

@collegeRoute.route("/colleges/delete/<string:college_code>", methods=["DELETE"])
def delete_college(college_code):
    result = college_model.delete_college(college_code)
    return jsonify({'success': result == 'College and its courses deleted successfully'})

@collegeRoute.route("/colleges/edit/<string:college_code>", methods=["POST"])
def edit_college(college_code):
    new_name = request.form.get("collegeName")
    result = college_model.update_college(college_code, new_name)
    return jsonify({'success': result == 'College updated successfully'})
