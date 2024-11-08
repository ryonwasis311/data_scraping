from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import csv
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


def scrape(driver) -> dict:
  results = []
  index = 1
  audit = True 
  while True:
    try:
      driver.get("https://mia.org.my/members-firm-search/")
      WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.NAME, 'quform_6_10')))
      selectObj = driver.find_element(By.NAME, 'quform_6_10')
      select_status = Select(selectObj)
      select_status.select_by_value("FSTATE")
      time.sleep(1)
      selectObj = driver.find_element(By.NAME, 'quform_6_27')
      options = len(selectObj.find_elements(By.TAG_NAME, "option"))
      if options > index:
        select_status = Select(selectObj)
        select_status.select_by_index(index)
        time.sleep(1)

        selectObj = driver.find_element(By.NAME, 'quform_6_19')
        select_status = Select(selectObj)
        if audit == True:
          select_status.select_by_value("A")
        else:
          select_status.select_by_value("NA")
        time.sleep(1)
        driver.execute_script("document.getElementsByClassName('quform-submit')[0].click();")
        time.sleep(5)
        try:
          WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tbody')))
          while True:
            tbodys = driver.find_elements(By.TAG_NAME, 'tbody')
            for tbody in tbodys:
              trs = tbody.find_elements(By.TAG_NAME, 'tr')
              for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, 'td')
                tdStr = tds[5].get_attribute('textContent')
                tel = tdStr.split("Fax:")[0].replace("Tel:", '').strip()
                email = tdStr.split("Email:")[1].strip()
                results.append({
                  "name": tds[1].get_attribute('textContent').strip(),
                  "address": tds[2].get_attribute('textContent').strip(),
                  "state": tds[3].get_attribute('textContent').strip(),
                  "tel": tel,
                  "email": email
                })
            liTags = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')
            nextPage = len(liTags) - 1
            if nextPage >= 0 and liTags[nextPage].get_attribute('textContent') == "Next Page":
              driver.execute_script("document.getElementsByClassName('pagination')[0].getElementsByTagName('li')[" + str(nextPage) + "].getElementsByTagName('a')[0].click();")
              time.sleep(5)
              WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tbody')))
            else:
              break
        except TimeoutException:
          pass
        if audit == True:
          audit = False
        else:
          index += 1
          audit = True
      else:
        break
    except:
      pass

    with open("list.csv", 'w', encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["Firm's name", "Address", "State", "Tel", "Email"])
        for result in results:
          writer.writerow([
            result["name"],
            result["address"],
            result["state"],
            result["tel"],
            result["email"]
          ])