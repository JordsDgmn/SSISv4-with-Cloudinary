from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from config import Config
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

# Create the SQLAlchemy instance outside the Flask app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure Cloudinary
    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET
    )

    # Initialize the SQLAlchemy extension
    db.init_app(app)

    # Import and register blueprints here
    from website.routes.collegeRoute import collegeRoute
    app.register_blueprint(collegeRoute)

    from website.routes.programRoute import programRoute
    app.register_blueprint(programRoute)

    from website.routes.studentRoute import studentRoute
    app.register_blueprint(studentRoute)
    
    from website.routes.logsRoute import logsRoute
    app.register_blueprint(logsRoute)

    # Add home route
    @app.route('/')
    def home():
        from flask import render_template
        from website.models.studentModels import StudentModel
        from website.models.programModels import ProgramModel
        from website.models.collegeModels import CollegeModel
        
        # Get counts for home page
        students = StudentModel.get_students(page_size=999999, page_number=1)
        programs = ProgramModel.get_programs()
        colleges = CollegeModel.get_colleges()
        
        total_students = students.get('total_count', 0) if isinstance(students, dict) else len(students)
        total_programs = len(programs) if isinstance(programs, list) else 0
        total_colleges = len(colleges) if isinstance(colleges, list) else 0
        
        return render_template('home.html',
                             total_students=total_students,
                             total_programs=total_programs,
                             total_colleges=total_colleges)
    
    from flask import redirect
    
    return app
