from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import json
from datetime import datetime, timedelta
from datetime import datetime
import sys
import mia
import csv


def countDown(seconds):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=seconds)
    
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        mins, secs = divmod(remaining_time.seconds, 60) 
        sys.stdout.write("\r{:02d}:{:02d} remaining".format(mins, secs)) 
        sys.stdout.flush()
        time.sleep(1) 
    
    sys.stdout.write("\rRefresh\n")
        

if __name__ == "__main__":
    service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)   
    driver.maximize_window()  

    mia.scrape(driver)

    driver.quit()