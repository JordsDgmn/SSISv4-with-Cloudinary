import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from contextlib import contextmanager

class DatabaseManager:
    @staticmethod
    def get_connection():
        """Get a database connection"""
        return psycopg2.connect(
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            database=Config.POSTGRES_DB
        )
    
    @staticmethod
    @contextmanager
    def get_cursor(dictionary=True):
        """Context manager for database cursor"""
        conn = DatabaseManager.get_connection()
        try:
            if dictionary:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            else:
                cursor = conn.cursor()
            yield cursor, conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()