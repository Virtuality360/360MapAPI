import psycopg
from dotenv import load_dotenv

load_dotenv()

def establish_connection():
    conn = psycopg.connect('')
    return conn