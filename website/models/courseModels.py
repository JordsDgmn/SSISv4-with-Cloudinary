from website.database import DatabaseManager

class CourseModel:
    @classmethod
    def create_course(cls, name, code, college_code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("INSERT INTO course (code, name, college_code) VALUES (%s, %s, %s)", (code, name, college_code))
            return "Course created successfully"
        except Exception as e:
            return f"Failed to create course: {str(e)}"
    
    @classmethod
    def get_courses(cls):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT course.code AS course_code, course.name AS course_name, 
                           college.code AS college_code, college.name AS college_name 
                    FROM course 
                    INNER JOIN college ON course.college_code = college.code 
                    ORDER BY course.code
                """)
                courses = cur.fetchall()
                return [dict(row) for row in courses]
        except Exception as e:
            return []

    @classmethod
    def update_course(cls, code, new_name, college_code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("UPDATE course SET name = %s, college_code = %s WHERE code = %s", (new_name, college_code, code))
            return "Course updated successfully"
        except Exception as e:
            return f"Failed to update course: {str(e)}"

    @classmethod
    def delete_course(cls, code):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("DELETE FROM course WHERE code = %s", (code,))
            return "Course and its students deleted successfully"
        except Exception as e:
            return f"Failed to delete course: {str(e)}"

    @classmethod
    def search_courses(cls, search_query):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                query = """
                SELECT course.code AS course_code, course.name AS course_name, 
                       college.code AS college_code, college.name AS college_name
                FROM course
                INNER JOIN college ON course.college_code = college.code
                WHERE course.name ILIKE %s OR course.code ILIKE %s
                OR college.name ILIKE %s OR college.code ILIKE %s
                ORDER BY course.code
                """
                search_param = f"%{search_query}%"
                cur.execute(query, (search_param, search_param, search_param, search_param))
                courses = cur.fetchall()
                return [dict(row) for row in courses]
        except Exception as e:
            return []