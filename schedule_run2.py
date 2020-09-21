# Schedule Library imported
import schedule
import time
import logging
import rice_calc.gpt_dir as ARD
import rice_calc.s1_download as download


# Setup time to run 'quytrinh_thanhlap_ricemap' at hh:mm everyday
start_time = "13:22"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('task.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


# Functions setup
def download_img():
    dwl = download.s1_dwl()
    return dwl


def preprocessing():
    input_img = 'download_temp'  # satelite imagery input directory
    output_img = 'ard_store'  # output ARD directory
    ARD.S1_process(input_img, output_img)  # call gpt to processing file
    return 'ok'

def download_n_processing():
    logger.info('running program')
    logger.info('search and collect new images...')
    check1 = download_img()

    if check1[0] == 'ok':
        logger.info('search and collect new images successful')
        logger.info(f'downloaded and stored temporary in {check1[1]} with user name {check1[2]}')
    else:
        logger.info('collect image false')
    logger.info('processing image...')
    check2 = preprocessing()

    if check2 == 'ok':
        logger.info('processing image successful')
    else:
        logger.info('processing image false')
        logger.info('..::Done::..')
    print('OK. Wait for the next running at ' + start_time + ' tomorrow.')


# After every 1 seconds run_task() is called.
def main():
    schedule.every().day.at(start_time).do(download_n_processing)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
