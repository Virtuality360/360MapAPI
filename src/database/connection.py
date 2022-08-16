import psycopg2

from dotenv import load_dotenv

load_dotenv()

def establish_connection():
    """Return the connection to the server"""
    conn = psycopg2.connect()
    return conn