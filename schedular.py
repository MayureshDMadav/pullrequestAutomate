import asyncio
import schedule
import time
import datetime
from backend.shopifydomainfetch import fetchShopifyDomain


# DOMAIN UPDATION

def domainFetchingSchedule():
    response = fetchShopifyDomain(0)
    print(response)


a = domainFetchingSchedule()
print(a)



# schedule.every(10).seconds.do(domainFetchingSchedule)   


# async def everyNextDayProcess():
#     await everyNextDay()


# current_datetime = datetime.datetime.now()
# next_day = current_datetime + datetime.timedelta(days=1)
# next_task_time = next_day.replace(hour=10, minute=0, second=0, microsecond=0)
# time_difference = (next_task_time - current_datetime).total_seconds()


# schedule.every(time_difference).seconds.do(everyNextDaySchedule)


# EVERY WEEK SCHEDULING


# async def everyNextWeekProcess():
#     await everyWeekDataProcess()


# def everyNextWeekSchedule():
#     asyncio.run(everyNextWeekProcess())


# schedule.every().thursday.at('17:00').do(everyNextWeekSchedule)

# def scheduled_job():
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(domainFetch())
#     print(result)

# schedule.every(10).seconds.do(domainFetch)



while True:
    schedule.run_pending()
    time.sleep(1)
