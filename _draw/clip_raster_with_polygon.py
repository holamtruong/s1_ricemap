from osgeo import gdal
import os

# Input and output paths:
inputPath = 'sample_data/list_img/'
outputPath = 'sample_data/result/'

# Read all .tif file in folder
imgList = [img for img in os.listdir(inputPath) if img[-4:] == '.tif']
print(imgList)
# ['bentre_man_s1_20191119.tif', 'bentre_man_s1_20191124.tif',...]

# Input shapefile:
shp_clip = 'sample_data/shp/bentre_town.shp'

# clip all the selected raster files with the Warp option from GDAL:
for image in imgList:
    options = gdal.WarpOptions(cutlineDSName=shp_clip, cropToCutline=True)  
    result_img = gdal.Warp(srcDSOrSrcDSTab=inputPath + image,
                           destNameOrDestDS=outputPath + image[:-4] + '_clip' + image[-4:],
                           options=options)
    # Clear the result:
    result_img = None
    print('Done: ' + outputPath + image[:-4] + '_clip' + image[-4:])
