#main.py
import rice_calc.gpt_dir as ARD
import rice_calc.modules as modules
import os

def main():
    input_img='input'#satelite imagery input directory
    output_img='output'#output ARD directory
    ARD.S1_process(input_img,output_img)
    #output_img='F:/S1_gpt/out_img'
    file_list_o=[img for img in os.listdir(output_img) if img[-4:] == '.tif']
    file_list=sorted(file_list_o)
    img_info=os.path.join(output_img,file_list[0])
    old_info = modules.get_img_info(img_info)
    stack_anh=modules.tiftostack(output_img,file_list,old_info['cols'],old_info['rows'])
    rice=modules.rice_map(stack_anh)
    print('exporting result...')
    print('exporting ricemap...')
    result_path='result'
    out_name=os.path.join(result_path,'ricemap.tif')
    modules.array2raster(out_name, (old_info['originX'],old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'],rice, 32648)
    file_list=sorted(os.listdir(output_img))
    day=modules.date(file_list)
    dos=modules.calc_dos(stack_anh,rice,day)
    out_name=os.path.join(result_path,'ricemap_dos.tif')
    print('exporting rice dos map...')
    modules.array2raster(out_name, (old_info['originX'],old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'],dos, 32648)
    stack_anh=None
    dos=None
    day=None
    return
if __name__ == "__main__":
    #ARGS = modules.arg_parsing()
    main()
    print('Done...')            
        