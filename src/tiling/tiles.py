import re
import datashader as ds
import math
import datetime
from datashader import transfer_functions as tf
from datashader.utils import lnglat_to_meters
from colorcet import bmw, coolwarm, fire, CET_L18

#from ..globals.dataframe import td


# TODO : Optimization
# Takes nearly 3 seconds to generate and serve a tile
# Do some local testing for generation to seperate the time
# it takes to create the tile to the time neeeded to serve it

# Takes less than 0.0001 seconds
def tile2mercator(xtile, ytile, zoom):
    # takes the zoom and tile path and passes back the EPSG:3857
    # coordinates of the top left of the tile.
    # From Openstreetmap
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)

    # Convert the results of the degree calulation above and convert
    # to meters for web map presentation
    mercator = lnglat_to_meters(lon_deg, lat_deg)
    return mercator


def generate_tiles(x, y, zoom, ddf, mcc, mnc, lac, cid):

    mccq = ""
    mncq = ""
    lacq = ""
    cidq = ""

    if mcc != "0":
        mccq = " & (mcc == {mcc})".format(mcc=str(mcc))
    if mnc != "0":
        mncq = " & (mnc == {mnc})".format(mnc=mnc)
    if lac != "0":
        lacq = " & (lac == {lac})".format(lac=lac)
    if cid != "0":
        cidq = " & (cid == {cid})".format(cid=cid)

    # The function takes the zoom and tile path from the web request,
    # and determines the top left and bottom right coordinates of the tile.
    # This information is used to query against the dataframe.
    xleft, yleft = tile2mercator(int(x), int(y), int(zoom)) # Northwest corner
    xright, yright = tile2mercator(int(x)+1, int(y)+1, int(zoom)) # Southeast corner

    #print(ddf.head())

    condition = f'(X >= {xleft}) & (X <= {xright}) & (Y <= {yleft}) & (Y >= {yright}){mccq}{mncq}{lacq}{cidq}'
    #print(condition)
    frame = ddf.query(condition)
    #print(ddf[ddf.mcc == "432"].head())
    #print(len(frame.index))
    # The dataframe query gets passed to Datashader to construct the graphic.
    # First the graphic is created, then the dataframe is passed to the Datashader aggregator.

    csv = ds.Canvas(plot_width=64, plot_height=64, x_range=(min(xleft, xright), max(
        xleft, xright)), y_range=(min(yleft, yright), max(yleft, yright)))
    agg = csv.points(frame, 'X', 'Y') # Takes a while

    # The image is created from the aggregate object, a color map and aggregation function.
    # Then the object is assighed to a bytestream and returned
    img = tf.shade(agg, cmap=CET_L18, how='log')
    img_io = img.to_bytesio('PNG')
    img_io.seek(0)
    bytes = img_io.read()
    return bytes