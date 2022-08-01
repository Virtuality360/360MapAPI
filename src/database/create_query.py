# TODO
# Might be wonky when viewing the prime meridian
def create_query(**kwargs):
    '''
    Generate a SQL query string
    north, south, east, and west are all required
    they are used to bound the results
    mcc, mnc, lac, and cid are optional
    they must be passed in an array
    '''
    COLS = "longitude, latitude, mcc, mnc, lac, cid"
    BASE = f"SELECT DISTINCT {COLS} FROM public.gsm_qp "
    WHERE = "WHERE "
    LOCATION = f"(latitude BETWEEN {kwargs['south']} AND {kwargs['north']}) AND (longitude BETWEEN {kwargs['west']} AND {kwargs['east']}) "
    filter = ""
    for key in kwargs.keys():
        # Skip the coordinates
        if key in ['north', 'south', 'east', 'west']:
            continue
        for val in key:
            # go from array of values to array of equations
            # [1,2,3] ==> ['mcc=1','mcc=2','mcc=3']
            # then join the values with an OR
            formated = list(map(lambda x: f"{key}={x}",val))
            formated = " OR ".join(formated)

            filter = f"{filter}AND {formated} "

    LIMIT = "LIMIT 500"
    QUERY = BASE + WHERE + LOCATION + filter + LIMIT
    print(QUERY)
    return QUERY
