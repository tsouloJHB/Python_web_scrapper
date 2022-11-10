from bs4 import BeautifulSoup
import requests
import json
import ftptransfer
import logging

#create and config logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename= "scrapper.log",
                    level= logging.DEBUG,
                    format= LOG_FORMAT,
                    filemode='w')

logger = logging.getLogger();


match_list = []; #holds all matches     
channel_list_data = []
soup = "";

def crawl_site():
     url= "https://watch.cricfree.io/category/football"  
     try:
          page = requests.get(url)
          logger.debug("page fetched");    
     except:
          logger.critical("failed to connect and fetch html code");   

     return BeautifulSoup(page.content, 'html.parser')

def Get_match_channels():
     global channel_list_data
     global match_list
     global soup

     channel_data = {}
     list_channel = []
     match_data = {}
     lists_schedule = soup.find_all('tbody', class_="schedule_lists")
     for list in lists_schedule:
          
          try:
               list_info_open = list.find_all('tr', class_="info-open")
               list_info = list.find_all('tr', class_="info")   
          
               for lister in list_info_open:
                    leagues_list = lister.find('td', class_="competition")
                    matches_list = lister.find('td', class_="event")
                    time_list = lister.find('td', class_="time dtstart")
                    # leagues_list = leagues_list.find('a').text
                    match_data = {}
                    match_data['league'] = leagues_list.find('a').text.lower()
                    match_data['teams'] = matches_list.find('a').text.lower()
                    match_data['time'] = time_list.find('span').text.lower()
                    match_data['channels'] = [];
                    match_list.append(match_data)  
               #Get all the channels which are separate from the info            
               for channel in list_info:
                    channel_data = {}
                    list_channel = []
                    
                    channel_list = channel.find('a', class_="btn")
                    if(channel_list != None):
                         
                         channel_data['channel'] = channel_list.text
                    else:     
                         channel_data['channel'] = ""
                    
                    for a in channel.find_all('a', href=True):
                         list_channel.append(a.text.lower())
                         #merge link and channel name separated by a at sign 
                    #save list in outer list
                    channel_list_data.append(list_channel)
                    logger.debug("html values found");
          except:
               logger.critical("failed to identify specific html elements in code");          


#check if channels exits,search for channel and create link then save channels in match_list
def create_channel_links():
     global channel_list_data
     f = open('channels.json')
     json_data = json.load(f)
     for count,data in enumerate(channel_list_data):
          for chan in data:
               link = ""
               if( chan in json_data['soccer']):
                    chan_index = json_data['soccer'][chan];
               
                    link = "live.php?channel="+chan+"@"+chan
                    match_list[count]['channels'].append(link)
               data = "";



def save_data():
     global match_list
     f = open('tvguide.json')
     json_data = []
     json_data = {'soccer':{}, 'cricket':{}}

     for count,fixtures in enumerate(match_list, start=1):
          match = "match "+ str(count)
          

          json_data['soccer'].update(
               {
                    match :{
                         "league":fixtures['league'],
                         "teams":fixtures['teams'],
                         "time":fixtures['time'],
                         "channels": {"channel "+str(c) :x for c,x in enumerate(fixtures['channels'],start=1) }
               }})    

     #save data to file
     logger.debug("saving json data")
     json_object = json.dumps(json_data, indent=4)
     
     # Writing to sample.json
     try:
          with open("tvguide.json", "w") as outfile:
               outfile.write(json_object) 
          #upload file to the sever     
          if(ftptransfer.upload()):
               print("file uploaded")
          else:
               print("file not uploaded");
     except:
          logger.critical("failed to save data into file");          

def run_webscrapper():
     global soup
     soup = crawl_site()
     Get_match_channels()
     create_channel_links()
     save_data()
   


run_webscrapper()









