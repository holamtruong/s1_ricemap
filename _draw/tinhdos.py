import rice_calc.modules as modules
import os
import datetime
import numpy as np

def main():
    print('calculating day after sowing of rice')
    in_path='output'
    out_path='result'
    file_list=sorted(os.listdir(in_path))
    img_info=os.path.join(in_path,file_list[0])
    old_info = modules.get_img_info(img_info)
    stack_anh=modules.tiftostack(in_path,file_list,old_info['cols'],old_info['rows'])
    rice=modules.rice_map(stack_anh)
    day=modules.date(file_list)
    dos=modules.calc_dos(stack_anh,rice,day)
    out_name=os.path.join(out_path,'ricemap_dos.tif')
    modules.array2raster(out_name, (old_info['originX'],old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'],dos, 32648)
    stack_anh=None
    dos=None
    day=None
    return
if __name__ == '__main__':
    main()
