import psycopg
from src.database.connection import establish_connection

async def queryDB(pool, query) -> any:
    try:
        async with pool.connection() as aconn:
            async with aconn.cursor() as cur:
                await cur.execute(query[0], query[1])
                return await cur.fetchall()
    except Exception as e:
        print("Error: ", e)
        try:
            pool = establish_connection()
        except psycopg.OperationalError:
            print("ERROR: Could not connect to the database server")
    finally:
        async with pool.connection() as aconn:
            async with aconn.cursor() as cur:
                await cur.execute(query[0], query[1])
                return await cur.fetchall()

