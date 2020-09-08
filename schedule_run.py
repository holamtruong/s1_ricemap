# Schedule Library imported
import schedule
import time


# Functions setup
def run_task_1():
    print("Good job Guys!")


def download_anh_1():
    print("tai xong img_1")
    img_1 = 123
    return img_1


def tien_xuly_anh_1(input_img):
    img_1_xuly = input_img + 456
    print("da xu ly img_1 xong")
    return img_1_xuly


def xuly_anh_1(input_img):
    img_1_xuly = input_img + 789
    print("da xu ly img_1 xong")
    return img_1_xuly


def quytrinh_thanhlap_ricemap():
    anh_download = download_anh_1()
    anh_tienxuly = tien_xuly_anh_1(anh_download)
    anh_daxuly = xuly_anh_1(anh_tienxuly)
    print(anh_daxuly)
    print("Thanh cong!")


# After every 1 seconds run_task() is called.
schedule.every(3).seconds.do(quytrinh_thanhlap_ricemap)

# Loop so that the scheduling task keeps on running all time.
while True:
    # Checks whether a scheduled task is pending to run or not (1 seconds)
    schedule.run_pending()
    time.sleep(1)
