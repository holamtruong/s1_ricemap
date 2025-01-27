import os
import datetime
import numpy as np
import gdal, osr
import argparse


def arg_parsing():
    parser = argparse.ArgumentParser(description='Detected rice area')
    parser.add_argument('-i', "--input", required=True,
                        help='Input directory')
    parser.add_argument('-o', "--output", required=True,
                        help='Output tif file')
    args = parser.parse_args()
    args = vars(args)
    args['input'] = os.path.abspath(args['input'])
    args['output'] = os.path.abspath(args['output'])
    return args


# read array as raster
def geo_array(img):
    raster = gdal.Open(img)
    band = raster.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    array = np.nan_to_num(array)
    raster = None
    return array


# calculating rice or non-rice area
def rice_map(array):
    min_array = array.min(axis=0)
    max_array = array.max(axis=0)
    mean_array = array.mean(axis=0)
    median_array = np.median(array, axis=0)
    count = (array < -20).sum(axis=0)
    increase = np.subtract(max_array, min_array)
    boundary = np.where(np.logical_and(min_array == 0, max_array == 0), 1, 0)
    water = np.where(mean_array < -22, 2, 0)  # np.logical_and(mean_array < -22,count>=10),2,0)
    urban = np.where(np.logical_and(median_array > -10, median_array != 0), 1, 0)
    rice = np.where(np.logical_and(increase > 6, min_array < -19,
                                   np.logical_and(max_array > -16, max_array < -8, np.logical_and(median_array <= -15,
                                                                                                  np.logical_and(
                                                                                                      median_array >= -22,
                                                                                                      count <= 9,
                                                                                                      count >= 2)))), 3,
                    0)
    rmap = np.where(water > 0, water,
                    np.where(urban > 0, urban, np.where(rice > 0, rice, np.where(boundary > 0, 0, 4))))
    return rmap


# get image geo-info
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


# create 3D array
def tiftostack(file_path, file_list, cols, rows):
    bb = len(file_list)
    stack_band = np.zeros(shape=(bb, rows, cols), dtype=float)
    for i in range(0, bb):
        file_name = os.path.join(file_path, file_list[i])
        array = geo_array(file_name)
        # arr_filter=lee_filter(array,3)
        arr2dB = linear2dB(array)
        stack_band[i, :, :] = arr2dB
    return stack_band


# convert linear value to decibel value
def linear2dB(array):
    array_dB = np.where(array > 0, 10 * np.log10(array), 0)
    array_dB2 = np.where(array_dB > -50, array_dB, 0)
    return array_dB2


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


# calculating rice age
def calc_dos(stack_anh, rice, day):
    size = stack_anh.shape
    tam = np.zeros(size[0], dtype=float)
    nss = np.where(rice == 0, -104, np.where(np.logical_or(rice == 1, rice == 4), -103, np.where(rice == 2, -102, 0)))
    d_end = 0
    for i in range(0, size[2]):
        for j in range(0, size[1]):
            if nss[j, i] == 0:
                if rice[j, i] == 3:
                    for k in range(0, size[0]):
                        tam[k] = stack_anh[k, j, i]

                    for k in range(0, len(tam) - 1):
                        if tam[k] - tam[k + 1] > 5:
                            # global d_end
                            d_end = k
                            for k in range(0, d_end + 1):
                                tam[k] = 0
                    minpos = np.argmin(tam)
                    vitri = minpos
                    if vitri < len(tam) - 1:
                        for k in range(vitri + 1, len(tam) - 1):
                            if abs(tam[k] - tam[vitri]) < 2:
                                vitri = k
                    else:
                        nss[j, i] = -99
                    if tam[vitri - 1] - tam[vitri] < 5:
                        d_start = vitri - 1
                    else:
                        d_start = vitri
                    if int((day[len(day) - 1] - day[vitri]).days) <= 120:
                        nss[j, i] = int((day[len(day) - 1] - day[d_start]).days)
                    else:
                        nss[j, i] = -99
            else:
                nss[j, i] == nss[j, i]
    return nss


# extract day of image from file name
def date(file_list):
    day = np.array([])
    for k in range(0, len(file_list)):
        date = datetime.datetime(int(file_list[k][0:4]), int(file_list[k][4:6]), int(file_list[k][6:8]))
        day = np.append(day, date)
    return day


# convert array of date to string
def strday(date_array):
    day = np.array([])
    for i in range(0, len(date_array)):
        date = date_array[i].strftime('%Y%m%d')
        day = np.append(day, date)
    return day


# lay gia tri gan nhat de chon ra ngay bat dau
def find_nearest(array, value):
    array = np.asarray(array)
    int_arr = np.array([])
    for i in range(0, len(array)):
        int_arr = np.append(int_arr, int(array[i]))
    idx = (np.abs(int_arr - value)).argmin()
    return array[idx]
