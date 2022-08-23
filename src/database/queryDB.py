async def queryDB(pool, query) -> any:
    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(query[0], query[1])
            return await cur.fetchall()

