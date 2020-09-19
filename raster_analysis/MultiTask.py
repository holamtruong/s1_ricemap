import json
import os
from pandas import DataFrame
from raster_analysis.reclassify import RasterReclass
from raster_analysis.clip_raster import ClipRasterFile
from raster_analysis.zonal_stats import zonal_stats
from postgres4Py import pgCRUD

# Declare raster input path
raster_inputPath = 'result_temp/20180910_ricemap_dos_clip.tif'
date = '2018-09-10'

# Declare age class of rice
age_class = [
    {"age": "1-10day", "min": 1, "max": 10},
    {"age": "11-20day", "min": 11, "max": 20},
    {"age": "21-30day", "min": 21, "max": 30},
    {"age": "31-40day", "min": 31, "max": 40},
    {"age": "41-50day", "min": 41, "max": 50},
    {"age": "51-60day", "min": 51, "max": 60},
    {"age": "61-70day", "min": 61, "max": 70},
    {"age": "71-80day", "min": 71, "max": 80},
    {"age": "81-90day", "min": 81, "max": 90},
    {"age": "91-100day", "min": 91, "max": 100},
    {"age": "101-110day", "min": 101, "max": 110},
    {"age": "111-120day", "min": 111, "max": 120},
]

# Get input filename in result_temp folder (20180910_ricemap_dos_clip.tif)
list_img = [img for img in os.listdir('../result_temp') if img[-16:] == '_ricemap_dos.tif']
last_img = list_img[-1]  # get last date raster file

# Declare input file, output folder, clip_polygon:
input_file = '../result_temp/' + last_img
output_folder = '../result_temp/'
clip_polygon = 'zonal_area/haugiang_tinh_polygon.shp'

# Run clip a raster file
ClipRasterFile(input_file, output_folder, clip_polygon)

# Get clipped filename in result_temp folder
clip_img_list = [clipimg for clipimg in os.listdir('../result_temp') if clipimg[-21:] == '_ricemap_dos_clip.tif']
last_clip_img = clip_img_list[-1]  # get last date of clipped raster file

raster_inputPath = '../result_temp/' + last_clip_img
zonal_polygon = 'zonal_area/haugiang_xa_polygon.shp'

for x_class in age_class:
    print(x_class)
    # Run raster reclassification
    rs_relass_path = RasterReclass(raster_inputPath, x_class["age"], x_class["min"], x_class["max"])
    # print(rs_relass_path)

    # Run zonal statistics
    stats_result = zonal_stats(zonal_polygon, rs_relass_path)
    print(DataFrame(stats_result))

    # send statistics result to database in server:
    for zone in stats_result:
        # Declare field list, value list
        fieldList = []
        valueList = []

        # Get date value
        fieldList.append('date')
        valueList.append(str(date))

        # Get rice_age
        fieldList.append('rice_age')
        valueList.append(str(x_class['age']))

        # Get maxa
        fieldList.append('maxa')
        valueList.append(str(zone['maxa']))

        # Get tenxa
        fieldList.append('tenxa')
        valueList.append(str(zone['tenxa']))

        # Get sum
        fieldList.append('sum')
        valueList.append(str(zone['sum']))

        # Get rice_age
        fieldList.append('area_ha')
        valueList.append(str(zone['area_ha']))

        # Run insert into table
        pgCRUD.insert_multi_column('public', 'rice_age_statistics', fieldList, valueList)

    '''
    # create and write a file (if the specified file does not exist)
    f = open('../result_temp/' + last_clip_img[0:25] + '_' + x["age"] + '.stadata', "w")
    stats_result_string = json.dumps(stats_result, indent=4)
    f.write(stats_result_string)
    f.close()
    '''
