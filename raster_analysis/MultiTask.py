import shutil
import os
import time
from pandas import DataFrame
from raster_analysis.reclassify import RasterReclass
from raster_analysis.clip_raster import ClipRasterFile
from raster_analysis.zonal_stats import zonal_stats
from postgres4Py import pgCRUD

# Start reclassify
start = time.time()

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

# Get input filename in result_temp folder
list_RasterName = [img for img in os.listdir('../result_temp') if img[-16:] == '_ricemap_dos.tif']
last_RasterName = list_RasterName[-1]  # get the last date (20180910_ricemap_dos_clip.tif)

# Get date of raster:
year_string = last_RasterName[0:4]
month_string = last_RasterName[4:6]
day_string = last_RasterName[6:8]
date = year_string + '-' + month_string + '-' + day_string  # 2018-09-10

'''
**************** Run clip a raster file (declare input file, output folder, clip_polygon) **************** 
'''
# Declare parameter
input_file = '../result_temp/' + last_RasterName
output_folder = '../result_temp/'
clip_polygon = 'zonal_area/haugiang_tinh_polygon.shp'
# Execute clip raster by polygon
raster_clip_path = ClipRasterFile(input_file, output_folder, clip_polygon)

# Copy result to publish folder (use for geoserver)
src_file = raster_clip_path
dst_folder = '../result_publish/'
shutil.copy(src_file, dst_folder)

'''
****************  Run zonal zonal statistics and send data to database **************** 
'''
# Declare parameter
raster_inputPath = raster_clip_path
zonal_polygon = 'zonal_area/haugiang_xa_polygon.shp'

# Each 'rice age' class do a zonal statistics
for x_class in age_class:
    print(x_class)
    # Run raster reclassification
    raster_relass_path = RasterReclass(raster_inputPath, x_class["age"], x_class["min"], x_class["max"])
    # print(raster_relass_path)

    # Run zonal statistics
    stats_result = zonal_stats(zonal_polygon, raster_relass_path)
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

        print("Finish insert into table in database.")

'''
****************  Clear all temporary files in 'result_temp' folder **************** 
'''
# Declare path to 'result_temp' folder
temp_folder = '../result_temp/'
for filename in os.listdir(temp_folder):
    file_path = os.path.join(temp_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
            print('Clear all temporary files.')
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print('Clear all temporary files.')
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Print successful information
end = time.time()
print('Finished raster analysis.')
print('Elapsed time is {} seconds'.format(round(end - start, 2)))
