import asyncio
import schedule
import time
import datetime
from backend.shopifydomainfetch import fetchShopifyDomain
from processheet.sheetprocessor import pushDataFromFirstToSecond,dataFilter
from backend.new_merchant_address import apiRequestCallforNewMerchant
from backend.weekly_data_request import apiRequestCallforWeeklyMerchant 


def domainUpdationToSheet(sheetNumber):
    fetchShopifyDomain(sheetNumber)


# SCHEDULAR FUNCTIONS

# Rest API CALL For New Merchant 
def firsSheetRequestProcess():
    print("Updating Domain and removing Duplicates ===>")
    fetchShopifyDomain(0)
    print("Executing Rest API CAll ===>")
    apiRequestCallforNewMerchant(0)
    print("Pushing Data To Another Sheet ===>")
    pushDataFromFirstToSecond(1)
    print("Removing Duplicated Data")
    dataFilter(1)
    print("Data have been pushed Successfully")
   
# Second Sheet Data Processng
def secondSheetRequestProcess():
    print("Updating Domain and removing Duplicates ===>")
    fetchShopifyDomain(1)
    print("Executing Rest API CAll ===>")
    apiRequestCallforWeeklyMerchant(1)
    print("Succesfully Update the details")

# NEW MERCHANT DATA PULL FUNCTION ===>
# firsSheetRequestProcess()

# WEEKLY MERCHANT DATA PULL FUNCTOIN ===>
# secondSheetRequestProcess()

# Update Shopify Domain 
domainUpdationToSheet(0)

# def main():
#     print("Processing First Sheet Request")
#     firstToSecondSheet()
#     print("Processing Second Sheet Request")
#     secondSheetRequestProcess()


# main()

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



# while True:
#     schedule.run_pending()
#     time.sleep(1)
