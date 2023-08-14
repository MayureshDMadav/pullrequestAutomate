import schedule
import time
import datetime
import asyncio
from script import everyNextDay


# Every Next Day Running
def everyNextDayRun():
    asyncio.run(everyNextDay())


current_datetime = datetime.datetime.now()
next_day = current_datetime + datetime.timedelta(days=1)
next_task_time = next_day.replace(hour=10, minute=0, second=0, microsecond=0)
time_difference = (next_task_time - current_datetime).total_seconds()


schedule.every(time_difference).seconds.do(everyNextDayRun)


# Every Week Running
# schedule.every().thursday.at('17:00').do(requestTriggered)


while True:
    schedule.run_pending()
    time.sleep(1)
