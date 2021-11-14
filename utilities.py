import re
import bs4
from src.requestproxy import *

from bs4 import BeautifulSoup



class Utilities:
    def __init__(self):
        pass


    def parse_spans(self, spans):
        open = False
        attrs = []
        for obj in spans:
            obj = str(obj)
            attr = ""
            for i in range(len(obj)):
                if obj[i] == '<':
                    open = True
                    attrs.append(attr)
                    attr = ""
                if obj[i] == '>' or obj[i] is '\n' or obj[i] is '':
                    open = False
                    continue
                if open:
                    continue
                if not open and obj[i] is not '':
                    attr += obj[i]
        return ' '.join(attrs).split()


    def bed_and_bath_count(self, attrs):
        if attrs[0][-1] == 'R' and attrs[2][-1] == 'a':
            return attrs[0] + " " + attrs[2]
        return "N/A"

    def square_footage(self, attrs):
        for attr in attrs:
            try:
                space = int(attr)
                if space < 100: #why sell a house any smaller?
                    continue
                else:
                    return space
            except:
                continue
        return "N/A"

    def extract_attrs(self, soup):
        spans = soup.find_all('p', attrs={"class": "attrgroup"})
        attrs = self.parse_spans(spans)

        print("span:", spans)
        print("ATTRS:", attrs)
        return attrs

    def available_by(self, attrs):
        for i in range(len(attrs)):
            if attrs[i] == 'available':
                return attrs[i+1] + " " + attrs[i+2]
        return "N/A"
    def extract_json_and_mdeta(self, ad, city):
        """
        This method contains the code which scrapes a majority of the meta data of the craigslist ad.

        :param ad: The url for the ad we are looking to scrape data from
        :param city: Unused parameter get rid of this sooner then later
        :return: this returns all the meta excluding the email and or phone number from the ad
        """
        print(ad)
        ID = re.findall(string=ad, pattern="(\/\d+\.)")[0]
        ID = re.findall(string=ID, pattern="\d+")[0]
        r = send_request(ad, 'default')
        soup = BeautifulSoup(r.content, 'html.parser')

        attrs = self.extract_attrs(soup)

        coords = re.findall(string=str(soup.find(attrs={'name': 'geo.position'})), pattern='[-0-9]+\.[0-9]+')

        bed_bath_count = self.bed_and_bath_count(attrs)
        square_feet = self.square_footage(attrs)



        try:
            available = self.available_by(attrs)
        except:
            available = "N/A"
        try:
            address = soup.find('div', {'class': 'mapaddress'}).string
        except:
            address = "N/A"
        try:
            city = re.findall(string=str(soup.find(attrs={'name': 'geo.placename'})), pattern='(?<=content=")\w*')[0]
        except:
            city = "N/A"
        try:
            price = soup.find(attrs={'class': 'price'}).string
        except:
            price = "N/A"
        region = re.findall(string=str(soup.find(attrs={'name': 'geo.region'})), pattern='(?<=content=")[\w-]*')[0]
        jsondata = (soup.find('script', {'id': 'ld_breadcrumb_data'}).string)
        title = soup.find(attrs={'id': 'titletextonly'}).string
        try:
            housing = soup.find(attrs={'class': 'housing'}).contents[0]
        except:
            housing = "N/A"
        print("Address:", address)
        print("available:", available)
        print("bed and bath count:", bed_bath_count)
        print("square feet:", square_feet)
        print("ad:", ad)
        # Some housing do not have housing class

        for i in range(2):
            # Finding all tags with 'time' and scraping them
            dateposted = re.findall(string=str(soup.find_all("time")[i].string), pattern="\w.+")[0]
            dateupdated = re.findall(string=str(soup.find_all("time")[i].string), pattern="\w.+")[0]

        imgurl = re.findall(string=str(soup.find("img")), pattern='https:\/\/[^"]*')  # Puts image urls into list
        if len(imgurl) > 0:  # if there are elements in the list
            img = imgurl[0] #we want image url
            # imgloc = "./Images/" + ID + ".jpg"
            # if img.status_code == 200:
            #     with open(imgloc, "wb") as f:
            #         f.write(img.content)
            # else:
            #     imgloc = "N/A"
        else:
            img = "N/A"

        bodytemp = []
        for string in soup.find(attrs={'id': 'postingbody'}).stripped_strings:
            bodytemp.append(string)
        body = '\n'.join(bodytemp)
        return ID, body, city, coords, dateposted, dateupdated, housing, img, jsondata, price, region, title, attrs,\
               address, available, bed_bath_count, square_feet

