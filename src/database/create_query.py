def create_query(type: str, table: str, **kwargs) -> str:
    match type:
        case "count":
            type = "COUNT(*)"
        case "filters":
            type = f'DISTINCT {kwargs["column"]}'
        case "geoJSON":
            type = "longitude, latitude, mcc, mnc, lac, cid"
        case "tiles":
            type = "longitude, latitude"
        case _:
            type = "*"
    
    query: str = f'SELECT {type} from public.{table}'

    filters: list = []
    filter_values: list = []

    for k, v in kwargs.items():
        if( v in [None] or k in ["column"]):
            continue
        elif ( k == "bounds"):
            if v["west"] != None:
                filters.append(f'(longitude BETWEEN {v["west"]} AND {v["east"]}) AND (latitude BETWEEN {v["south"]} AND {v["north"]})')
            continue
        else:
            filters.append( f'({" OR ".join( map(lambda x: f"{k}=%s", v) )})' )
            filter_values.extend(v)

    filter:str = ''
    if len(filters) > 0:
        filter:str = f' WHERE {" AND ".join(filters)}'
        
    #TODO: Remove limit for production
    query = query + filter #+ " LIMIT 500"
    query_fill: tuple = (query, tuple(filter_values))
    return query_fill