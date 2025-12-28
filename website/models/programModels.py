from website.database import DatabaseManager

class ProgramModel:
    @classmethod
    def create_program(cls, name, code, college_id):
        """Create a new program - uses college_id instead of code"""
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                print(f"🔍 Checking for duplicate code: {code}")
                # Check for duplicate code
                cur.execute("SELECT program_id FROM program WHERE code = %s", (code,))
                if cur.fetchone():
                    print(f"❌ Duplicate code found!")
                    return {"success": False, "message": f"Program code '{code}' already exists"}
                
                print(f"✅ No duplicate, inserting program...")
                print(f"   Parameters: code={code}, name={name}, college_id={college_id}")
                cur.execute(
                    "INSERT INTO program (code, name, college_id) VALUES (%s, %s, %s) RETURNING program_id", 
                    (code, name, college_id)
                )
                result = cur.fetchone()
                print(f"📊 Database returned: {result}")
                
                if result:
                    program_id = result['program_id']  # Access dict by key, not index!
                    print(f"✅ Program created with ID: {program_id}")
                    return {"success": True, "message": "Program created successfully", "program_id": program_id}
                else:
                    print(f"❌ No result returned from INSERT")
                    return {"success": False, "message": "Failed to create program: No ID returned"}
        except Exception as e:
            print(f"❌ EXCEPTION in create_program:")
            print(f"   Type: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            import traceback
            traceback.print_exc()
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
        """Search programs by code or name"""
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
                    WHERE p.name ILIKE %s OR p.code ILIKE %s OR c.name ILIKE %s OR c.code ILIKE %s
                    ORDER BY p.code
                """, tuple([f'%{search_query}%'] * 4))
                programs = cur.fetchall()
                return [dict(row) for row in programs]
        except Exception as e:
            return []
    
    @classmethod
    def get_programs_server_side(cls, start, length, search_value, order_column, order_dir, column_filters=None):
        """Server-side pagination for DataTables with column filters
        JS columns: 0=code, 1=name, 2=college, 3=actions(no)
        """
        if column_filters is None:
            column_filters = {}
        warnings = []
        try:
            with DatabaseManager.get_cursor() as (cur, conn):
                # Map JS column indices to SQL
                columns_map = {0: 'p.code', 1: 'p.name', 2: 'c.name'}
                order_col = columns_map.get(order_column, 'p.code')
                print(f"[DEBUG] Programs: col {order_column} -> {order_col} {order_dir}")
                print(f"[DEBUG] Initial column_filters: {column_filters}")

                base_query = "FROM program p LEFT JOIN college c ON p.college_id = c.college_id"
                
                where_clauses = []
                search_params = []

                # Global search
                search_value = str(search_value or '').strip()
                if search_value:
                    where_clauses.append("(p.code ILIKE %s OR p.name ILIKE %s OR c.code ILIKE %s OR c.name ILIKE %s)")
                    pattern = f'%{search_value}%'
                    search_params.extend([pattern, pattern, pattern, pattern])
                    print(f"[DEBUG] Global search enabled: {search_value}")

                # Column filters
                if column_filters.get('code'):
                    where_clauses.append("p.code ILIKE %s")
                    search_params.append(f"%{column_filters.get('code')}%")
                    print(f"[DEBUG] Program code filter: {column_filters.get('code')}")
                if column_filters.get('name'):
                    where_clauses.append("p.name ILIKE %s")
                    search_params.append(f"%{column_filters.get('name')}%")
                    print(f"[DEBUG] Program name filter: {column_filters.get('name')}")
                if column_filters.get('college'):
                    col_val = column_filters.get('college')
                    try:
                        col_id = int(col_val)
                        # verify
                        cur.execute("SELECT 1 FROM college WHERE college_id = %s", (col_id,))
                        if not cur.fetchone():
                            warnings.append(f"College id {col_id} not found")
                            print(f"[WARN] College id {col_id} not found")
                        where_clauses.append("p.college_id = %s")
                        search_params.append(col_id)
                        print(f"[DEBUG] College filter by id: {col_id}")
                    except Exception:
                        where_clauses.append("(c.code ILIKE %s OR c.name ILIKE %s)")
                        search_params.extend([f"%{col_val}%", f"%{col_val}%"])
                        print(f"[DEBUG] College filter by text: {col_val}")

                where_clause = ""
                if where_clauses:
                    where_clause = "WHERE " + " AND ".join(where_clauses)
                    print(f"[DEBUG] Combined WHERE clause: {where_clause}")

                # Total count
                cur.execute(f"SELECT COUNT(*) as total {base_query}")
                total_records = cur.fetchone()['total']

                # Filtered count
                count_query = f"SELECT COUNT(*) as total {base_query} {where_clause}"
                if search_params:
                    cur.execute(count_query, tuple(search_params))
                    filtered_records = cur.fetchone()['total']
                else:
                    filtered_records = total_records

                # Get data
                query = f"""SELECT p.program_id, p.code, p.name, p.college_id,
                        c.code AS college_code, c.name AS college_name
                    {base_query} {where_clause}
                    ORDER BY {order_col} {order_dir} LIMIT %s OFFSET %s"""

                params = list(search_params) + [length, start]
                print(f"[DEBUG] Executing data query with params: {params}")
                print(f"[DEBUG] Query: {query[:200]}...")
                cur.execute(query, tuple(params))
                results = cur.fetchall()
                data = [dict(row) for row in results]

                debug = {'where_clause': where_clause, 'count_query': count_query, 'count_params': search_params, 'data_query': query, 'data_params': params}

                result = {'data': data, 'recordsTotal': total_records, 'recordsFiltered': filtered_records, 'debug': debug}
                if warnings:
                    result['warnings'] = warnings
                print(f"[DEBUG] Programs returned {len(data)} rows; filtered={filtered_records}; warnings={warnings}")

                return result
        except Exception as e:
            print(f"Error in get_programs_server_side: {e}")
            import traceback
            traceback.print_exc()
            return {'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

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
