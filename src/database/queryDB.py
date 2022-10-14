SERVER_SIDE_CURSOR_LIMIT = 1000
CLIENT_SIDE_CURSOR_LIMIT = SERVER_SIDE_CURSOR_LIMIT

async def queryDB(pool, query, tries = 0) -> any:
    await pool.check() # Discards broken connections. Increases latency based on the number of connections in the pool
    async with pool.connection() as aconn:
        async with aconn.cursor("v360API-ssc") as acur: # Creates a server side cursor on the database
            acur.itersize = SERVER_SIDE_CURSOR_LIMIT
            await acur.execute(query[0], query[1])
            return await acur.fetchall()