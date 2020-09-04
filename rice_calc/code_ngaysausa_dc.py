########################################################
#   Code tinh vung ngap nuoc tu anh Sentinel-1
#   author: Nguyen Van Anh Vu
#   contact: nvavu@vnsc.org.vn
#
#
#
import datetime
import os
import numpy as np
import gdal, ogr, osr
import array as arr
from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance
import argparse
def arg_parsing():
    parser = argparse.ArgumentParser(description='Calculate rice and water')
    parser.add_argument('-i', "--input", required=True,
                        help='Input directory')
    parser.add_argument('-o', "--output", required=True,
                        help='Output tif file')
    args = parser.parse_args()
    args = vars(args)
    args['input'] = os.path.abspath(args['input'])
    args['output'] = os.path.abspath(args['output'])
    return args
def geo_array(img):
    raster=gdal.Open(img)
    band = raster.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    array=np.nan_to_num(array)
    raster=None
    return array
def lee_filter(img, size):
    img_mean = uniform_filter(img, (size, size))
    img_sqr_mean = uniform_filter(img**2, (size, size))
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + overall_variance)
    img_output = img_mean + img_weights * (img - img_mean)
    return img_output
def day2jday(date):
     #date=datetime.datetime(int(name[0:4]),int(name[4:6]),int(name[6:8]))
     jday=date.toordinal() + 1721425
     return jday
def rice_map(array):
    min_array=array.min(axis=0)
    max_array=array.max(axis=0)
    mean_array=array.mean(axis=0)
    median_array=np.median(array,axis=0)
    count = (array < -20).sum(axis=0)
    increase=np.subtract(max_array,min_array)
    boundary=np.where(np.logical_and(min_array==0,max_array==0),1,0)
    water=np.where(mean_array < -20,2,0)
    urban=np.where(np.logical_and(median_array > -10,median_array!=0),1,0)
    rice=np.where(np.logical_and(increase>6,min_array<-19,
                                 np.logical_and(max_array>-16,max_array<-8,np.logical_and(median_array <= -15,
                                                np.logical_and(median_array >= -20,count<=5, count>=2)))),3,0)
    rmap=np.where(water>0,water,np.where(urban>0,urban,np.where(rice>0,rice,np.where(boundary>0,0,4))))
    return rmap
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
    prj=img.GetProjection()
    kq = {'cols':cols,
        'rows':rows,
        'bands':bands,
        'geotransform':geotransform,
        'originX':originX,
        'originY':originY,
        'pixelWidth':pixelWidth,
        'pixelHeight':pixelHeight,
        'projection':prj}
    return kq
def tiftostack(file_path,file_list,cols,rows):
    bb=len(file_list)
    stack_band=np.zeros(shape=(bb,rows,cols),dtype=float)
    for i in range(0,bb):
        file_name = os.path.join(file_path,file_list[i])
        array=geo_array(file_name)
        #arr_filter=lee_filter(array,3)
        arr2dB=linear2dB(array)
        stack_band[i,:,:]=arr2dB
    return stack_band
def linear2dB(array):
    array_dB=np.where(array>0,10*np.log10(array),0)
    array_dB2=np.where(array_dB>-50,array_dB,0) 
    return array_dB2
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
    outband.SetStatistics(float(np.nanmin(array)),float(np.nanmax(array)),float(np.nanmean(array)),float(np.nanstd(array)))
    outband.WriteArray(array)
    outband.SetNoDataValue(np.nan)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(sridcode)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()
def ngaysausa(stack_anh, rice,day):
    size=stack_anh.shape
    tam=np.zeros(size[0],dtype=float)
    nss=np.where(rice==0,-104,np.where(np.logical_or(rice==1,rice==4),-103,np.where(rice==2,-102,0)))
    for i in range(0,size[2]):
        for j in range(0,size[1]):
            if nss[j,i]==0:
                if rice[j,i]==3:
                    for k in range(0,size[0]):
                        tam[k]=stack_anh[k,j,i]
                    for k in range(0,len(tam)-1):
                        if tam[k]-tam[k+1]>5:
                             d_end=k
                    for k in range(0,d_end+1):
                        tam[k]=0
                    minpos=np.argmin(tam)
                    vitri=minpos
                    if vitri<len(tam)-1:
                        for k in range(vitri+1,len(tam)-1):
                            if tam[k]-tam[vitri]<1.5:
                                vitri=k
                    else:
                        nss[j,i]=-99
                    if tam[vitri-1]-tam[vitri]<5:
                        d_start=vitri-1
                    else:
                        d_start=vitri
                    if day[len(day)-1] - day[vitri] <=120:
                        nss[j,i]=day[len(day)-1] - day[d_start]
                    else:
                        nss[j,i]=-99
            else:
                nss[j,i]==nss[j,i]         
    return nss
