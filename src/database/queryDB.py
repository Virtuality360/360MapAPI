def queryDB(conn, query) -> any:
    with conn.cursor() as cur:
        cur.execute(query[0], query[1])
        return cur.fetchall()