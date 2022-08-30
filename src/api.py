#TODO Error handling

import psycopg

from fastapi import FastAPI, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.database.create_query import create_query
from src.database.connection import establish_connection
from src.database.queryDB import queryDB
from src.geoJSON.toGeoJSON import toGeoJSON
from src.tiling.tiles import generate_tile

api: FastAPI = FastAPI()

# TODO
# Formalize allowed resource requests
# Don't push to production with wildcard
origins: List = [
    "*"
]

# TODO
# Formalize allowed methods
# Don't push to production with wildcards
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@api.on_event("startup")
async def startup_event():
    """On the startup of the api, instantiate the connection with the database."""
    global pool
    try:
        pool = await establish_connection()
    except psycopg.OperationalError:
        print("ERROR: Could not connect to the database server")

@api.get("/")
def root() -> dict:
    """Provide a page to inform the user about the documentation."""
    return {"message": "Hello World",
            "docs": "Visit ./docs or ./redoc to view automatically generated documentation."
            }

@api.get("/count/{table}/")
async def get_count(table: str, north: float = Query(None), south: float = Query(None),
                    east: float = Query(None), west: float = Query(None),
                    mcc: List[str] = Query(None), mnc: List[str] = Query(None), 
                    lac: List[str] = Query(None), cid: List[str] = Query(None)) -> dict:
    """Return the number of points that match the query for the given table."""
    bounds: dict = {"north":north,"south":south, "east":east, "west": west}
    query: str = create_query("count", table, mcc=mcc, mnc=mnc, lac=lac, cid=cid, bounds=bounds )
    result = await queryDB(pool, query)

    return {"result": result[0][0],
            "query": query}

@api.get("/filters/{table}")
async def get_filters(table: str,
                        mcc: List[str] = Query(None), mnc: List[str] = Query(None), 
                        lac: List[str] = Query(None), cid: List[str] = Query(None)) -> dict:
    """
    Return the unique values in each column.
    Removes any null or empty values.
    """
    result: dict = {}
    for col in ["mcc", "mnc", "lac", "cid"]:
        query = create_query("filters", table, mcc=mcc, mnc=mnc, lac=lac, cid=cid, column=col)
        result[col] = [item for sublist in await queryDB(pool, query) for item in sublist if item not in [None, ""] ]
        result[col].sort()

    return {"result": result}

@api.get("/get-geoJSON/{table}")
async def get_geoJSON(table:str, north: float = Query(None), south: float = Query(None),
                    east: float = Query(None), west: float = Query(None),
                    mcc: List[str] = Query(None), mnc: List[str] = Query(None), 
                    lac: List[str] = Query(None), cid: List[str] = Query(None)) -> dict:
    """
    Returns a geojson file describing various points
    """
    bounds: dict = {"north":north,"south":south, "east":east, "west": west}
    query:str = create_query("geoJSON", table, mcc=mcc, mnc=mnc, lac=lac, cid=cid, bounds=bounds)
    response: any = await queryDB(pool,query)
    geoJSON: dict = toGeoJSON(response)
    return {"query": query,
            "response": geoJSON}

@api.get("/tiles/{table}/{zoom}/{x}/{y}.png")
async def response_tiles(table, zoom, x, y,
                        mcc: List[str] = Query(None), mnc: List[str] = Query(None), 
                        lac: List[str] = Query(None), cid: List[str] = Query(None)) -> dict:
    """
    Rasterize datapoints into a slippy map.
    TODO: filter based on already set values
    """
    results: any = await generate_tile(table, x, y, zoom, pool, mcc, mnc, lac, cid)
    return Response(content=results, media_type="image/png")