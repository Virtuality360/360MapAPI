# TODO
# Might be wonky when viewing the prime meridian
def create_query(**kwargs):
    base = "SELECT DISTINCT longitude, latitude FROM public.gsm_qp "
    WHERE = "WHERE "
    location = f"(latitude BETWEEN {kwargs['south']} AND {kwargs['north']}) AND (longitude BETWEEN {kwargs['west']} AND {kwargs['east']})"
    LIMIT = "LIMIT 5"
    query = base + WHERE + location + LIMIT
    print(query)
    return query
