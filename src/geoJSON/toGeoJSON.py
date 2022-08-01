def create_collection(): 
    """Returns an empty geoJSON Feature Collection"""
    geojson_feature_collection = {
      "type": "FeatureCollection",
      "features": []
    }
    return geojson_feature_collection

def create_feature(coords):
    """Return an empty geoJSON Feature"""
    feature = {
        "type": "Feature",
        "properties": {
            "mcc": coords[2],
            "mnc": coords[3],
            "lac": coords[4],
            "cid": coords[5]
        },
        "geometry": {
            "type": "Point",
            "coordinates": [*coords[:2]]
        }
    }
    return feature

def toGeoJSON(dataset):
    """
    For every datapoint in the given dataset,
    create a new geoJSON feature and populate the 
    geoJSON feature collection
    """
    collection = create_collection()
    for datapoint in dataset:
        feature = create_feature(datapoint)
        collection["features"].append(feature)
    return collection
