import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'b12_app')
DB_SSL = os.environ.get('DB_SSL', 'false').lower() in ('true', '1', 't', 'yes')

def get_connection():
    """
    Establish and return a MySQL database connection.
    Supports both mysql.connector and PyMySQL fallback.
    """
    try:
        import mysql.connector
        config = {
            'host': DB_HOST,
            'port': DB_PORT,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'database': DB_NAME,
        }
        if DB_SSL:
            import certifi
            config['ssl_ca'] = certifi.where()
            config['ssl_disabled'] = False
        return mysql.connector.connect(**config)
    except Exception as e1:
        try:
            import pymysql
            import certifi
            ssl_dict = {'ssl': {'ca': certifi.where(), 'ssl_verify_cert': True, 'ssl_verify_identity': True}} if DB_SSL else {}
            return pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=True,
                **ssl_dict
            )
        except Exception as e2:
            raise RuntimeError(f"Failed to connect to MySQL database via mysql-connector ({e1}) and PyMySQL ({e2})")
