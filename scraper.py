import requests
import re

# locating elements from HTML using selenium https://www.youtube.com/watch?v=b5jt2bhSeXs
import csv
import random
from bs4 import BeautifulSoup
import json
from requestproxy import send_request
from Captcha import captcha_solver
import utilities
# TODO: Elian

# - figure out why moving the random city choice outside of the for loop breaks the program

# - Update README and upload to github
# - Find a way to fix the json file so that it is framed --> fixed this but I wont be able to test it works until I finish captcha
# - Figure out why the csv writing is not contained on a single line
# - reformat how the program writes to csv so it looks like what Dr. Bryan gave me


utils = utilities.Utilities()

cities = ['nyc', 'losangeles', 'chicago', 'houston', 'phoenix', 'philadelphia', 'sanantonio', 'sandiego', 'dallas',
          'sfbay']
finads = []

# This gives a list of ad urls we have already scraped, so that we don't re-scrape them
# if not utils.is_empty_csv('housingData.csv'):
with open('housingData.csv', encoding='utf-8', errors='ignore') as f:
    csv_reader = csv.reader((l.replace('\0', '') for l in f), delimiter=',')

    next(csv_reader)
    for lines in csv_reader:
        # print(lines)
        finads.append(lines[1])

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


###### helpers #######
# def retrieve_all_ads(ads, city, entrynum, soup):
#     entrynum = entrynum + 120
#     r = send_request('https://' + city + '.craigslist.org/d/apartments-housing-for-rent/search/apa?s=' + str(
#         entrynum) + '&availabilityMode=0&bundleDuplicates=1&postedToday=1', scraper='default')
#     soup = BeautifulSoup(r.content, 'html.parser')
#     # Regular Expression only works for houston ads ====> FIX THIS
#     # ads.extend adds the list of links to the ads list
#     ads.extend(
#         re.findall(pattern=re.compile('(?<=")\S*houston.craigslist.org/apa/d\S*(?=")'), string=str(soup)))
#     return soup
CITIES = ["auburn", "bham", "dothan", "shoals", "gadsden", "huntsville", "mobile", "montgomery", "tuscaloosa", "anchorage", "fairbanks", "kenai", "juneau", "flagstaff", "mohave", "phoenix", "prescott", "showlow", "sierravista", "tucson", "yuma", "fayar", "fortsmith", "jonesboro", "littlerock", "texarkana", "bakersfield", "chico", "fresno", "goldcountry", "hanford", "humboldt", "imperial", "inlandempire", "losangeles", "mendocino", "merced", "modesto", "monterey", "orangecounty", "palmsprings", "redding", "sacramento", "sandiego", "sfbay", "slo", "santabarbara", "santamaria", "siskiyou", "stockton", "susanville", "ventura", "visalia", "yubasutter", "boulder", "cosprings", "denver", "eastco", "fortcollins", "rockies", "pueblo", "westslope", "newlondon", "hartford", "newhaven", "nwct", "delaware", "washingtondc", "daytona", "keys", "fortlauderdale", "fortmyers", "gainesville", "cfl", "jacksonville", "lakeland", "lakecity", "ocala", "okaloosa", "orlando", "panamacity", "pensacola", "sarasota", "miami", "spacecoast", "staugustine", "tallahassee", "tampa", "treasure", "westpalmbeach", "albanyga", "athensga", "atlanta", "augusta", "brunswick", "columbusga", "macon", "nwga", "savannah", "statesboro", "valdosta", "honolulu", "boise", "eastidaho", "lewiston", "twinfalls", "bn", "chambana", "chicago", "decatur", "lasalle", "mattoon", "peoria", "rockford", "carbondale", "springfieldil", "quincy", "bloomington", "evansville", "fortwayne", "indianapolis", "kokomo", "tippecanoe", "muncie", "richmondin", "southbend", "terrehaute", "ames", "cedarrapids", "desmoines", "dubuque", "fortdodge", "iowacity", "masoncity", "quadcities", "siouxcity", "ottumwa", "waterloo", "lawrence", "ksu", "nwks", "salina", "seks", "swks", "topeka", "wichita", "bgky", "eastky", "lexington", "louisville", "owensboro", "westky", "batonrouge", "cenla", "houma", "lafayette", "lakecharles", "monroe", "neworleans", "shreveport", "maine", "annapolis", "baltimore", "easternshore", "frederick", "smd", "westmd", "boston", "capecod", "southcoast", "westernmass", "worcester", "annarbor", "battlecreek", "centralmich", "detroit", "flint", "grandrapids", "holland", "jxn", "kalamazoo", "lansing", "monroemi", "muskegon", "nmi", "porthuron", "saginaw", "swmi", "thumb", "up", "bemidji", "brainerd", "duluth", "mankato", "minneapolis", "rmn", "marshall", "stcloud", "gulfport", "hattiesburg", "jackson", "meridian", "northmiss", "natchez", "columbiamo", "joplin", "kansascity", "kirksville", "loz", "semo", "springfield", "stjoseph", "stlouis", "billings", "bozeman", "butte", "greatfalls", "helena", "kalispell", "missoula", "montana", "grandisland", "lincoln", "northplatte", "omaha", "scottsbluff", "elko", "lasvegas", "reno", "nh", "cnj", "jerseyshore", "newjersey", "southjersey", "albuquerque", "clovis", "farmington", "lascruces", "roswell", "santafe", "albany", "binghamton", "buffalo", "catskills", "chautauqua", "elmira", "fingerlakes", "glensfalls", "hudsonvalley", "ithaca", "longisland", "newyork", "oneonta", "plattsburgh", "potsdam", "rochester", "syracuse", "twintiers", "utica", "watertown", "asheville", "boone", "charlotte", "eastnc", "fayetteville", "greensboro", "hickory", "onslow", "outerbanks", "raleigh", "wilmington", "winstonsalem", "bismarck", "fargo", "grandforks", "nd", "akroncanton", "ashtabula", "athensohio", "chillicothe", "cincinnati", "cleveland", "columbus", "dayton", "limaohio", "mansfield", "sandusky", "toledo", "tuscarawas", "youngstown", "zanesville", "lawton", "enid", "oklahomacity", "stillwater", "tulsa", "bend", "corvallis", "eastoregon", "eugene", "klamath", "medford", "oregoncoast", "portland", "roseburg", "salem", "altoona", "chambersburg", "erie", "harrisburg", "lancaster", "allentown", "meadville", "philadelphia", "pittsburgh", "poconos", "reading", "scranton", "pennstate", "williamsport", "york", "providence", "charleston", "columbia", "florencesc", "greenville", "hiltonhead", "myrtlebeach", "nesd", "csd", "rapidcity", "siouxfalls", "sd", "chattanooga", "clarksville", "cookeville", "jacksontn", "knoxville", "memphis", "nashville", "tricities", "abilene", "amarillo", "austin", "beaumont", "brownsville", "collegestation", "corpuschristi", "dallas", "nacogdoches", "delrio", "elpaso", "galveston", "houston", "killeen", "laredo", "lubbock", "mcallen", "odessa", "sanangelo", "sanantonio", "sanmarcos", "bigbend", "texoma", "easttexas", "victoriatx", "waco", "wichitafalls", "logan", "ogden", "provo", "saltlakecity", "stgeorge", "burlington", "charlottesville", "danville", "fredericksburg", "norfolk", "harrisonburg", "lynchburg", "blacksburg", "richmond", "roanoke", "swva", "winchester", "bellingham", "kpr", "moseslake", "olympic", "pullman", "seattle", "skagit", "spokane", "wenatchee", "yakima", "charlestonwv", "martinsburg", "huntington", "morgantown", "wheeling", "parkersburg", "swv", "wv", "appleton", "eauclaire", "greenbay", "janesville", "racine", "lacrosse", "madison", "milwaukee", "northernwi", "sheboygan", "wausau", "wyoming", "micronesia", "puertorico", "virgin", "brussels", "bulgaria", "zagreb", "copenhagen", "bordeaux", "rennes", "grenoble", "lille", "loire", "lyon", "marseilles", "montpellier", "cotedazur", "rouen", "paris", "strasbourg", "toulouse", "budapest", "reykjavik", "dublin", "luxembourg", "amsterdam", "oslo", "bucharest", "moscow", "stpetersburg", "ukraine", "bangladesh", "micronesia", "jakarta", "tehran", "baghdad", "haifa", "jerusalem", "telaviv", "ramallah", "kuwait", "beirut", "malaysia", "pakistan", "dubai", "vietnam", "auckland", "christchurch", "wellington", "buenosaires", "lapaz", "belohorizonte", "brasilia", "curitiba", "fortaleza", "portoalegre", "recife", "rio", "salvador", "saopaulo", "caribbean", "santiago", "colombia", "costarica", "santodomingo", "quito", "elsalvador", "guatemala", "managua", "panama", "lima", "puertorico", "montevideo", "caracas", "virgin", "cairo", "addisababa", "accra", "kenya", "casablanca", "tunis"]

