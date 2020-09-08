# Schedule Library imported
import schedule
import time


# Functions setup
def run_task():
    print("Good job Guys!")


# After every 1 seconds run_task() is called.
schedule.every(1).second.do(run_task)

# After every 10 mins run_task() is called.
# schedule.every(10).minutes.do(run_task)


# Every day at 12am or 00:00 time run_task() is called.
# schedule.every().day.at("00:00").do(run_task)


# Every tuesday at 18:00 run_task() is called
# schedule.every().tuesday.at("18:00").do(run_task)

# Loop so that the scheduling task keeps on running all time.
while True:
    # Checks whether a scheduled task is pending to run or not (1 seconds)
    schedule.run_pending()
    time.sleep(1)
