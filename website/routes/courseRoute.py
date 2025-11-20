from flask import Blueprint, render_template, request, jsonify, flash
from website.models.courseModels import CourseModel
from website.models.collegeModels import CollegeModel

courseRoute = Blueprint('courses', __name__)
course_model = CourseModel()
college_model = CollegeModel()

@courseRoute.route("/courses", methods=["GET", "POST"])
def courses():
    if request.method == "POST":
        name = request.form.get("courseName")
        code = request.form.get("courseCode")
        college_code = request.form.get("collegeCode")
        course_model.create_course(name, code, college_code)
        flash('Courses created successfully', 'success')

    search_query = request.args.get("search", default="")  

    courses = course_model.search_courses(search_query) if search_query else course_model.get_courses()
    colleges = college_model.get_colleges()

    return render_template("courses.html", courses=courses, colleges=colleges, search_query=search_query)


@courseRoute.route("/courses/edit/<string:course_code>", methods=["POST"])
def edit_course(course_code):
    new_name = request.form.get("courseName")
    college_code = request.form.get("collegeCode")
    result = course_model.update_course(course_code, new_name, college_code)
    return jsonify({'success': result == 'Course updated successfully'})

@courseRoute.route("/courses/delete/<string:course_code>", methods=["DELETE"])
def delete_course(course_code):
    result = course_model.delete_course(course_code)
    return jsonify({'success': result == 'Course and its students deleted successfully'})
