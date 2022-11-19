import schedule
import time

 

print("inside");  
def job():
    print("Starting job")
    print("job time %s" % time.ctime())
  
 
schedule.every().day.at("02:00").do(job)
schedule.every().day.at("11:00").do(job)
schedule.every().day.at("14:00").do(job)
 
while True:
    print("in the loop");  
    schedule.run_pending()
    time.sleep(1)