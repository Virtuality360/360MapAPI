from urllib import response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.connection import establish_connection
from .database.create_query import create_query
from .database.queryDB import queryDB

from .geoJSON.toGeoJSON import toGeoJSON

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

conn = establish_connection()

@api.get("/")
def root():
    return {"message": "Hello World",
        "docs": "Visit ./docs or redoc to view automatically generated documentation."
        }

# Latitude is North/South, Longitude is West/East
@api.get("/get_features/{north}/{south}/{east}/{west}")
async def get_features(north: float, south: float, east: float, west: float,
                        mcc:int=0,mnc:int=0,lac:int=0, cid:int=0):
    
    query = create_query(north=north, south=south, east=east, west=west)
    response = queryDB(conn,query)

    geoJSON = toGeoJSON(response)

    return {"response": geoJSON}

@api.get("get_features/{geohash}")
async def get_features(geohash: str):
    return {"message": "Not implemented yet"}
