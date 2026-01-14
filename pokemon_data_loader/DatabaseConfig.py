import psycopg2

from utils.models import Config


class DatabaseConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConfig, cls).__new__(cls)

            # I only need one connection to the database
            try:
                cls._instance.conn = psycopg2.connect(
                    host=Config.database.host,
                    database=Config.database.name,
                    user=Config.database.user,
                    password=Config.database.password
                )
                cls._instance.cursor = cls._instance.conn.cursor()
                print("Database connection established.")
            except psycopg2.Error as e:
                print(f"Error connecting to PostgreSQL: {e}")
                cls._instance = None  
                raise
        return cls._instance

    def close(self):
        """Clean up resources when the tool finishes."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        DatabaseConfig._instance = None

        