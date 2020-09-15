import time
from selenium import webdriver
import pandas as pd
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep

driver = webdriver.Chrome()
driver.set_page_load_timeout(10)
data = None
SIZE = None
DELAY = float(sys.argv[2])
MAX_SIZE = int(sys.argv[1])

def getIcInfo():
    driver.get("https://www.random-name-generator.com/?")
    time.sleep(DELAY)

    N = driver.find_element_by_name("n")
    driver.execute_script("arguments[0].value = ''", N)
    N.send_keys("1")
    data = pd.read_csv("IC_data.csv")
    SIZE = data.shape[0]
    print("Calling getIcInfo(): " + str(data.shape) + "\n")
    try:
        while(SIZE < MAX_SIZE):
            fullname = None
            gender = None
            religion = None
            button =  WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))
            button.click()
            time.sleep(DELAY)

            address =  WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-8')))
            name  =  WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'mt-0')))

            if ("female" in name.text):
                fullname = name.text.replace(" (female)","")
            else:
                fullname = name.text.replace(" (male)","")

            if ("female" in name.text):
                gender = "PEREMPUAN"
            else:
                gender = "LELAKI"

            if("bin" in fullname or "Bin" in fullname or "binti" in fullname or "Binti" in fullname):
                religion = "ISLAM"
            address = address.text.upper()
            fullname = fullname.upper()
            data = data.append(pd.DataFrame([[address,fullname,gender,religion]],columns = data.columns),ignore_index=True)
            print([address, fullname,gender,religion])
            isDup = data.duplicated().any()
            print("Any Duplicate ? : " + str(isDup))
            data.drop_duplicates(inplace=True)
            if(isDup):
                driver.delete_all_cookies()
                getIcInfo()
                return
            data.to_csv("IC_data.csv",index=False)
            data = None
            data = pd.read_csv("IC_data.csv")
            SIZE = data.shape[0]
            print("Current Entry: " + str(SIZE) + "\n")
            del button, address, name, isDup
            

        data.to_csv("IC_data.csv",index=False)
        print("DONE Recording " + str(data.shape[0]) + " data")
        print("Saved to IC_data.csv\n" )

    except TimeoutException as Ts:
        print("Exception has been thrown. " + str(Ts))
        data.to_csv("IC_data.csv",index=False)
        print(str(data.shape[0]) + " data Recorded")
        print("Saved to IC_data.csv" )
        print("Reconnecting..............................................\n")
        time.sleep(10)
        getIcInfo()

    except:
        print("ERROR")
        data.to_csv("IC_data.csv",index=False)
        print("DONE Recording " + str(data.shape[0]) + " data")
        print("Saved to IC_data.csv\n" )


    try:
        driver.close()
    except Exception as ex:
        print("Driver Already Closed " + str(ex) + "\n")

getIcInfo()