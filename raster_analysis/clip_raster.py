# Readmore: https://www.hatarilabs.com/ih-en/clip-multiple-landsat-8-bands-with-python-and-gdal

from osgeo import gdal
import os

# Input and output paths:
inputPath = '../result/'
outputPath = 'demo_data/'
# Input shapefile:
shp_clip = 'zonal_area/haugiang_tinh_polygon.shp'

# Read all .tif file in folder
imgList = [img for img in os.listdir(inputPath) if img[-4:] == '.tif']
print(imgList)

# clip all the selected raster files with the Warp option from GDAL:
for image in imgList:
    options = gdal.WarpOptions(cutlineDSName=shp_clip, cropToCutline=False, dstNodata=-9999)
    result_img = gdal.Warp(srcDSOrSrcDSTab=inputPath + image,
                           destNameOrDestDS=outputPath + image[:-4] + '_clip' + image[-4:],
                           options=options)
    # Clear the result:
    result_img = None
    print('Finished clipping raster by polygon: ' + outputPath + image[:-4] + '_clip' + image[-4:])
