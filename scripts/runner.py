import schedule
import time
import webscrapper
 
 

print("inside");  
def job():
    print("Starting job")
    print("job time %s" % time.ctime())
    webscrapper.run_webscrapper()
 
# schedule.every().day.at("02:00").do(job)
# schedule.every().day.at("11:00").do(job)
# schedule.every().day.at("14:00").do(job)
schedule.every(1).minutes.do(job)
 
while True:
  
    schedule.run_pending()
    time.sleep(1)