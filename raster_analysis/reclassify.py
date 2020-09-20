# Readmore: https://gis.stackexchange.com/questions/163007/raster-reclassify-using-python-gdal-and-numpy
from pathlib import Path
from osgeo import gdal, osr
import numpy as np

'''
************* Basic raster reclassify  *************
'''
def RasterReclass_basic(raster_inputPath, age_value, min_value, max_value):
    driver = gdal.GetDriverByName('GTiff')
    file = gdal.Open(raster_inputPath)  # '20180910_ricemap_dos_clip.tif'
    file_name = Path(file.GetDescription()).stem  # 20180910_ricemap_dos_clip
    band = file.GetRasterBand(1)
    lista = band.ReadAsArray()

    # reclassification
    print('Start reclassify: ' + file.GetDescription())
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

    print("Finish reclassification.")
    return result_temp





'''
************* Basic raster reclassify with NumPy *************
'''

# read array as raster
def geo_array(img):
    driver = gdal.GetDriverByName('GTiff')
    raster = gdal.Open(img)
    band = raster.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    array = np.nan_to_num(array)
    raster = None
    return array

# get geo info
def get_img_info(img):
    img = gdal.Open(img)
    cols = img.RasterXSize
    rows = img.RasterYSize
    bands = img.RasterCount
    geotransform = img.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    prj = img.GetProjection()
    kq = {'cols': cols,
          'rows': rows,
          'bands': bands,
          'geotransform': geotransform,
          'originX': originX,
          'originY': originY,
          'pixelWidth': pixelWidth,
          'pixelHeight': pixelHeight,
          'projection': prj}
    return kq


# export array to raster img
def array2raster(newRasterFilename,
                 rasterOrigin,
                 pixelWidth,
                 pixelHeight,
                 array,
                 sridcode):
    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterFilename, cols, rows, 1, gdal.GDT_Int16)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.SetStatistics(float(np.nanmin(array)), float(np.nanmax(array)), float(np.nanmean(array)),
                          float(np.nanstd(array)))
    outband.WriteArray(array)
    outband.SetNoDataValue(np.nan)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(sridcode)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


# raster reclassify using NumPy
def RasterReclass(raster_inputPath, age_value, min_value, max_value):
    print('Start reclassify: ' + raster_inputPath)
    # Get info of raster
    file = gdal.Open(raster_inputPath)  # '20180910_ricemap_dos_clip.tif'
    file_name = Path(file.GetDescription()).stem  # 20180910_ricemap_dos_clip
    raster_ESPG = int(osr.SpatialReference(wkt=file.GetProjection()).GetAttrValue('AUTHORITY', 1))  # 32648

    lista = geo_array(raster_inputPath)
    img_info = get_img_info(raster_inputPath)
    reclass = np.where(np.logical_and(lista >= min_value, lista <= max_value), 1, 0)


    # create new file
    result_temp = '../result_temp/' + file_name + '_' + age_value + '_relass.tif'

    array2raster(result_temp, (img_info['originX'], img_info['originY']),
                 img_info['pixelWidth'], img_info['pixelHeight'], reclass, raster_ESPG)
    lista = None

    print('Finished reclassify. Saved in temporary file: ' + result_temp)
    return result_temp



