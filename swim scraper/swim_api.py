import try_post_request as post_rq
import re


def get_data():
    sections = post_rq.post_data() 

    #get useful locations
    locations = []
    counter = 0
    print(len(sections[0]["classes"]))
    print(len(sections[1]["classes"]))
    print(len(sections[2]["classes"]))
    for i in range(len(sections)):
        print(len(sections[i]))
        section = sections[i]
        for data in section["classes"]:
            if "Length Swim" in data["EventName"] and "Small" not in data["Location"]:
                # print(data)
                location = data["Location"]
                time = data["EventTimeDescription"]
                date = data["FormattedStartDate"]
                rawDate = data["OccurrenceDate"]
                id = data["EventId"]
                iid = counter
            
                if "Full" in data["Spots"]:
                    spots = "Full"
                elif "More" in data["Spots"]:
                    continue
                else:
                    spots = re.search(r'\d+', data["Spots"]).group() + " spot(s)"

                counter += 1
                obj = Location(location, time, spots, date, rawDate, id, iid)
                locations.append(obj)
        
    return locations


# raw = post_rq.post_data()  # result.text

#format to print readable json
# data = json.loads(raw)
# pretty_data = json.dumps(data, indent=4)

# print(pretty_data)

# buttonUrlExample = "https://vaughan.perfectmind.com/25076/Clients/BookMe4LandingPages/Class?widgetId=dff88c8a-0b78-4a94-9dde-250040385300&redirectedFromEmbededMode=False&classId=ab1f9a42-1e3a-b8ef-32b1-a52c9131869a&occurrenceDate=20250907"

def generateButtonUrl(id, date):
    """ 
    generates button url from id and date,
    id example - ab1f9a42-1e3a-b8ef-32b1-a52c9131869a (CourseId in data),
    date format - 20250907 (sep 7 2025),
    returns link to register page"""
    return f"https://vaughan.perfectmind.com/25076/Clients/BookMe4LandingPages/Class?widgetId=dff88c8a-0b78-4a94-9dde-250040385300&redirectedFromEmbededMode=False&classId={id}&occurrenceDate={date}"



#class for each location
class Location:
    def __init__(self, location, time, spots, date, rawDate, id, iid):
        self.location = location
        self.time = time
        self.spots = spots
        self.date = date
        self.rawDate = rawDate
        self.id = id
        self.iid = iid





# uniqueLocations = []

# for obj in locations:
#     if obj.location not in uniqueLocations:
#         uniqueLocations.append(obj.location)

# #user input
# for i in range(len(uniqueLocations)):
#     print(f"{i+1}: {uniqueLocations[i]}")

# run = True
# while run:
#     inp = input("enter number for corresponding location: ")
#     try:
#         inp = int(inp)
#         run = False
#     except ValueError:
#         print("not a number!")

# selectedLocation = uniqueLocations[inp-1]
# print(f"selected: {selectedLocation}")


# possibleLocations = []
# for i in range(len(locations)):
#     spot = locations[i]
#     if spot.location == selectedLocation:
#         possibleLocations.append(spot)


# for i in range(len(possibleLocations)):
#     spot = possibleLocations[i]
#     print(f"{i+1}: {spot.location, spot.date, spot.time, spot.spots}")


# run = True
# while run:
#     spotIndex = input("enter number for spot: ")
#     try:
#         spotIndex = int(spotIndex)
#         run = False
#     except ValueError:
#         print("not a number!")

# selectedSpot = possibleLocations[spotIndex-1]
# url = generateButtonUrl(selectedSpot.id, selectedSpot.rawDate)
# print(url)

