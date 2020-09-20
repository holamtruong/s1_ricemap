# Readmore: https://www.hatarilabs.com/ih-en/clip-multiple-landsat-8-bands-with-python-and-gdal
from osgeo import gdal
import os
from pathlib import Path


# Clip all raster file in a folder, and export to a folder
def ClipRasterFolder(input_folder, output_folder, feature_clip_shp):
    # Input and output paths:
    inputDir = input_folder
    outputDir = output_folder
    # Input shapefile:
    shp_clip = feature_clip_shp

    # Read all .tif file in folder
    imgList = [img for img in os.listdir(inputDir) if img[-4:] == '.tif']
    print(imgList)

    # clip all the selected raster files with the Warp option from GDAL:
    for image in imgList:
        options = gdal.WarpOptions(cutlineDSName=shp_clip, cropToCutline=False, dstNodata=-9999)
        result_img = gdal.Warp(srcDSOrSrcDSTab=inputDir + image,
                               destNameOrDestDS=outputDir + image[:-4] + '_clip' + image[-4:],
                               options=options)
        # Clear the result:
        result_img = None
        print('Finished clipping raster by polygon: ' + outputDir + image[:-4] + '_clip' + image[-4:])


# Clip a raster file, and export to a folder
def ClipRasterFile(input_file, output_folder, feature_clip_path):
    # Input and output paths:
    inputFilePath = input_file
    outputDir = output_folder
    # Input shapefile:
    shp_clip = feature_clip_path

    # get raster filename and extension
    raster_filename = Path(inputFilePath).stem  # 20180910_ricemap_dos_clip
    raster_ext = Path(inputFilePath).suffix  # .tif

    # Warp by Gdal
    options = gdal.WarpOptions(cutlineDSName=shp_clip, cropToCutline=False, dstNodata=-9999)
    result_img = gdal.Warp(srcDSOrSrcDSTab=inputFilePath,
                           destNameOrDestDS=outputDir + raster_filename + '_clip' + raster_ext,
                           options=options)
    # Clear the result:
    result_img = None

    # return result
    result_path = outputDir + raster_filename + '_clip' + raster_ext
    print('Finish clipping raster by polygon, saved in: ' + result_path)
    return result_path


'''
shp = 'zonal_area/haugiang_tinh_polygon.shp'
input = '../result/'
output = 'temp_data/'
ClipRasterFolder(input, output, shp)
'''


'''
input = '../result/20180910_ricemap_dos.tif'
output = 'temp_data/'
shp = 'zonal_area/haugiang_tinh_polygon.shp'
ClipRasterFile(input, output, shp)
'''


