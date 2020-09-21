import datetime
import os
import subprocess as sp
import sys


# call cmd to download
def s1collect(dwl_dir, day_start, user, password, searchbox):
    print("Starting search and collect data...")
    today = datetime.datetime.today()
    day_end = today.strftime('%Y%m%d')
    dstart = datetime.datetime(int(day_start[0:4]), int(day_start[4:6]), int(day_start[6:8]))
    dstart_plus = dstart + datetime.timedelta(days=1)
    day_start_str = dstart_plus.strftime('%Y%m%d')
    # const='-d --producttype GRD -q \"orbitdirection=Descending\" --url \"https://scihub.copernicus.eu/dhus\"'
    url = '''https://scihub.copernicus.eu/dhus'''
    cmd = ['sentinelsat', '-u', user, '-p', password, '-g', searchbox,
           '-s', day_start_str, '-e', day_end, '-d', '--producttype', 'GRD', '-q',
           'orbitdirection=Descending', '--url', url,
           '--path', dwl_dir]
    # print(cmd)
    try:
        output = sp.check_call(cmd)
    except sp.CalledProcessError as e:
        output = e.output
    return


# download image
def s1_dwl():
    dirname = os.path.dirname(__file__)
    sys.path.append(os.path.realpath('..'))
    download_path = os.path.join(dirname, "../download_temp")
    user_path = os.path.join(dirname, "../rice_calc/top_secret.TXT")
    box = os.path.join(dirname, '../rice_calc/polygon.json')
    ard_folder = os.path.join(dirname, "../ard_store")
    check_list = [img for img in os.listdir(ard_folder) if img[-4:] == '.tif']
    start_check = check_list[-1][0:8]
    with open(user_path) as f:
        user = f.read().splitlines()
    f.close()
    s1collect(download_path, start_check, user[0], user[1], box)
    return 'ok', download_path, user[0]