def city_ads(city, soup):
    # After we get the code working we will add this so that it works for whatever city we choose
    if city == 'nyc':
        return re.findall(pattern=re.compile('(?<=")\S*newyork.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'losangeles':
        return re.findall(pattern=re.compile('(?<=")\S*losangeles.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'chicago':
        return re.findall(pattern=re.compile('(?<=")\S*chicago.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'houston':
        return re.findall(pattern=re.compile('(?<=")\S*houston.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'phoenix':
        return re.findall(pattern=re.compile('(?<=")\S*phoenix.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'philadelphia':
        return re.findall(pattern=re.compile('(?<=")\S*philadelphia.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'sanantonio':
        return re.findall(pattern=re.compile('(?<=")\S*sanantonio.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'sandiego':
        return re.findall(pattern=re.compile('(?<=")\S*sandiego.craigslist.org/\S*(?=")'), string=str(soup))
    elif city == 'dallas':
        return re.findall(pattern=re.compile('(?<=")\S*dallas.craigslist.org/\S*(?=")'), string=str(soup))
    else:
        return re.findall(pattern=re.compile('(?<=")\S*sfbay.craigslist.org/\S*(?=")'), string=str(soup))

# def write_json_data(jsondata):
#     # this does not write a valid json file ==>  "JSON is not a framed protocol, so trying to serialize multiple
#     # objects with repeated calls to dump() using the same fp will result in an invalid JSON file.
#     # FIX THIS
#     print("writing json data")
#     with open('housingdata.json', 'a+') as f:
#         data = json.loads(jsondata)
#         json.dump(data, f, indent="")
def remove_scraped_ads(ads):
    print("removing scraped ads")
    for ad in ads:
        if ad in finads:
            ads.remove(ad)


# mess around with n values so that the program scrapes new cities with less ads
def adscraper(n=1000):
    """
    This is the main function where bring all the functions together. We are making a request to find proxies.
    Then we scrape the different ads from a random city of choice and then write all of the scraped metadata

    :param n: Number of total ads we are looking to scrape
    :return: This method doesn't return antyhing however it writes to a csv which should appear in the src folder
    """
    send_request_ad = 0

    while len(finads) < n:
        print("RESTART\n")
        city = random.choice(cities)

        # send request. This request goes straight to the apartments listing page with options "posted today" and "bundle duplicates"
        r = send_request(
            'https://' + city + '.craigslist.org/search/apa?postedToday=1&bundleDuplicates=1&min_price=5&availabilityMode=0&sale_date=all+dates',
            scraper='default')
        soup = BeautifulSoup(r.content, 'html.parser')
        ads = utils.scan_links(city_ads(city, soup))  # extracts ads for correct city
        entrynum = 0

        print('Random city chosen:', city)
        print("All ads acquired", len(ads))

        # while re.search(pattern=re.compile('search and you will find'), string=str(soup)) == None:
        #     r = send_request('https://' + city + '.craigslist.org/d/apartments-housing-for-rent/search/apa?s=' + str(
        #         entrynum) + '&availabilityMode=0&bundleDuplicates=1&postedToday=1', scraper='default')
        #     entrynum = entrynum + 120
        #     soup = BeautifulSoup(r.content, 'html.parser')
        #     ads.extend(ads)
        while True:
            r = send_request('https://' + city + '.craigslist.org/d/apartments-housing-for-rent/search/apa?s=' + str(entrynum), scraper='default')
            if r.status_code != 200 or entrynum > n:
                print("LEAVING WHILE LOOP!")
                break
            entrynum += 120
            soup = BeautifulSoup(r.content, 'html.parser')
            new_ads = utils.scan_links(city_ads(city,soup))
            print(ads)
            ads.extend(new_ads)

        # removes duplicates
        print("len ads before removing duplicates:", len(ads))
        print("len ads when we make a set:", len(set(ads)))
        ads = list(dict.fromkeys(ads))
        print("len ads after removing duplicates:", len(ads))
        # removes already scraped ads
        remove_scraped_ads(ads)

        # iterate through all of the ads we have grabbed
        print("iterating through ads to retrieve metadata", ads)

        # json_objects = []
        for ad in ads:
            send_request_ad += 1
            print("Successfully gathered ads:", send_request_ad)
            ID, body, city, coords, dateposted, dateupdated, housing, img, jsondata, price, region, title, attrs, \
            address, available, bed_bath_count, square_feet, phone_number, email = utils.extract_json_and_mdeta(
                ad, city)
            #this will see if there is a phone number in the text body


            # TODO: uncomment this if captcha works
            # try:
            #     email = captcha_solver(ad)
            #     print("email:", email)
            # except:
            #     continue
            with open('housingData.csv', 'a+', newline='',encoding='utf8') as f:
                csv_writer = csv.writer(f)
                try:
                    csv_writer.writerow(
                        [ad, ID, body, city, coords, dateposted, dateupdated, housing, img, jsondata, price, region, title,\
           address, available, bed_bath_count, square_feet, phone_number, email])
                except Exception as e:
                    finads.append(ad)
                    continue
            # json_objects.append(jsondata)
            finads.append(ad)

        # write_json_data(str(json_objects))


adscraper()
