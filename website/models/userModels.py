from website.database import DatabaseManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserModel:
    @classmethod
    def create_user(cls, email, password, full_name):
        """Create a new user with hashed password"""
        try:
            password_hash = generate_password_hash(password)
            
            with DatabaseManager.get_cursor() as (cur, conn):
                # Check if email already exists
                cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    return {"success": False, "message": f"Email '{email}' is already registered"}
                
                cur.execute(
                    """INSERT INTO users (email, password_hash, full_name) 
                       VALUES (%s, %s, %s) RETURNING user_id""",
                    (email, password_hash, full_name)
                )
                result = cur.fetchone()
                user_id = result['user_id']
                return {"success": True, "message": "User created successfully", "user_id": user_id}
        except Exception as e:
            return {"success": False, "message": f"Failed to create user: {str(e)}"}
    
    @classmethod
    def verify_user(cls, email, password):
        """Verify user credentials and return user data if valid"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "SELECT user_id, email, password_hash, full_name FROM users WHERE email = %s",
                    (email,)
                )
                user = cur.fetchone()
                
                if not user:
                    return {"success": False, "message": "Invalid email or password"}
                
                # Check password
                if check_password_hash(user['password_hash'], password):
                    # Update last login
                    cur.execute(
                        "UPDATE users SET last_login = %s WHERE user_id = %s",
                        (datetime.now(), user['user_id'])
                    )
                    
                    return {
                        "success": True,
                        "user": {
                            "user_id": user['user_id'],
                            "email": user['email'],
                            "full_name": user['full_name']
                        }
                    }
                else:
                    return {"success": False, "message": "Invalid email or password"}
        except Exception as e:
            return {"success": False, "message": f"Authentication failed: {str(e)}"}
    
    @classmethod
    def get_user_by_id(cls, user_id):
        """Get user by ID (for session management)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "SELECT user_id, email, full_name FROM users WHERE user_id = %s",
                    (user_id,)
                )
                user = cur.fetchone()
                return dict(user) if user else None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    @classmethod
    def get_all_users(cls):
        """Get all users (for admin purposes)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    """SELECT user_id, email, full_name, created_at, last_login 
                       FROM users ORDER BY created_at DESC"""
                )
                users = cur.fetchall()
                return [dict(row) for row in users]
        except Exception as e:
            return []
    
    @classmethod
    def update_password(cls, user_id, new_password):
        """Update user password"""
        try:
            password_hash = generate_password_hash(new_password)
            
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "UPDATE users SET password_hash = %s WHERE user_id = %s",
                    (password_hash, user_id)
                )
                return {"success": True, "message": "Password updated successfully"}
        except Exception as e:
            return {"success": False, "message": f"Failed to update password: {str(e)}"}
    
    @classmethod
    def delete_user(cls, user_id):
        """Delete user (admin function)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                return {"success": True, "message": "User deleted successfully"}
        except Exception as e:
            return {"success": False, "message": f"Failed to delete user: {str(e)}"}
