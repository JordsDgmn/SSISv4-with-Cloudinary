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

    from website.routes.courseRoute import courseRoute
    app.register_blueprint(courseRoute)

    from website.routes.studentRoute import studentRoute
    app.register_blueprint(studentRoute)

    # Add home route
    @app.route('/')
    def home():
        return redirect('/students')
    
    from flask import redirect
    
    return app
