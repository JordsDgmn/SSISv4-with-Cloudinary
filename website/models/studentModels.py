from website.database import DatabaseManager

class StudentModel:
    @classmethod
    def create_student(cls, id, firstname, lastname, program_code, year, gender):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "INSERT INTO student (id, firstname, lastname, program_code, year, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, firstname, lastname, program_code, year, gender)
                )
            return "Student created successfully"
        except Exception as e:
            return f"Failed to create student: {str(e)}"

    @classmethod
    def get_students(cls, page_size: int, page_number: int):
        print(f"Page size: {page_size}, Page number: {page_number}")
        offset = (page_number - 1) * page_size
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT student.id, student.firstname, student.lastname,
                        student.program_code, student.year, student.gender,
                        student.profile_pic_url,
                        program.name AS program_name, program.code AS program_code,
                        college.name AS college_name, college.code AS college_code
                    FROM student
                    INNER JOIN program ON student.program_code = program.code
                    INNER JOIN college ON program.college_code = college.code 
                    ORDER BY student.id ASC
                    LIMIT %s OFFSET %s
                """, [page_size, offset])

                results = cur.fetchall()

                # Convert RealDictRow to regular dict
                results = [dict(row) for row in results]

                cur.execute("SELECT COUNT(*) as student_count FROM student")
                total_count = cur.fetchone()['student_count']

                has_prev = offset > 0
                has_next = (offset + page_size) < total_count

                return {
                    'results': results,
                    'total_count': total_count,
                    'has_prev': has_prev,
                    'has_next': has_next
                }
        except Exception as e:
            return f"Failed to retrieve students: {str(e)}"

    @classmethod
    def delete_student(cls, id):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("DELETE FROM student WHERE id = %s", (id,))
            return "Student deleted successfully"
        except Exception as e:
            return f"Failed to delete student: {str(e)}"

    @classmethod
    def update_student(cls, id, firstname, lastname, program_code, year, gender):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "UPDATE student SET firstname = %s, lastname = %s, program_code = %s, year = %s, gender = %s WHERE id = %s", 
                    (firstname, lastname, program_code, year, gender, id)
                )
            return "Student updated successfully"
        except Exception as e:
            return f"Failed to update student: {str(e)}"

    @classmethod
    def search_students(cls, search_query):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                query = """
                SELECT student.id, student.profile_pic_url, student.firstname, student.lastname, 
                       program.code AS program_code, program.name AS program_name, student.year, student.gender, 
                       college.code AS college_code, college.name AS college_name
                FROM student
                INNER JOIN program ON student.program_code = program.code
                INNER JOIN college ON program.college_code = college.code
                WHERE (student.id ILIKE %s
                OR student.firstname ILIKE %s
                OR student.lastname ILIKE %s
                OR program.name ILIKE %s
                OR program.code ILIKE %s
                OR college.name ILIKE %s
                OR college.code ILIKE %s
                OR student.year ILIKE %s
                OR student.gender ILIKE %s)
                """
                search_query_param = f"%{search_query}%"
                cur.execute(query, (search_query_param,) * 9)
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            return []

    @classmethod
    def update_student_profile_pic(cls, student_id, profile_pic_url):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "UPDATE student SET profile_pic_url = %s WHERE id = %s",
                    (profile_pic_url, student_id)
                )
            return "Profile picture updated successfully"
        except Exception as e:
            return f"Failed to update profile picture: {str(e)}"
        
    @classmethod
    def get_student_profile_pic_url(cls, student_id):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("SELECT profile_pic_url FROM student WHERE id = %s", (student_id,))
                result = cur.fetchone()
                return result['profile_pic_url'] if result else None
        except Exception as e:
            return None