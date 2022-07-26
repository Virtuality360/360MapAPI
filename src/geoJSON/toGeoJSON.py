def create_collection(): 
    geojson_feature_collection = {
      "type": "FeatureCollection",
      "features": []
    }
    return geojson_feature_collection

def create_feature(coords):
    feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Point",
            "coordinates": [*coords]
        }
    }
    return feature

def toGeoJSON(dataset):
    collection = create_collection()
    for datapoint in dataset:
        feature = create_feature(datapoint)
        collection["features"].append(feature)
    return collection
