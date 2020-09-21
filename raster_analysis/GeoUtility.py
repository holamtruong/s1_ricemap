from osgeo import ogr

# Export WKT information
def export2wkt(path2shp):
    # shape = ogr.Open("../config/study_area/tile.shp")
    shape = ogr.Open(path2shp)
    layer = shape.GetLayer()
    feature = layer.GetNextFeature()
    geom = feature.GetGeometryRef()
    wkt = geom.ExportToWkt()
    # print(wkt)
    return wkt
    # return POLYGON ((-99.90467936217...))

# Export bbox
def get_bounding_box(path2shp):
    shape = ogr.Open(path2shp)
    layer = shape.GetLayer()
    feature = layer.GetNextFeature()
    geom = feature.GetGeometryRef()
    wkt = geom.ExportToWkt()
    poly = ogr.CreateGeometryFromWkt(wkt)
    # GetEnvelope to get bbox
    bbox = poly.GetEnvelope()
    # print(bbox)
    return bbox
    # return (-114.317157696392, -75.0103986030767, 23.2462726889969, 51.6981476867451)


