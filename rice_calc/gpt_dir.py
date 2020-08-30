""" Code goc
 gpt = r'your_gpt_path' # If it is in your PATH environment variable you can just use 'gpt'
 graph_path = r'your_graph.xml'

cmd_pts = [gpt,
            graph_path,
            '-PyourParameter1="{}"'.format(yourVal1),
            '-PyourParameter2="{}"'.format(yourVal2)]

sp.check_call(cmd_pts)
"""
import subprocess as sp
import os
def S1_process(in_path,out_path):
    gpt = 'C:/Program Files/snap/bin/gpt.exe'
    graph_path = '/s1_ricemap/rice_calc/graph_ARD.xml'
    shp='/s1_ricemap/sample_data/tile.shp'
    file_list=[img for img in os.listdir(in_path) if img[-4:] == '.zip']
    for i in file_list:
        in_name='-Pinput='+os.path.join(in_path,file_list[i])
        out_name='-Poutput='+os.path.join(out_path,file_list[i][17:25]+'_'+file_list[i][63:67]+'_AO_ML_CL_TC'+'{}').format('')
        file_name=file_list[i][17:25]+'_'+file_list[i][63:67]+'_AO_ML_CL_TC'+'{}'.format('.tif')
        file_out=file_list[i][17:25]+'_'+file_list[i][63:67]+'_AO_ML_CL_TC'+'_cut'+'{}'.format('.tif')
        cmd = [gpt,
                   graph_path,
                   in_name,
                   out_name]
        sp.check_call(cmd)
        check_path=os.path.join(out_path,file_name)
        check_out=os.path.join(out_path,file_out)
        options = gdal.WarpOptions(cutlineDSName=shp, cropToCutline=True)
        result_img = gdal.Warp(srcDSOrSrcDSTab=inputPath + image,
            destNameOrDestDS=outputPath + image[:-4] + '_clip' + image[-4:],
            options=options)
        result_img = None
        os.remove(check_path)
    return