from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import schedule

import swim_api

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
    time.sleep(2) #stops on last page because i dont want it to book a million sessions when testing



booked = {} #cant be asked to put template data so ill just code it in
# -- automate booking days --
def autoBook(rawDate, courseId):
    """
    ONE-AT-A-TIME SINGLE WEEKDAY BOOKING
    takes rawDate and converts to weekday,
    then books every weekday
    ONLY WORKS AS LONG AS APP IS RUNNING
    """
    global booked
    dateInfo = datetime.strptime(rawDate, "%Y%m%d")
    weekday = dateInfo.strftime("%a") # %A for full weekday name, %a for abbreviated name

    if weekday not in booked:
        booked[weekday] = []
    booked[weekday].append({"date": dateInfo, "id": courseId})
    print(booked[weekday], dateInfo.strftime("%Y%m%d"))
    location = swim_api.findLocationFromCourseId(courseId, dateInfo.strftime("%Y%m%d"), 1)
    register(swim_api.generateButtonUrl(location.id, location.rawDate, True))
    schedule.run_all()



def bookAll():
    #schedule run every day and book whatever is in booked for that day
    #booking opens 7 days in future
    global booked
    current_weekday = datetime.now().strftime("%a")
    print(f"weekday: {current_weekday}, booked: {booked}")
    if current_weekday in booked and booked[current_weekday] != []: #if day exists and isnt empty list
        for booking in booked[current_weekday]:
            next_day = datetime.now() + timedelta(days=7)
            location = swim_api.findLocationFromCourseId(booking["id"], next_day.strftime("%Y%m%d"), 1)
            print(f"BOOKING: {location.location} at {location.time}")
            register(swim_api.generateButtonUrl(location.id, location.rawDate, True))


def start():
    schedule.every().day.at("01:00").do(bookAll) # 1am
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start()