import requests
import re
import lxml
from lxml.html import fromstring
import random
import csv

most_common_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
]

def send_request(url, scraper):
    """
    Generalized send_request, specify which proxy system to use.

    :param url: Desired URL we seek to scrape
    :param scraper: Desired scraper we seek to use
    :return: Get request to the specified url with specified proxy
    """

    if (scraper == "scrapingbee"):
        response = scrapingbee(url, "false")
    elif (scraper == "free"):
        response = free_proxy(url)
    elif (scraper == "crawlera"):
        response = crawlera(url)
    elif (scraper == "default"):
        response = requests.get(url)
    else:
        raise Exception("No suitable proxy method given")
    return response

def free_proxy(url):
    """
    This method extracts a single proxy from the list of proxies acquired from
    get_proxies and makes a request to the specific proxy we chose

    :param url: URL to the proxy
    :return: Returns a get request from the url we specify from the random proxy we have chosen
    """

    proxylist = []
    #if we do not have any proxies then call get_proxies to make a list
    if len(proxylist) == 0:
        proxylist = get_proxies()
    proxy = random.choice(proxylist)
    proxylist.remove(proxy)
    proxies = {"http": proxy, "https": proxy}
    return requests.get(url=url, proxies=proxies)

def get_proxies():
    """
    Method for getting a list of proxies. We want to be using different proxies so that Craigslist
    doesn't ban our machine's IP for too many requests to there website

    :return: List of Proxy urls
    """
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    #fromstring(response.text) returns a 1-D arrary from text data in a string. Maybe this was for debugging?
    parser = fromstring(response.text)
    proxies = re.findall("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).*",
                         response.text, re.MULTILINE)
    return (proxies)

def scrapingbee(url, js):
    """
    Sends get request to the Scraping Bee api

    :param url: URL from a specified domain
    :param js: javascript -- not really sure what this param is for
    :return: Get request for the URL using scraping Bee api
    """
    return (requests.get(url=url,
                         params={
                             "api_key": "PVOYIDL5FRF939XKB13NVDML045BDNRXG9910JNQWEFGNJS61PGGPPPXP72CJSZ4KNPA0F4VPQWNZHHH",
                             "url": url,
                             "render_js": js}))

def crawlera(url):
    """
    Sends get request through crawlera

    :param url: URL from specified domain
    :return: Get request for the URL using crawlera
    """
    counter = int(retrieve_count())
    if (counter > 9500):
        raise Exception("Too close to usage cap-- change proxies or manually change cap")
    proxy_host = "proxy.crawlera.com"
    proxy_port = "8010"
    proxy_auth = "c47caddc62f54928b5d825cd0f331e78:"  # Make sure to include ':' at the end
    proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
               "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
    counter = counter + 1
    r = requests.get(url, proxies=proxies, verify=False)
    update_count(str(counter))
    return r

def update_count(count):
    with open("UsageCount", "w") as f:
        f.write(count)

def retrieve_count():
    with open("UsageCount", "r") as f:
        return (f.readline().strip())

# Returns list of proxies from freeproxylist. Unfortunately, requires a proxy... WIP

# def get_proxy_from_freeproxylist():
#    proxies = ''
#    counter = 1
#    has_next_page = True
#    r = requests.get('http://freeproxylists.net/?c=&pt=&pr=HTTPS&a%5B%5D=2&u=0')
#    counter += 1
#
#    soup = BeautifulSoup(r.content, 'html.parser')
#    print(soup)
#    lines = soup.select('table.DataGrid tbody tr')
#    for i in lines[1:]: 
#        
#        if not 'adsbygoogle' in i.text:
#            proxy = i.select('td a')[0].text
#            port = i.select('td')[1].text
#            proxies += proxy + ':' + port + '\n'
#    return(proxies)

## Generalized proxy request-- WIP

# def request_proxy(url):
#    #random_proxy = random.choice(proxylist)
#    # random_proxy = "62.210.75.50:13732"
#    payload = {
#            "proxies": {"http": loop.run_until_complete(tasks)},
#        "url": url,
#        "verify": True,
#        "timeout": 60,
#        "headers": {
#            "User-Agent": random.choice(most_common_user_agents),
#            "referrer": "https://www.google.com",
#    }}
#    return(requests.get(**payload))
