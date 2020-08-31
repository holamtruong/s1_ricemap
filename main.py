#main.py
import rice_calc.gpt_dir as ARD
import rice_calc.modules as modules
import os

def main():
	input_img='F:/DEV/rice_test/input'#satelite imagery input directory
	output_img='F:/DEV/rice_test/output'#output ARD directory
	ARD.S1_process(input_img,output_img)
	#output_img='F:/S1_gpt/out_img'
	file_list_o=[img for img in os.listdir(output_img) if img[-4:] == '.tif']
	file_list=sorted(file_list_o)
	img_info=os.path.join(output_img,file_list[0])
	old_info = modules.get_img_info(img_info)
	stack_anh=modules.tiftostack(output_img,file_list,old_info['cols'],old_info['rows'])
	kq=modules.rice_map(stack_anh)
	print('xuat ket qua ra file')
	print('exporting...')
	result_path='F:/DEV/s1_ricemap/result'
	out_name=os.path.join(result_path,'ricemap.tif')
	modules.array2raster(out_name, (old_info['originX'],old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'],kq, 32648)
	return
if __name__ == "__main__":
	main()
	print('Done...')                   
        