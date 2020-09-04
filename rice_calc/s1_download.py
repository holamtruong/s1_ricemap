import schedule
import time
import datetime
import os
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
    
def main():   
    download_path="F:/DEV/s1_ricemap/download_dir"
    box='F:/DEV/s1_ricemap/rice_calc/polygon.json'
    with open('F:/DEV/s1_ricemap/rice_calc/top_secret.TXT') as f:
        user = f.read().splitlines()
    f.close()
    s1collect(download_path,user[0],user[1],box)
    return

if __name__=='__main__':
    #main()
    schedule.every(1).day.at("09:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
  
#schedule.every(10).seconds.do(s1collect(download_path))
"""
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)
"""
#while True:
#   schedule.run_pending()
#   time.sleep(1)
