import os
import random
import sys
import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time





from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha



PATH = r'C:\Users\Elian\anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe'
# def crowd_captcha(ads):
#     #load the file
#     with open("crowdCaptcha.html") as inf:
#         txt = inf.read()
#         soup = BeautifulSoup(txt)
#
#
#
#     #save the file
#     with open("crowdCaptcha.html") as outf:
#         outf.write(str(soup))

def captcha_solver(ad):
    # 1 initialize the captcha solver
    api_key_id = '56fd8ea7c70ba057be29491956d8bdde'
    # api_key = os.getenv('APIKEY_2CAPTCHA', api_key_id)
    # solver = TwoCaptcha(api_key)



    # 2 Open the craigslist page
    driver = webdriver.Firefox(executable_path=PATH)
    driver.get(ad)
    button = driver.find_element_by_class_name("reply-button")  # find the reply button
    button.click()

    time.sleep(5)

    # 4 extract the dynamically loaded html
    soup_file = driver.page_source
    soup = BeautifulSoup(soup_file, features="lxml")
    alt_sitekey = soup.find('div', {'class': 'h-captcha'})['data-sitekey'] #SITEKEY EXTRACTED!
    # print("alt_sitekey:", alt_sitekey)
    # time.sleep(4)
    # gwidget = re.findall(string=str(soup.findAll(attrs={'name': 'g-recaptcha-response'})),
    #                              pattern='[g|h]-[re]*captcha-response-[0-9a-zA-Z]{12}')[0]
    # code = gwidget[len(gwidget)-12:]
    # print("code:", code)
    # hwidget = "h-captcha-response-" + code
    #
    # iframe_src = re.findall(string=str(soup.findAll('iframe')), pattern='(?<=src=\")[\S-]*\"')[1]
    # iframe_src = iframe_src[:-1]
    # print("iframe_src:", iframe_src)

    #5 retrieve captcha token
    try:
        r2 = requests.get(
            'http://2captcha.com/in.php?key=' + api_key_id + '&method=hcaptcha&sitekey=' + alt_sitekey + '&pageurl=' + ad)

        print("r2:", r2.text)
        print('http://2captcha.com/in.php?key=' + api_key_id + '&method=hcaptcha&sitekey=' + alt_sitekey + '&pageurl=' + ad)
    except Exception as e:
        print("Exiting with code:", e)
        sys.exit(e)

    # else:
    captcha_id = re.findall("(?<=OK\|).*", r2.text)[0]
    print("captcha_id:", captcha_id)

    print('Sent CAPTCHA successfully, awaiting solve')
     # According to 2Captcha this can be anywhere from 15-20 seconds
    time.sleep(random.choice(range(15,17)))
    while True:
        time.sleep(5)
        r3 = requests.post('http://2captcha.com/res.php?key=' + api_key_id + '&action=get&id=' + captcha_id)
        if r3.text == "CAPTCHA_NOT_READY": continue
        else: break
        print(r3)
    captcha_token = re.findall("(?<=OK\|).*", r3.text)[0]
    print("Captcha token type:", type(captcha_token))
    print("Captcha token:", captcha_token)

    val = "document.querySelector(\"div.h-captcha iframe\").setAttribute(\"data-hcaptcha-response\", \""+captcha_token+"\");"
    print("VAL >>>>", val)
    # driver.execute_script(
    #     "document.querySelector(\"div.h-captcha iframe\").setAttribute(\"data-hcaptcha-response\", \""+captcha_token+"\");")


    # container = driver.find_element_by_id(gwidget)
    # driver.execute_script("arguments[0].style.display = 'block';", container)
    # container2 = driver.find_element_by_id(hwidget)
    # driver.execute_script("arguments[0].style.display = 'block';", container2)
    # # container.click()
    # container.send_keys(captcha_token)
    # # container2.click()
    # container2.send_keys(captcha_token)
    # driver.switch_to.frame(frames[2])
    # submit = driver.find_element_by_class_name("button-submit")
    # driver.execute_script("arguments[0].click();", submit)



    # print("submit text:", submit.text)
    # submit.click()

    # driver.execute_script("___grecaptcha_cfg.clients['1']['Z']['Z']['callback']('%s')" %captcha_token)
#     # driver.execute_script('document.getElement')
#     # id = "g-recaptcha-response-" + gwidget
#     # driver.execute_script('document.getElementByID('+id+').submit();')
#
#
#
#     time.sleep(15)
#
#
#
#
#     # _by_xpath("/html/body/section/section/header/div[2]/div/div[1]/textarea[1]").send_keys(captcha_token)
#
#
#     # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
#     # captcha_token = re.findall("(?<=OK\|).*", r3.text)[0]
#
#
#     # new_reply = driver.find_element_by_name("reply_button")
#     # new_reply.click()
#     # print(driver.page_source.encode('utf-8'))
#     # email = soup.find({'class', 'mailapp'})
#     # print(email)
#     # url = driver.current_url
#
#
# ######open new driver that hopefully acknowledges that captcha has been solved ###################
# #                                                                                                #
# ##################################################################################################
#     #save the cookies from the solved website after captcha has been solved
#
#     #new driver with added cookies
# #     driver2 = webdriver.Chrome(PATH)
# #     driver2.get(url)
# #     cookies = pickle.load(open("cookies.pkl", "rb"))
# #     for cookie in cookies:
# #         print("adding cookies:", cookie)
# #         driver2.add_cookie(cookie)
# #
# #     #if we open a pickle file we must close it to prevent a memory leak
# #     with open('cookies.pkl','rb') as cookie_file:
# #         cookies = pickle.load(cookie_file)
# #     #if this works how I think it does the page should update and recognize that captcha has been solved
# #     #if so, we can then press the reply button
# #     button2 = driver2.find_element_by_class_name("reply-button")  # find the reply button
# #     button2.click()
# #
# #     #then click the email button
# #     email_button = driver2.find_element_by_class_name("show-email")
# #     email_button.click()
# #     email_info = driver2.find_element_by_class_name("mailapp")
# #
# #     #add try statement if there is a 'show contact' button"
# #     try:
# #         contact_button = driver2.find_element_by_link_text("#")
# #         contact_button.click()
# #         text = driver2.find_element_by_id("postingbody").text
# #         info = re.findall(text, "[0-9]{3}-[0-9]{3}-[0-9]{4}")
# #     except:
# #         info = "not found"
# #
# # ##################################################################################################
# # #                                                                                                #
# # ##################################################################################################
# #     #TODO : https://www.youtube.com/watch?v=gykWsW9PxoU
# #     print("Info:", info)
# #     print("Email:", email_info)
# #     driver.close()
    return alt_sitekey


#### /// Another approach worth trying /// ####

# That happens because 'g-recaptcha-response' element doesn't exist at this moment.
# As far as I know it's created at the moment you click on "Reply" and deleted when ReCaptcha verification is finished.
#
# Looks like the best way to deal with Craigslist is to make GET/POST requests without browser simulation.
# The process looks like this:
# 1. Make GET request to the URL of the post.
# https://chicago.craigslist.org/nch/act/d/looking-for-fantasy-football/6653564099.html
# 2. Make GET request to "Reply" URL: https://chicago.craigslist.org/reply/chi/act/6653564099
# Parse the HTML to find "n" element value.
# 3. Make POST request to "Reply" URL: https://chicago.craigslist.org/reply/chi/act/6653564099
# providing two fields: "n" (found on previous step) and "g-recaptcha-response" (that you got from API). Also try V3 method to get a token as they can be using V3 at the moment.
# 4. If you're lucky Craigslist will return you an HTML with contact info.

#### /// ----------------------------- /// ####