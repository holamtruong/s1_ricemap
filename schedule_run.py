# Schedule Library imported
import schedule
import time
import logging
import rice_calc.gpt_dir as ARD
import rice_calc.modules as modules
import rice_calc.s1_download as download
import os
 
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
    return


def preprocessing():
    input_img='download_dir'#satelite imagery input directory
    output_img='output'#output ARD directory
    ARD.S1_process(input_img,output_img) #call gpt to processing file
    return


def cacl_rice_dos():
    output_img='output'
    file_list_o=[img for img in os.listdir(output_img) if img[-4:] == '.tif']
    file_list=sorted(file_list_o)
    img_info=os.path.join(output_img,file_list[0])
    old_info = modules.get_img_info(img_info)
    stack_anh=modules.tiftostack(output_img,file_list,old_info['cols'],old_info['rows'])
    rice=modules.rice_map(stack_anh)
    result_path='result'
    file_list=sorted(os.listdir(output_img))
    out_name=os.path.join(result_path,f'{file_list[-1][0:8]}_ricemap_dos.tif')
    if os.path.exists(out_name) is True:
        print ("No new Image, see you nexttime...")
    else:
        day=modules.date(file_list)
        dos=modules.calc_dos(stack_anh,rice,day)
        print('exporting rice dos map...')
        modules.array2raster(out_name, (old_info['originX'],old_info['originY']),
                             old_info['pixelWidth'], old_info['pixelHeight'],dos, 32648)
        stack_anh=None
        dos=None
        day=None
    return


def quytrinh_thanhlap_ricemap():
    logger.info('running program')
    download_img()
    logger.info('search and collect new images...')
    preprocessing()
    logger.info('processing image...')
    cacl_rice_dos()
    logger.info('calculating rice dos...')
    logger.info('..::Done::..')


# After every 1 seconds run_task() is called.
if __name__=='__main__':
    schedule.every().day.at("16:59").do(quytrinh_thanhlap_ricemap)
    print('waiting...')
    # Loop so that the scheduling task keeps on running all time.
    while True:
        # Checks whether a scheduled task is pending to run or not (1 seconds)
        schedule.run_pending()
        time.sleep(1)
