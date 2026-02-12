from selenium import webdriver
from selenium.webdriver.common.by import By
import webbrowser
import time


import os
from dotenv import load_dotenv
load_dotenv()
USERNAME = os.getenv("LOGIN_USERNAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")


# == MAIN REGISTER FUNCTION ==
def register(url):
    driver = webdriver.Chrome()
    driver.get(url=url)
    driver.implicitly_wait(5)

    if driver.current_url != url: #redirected to login page
        #IMPLEMENT SAVING LOGIN
        #hardcoded login for now
        driver.implicitly_wait(0.5)
        driver.find_element(by=By.ID, value="textBoxUsername").send_keys(USERNAME)
        driver.find_element(by=By.ID, value="textBoxPassword").send_keys(PASSWORD)

        driver.find_element(by=By.ID, value="buttonLogin").click()
    
    driver.find_element(by=By.NAME, value="ParticipantsFamily.FamilyMembers[0].IsParticipating").click() #hard coded first person in family (me), later will implement selecting members
    driver.find_element(by=By.CSS_SELECTOR, value='a[title="Next"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value='a[title="Next"]').click()
    driver.find_element(by=By.ID, value="btnNext").click()
    driver.find_element(by=By.ID, value="checkoutButton").click()
    time.sleep(2)
    print(f"SENDING USER TO: {driver.current_url}")
    webbrowser.open(driver.current_url)