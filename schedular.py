import asyncio
import schedule
import time
import datetime
from script import everyNextDay, everyWeekDataProcess
from processheet.sheetprocessor import fetchSheetData,writeShopifyDomain
from backend.shopifydomainfetch import fetchShopifyDomain

# NEXT DAY SCHEDULING

def domainFetch():
    try:
        sheetFromData =  fetchSheetData(0)
        jsonDomainFetch = fetchShopifyDomain(sheetFromData)
        a = writeShopifyDomain(sheetFromData,jsonDomainFetch,0)
        return a
    except Exception as e:
        print(e)
        return e

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

domainFetch()

while True:
    schedule.run_pending()
    time.sleep(1)
