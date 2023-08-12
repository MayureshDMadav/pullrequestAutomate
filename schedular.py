import schedule
import time
import datetime
from script import requestTriggered


current_datetime = datetime.datetime.now()

next_day = current_datetime + datetime.timedelta(days=1)
next_task_time = next_day.replace(hour=10, minute=0, second=0, microsecond=0)
time_difference = (next_task_time - current_datetime).total_seconds()

# Every Next Day Running
schedule.every(time_difference).seconds.do(requestTriggered)
print(current_datetime)

# Every Week Running
schedule.every().thursday.at('17:00').do(requestTriggered)


while True:
    schedule.run_pending()
    time.sleep(1)


# Every Next Day
