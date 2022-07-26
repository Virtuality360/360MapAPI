def queryDB(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()