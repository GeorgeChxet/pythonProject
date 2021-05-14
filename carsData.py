from sqlite3.dbapi2 import Cursor
from typing import Counter
import requests
import json
import sqlite3


# nabiji #1
request = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/GetWMIsForManufacturer/hon?format=json")
statuscode = request.status_code
headers = request.headers


# nabiji #2
rjson = json.loads(request.text)
results = rjson['Results']

storeJson =  open('carData.json', 'w')
json.dump(rjson, storeJson)
storeJson.close()


# nabiji 3 
while True:
    country = input("შეიყვანეთ მწარმოებელი ქვეყანა: (USA, UK, ITALY, THAILAND, CHINA, VIETNAM, SPAIN, MEXICO, CANADA, JAPAN, BELGIUM, HONG KONG) ").strip()
    countrys = []
    for item in results:
        if item['Country'] != None:
            if item['Country'].lower() == country.lower() or country.lower() in item['Country'].lower():
                if item['Name'] not in countrys:
                    countrys.append(item['Name'])
    print(f"ამ ქვეყანაზე ნაპოვნია {len(countrys)} მწარმოებელი: ")
    for i in countrys:
        print(f"• {i}")
    ask = input("გსურთ გაგრძელება (y/n): ").strip()
    if ask == "n":
        break
    elif ask == "y":
        continue



#  nabiji 4
connection = sqlite3.connect("Cars.db")
cursor = connection.cursor()
# cxrilshi sheinaxeba API dan wamogebuli informacia manqanis mwarmoebeli qveknis, mwarmoeblis, manqanis tipis da gamoshvebis tarigis shesaxeb 
cursor.execute("""CREATE TABLE IF NOT EXISTS cars(
                    cid INTEGER PRIMARY KEY AUTOINCREMENT,
                    countryName VARCHAR,
                    manufacturer VARCHAR,
                    carType VARCHAR,
                    releaseDate Varchar)""")

for dict in results:
    if dict['Country'] == None:
        continue
    else:
        country = dict['Country']
        manufacturer = dict['Name']
        carType = dict['VehicleType']
        releasedate = dict['DateAvailableToPublic']
        cursor.execute("INSERT INTO cars(countryName, manufacturer, carType, releaseDate) VALUES (?, ?, ?, ?)",(country, manufacturer, carType, releasedate))
        connection.commit()

cursor.close()
connection.close()
