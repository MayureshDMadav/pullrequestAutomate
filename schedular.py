import asyncio
import schedule
import time
import datetime
from script import everyNextDay, everyWeekDataProcess


# NEXT DAY SCHEDULING

async def everyNextDayProcess():
    await everyNextDay()


def everyNextDaySchedule():
    asyncio.run(everyNextDayProcess())


current_datetime = datetime.datetime.now()
next_day = current_datetime + datetime.timedelta(days=1)
next_task_time = next_day.replace(hour=10, minute=0, second=0, microsecond=0)
time_difference = (next_task_time - current_datetime).total_seconds()


schedule.every(time_difference).seconds.do(everyNextDaySchedule)


# EVERY WEEK SCHEDULING


async def everyNextWeekProcess():
    await everyWeekDataProcess()


def everyNextWeekSchedule():
    asyncio.run(everyNextWeekProcess())


schedule.every().thursday.at('17:00').do(everyNextWeekSchedule)


while True:
    schedule.run_pending()
    time.sleep(1)
