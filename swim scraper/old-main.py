# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import requests


# driver = webdriver.Chrome()

# url = "https://vaughan.perfectmind.com/25076/Clients/BookMe4BookingPages/Classes?calendarId=71fe848e-2dbd-4ec5-92fa-7f2d0ad09354&widgetId=dff88c8a-0b78-4a94-9dde-250040385300&embed=False"

# request_url = "https://vaughan.perfectmind.com/25076/Clients/BookMe4BookingPagesV2/ClassesV2"
# result = requests.request(request_url)
# print(result)
# driver.get(url)

# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, "bm-marker-row"))
# )

# result = driver.page_source
# soup = BeautifulSoup(result, "html.parser")
# # driver.quit()
# spots = {}
# index = -1

# table = soup.find("table", id="classes", class_="bm-classes-grid")
# if table:
#     rows = table.find_all("tr", class_="bm-class-row")
#     for row in rows:
#         #format
#         cells = [cell.text.strip() for cell in row.find_all("td")]
#         text = cells[0]
#         lines = [line.strip() for line in text.split("\n") if line.strip()]

#         if lines[0] == "Length Swim":
#             #track index
#             index += 1

#             #create the index in table
#             spots[index] = {}

#             #store info
#             spots[index]["service"] = lines[0]
#             spots[index]["time"] = lines[1]
#             spots[index]["location"] = lines[2]
#             spots[index]["price"] = lines[3]
#             spots[index]["space"] = lines[4]

#     for spot in spots:
#         print(spots[spot])


# uniqueLocations = []

# for i in range(len(spots)):
#     if spots[i]["location"] not in uniqueLocations and "Small" not in spots[i]["location"]:
#         uniqueLocations.append(spots[i]["location"])

# for i in range(len(uniqueLocations)):
#     print(f"{i+1}: {uniqueLocations[i]}")

# run = True
# while run:
#     locationIndex = input("enter number for location: ")

#     if int(locationIndex):
#         run = False
#         location = uniqueLocations[int(locationIndex)-1]

#         for spot in spots:
#             if spots[spot]["location"] == location:
#                 print(spots[spot])
#     else:
#         print("not a number!")