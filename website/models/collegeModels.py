from website.database import DatabaseManager

class CollegeModel:
    @classmethod
    def create_college(cls, name, code):
        """Create a new college - returns college_id"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Check for duplicate code
                cur.execute("SELECT college_id FROM college WHERE code = %s", (code,))
                if cur.fetchone():
                    return {"success": False, "message": f"College code '{code}' already exists"}
                
                cur.execute(
                    "INSERT INTO college (code, name) VALUES (%s, %s) RETURNING college_id",
                    (code, name)
                )
                result = cur.fetchone()
                college_id = result['college_id']  # Access dict by key, not index!
                return {"success": True, "message": "College created successfully", "college_id": college_id}
        except Exception as e:
            return {"success": False, "message": f"Failed to create college: {str(e)}"}

    @classmethod
    def get_colleges(cls):
        """Get all colleges with college_id"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("SELECT college_id, code, name FROM college ORDER BY code")
                colleges = cur.fetchall()
                return [dict(row) for row in colleges]
        except Exception as e:
            return []

    @classmethod
    def delete_college(cls, college_id):
        """Delete college by ID - programs will have college_id set to NULL"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Get college details before deletion
                cur.execute("SELECT code, name FROM college WHERE college_id = %s", (college_id,))
                college = cur.fetchone()
                if not college:
                    return {"success": False, "message": "College not found"}
                
                # Delete (programs will have college_id set to NULL automatically)
                cur.execute("DELETE FROM college WHERE college_id = %s", (college_id,))
                return {"success": True, "message": f"College '{college['code']}' deleted. Programs are now unassigned."}
        except Exception as e:
            return {"success": False, "message": f"Failed to delete college: {str(e)}"}

    @classmethod
    def update_college(cls, college_id, new_code, new_name):
        """Update college by ID - code is now editable!"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Get current college
                cur.execute("SELECT code FROM college WHERE college_id = %s", (college_id,))
                current = cur.fetchone()
                if not current:
                    return {"success": False, "message": "College not found"}
                
                # If code changed, check for duplicates
                if new_code != current['code']:
                    cur.execute("SELECT college_id FROM college WHERE code = %s AND college_id != %s", (new_code, college_id))
                    if cur.fetchone():
                        return {"success": False, "message": f"College code '{new_code}' already exists"}
                
                cur.execute(
                    "UPDATE college SET code = %s, name = %s WHERE college_id = %s", 
                    (new_code, new_name, college_id)
                )
                return {"success": True, "message": "College updated successfully"}
        except Exception as e:
            return {"success": False, "message": f"Failed to update college: {str(e)}"}
        
    @classmethod
    def search_colleges(cls, search_query):
        """Search colleges by code or name"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "SELECT college_id, code, name FROM college WHERE name ILIKE %s OR code ILIKE %s ORDER BY code", 
                    (f'%{search_query}%', f'%{search_query}%')
                )
                colleges = cur.fetchall()
                return [dict(row) for row in colleges]
        except Exception as e:
            return []

    @classmethod
    def get_college_by_id(cls, college_id):
        """Get a single college by ID"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("SELECT college_id, code, name FROM college WHERE college_id = %s", (college_id,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Failed to retrieve college: {str(e)}")
            return None

    @classmethod
    def get_college_with_details(cls, college_id):
        """Get a single college by ID with details"""
        return cls.get_college_by_id(college_id)

    @classmethod
    def get_college_programs(cls, college_id):
        """Get all programs under a specific college"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT program_id, code, name, college_id
                    FROM program
                    WHERE college_id = %s
                    ORDER BY code
                """, (college_id,))
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"Failed to retrieve college programs: {str(e)}")
            return []
