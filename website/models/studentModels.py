from website.database import DatabaseManager
from datetime import datetime

class StudentModel:
    @classmethod
    def generate_next_student_id(cls, year=None):
        """Generate next student ID in YYYY-XXXX format using database function"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                if year is None:
                    year = datetime.now().year
                
                # Call PostgreSQL function
                cur.execute("SELECT generate_student_id(%s) as next_id", (year,))
                result = cur.fetchone()
                return result['next_id']
        except Exception as e:
            print(f"Error generating student ID: {e}")
            # Fallback: generate manually
            return cls._generate_id_fallback(year)
    
    @classmethod
    def _generate_id_fallback(cls, year=None):
        """Fallback method if database function fails"""
        if year is None:
            year = datetime.now().year
        
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT id FROM student 
                    WHERE id LIKE %s 
                    ORDER BY id DESC LIMIT 1
                """, (f"{year}-%",))
                
                result = cur.fetchone()
                if result:
                    last_id = result['id']
                    last_num = int(last_id.split('-')[1])
                    next_num = last_num + 1
                else:
                    next_num = 1
                
                return f"{year}-{next_num:04d}"
        except Exception as e:
            print(f"Error in fallback ID generation: {e}")
            return f"{year}-0001"
    
    @classmethod
    def create_student(cls, student_id, firstname, lastname, program_id, year, gender, profile_pic_url=None):
        """Create student with provided ID - uses program_id"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Check if ID already exists
                cur.execute("SELECT id FROM student WHERE id = %s", (student_id,))
                if cur.fetchone():
                    return {"success": False, "message": f"Student ID '{student_id}' already exists."}
                
                cur.execute(
                    "INSERT INTO student (id, firstname, lastname, program_id, year, gender, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (student_id, firstname, lastname, program_id, year, gender, profile_pic_url)
                )
            return {"success": True, "message": "Student created successfully", "student_id": student_id}
        except Exception as e:
            return {"success": False, "message": f"Failed to create student: {str(e)}"}

    @classmethod
    def get_all_students(cls):
        """Fetch all students without pagination - handles NULL program_id (orphans)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT s.id, s.firstname, s.lastname,
                        s.program_id, s.year, s.gender,
                        s.profile_pic,
                        p.program_id, p.code AS program_code, p.name AS program_name,
                        c.college_id, c.code AS college_code, c.name AS college_name
                    FROM student s
                    LEFT JOIN program p ON s.program_id = p.program_id
                    LEFT JOIN college c ON p.college_id = c.college_id 
                    ORDER BY s.id ASC
                """)

                results = cur.fetchall()
                # Convert RealDictRow to regular dict
                results = [dict(row) for row in results]
                return results
        except Exception as e:
            print(f"Error fetching all students: {str(e)}")
            return []

    @classmethod
    def get_students(cls, page_size: int, page_number: int):
        print(f"Page size: {page_size}, Page number: {page_number}")
        offset = (page_number - 1) * page_size
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT s.id, s.firstname, s.lastname,
                        s.program_id, s.year, s.gender,
                        s.profile_pic,
                        p.program_id, p.code AS program_code, p.name AS program_name,
                        c.college_id, c.code AS college_code, c.name AS college_name
                    FROM student s
                    LEFT JOIN program p ON s.program_id = p.program_id
                    LEFT JOIN college c ON p.college_id = c.college_id 
                    ORDER BY s.id ASC
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
    def get_student_by_id(cls, id):
        """Get a single student by ID"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT id, firstname, lastname,
                        program_id, year, gender,
                        profile_pic
                    FROM student
                    WHERE id = %s
                """, (id,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Failed to retrieve student: {str(e)}")
            return None

    @classmethod
    def delete_student(cls, id):
        print(f"\n=== DELETE_STUDENT MODEL METHOD ===")
        print(f"Attempting to delete student ID: {id}")
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Check if student exists first
                cur.execute("SELECT id FROM student WHERE id = %s", (id,))
                exists = cur.fetchone()
                
                if not exists:
                    print(f"ERROR: Student {id} does not exist in database")
                    return f"Student {id} not found"
                
                print(f"Student exists, proceeding with deletion...")
                
                # Perform the deletion
                cur.execute("DELETE FROM student WHERE id = %s", (id,))
                deleted_count = cur.rowcount
                
                print(f"Rows deleted: {deleted_count}")
                
                if deleted_count > 0:
                    print(f"SUCCESS: Student {id} deleted from database")
                    return "Student deleted successfully"
                else:
                    print(f"WARNING: No rows were deleted")
                    return "No student was deleted"
                    
        except Exception as e:
            error_msg = f"Failed to delete student: {str(e)}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg

    @classmethod
    def update_student(cls, id, firstname, lastname, program_id, year, gender):
        """Update student - uses program_id (can be NULL for orphans)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute(
                    "UPDATE student SET firstname = %s, lastname = %s, program_id = %s, year = %s, gender = %s WHERE id = %s", 
                    (firstname, lastname, program_id, year, gender, id)
                )
            return {"success": True, "message": "Student updated successfully"}
        except Exception as e:
            return {"success": False, "message": f"Failed to update student: {str(e)}"}

    @classmethod
    def search_students(cls, search_query):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                query = """
                SELECT s.id, s.profile_pic, s.firstname, s.lastname, 
                       s.program_id, s.year, s.gender,
                       p.program_id, p.code AS program_code, p.name AS program_name,
                       c.college_id, c.code AS college_code, c.name AS college_name
                FROM student s
                LEFT JOIN program p ON s.program_id = p.program_id
                LEFT JOIN college c ON p.college_id = c.college_id
                WHERE (s.id ILIKE %s
                OR s.firstname ILIKE %s
                OR s.lastname ILIKE %s
                OR p.name ILIKE %s
                OR p.code ILIKE %s
                OR c.name ILIKE %s
                OR c.code ILIKE %s
                OR s.year ILIKE %s
                OR s.gender ILIKE %s)
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
                    "UPDATE student SET profile_pic = %s WHERE id = %s",
                    (profile_pic_url, student_id)
                )
            return "Profile picture updated successfully"
        except Exception as e:
            return f"Failed to update profile picture: {str(e)}"
        
    @classmethod
    def get_student_profile_pic_url(cls, student_id):
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("SELECT profile_pic FROM student WHERE id = %s", (student_id,))
                result = cur.fetchone()
                return result['profile_pic'] if result else None
        except Exception as e:
            return None

    @classmethod
    def get_students_by_program(cls, program_id):
        """Get all students enrolled in a specific program"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT s.id, s.firstname, s.lastname,
                        s.program_id, s.year, s.gender,
                        s.profile_pic,
                        p.program_id, p.code AS program_code, p.name AS program_name,
                        c.college_id, c.code AS college_code, c.name AS college_name
                    FROM student s
                    LEFT JOIN program p ON s.program_id = p.program_id
                    LEFT JOIN college c ON p.college_id = c.college_id
                    WHERE s.program_id = %s
                    ORDER BY s.id ASC
                """, (program_id,))
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"Failed to retrieve students by program: {str(e)}")
            return []

    @classmethod
    def get_orphaned_students(cls):
        """Get students without a program (program_id IS NULL)"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT id, firstname, lastname, year, gender, profile_pic
                    FROM student 
                    WHERE program_id IS NULL
                    ORDER BY id
                """)
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            return []

    @classmethod
    def get_students_by_college(cls, college_id):
        """Get all students in programs under a specific college"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT s.id, s.firstname, s.lastname,
                        s.program_id, s.year, s.gender,
                        s.profile_pic,
                        p.program_id, p.code AS program_code, p.name AS program_name,
                        c.college_id, c.code AS college_code, c.name AS college_name
                    FROM student s
                    INNER JOIN program p ON s.program_id = p.program_id
                    INNER JOIN college c ON p.college_id = c.college_id
                    WHERE c.college_id = %s
                    ORDER BY p.code ASC, s.id ASC
                """, (college_id,))
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"Failed to retrieve students by college: {str(e)}")
            return []

    @classmethod
    def get_student_with_details(cls, student_id):
        """Get a single student with full program and college details - handles NULL program_id"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                cur.execute("""
                    SELECT s.id, s.firstname, s.lastname,
                        s.program_id, s.year, s.gender,
                        s.profile_pic,
                        p.program_id, p.code AS program_code, p.name AS program_name,
                        c.college_id, c.code AS college_code, c.name AS college_name
                    FROM student s
                    LEFT JOIN program p ON s.program_id = p.program_id
                    LEFT JOIN college c ON p.college_id = c.college_id
                    WHERE s.id = %s
                """, (student_id,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Failed to retrieve student with details: {str(e)}")
            return None