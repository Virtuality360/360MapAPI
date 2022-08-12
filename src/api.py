from cmath import isnan, nan
from enum import unique
import sys
from os.path import exists
from urllib import response
import numpy as np
from datashader.utils import lnglat_to_meters
from fastapi import FastAPI, Response, Request, Query
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import dask.dataframe as dd
from .database.connection import establish_connection
from .database.create_query import create_query
from .database.queryDB import queryDB

from .geoJSON.toGeoJSON import toGeoJSON

from .tiling.tiles import generate_tiles

api = FastAPI()

# TODO
# Formalize allowed resource requests
# Don't push to production with wildcard
origins = [
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
def startup_event():
    """On the startup of the api, instantiate the connection with the database."""
    global conn
    conn = establish_connection()

@api.get("/")
def root():
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
    bounds = {"north":north,"south":south, "east":east, "west": west}
    query: str = create_query("count", table, mcc=mcc, mnc=mnc, lac=lac, cid=cid, bounds=bounds )
    result = queryDB(conn, query)

    return {"result": result,
            "query": query}

@api.get("/filters/{table}")
async def get_filters(table: str,
                        mcc: List[str] = Query(None), mnc: List[str] = Query(None), 
                        lac: List[str] = Query(None), cid: List[str] = Query(None)) -> dict:
    """
    Return the unique values in each column.
    Removes any null or empty values.
    TODO: filter based on already set values
    """
    result: dict = {}
    for col in ["mcc", "mnc", "lac", "cid"]:
        query = create_query("filters", table, column=col)
        result[col] = [item for sublist in queryDB(conn, query) for item in sublist if item not in [None, ""] ]
        result[col].sort()

    return {"result": result}

@api.get("/get-geoJSON/{table}")
async def get_geoJSON(table:str, north: float = Query(None), south: float = Query(None),
                    east: float = Query(None), west: float = Query(None),
                    mcc: List[str] = Query(None), mnc: List[str] = Query(None), 
                    lac: List[str] = Query(None), cid: List[str] = Query(None)) -> dict:
    """
    Returns a geojson file describing various points
    TODO: filter based on already set values
    """
    bounds = {"north":north,"south":south, "east":east, "west": west}
    query:str = create_query("geoJSON", table, mcc=mcc, mnc=mnc, lac=lac, cid=cid, bounds=bounds)
    response = queryDB(conn,query)
    geoJSON = toGeoJSON(response)
    return {"query": query,
            "response": geoJSON}

@api.get("/tiles/{table}/{zoom}/{x}/{y}")
async def response_tiles(x, y, zoom, mcc=0, mnc=0, lac=0, cid=0):
    """
    Rasterize datapoints into a slippy map.
    TODO: filter based on already set values
    """
    results = generate_tiles(x, y, zoom)
    return Response(content=results, media_type="image/png")