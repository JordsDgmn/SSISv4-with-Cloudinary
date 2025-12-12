from website.database import DatabaseManager

class ProgramModel:
    @classmethod
    def create_program(cls, name, code, college_id):
        """Create a new program - uses college_id instead of code"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Check for duplicate code
                cur.execute("SELECT program_id FROM program WHERE code = %s", (code,))
                if cur.fetchone():
                    return {"success": False, "message": f"Program code '{code}' already exists"}
                
                cur.execute(
                    "INSERT INTO program (code, name, college_id) VALUES (%s, %s, %s) RETURNING program_id", 
                    (code, name, college_id)
                )
                program_id = cur.fetchone()[0]
                return {"success": True, "message": "Program created successfully", "program_id": program_id}
        except Exception as e:
            return {"success": False, "message": f"Failed to create program: {str(e)}"}
    
    @classmethod
    def get_programs(cls):
        """Get all programs with college info - handles NULL college_id (orphans)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT 
                        p.program_id, 
                        p.code, 
                        p.name, 
                        p.college_id,
                        c.code AS college_code, 
                        c.name AS college_name 
                    FROM program p
                    LEFT JOIN college c ON p.college_id = c.college_id 
                    ORDER BY p.code
                """)
                programs = cur.fetchall()
                return [dict(row) for row in programs]
        except Exception as e:
            return []

    @classmethod
    def update_program(cls, program_id, new_code, new_name, college_id):
        """Update program by ID - code is now editable, college_id can be NULL"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Get current program
                cur.execute("SELECT code FROM program WHERE program_id = %s", (program_id,))
                current = cur.fetchone()
                if not current:
                    return {"success": False, "message": "Program not found"}
                
                # If code changed, check for duplicates
                if new_code != current['code']:
                    cur.execute("SELECT program_id FROM program WHERE code = %s AND program_id != %s", (new_code, program_id))
                    if cur.fetchone():
                        return {"success": False, "message": f"Program code '{new_code}' already exists"}
                
                cur.execute(
                    "UPDATE program SET code = %s, name = %s, college_id = %s WHERE program_id = %s", 
                    (new_code, new_name, college_id, program_id)
                )
                return {"success": True, "message": "Program updated successfully"}
        except Exception as e:
            return {"success": False, "message": f"Failed to update program: {str(e)}"}

    @classmethod
    def delete_program(cls, program_id):
        """Delete program by ID - students will have program_id set to NULL"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Get program details before deletion
                cur.execute("SELECT code, name FROM program WHERE program_id = %s", (program_id,))
                program = cur.fetchone()
                if not program:
                    return {"success": False, "message": "Program not found"}
                
                # Delete (students will have program_id set to NULL automatically)
                cur.execute("DELETE FROM program WHERE program_id = %s", (program_id,))
                return {"success": True, "message": f"Program '{program['code']}' deleted. Students are now unassigned."}
        except Exception as e:
            return {"success": False, "message": f"Failed to delete program: {str(e)}"}

    @classmethod
    def search_programs(cls, search_query):
        """Search programs by code or name - handles NULL college_id"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                query = """
                SELECT 
                    p.program_id, 
                    p.code, 
                    p.name, 
                    p.college_id,
                    c.code AS college_code, 
                    c.name AS college_name
                FROM program p
                LEFT JOIN college c ON p.college_id = c.college_id
                WHERE p.name ILIKE %s OR p.code ILIKE %s
                OR c.name ILIKE %s OR c.code ILIKE %s
                ORDER BY p.code
                """
                search_param = f"%{search_query}%"
                cur.execute(query, (search_param, search_param, search_param, search_param))
                programs = cur.fetchall()
                return [dict(row) for row in programs]
        except Exception as e:
            return []

    @classmethod
    def get_program_by_id(cls, program_id):
        """Get a single program by ID with college details"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT 
                        p.program_id, 
                        p.code, 
                        p.name,
                        p.college_id,
                        c.code AS college_code, 
                        c.name AS college_name
                    FROM program p
                    LEFT JOIN college c ON p.college_id = c.college_id
                    WHERE p.program_id = %s
                """, (program_id,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Failed to retrieve program: {str(e)}")
            return None

    @classmethod
    def get_program_with_details(cls, program_id):
        """Get a single program with college details"""
        return cls.get_program_by_id(program_id)

    @classmethod
    def get_orphaned_programs(cls):
        """Get programs without a college (college_id IS NULL)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT program_id, code, name 
                    FROM program 
                    WHERE college_id IS NULL
                    ORDER BY code
                """)
                programs = cur.fetchall()
                return [dict(row) for row in programs]
        except Exception as e:
            return []
