import asyncio
import schedule
import time
import datetime
from backend.shopifydomainfetch import fetchShopifyDomain
from backend.new_merchant_address import apiRequestCallforNewMerchant


# DOMAIN UPDATION

def domainFetching(sheetNumber):
    response = fetchShopifyDomain(sheetNumber)
    return response

# Rest API CALL For New Merchant Sheet and Updating the Status as Done or Failed

def restApiCallForNewMerchant(sheetNumber):
    response = apiRequestCallforNewMerchant(sheetNumber)
    return response



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
