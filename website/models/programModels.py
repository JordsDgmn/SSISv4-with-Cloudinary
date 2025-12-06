from website.database import DatabaseManager

class ProgramModel:
    @classmethod
    def create_program(cls, name, code, college_code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("INSERT INTO program (code, name, college_code) VALUES (%s, %s, %s)", (code, name, college_code))
            return "Program created successfully"
        except Exception as e:
            return f"Failed to create program: {str(e)}"
    
    @classmethod
    def get_programs(cls):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT program.code AS program_code, program.name AS program_name, 
                           college.code AS college_code, college.name AS college_name 
                    FROM program 
                    INNER JOIN college ON program.college_code = college.code 
                    ORDER BY program.code
                """)
                programs = cur.fetchall()
                return [dict(row) for row in programs]
        except Exception as e:
            return []

    @classmethod
    def update_program(cls, code, new_name, college_code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("UPDATE program SET name = %s, college_code = %s WHERE code = %s", (new_name, college_code, code))
            return "Program updated successfully"
        except Exception as e:
            return f"Failed to update program: {str(e)}"

    @classmethod
    def delete_program(cls, code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("DELETE FROM program WHERE code = %s", (code,))
            return "Program and its students deleted successfully"
        except Exception as e:
            return f"Failed to delete program: {str(e)}"

    @classmethod
    def search_programs(cls, search_query):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                query = """
                SELECT program.code AS program_code, program.name AS program_name, 
                       college.code AS college_code, college.name AS college_name
                FROM program
                INNER JOIN college ON program.college_code = college.code
                WHERE program.name ILIKE %s OR program.code ILIKE %s
                OR college.name ILIKE %s OR college.code ILIKE %s
                ORDER BY program.code
                """
                search_param = f"%{search_query}%"
                cur.execute(query, (search_param, search_param, search_param, search_param))
                programs = cur.fetchall()
                return [dict(row) for row in programs]
        except Exception as e:
            return []
