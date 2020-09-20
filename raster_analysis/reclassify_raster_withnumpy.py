# Readmore: https://gis.stackexchange.com/questions/163007/raster-reclassify-using-python-gdal-and-numpy

from osgeo import gdal, osr
import time
import numpy as np
import os
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
# Start reclassify
start = time.time()
print("Start reclassify")

file = 'demo_data/20180910_ricemap_dos_clip.tif'
out_path='temp_export'

lista = geo_array(file)
img_info = get_img_info(file)
for i in range(1,121,10):
    reclass = np.where(np.logical_and(lista >= i, lista <= i+9), 1, 0)
    out_name = f'reclass_{i}-{i+9}.tif'
    path_out = os.path.join(out_path,out_name)
    array2raster(path_out,(img_info['originX'], img_info['originY']),
                             img_info['pixelWidth'], img_info['pixelHeight'], reclass, 32648)
    reclass=None
# Finished reclassify
end = time.time()
print('Finished reclassify. Elapsed time is {} seconds'.format(round(end - start, 2)))
