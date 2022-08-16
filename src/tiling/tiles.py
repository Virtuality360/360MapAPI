import datashader as ds
import pandas as pd
import math

from colorcet import bmw, coolwarm, fire, CET_L18
from datashader import transfer_functions as tf
from datashader.utils import lnglat_to_meters

from src.database.create_query import create_query
from src.database.queryDB import queryDB

def degree2num(lat_degree, long_degree, zoom):
    """
    Takes a coordinate and return what tile it belongs to.
    https://wiki.openstreetmap.org/wiki/Tiles
    """
    lat_radians = math.radians(lat_degree)
    n = 2 ** zoom
    xtile = int((long_degree + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_radians)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2degree(xtile, ytile, zoom):
    """
    Returns the NW-corner of the square.
    Use the function with xtile+1 and/or ytile+1 to get the other corners.
    With xtile+0.5 & ytile+0.5 it will return the center of the tile
    https://wiki.openstreetmap.org/wiki/Tiles
    """
    n = 2.0 ** zoom
    long_degree = xtile / n * 360.0 - 180.0
    lat_radians = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_degree = math.degrees(lat_radians)
    return (lat_degree, long_degree)

def generate_tile(table, x, y, zoom, conn, mcc, mnc, lac, cid):
    """
    Generate a slippy map tile
    """
    # Get the northwest and southeast corners of the tile
    north, west = num2degree(int(x), int(y), int(zoom))
    south, east = num2degree(int(x)+1, int(y)+1, int(zoom))

    # Query the database for all points within the tile
    bounds = {"north":north,"south":south, "east":east, "west": west}
    query = create_query("tiles", table,  mcc=mcc, mnc=mnc, lac=lac, cid=cid, bounds=bounds)
    response = queryDB(conn,query)

    # Put the database response into a pandas dataframe
    # Convert the projection to web-mercator
    df = pd.DataFrame(response, columns=["longitude", "latitude"])
    df["longitude"], df["latitude"] = lnglat_to_meters(df.longitude, df.latitude)

    # Create a 256x256 canvas
    west, north = lnglat_to_meters(west, north)
    east, south = lnglat_to_meters(east, south)
    csv = ds.Canvas(plot_width=256, plot_height=256, x_range=(min(west, east), max(west, east)),
                    y_range=(min(north, south), max(north, south)))

    # If there are no points in the tile return 
    # Else create an aggregate of all the points
    if(df.size == 0):
        return          # Might want to change to returning an empty png instead of null
    agg = csv.points(df, 'longitude', 'latitude')

    # Create the rasterization from the aggregate, color it, and determine how it is displayed
    img = tf.shade(agg, cmap=CET_L18, how='log')
    # Write the image to a byte stream to return
    img_io = img.to_bytesio('PNG')
    img_io.seek(0)
    bytes = img_io.read()
    return bytes