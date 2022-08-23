import psycopg
from psycopg_pool import AsyncConnectionPool

from dotenv import load_dotenv

load_dotenv()

def establish_connection():
    """Return the connection to the server"""
    return AsyncConnectionPool()