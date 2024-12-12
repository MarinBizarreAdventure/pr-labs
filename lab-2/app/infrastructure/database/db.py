from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pymysql
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pymysql.install_as_MySQLdb()

class DB:
    def __init__(self):
        self.DB_USER = "admin"
        self.DB_PASSWORD = "admin"
        self.DB_HOST = "localhost"  
        self.DB_PORT = "3306"
        self.DB_NAME = "mariadb"
        
        self.SQLALCHEMY_DATABASE_URL = (
            f"mysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
        try:
            self.engine = create_engine(
                self.SQLALCHEMY_DATABASE_URL,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600,
                connect_args={
                    'charset': 'utf8mb4',
                    'connect_timeout': 60,
                }
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            self.Base = declarative_base()
            
            self.test_connection()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise




    def test_connection(self) -> bool:
        """
        Test the database connection by executing a simple query.
        Returns True if successful, raises an exception if connection fails.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database connection test failed: {str(e)}")
            raise ConnectionError(f"Could not connect to database: {str(e)}")

    def check_connection_status(self) -> dict:
        """
        Check the current status of the database connection pool.
        Returns a dictionary with connection pool statistics.
        """
        try:
            return {
                "pool_size": self.engine.pool.size(),
                "checked_out_connections": self.engine.pool.checkedin(),
                "overflow_connections": self.engine.pool.overflow(),
                "database_url": f"mysql://{self.DB_USER}:****@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
                "status": "connected" if self.test_connection() else "disconnected"
            }
        except Exception as e:
            logger.error(f"Error checking connection status: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }


    def create_tables(self):
        """
        Explicitly creates tables by executing raw SQL queries.
        """
        create_users_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            INDEX (id),
            INDEX (email),
            INDEX (username)
        );
        """

        with self.engine.begin() as conn:
            conn.execute(text(create_users_table_sql))
            conn.commit() 
            logger.info("Users table created successfully!")
    
    def get_db(self):
        """
        Get a database session from the connection pool.
        Yields a session and ensures it's closed after use.
        """
        db = self.SessionLocal()
        try:
            yield db
        except SQLAlchemyError as e:
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            db.close()

    def close(self):
        """
        Properly close the database connection pool.
        """
        try:
            self.engine.dispose()
            logger.info("Database connection pool closed")
        except Exception as e:
            logger.error(f"Error closing database connection pool: {str(e)}")
            raise