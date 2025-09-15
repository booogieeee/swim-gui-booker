import requests
import json
from datetime import datetime

url = "https://vaughan.perfectmind.com/25076/Clients/BookMe4BookingPagesV2/ClassesV2"
date = None

headers = {
  "authority": "vaughan.perfectmind.com",
  "method": "POST",
  "path": "/25076/Clients/BookMe4BookingPagesV2/ClassesV2",
  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "en-US,en;q=0.9,fr;q=0.8",
  "content-length": "649",
  "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
  "cookie": "PMSessionId=pafxrh5d23shwnlockcmv3zr; perfectmindmobilefeature=0; __RequestVerificationToken=PbSrCrbs4bEuS7ZG_c1u0V4-CiEsNBV2TDNEpUTHQoQUJMHLrErGJyHg89uy71MyuHSR8gE9uhOE3dz1Qtg_PmWygsM1; mobileWidthCookie=0; _lr_hb_-wehk4y%2Fperfectmind={%22heartbeat%22:1756869997146}; _lr_tabs_-wehk4y%2Fperfectmind={%22recordingID%22:%226-01990d9c-b251-7613-950c-440c224fe832%22%2C%22sessionID%22:0%2C%22lastActivity%22:1756869997461%2C%22hasActivity%22:false%2C%22clearsIdentifiedUser%22:false%2C%22confirmed%22:true}; ClusterId=default",
  "dnt": "1",
  "origin": "https://vaughan.perfectmind.com",
  "priority": "u=1, i",
  "referer": "https://vaughan.perfectmind.com/25076/Clients/BookMe4BookingPages/Classes?calendarId=71fe848e-2dbd-4ec5-92fa-7f2d0ad09354&widgetId=dff88c8a-0b78-4a94-9dde-250040385300&embed=False",
  "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "Windows",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
  "x-requested-with": "XMLHttpRequest"
}

payload = {
  "calendarId": "71fe848e-2dbd-4ec5-92fa-7f2d0ad09354",
  "widgetId": "dff88c8a-0b78-4a94-9dde-250040385300",
  "page": 0,
  "values": [
    {
      "Name": "Keyword",
      "Value": "",
      "Value2": "",
      "ValueKind": 9
    },
    {
      "Name": "Date Range",
      "Value": "2025-09-05T00:00:00.000Z",
      "Value2": "2025-09-16T00:00:00.000Z",
      "ValueKind": 6
    },
    {
      "Name": "Age",
      "Value": 0,
      "Value2": 1188,
      "ValueKind": 0
    }
  ],
  "after": date,
  "__RequestVerificationToken": "p85DWZVj4ienxZdB3YqxYyc4_Y-7auB9Zqmk3Je2zMNp2dGjRcs60n-2rXg11HZThB0qKYwko0k6RDgAD9V5khcIbvwlNU_-wowsR7G7_624n_Dc0"
}

def post_data():
  data = {}
  global date
  for i in range(5):
    if i == 0:
      date = str(datetime.now().date())
    result = requests.post(url=url, headers=headers, data=payload).text
    result = json.loads(result)
    data[i] = result
    date = data[i]["nextKey"]
    payload["after"] = date
  return data