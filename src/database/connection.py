from psycopg_pool import AsyncConnectionPool

from dotenv import load_dotenv

load_dotenv()

async def establish_connection():
    """Return the connection to the server"""
    pool = AsyncConnectionPool()
    await pool.wait()
    return pool