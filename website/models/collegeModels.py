from website.database import DatabaseManager

class CollegeModel:
    @classmethod
    def create_college(cls, name, code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("INSERT INTO college (code, name) VALUES (%s, %s)", (code, name))
            return "College created successfully"
        except Exception as e:
            return f"Failed to create college: {str(e)}"

    @classmethod
    def get_colleges(cls):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("SELECT code, name FROM college ORDER BY code")
                colleges = cur.fetchall()
                return [dict(row) for row in colleges]
        except Exception as e:
            return []

    @classmethod
    def delete_college(cls, code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("DELETE FROM college WHERE code = %s", (code,))
            return "College and its courses deleted successfully"
        except Exception as e:
            return f"Failed to delete college: {str(e)}"

    @classmethod
    def update_college(cls, code, new_name):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("UPDATE college SET name = %s WHERE code = %s", (new_name, code))
            return "College updated successfully"
        except Exception as e:
            return f"Failed to update college: {str(e)}"
        
    @classmethod
    def search_colleges(cls, search_query):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "SELECT code, name FROM college WHERE name ILIKE %s OR code ILIKE %s ORDER BY code", 
                    (f'%{search_query}%', f'%{search_query}%')
                )
                colleges = cur.fetchall()
                return [dict(row) for row in colleges]
        except Exception as e:
            return []

    @classmethod
    def get_college_with_details(cls, college_code):
        """Get a single college by code"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("SELECT code, name FROM college WHERE code = %s", (college_code,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Failed to retrieve college: {str(e)}")
            return None

    @classmethod
    def get_college_programs(cls, college_code):
        """Get all programs under a specific college"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT code AS program_code, name AS program_name, college_code
                    FROM program
                    WHERE college_code = %s
                    ORDER BY code
                """, (college_code,))
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"Failed to retrieve college programs: {str(e)}")
            return []