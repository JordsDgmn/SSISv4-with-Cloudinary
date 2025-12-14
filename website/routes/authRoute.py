from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.models.userModels import UserModel

authRoute = Blueprint('auth', __name__)
user_model = UserModel()

@authRoute.route("/login", methods=["GET", "POST"])
def login():
    # Redirect if already logged in
    if 'user_id' in session:
        flash('You are already logged in', 'info')
        return redirect(url_for('students.students'))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            flash('Email and password are required', 'danger')
            return render_template("login.html")
        
        # Verify credentials
        result = user_model.verify_user(email, password)
        
        if result['success']:
            # Set session
            user = result['user']
            session['user_id'] = user['user_id']
            session['user_email'] = user['email']
            session['user_name'] = user['full_name']
            session.permanent = True  # Session persists after browser close
            
            flash(f"Welcome back, {user['full_name']}!", 'success')
            
            # Redirect to originally requested page or default to students
            next_page = request.args.get('next')
            return redirect(next_page or url_for('students.students'))
        else:
            flash(result['message'], 'danger')
            return render_template("login.html", email=email)
    
    return render_template("login.html")

@authRoute.route("/signup", methods=["GET", "POST"])
def signup():
    # Redirect if already logged in
    if 'user_id' in session:
        flash('You are already logged in', 'info')
        return redirect(url_for('students.students'))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        full_name = request.form.get("fullName")
        
        # Validation
        if not all([email, password, confirm_password, full_name]):
            flash('All fields are required', 'danger')
            return render_template("signup.html", email=email, full_name=full_name)
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template("signup.html", email=email, full_name=full_name)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template("signup.html", email=email, full_name=full_name)
        
        # Create user
        result = user_model.create_user(email, password, full_name)
        
        if result['success']:
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['message'], 'danger')
            return render_template("signup.html", email=email, full_name=full_name)
    
    return render_template("signup.html")

@authRoute.route("/logout")
def logout():
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f"Goodbye, {user_name}! You have been logged out.", 'info')
    return redirect(url_for('auth.login'))

@authRoute.route("/")
def index():
    """Root route - redirect based on auth status"""
    if 'user_id' in session:
        return redirect(url_for('students.students'))
    return redirect(url_for('auth.login'))
