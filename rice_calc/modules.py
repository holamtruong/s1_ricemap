import os
import numpy as np
import gdal,  osr
import array as arr
def geo_array(img):
    raster=gdal.Open(img)
    band = raster.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    array=np.nan_to_num(array)
    raster=None
    return array
def rice_map(array):
    min_array=array.min(axis=0)
    max_array=array.max(axis=0)
    mean_array=array.mean(axis=0)
    median_array=np.median(array,axis=0)
    count = (array < -20).sum(axis=0)
    increase=np.subtract(max_array,min_array)
    boundary=np.where(np.logical_and(min_array==0,max_array==0),1,0)
    water=np.where(mean_array < -20,2,0)
    urban=np.where(np.logical_and(median_array > -10,median_array!=0),1,0)
    rice=np.where(np.logical_and(increase>6,min_array<-19,
                                 np.logical_and(max_array>-16,max_array<-8,np.logical_and(median_array <= -15,
                                                np.logical_and(median_array >= -20,count<=5, count>=2)))),3,0)
    rmap=np.where(water>0,water,np.where(urban>0,urban,np.where(rice>0,rice,np.where(boundary>0,0,4))))
    return rmap
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
    prj=img.GetProjection()
    kq = {'cols':cols,
        'rows':rows,
        'bands':bands,
        'geotransform':geotransform,
        'originX':originX,
        'originY':originY,
        'pixelWidth':pixelWidth,
        'pixelHeight':pixelHeight,
        'projection':prj}
    return kq
def tiftostack(file_path,file_list,cols,rows):
    bb=len(file_list)
    stack_band=np.zeros(shape=(bb,rows,cols),dtype=float)
    for i in range(0,bb):
        file_name = os.path.join(file_path,file_list[i])
        array=geo_array(file_name)
        #arr_filter=lee_filter(array,3)
        arr2dB=linear2dB(array)
        stack_band[i,:,:]=arr2dB
    return stack_band
def linear2dB(array):
    array_dB=np.where(array>0,10*np.log10(array),0)
    array_dB2=np.where(array_dB>-50,array_dB,0) 
    return array_dB2
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
    outband.SetStatistics(float(np.nanmin(array)),float(np.nanmax(array)),float(np.nanmean(array)),float(np.nanstd(array)))
    outband.WriteArray(array)
    outband.SetNoDataValue(np.nan)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(sridcode)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()