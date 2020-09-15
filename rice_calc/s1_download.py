import datetime
import os,sys
import subprocess as sp
#call cmd to download
def s1collect(dwl_dir,day_start,user,password,searchbox):
    print("Starting search and collect data...")
    today = datetime.datetime.today()
    day_end = today.strftime('%Y%m%d')
    #const='-d --producttype GRD -q \"orbitdirection=Descending\" --url \"https://scihub.copernicus.eu/dhus\"'
    url = '''https://scihub.copernicus.eu/dhus'''
    cmd=['sentinelsat','-u',user,'-p',password,'-g',searchbox,
         '-s',day_start, '-e',day_end,'-d','--producttype','GRD','-q',
         'orbitdirection=Descending','--url',url,
         '--path',dwl_dir]
    #print(cmd)
    try:
        output = sp.check_call(cmd)
    except sp.CalledProcessError as e:
        output = e.output
    return
#download image  
def s1_dwl(): 
    dirname = os.path.dirname(__file__)
    sys.path.append(os.path.realpath('..'))
    download_path = os.path.join(dirname,"../download_dir")
    user_path=os.path.join(dirname,"../rice_calc/top_secret.TXT")
    box = os.path.join(dirname,'../rice_calc/polygon.json')
    start_path = os.path.join(dirname,"../list.data")
    with open(start_path) as f:
        start_day = f.read().splitlines()
    f.close()
    with open(user_path) as f:
        user = f.read().splitlines()
    f.close()
    s1collect(download_path,start_day[-1],user[0],user[1],box)
    return 'ok', download_path,user[0]