if __name__ == "__main__":
    print('nhap nam va thang bat dau theo cu phap: YYYYMM')
    day_start=int(input())
    print('nhap ngay thang nam ket thuc theo cu phap: YYYYMMDD')
    day_end=int(input())
    with open('D:/V/work/2018-2019/datacube/hoc_code/tile_of_MekongDelta.txt') as f:
        tile_list = f.read().splitlines()
    list_dir=sorted(tile_list)
    ARGS = arg_parsing()
    #list_dir=sorted(os.listdir(ARGS['input']))
    for i in range(0,len(list_dir)):
        file_path=os.path.join(ARGS['input'],list_dir[i])
        file_list=os.listdir(file_path)
        list_road=np.array([])
        for j in range(0,len(file_list)):
            if len(file_list[j])==40 and file_list[j][13:16]=='DES':
                list_road=np.append(list_road,file_list[j][17:20])
        list_road=np.unique(list_road)
        for j in range(0,len(list_road)):
            print('calc for road: ',list_road[j])
            list_vh=np.array([])            
            for k in range(0,len(file_list)):
                if file_list[k][0:3]=='s1a' and len(file_list[k])==40 and file_list[k][13:16]=='DES' and file_list[k][10:12]=='vh'\
                    and file_list[k][17:20]==list_road[j] and int(file_list[k][21:27])>= day_start and int(file_list[k][21:29])<=day_end:
                        list_vh=sorted(np.append(list_vh,file_list[k]))
                elif file_list[k][0:3]=='s1a' and len(file_list[k])==40 and file_list[k][13:16]=='DES' and file_list[k][10:12]=='vh'\
                    and file_list[k][17:20]==list_road[j] and int(file_list[k][21:27])>= day_start and int(file_list[k][21:29])>day_end:
                    break
            old_settings = np.seterr(all='ignore')
            img_info=os.path.join(file_path,list_vh[0])
            check_array=geo_array(img_info)
            count_check=(check_array==0).sum()
            img_info=os.path.join(file_path,list_vh[1])
            check_array_2=geo_array(img_info)
            count_check_2=(check_array_2==0).sum()
            if abs(count_check-count_check_2)>1000000:
                count_check=count_check_2
            list_vh2=np.array([])
            for k in range(0,len(list_vh)):
                path_check=os.path.join(file_path,list_vh[k])
                array=geo_array(path_check)
                count=(array==0).sum()
                if abs(count-count_check)<=1000000:
                    list_vh2=sorted(np.append(list_vh2,list_vh[k]))
            print('tinh ngay sau sa/cay cua tile: ',list_dir[i],' ngay tinh: ',list_vh[len(list_vh)-1][21:29])
            print('reading file...')
            print('tao chuoi anh da thoi gian')
            old_info = get_img_info(img_info)
            stack_anh=tiftostack(file_path,list_vh2,old_info['cols'],old_info['rows'])
            print('kich thuoc du lieu: ',stack_anh.shape)    
            print('tinh toan lap ban do lua')
            rice=rice_map(stack_anh)
            print('tinh toan ngay sau sa')
            day=np.array([])
            for k in range(0,len(list_vh2)):
                date=datetime.datetime(int(list_vh2[k][21:25]),int(list_vh2[k][25:27]),int(list_vh2[k][27:29]))
                jday=day2jday(date)
                day=np.append(day,jday)
            dos=ngaysausa(stack_anh,rice,day)
            print('xuat ket qua ban do lua ra file')
            print('exporting...')
            out_name=ARGS['output']+os.path.sep+list_dir[i]+'_'+list_road[j]+'_'+str(day_start) +'_'+str(day_end)+'_ricemap.tif'
            array2raster(out_name, (old_info['originX'],old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'],rice, int('326'+list_dir[i][0:2]))                             
            print('writting file ', out_name)
            print('xuat ket qua ngay sau sa ra file')
            print('exporting...')
            out_name=ARGS['output']+os.path.sep+list_dir[i]+'_'+list_road[j]+'_'+str(day_start) +'_'+str(day_end)+'_NgaySauSa.tif'
            array2raster(out_name, (old_info['originX'],old_info['originY']),
                         old_info['pixelWidth'], old_info['pixelHeight'],dos, int('326'+list_dir[i][0:2]))                             
            print('writting file ', out_name)
        print('Done Tile')
print('Done')                         
   