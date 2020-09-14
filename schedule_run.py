# Schedule Library imported
import schedule
import time
import logging
import rice_calc.gpt_dir as ARD
import rice_calc.modules as modules
import rice_calc.s1_download as download
import os
import numpy as np
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('task.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


# Functions setup
def download_img():
    download.s1_dwl()
    return 1


def preprocessing():
    input_img = 'download_dir'  # satelite imagery input directory
    output_img = 'output'  # output ARD directory
    ARD.S1_process(input_img, output_img)  # call gpt to processing file
    return 1


def cacl_rice_dos():
    output_img='output'
    file_list_o=[img for img in os.listdir(output_img) if img[-4:] == '.tif']
    file_list=sorted(file_list_o)
    img_info=os.path.join(output_img,file_list[-1])
    old_info = modules.get_img_info(img_info)
    choose_list=np.array([])
    listday=modules.date(file_list)
    list_str_day=modules.strday(listday)
    start_day=listday[-1]-datetime.timedelta(days=140)
    start_str_day=start_day.strftime('%Y%m%d')
    day_start=modules.find_nearest(list_str_day, int(start_str_day))
    index=np.where(list_str_day==day_start)
    for i in range(int(index[0]),len(list_str_day)):
        choose_list=np.append(choose_list,file_list[i])
    stack_anh=modules.tiftostack(output_img,choose_list,old_info['cols'],old_info['rows'])
    rice=modules.rice_map(stack_anh)
    result_path='result'
    file_list=sorted(os.listdir(output_img))
    out_name=os.path.join(result_path,f'{file_list[-1][0:8]}_ricemap_dos.tif')
    if os.path.exists(out_name) is True:
        print("No new Image, see you nexttime...")
        return 1
    else:
        day = modules.date(file_list)
        dos = modules.calc_dos(stack_anh, rice, day)
        print('exporting rice dos map...')
        modules.array2raster(out_name, (old_info['originX'], old_info['originY']),
                             old_info['pixelWidth'], old_info['pixelHeight'], dos, 32648)
        stack_anh = None
        dos = None
        day = None
        return 1


def quytrinh_thanhlap_ricemap():
    logger.info('running program')
    logger.info('search and collect new images...')
    check=download_img()
    if check==1:
        logger.info('search and collect new images successful')
    else:
        logger.info('collect image false')
    logger.info('processing image...')
    check=preprocessing()
    if check==1:
        logger.info('processing image successful')
    else:
        logger.info('processing image false')
    logger.info('calculating rice dos...')
    check=cacl_rice_dos()
    if check==1:
        logger.info('calculating rice dos successful')
    else:
        logger.info('calculating rice dos false')
    logger.info('..::Done::..')
    print('waiting...')


# After every 1 seconds run_task() is called.
def main(): 
    start_time = "15:12"
    schedule.every().day.at(start_time).do(quytrinh_thanhlap_ricemap)


if __name__=='__main__':
    main()

