# Readmore: https://gis.stackexchange.com/questions/163007/raster-reclassify-using-python-gdal-and-numpy
from osgeo import gdal
import time

# Start reclassify
start = time.time()
print("Start reclassify")

driver = gdal.GetDriverByName('GTiff')
file = gdal.Open('demo_data/20180910_ricemap_dos_clip.tif')
print('Read file: ' + file.GetDescription())


band = file.GetRasterBand(1)
lista = band.ReadAsArray()

# reclassification
for j in range(file.RasterXSize):
    for i in range(file.RasterYSize):
        if 1 <= lista[i, j] <= 10:
            lista[i, j] = 1
        else:
            lista[i, j] = 0

# create new file
file2 = driver.Create('demo_data/raster2.tif', file.RasterXSize, file.RasterYSize, 1)
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
print('Finished reclassify. Elapsed time is {} seconds'.format(round(end - start, 2)))
