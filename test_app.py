"""
Simple test runner for the Flask app without database
This will help you see the basic structure of the app
"""
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '8a2b4c6d8e0f1a2b3c4d5e6f7a8b9c0d'

# Mock data for testing
mock_colleges = [
    {'code': 'CCS', 'name': 'College of Computer Studies'},
    {'code': 'COE', 'name': 'College of Engineering'},
    {'code': 'CBA', 'name': 'College of Business Administration'},
]

mock_courses = [
    {'course_code': 'BSCS', 'course_name': 'Bachelor of Science in Computer Science', 'college_code': 'CCS', 'college_name': 'College of Computer Studies'},
    {'course_code': 'BSIT', 'course_name': 'Bachelor of Science in Information Technology', 'college_code': 'CCS', 'college_name': 'College of Computer Studies'},
    {'course_code': 'BSCE', 'course_name': 'Bachelor of Science in Civil Engineering', 'college_code': 'COE', 'college_name': 'College of Engineering'},
]

mock_students = [
    {'id': '2023-12345', 'firstname': 'John', 'lastname': 'Doe', 'course_code': 'BSCS', 'course_name': 'Bachelor of Science in Computer Science', 'year': '3rd Year', 'gender': 'Male', 'profile_pic_url': None, 'college_name': 'College of Computer Studies'},
    {'id': '2023-12346', 'firstname': 'Jane', 'lastname': 'Smith', 'course_code': 'BSIT', 'course_name': 'Bachelor of Science in Information Technology', 'year': '2nd Year', 'gender': 'Female', 'profile_pic_url': None, 'college_name': 'College of Computer Studies'},
    {'id': '2023-12347', 'firstname': 'Mike', 'lastname': 'Johnson', 'course_code': 'BSCE', 'course_name': 'Bachelor of Science in Civil Engineering', 'year': '4th Year', 'gender': 'Male', 'profile_pic_url': None, 'college_name': 'College of Engineering'},
]

@app.route('/')
def home():
    return render_template('students.html', 
                         students=mock_students, 
                         courses=mock_courses, 
                         search_query='', 
                         page_number=1, 
                         page_size=8, 
                         has_prev=False, 
                         has_next=False)

@app.route('/students')
def students():
    return render_template('students.html', 
                         students=mock_students, 
                         courses=mock_courses, 
                         search_query='', 
                         page_number=1, 
                         page_size=8, 
                         has_prev=False, 
                         has_next=False)

@app.route('/courses')
def courses():
    return render_template('courses.html', courses=mock_courses, colleges=mock_colleges, search_query='')

@app.route('/colleges')
def colleges():
    return render_template('colleges.html', colleges=mock_colleges, search_query='')

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Flask app is working!',
        'students': len(mock_students),
        'courses': len(mock_courses),
        'colleges': len(mock_colleges)
    })

if __name__ == '__main__':
    print("🚀 Starting SSIS Test Server...")
    print("📋 This is a MOCK version without database")
    print("🌐 Visit: http://localhost:5000")
    print("📊 Test endpoint: http://localhost:5000/test")
    app.run(host='0.0.0.0', debug=True, port=5000)