import datetime
import os,sys
import subprocess as sp

def key_sort(name):
    return name[17:25]

def s1collect(dwl_dir,user,password,searchbox):
    print("Starting search and collect data...")
    today=datetime.datetime.today()
    list_file=sorted(os.listdir(dwl_dir),key=key_sort,reverse=True)
    day_end=today.strftime('%Y%m%d')
    backday= datetime.datetime(int(list_file[0][17:21]),int(list_file[0][21:23]),int(list_file[0][23:25]))
    day_start=backday.strftime('%Y%m%d')
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
    
def s1_dwl(): 
    dirname = os.path.dirname(__file__)
    sys.path.append(os.path.realpath('..'))
    download_path = os.path.join(dirname,"../download_dir")
    user_path=os.path.join(dirname,"../rice_calc/top_secret.TXT")
    box=os.path.join(dirname,'../rice_calc/polygon.json')
    with open(user_path) as f:
        user = f.read().splitlines()
    f.close()
    s1collect(download_path,user[0],user[1],box)
    return
