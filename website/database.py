import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from contextlib import contextmanager
import os

class DatabaseManager:
    @staticmethod
    def get_connection():
        """Get a database connection"""
        try:
            return psycopg2.connect(
                host=Config.POSTGRES_HOST,
                port=Config.POSTGRES_PORT,
                user=Config.POSTGRES_USER,
                password=Config.POSTGRES_PASSWORD,
                database=Config.POSTGRES_DB
            )
        except psycopg2.OperationalError as e:
            # If database doesn't exist, try to connect to default 'postgres' database
            if "database" in str(e) and "does not exist" in str(e):
                return psycopg2.connect(
                    host=Config.POSTGRES_HOST,
                    port=Config.POSTGRES_PORT,
                    user=Config.POSTGRES_USER,
                    password=Config.POSTGRES_PASSWORD,
                    database='postgres'
                )
            raise e
    
    @staticmethod
    @contextmanager
    def get_cursor(dictionary=True):
        """Context manager for database cursor"""
        conn = None
        cursor = None
        try:
            conn = DatabaseManager.get_connection()
            if dictionary:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            else:
                cursor = conn.cursor()
            yield cursor, conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()