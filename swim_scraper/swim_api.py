import try_post_request as post_rq
import re


def get_data(date):
    data = {}
    section, nextDate = post_rq.post_data(date) 

    #get useful locations
    locations = []
    print(f"class amount: {len(section["classes"])}")
    print(f"section length: {len(section)}")
    for data in section["classes"]:
        if "Length Swim" in data["EventName"] and "Small" not in data["Location"]:
            #print(data)
            location = data["Location"]
            time = data["EventTimeDescription"]
            date = data["FormattedStartDate"]
            rawDate = data["OccurrenceDate"]
            id = data["EventId"]
            courseId = data["CourseId"]
        
            if "Full" in data["Spots"]:
                spots = "Full"
            elif "More" in data["Spots"]:
                continue
            elif data["Spots"] == "":
                continue
            else:
                spots = re.search(r'\d+', data["Spots"]).group() + " spot(s)"

            obj = Location(location, time, spots, date, rawDate, id, courseId)
            locations.append(obj)
    
    return locations, nextDate


# raw = post_rq.post_data()  # result.text

#format to print readable json
# data = json.loads(raw)
# pretty_data = json.dumps(data, indent=4)

# print(pretty_data)

# buttonUrlExample = "https://vaughan.perfectmind.com/25076/Clients/BookMe4LandingPages/Class?widgetId=dff88c8a-0b78-4a94-9dde-250040385300&redirectedFromEmbededMode=False&classId=ab1f9a42-1e3a-b8ef-32b1-a52c9131869a&occurrenceDate=20250907"

def generateButtonUrl(id, date, register=False):
    """ 
    generates button url from id and date,
    id example - ab1f9a42-1e3a-b8ef-32b1-a52c9131869a (Location.id),
    date format - 20250907 (Location.rawDate),
    returns link to register page"""
    if not register:
        return f"https://vaughan.perfectmind.com/25076/Clients/BookMe4LandingPages/Class?redirectedFromEmbededMode=False&classId={id}&occurrenceDate={date}"
    else:
        return f"https://vaughan.perfectmind.com/25076/MyProfile/BookMe4EventParticipants?eventId={id}&occurrenceDate={date}&waitListMode=False"


def findLocationFromCourseId(courseId, date):
    maxAttempts = 3
    while maxAttempts > 0:
        locations, date = get_data(date)
        for location in locations:
            if location.courseId == courseId:
                return location
        maxAttempts -= 1
    print(f"COULD NOT FIND LOCATION WITH COURSEID: {courseId} AND DATE: {date}")


#class for each location
class Location:
    def __init__(self, location, time, spots, date, rawDate, id, courseId):
        self.location = location
        self.time = time
        self.spots = spots
        self.date = date
        self.rawDate = rawDate
        self.id = id
        self.courseId = courseId



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

