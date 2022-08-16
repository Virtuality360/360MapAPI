from src.utils.progressBar import progressBar

def create_collection() -> dict: 
    """Returns an empty geoJSON Feature Collection"""
    geojson_feature_collection: dict = {
      "type": "FeatureCollection",
      "features": []
    }
    return geojson_feature_collection

def create_feature(coords) -> dict:
    """Return an empty geoJSON Feature"""
    feature: dict = {
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

def toGeoJSON(dataset) -> dict:
    """
    For every datapoint in the given dataset,
    create a new geoJSON feature and populate the 
    geoJSON feature collection
    """
    collection: dict = create_collection()
    # Loads the iterator into a progress bar
    for datapoint in progressBar(dataset, prefix = 'Progress:', suffix = 'Complete', length = 50):
        feature: dict = create_feature(datapoint)
        collection["features"].append(feature)
    return collection
