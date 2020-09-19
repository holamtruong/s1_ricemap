# Readmore: https://gis.stackexchange.com/questions/163007/raster-reclassify-using-python-gdal-and-numpy

from osgeo import gdal
import time
from pathlib import Path


def RasterReclass(raster_inputPath, age_value, min_value, max_value):
    # Start reclassify
    start = time.time()
    driver = gdal.GetDriverByName('GTiff')
    file = gdal.Open(raster_inputPath)  # '20180910_ricemap_dos_clip.tif'
    file_name = Path(file.GetDescription()).stem  # 20180910_ricemap_dos_clip
    band = file.GetRasterBand(1)
    lista = band.ReadAsArray()
    print('Start reclassify: ' + file.GetDescription())

    # reclassification
    for j in range(file.RasterXSize):
        for i in range(file.RasterYSize):
            if min_value <= lista[i, j] <= max_value:
                lista[i, j] = 1
            else:
                lista[i, j] = 0

    # create new file
    result_temp = '../result_temp/' + file_name + '_' + age_value + '_relass.tif'
    file2 = driver.Create(result_temp, file.RasterXSize, file.RasterYSize, 1)
    file2.GetRasterBand(1).WriteArray(lista)
    lista = None

    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()

    # Finished reclassify
    end = time.time()
    print('Finished reclassify : ' + result_temp + '. Elapsed time is {} seconds'.format(round(end - start, 2)))

    return result_temp

# Run reclassification (raster_inputPath ,min_threshold, max_threshold)
# RasterReclass('20180910_ricemap_dos_clip.tif', 1, 10)
