import rice_calc.modules as modules
import os
import numpy as np
import datetime

def cacl_rice_dos(list_str_day, day_input, file_list,result_path):
    '''
        output_img = 'ard_store'
        file_list_o = [img for img in os.listdir(output_img) if img[-4:] == '.tif']
        file_list = sorted(file_list_o)
        img_info = os.path.join(output_img, file_list[-1])
        old_info = modules.get_img_info(img_info)
        choose_list = np.array([])
        listday = modules.date(file_list)
        list_str_day = modules.strday(listday)
    '''
    output_img = 'ard_store'
    day_in_date = datetime.datetime(int(day_input[0:4]), int(day_input[4:6]), int(day_input[6:8]))
    start_day = day_in_date - datetime.timedelta(days=140)
    start_str_day = start_day.strftime('%Y%m%d')
    day_start = modules.find_nearest(list_str_day, int(start_str_day))
    day_end = day_input
    index_1 = np.where(list_str_day == day_start)
    index_2 = np.where(list_str_day == day_end)
    choose_list = np.array([])
    img_info = os.path.join(output_img, file_list[-1])
    old_info = modules.get_img_info(img_info)
    for i in range(int(index_1[0]), int(index_2[0])+1):
        choose_list = np.append(choose_list, file_list[i])
    stack_anh = modules.tiftostack(output_img, choose_list, old_info['cols'], old_info['rows'])
    rice = modules.rice_map(stack_anh)
    rs_name = f'{choose_list[-1][0:8]}_ricemap_dos.tif'
    out_name = os.path.join(result_path, rs_name)
    day = modules.date(choose_list)
    dos = modules.calc_dos(stack_anh, rice, day)
    print('exporting rice dos map...')
    modules.array2raster(out_name, (old_info['originX'], old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'], dos, 32648)
    stack_anh = None
    dos = None
    day = None
    return 'ok', str(day_start), day_end


def main():
    print('Input day your want to calc rice age with syntax: YYYYMMDD')
    day_in=input('Input here: ')
    while (len(day_in) != 8 or day_in[0:4] != '2020' or int(day_in[4:6])==0 or int(day_in[4:6]) > 12 or int(day_in[6:8]) > 31):
        print('Please type correct the day you want!!!')
        day_in=input('Input here: ')
    ard_path = 'ard_store'
    result_path = 'result'
    #result_list_o = [img for img in os.listdir(result_path) if img[-4:] == '.tif']
    file_list_o = [img for img in os.listdir(ard_path) if img[-4:] == '.tif']
    file_list = sorted(file_list_o)
    listday = modules.date(file_list)
    list_str_day = modules.strday(listday)
    day_start = modules.find_nearest(list_str_day, int(day_in))
    print('Nearest day of Sentinel-1 data is: '+ day_start)
    check_name = f'{day_start}_ricemap_dos.tif'
    check_out = os.path.join(result_path, check_name)
    if os.path.exists(check_out) is True:
        print('result exist')
    else:
        cacl_rice_dos(list_str_day, day_start, file_list, result_path)
    return


if __name__ == '__main__':
    main()