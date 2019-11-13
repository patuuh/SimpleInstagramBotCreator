# Instagram account creator
# Patrik Jokela 2019
#
# NOTE: Current problem is that instagram requires mobile phone verification
# this code is not able to do that

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import randint
import pickle
from time import sleep
import mechanicalsoup
import requests
import re
import random
import string
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class InstagramBot():
    def __init__(self):
        self.proxy = []


    def __collect_proxy(self):
        r = requests.get("https://www.sslproxies.org/")
        matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised_list = [m1.replace("<td>", "") for m1 in matches]
        for proxy_str in revised_list:
            self.proxy.append(proxy_str[:-5].replace("</td>", ":"))


    def run(self):
        account_info = new_account()
        print(account_info["username"], account_info["password"])
        self.__collect_proxy()
        current_proxy = self.proxy.pop(0)

        if current_proxy != None:
            try:
                print("current proxy: " + current_proxy)
                self.creation(current_proxy, account_info)
            except Exception as e:
                print('Error!, Trying another Proxy')
                current_proxy = self.proxy.pop(0)
                print("current proxy now: " + current_proxy)
                self.creation(current_proxy, account_info)
            

    def creation(self, current_proxy, account_info):
        ''' main function used to create the account
        '''
        account_info = account_info
        options = Options()
        options.add_argument('--proxy-server=%s' % current_proxy)

        #options.add_argument('headless')
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-infobars")
        
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(chrome_options=options, executable_path=r'D:\chromedriver.exe') # PUT HERE YOUR CHROMEDRIVER LOCATION
        #options.add_argument("--incognito")
        #options.add_argument('window-size=600x600')
        #driver.get('https://itunes.apple.com/app/instagram/id389801252?mt=8&vt=lo')
        driver.get('https://www.instagram.com/accounts/emailsignup/')

        #driver.implicitly_wait(10)
        #ig_site = driver.find_element_by_link_text('Developer Website')
        #print(ig_site)
        #ig_site.click()
        driver.implicitly_wait(10)

        emailInput = driver.find_elements_by_css_selector('form input')[
            0]
        nameInput = driver.find_elements_by_css_selector('form input')[
            1]
        usernameInput = driver.find_elements_by_css_selector('form input')[
            2]
        passwordInput = driver.find_elements_by_css_selector('form input')[
            3]

        print(account_info["name"])
        mail = account_info["email"]
        emailInput.send_keys(str(mail))
        sleep(1)

        sleep(2)
        nimi = account_info["name"]
        nameInput.send_keys(str(nimi))
        sleep(1)

        driver.implicitly_wait(3)
        print(account_info["username"])
        usernameInput.send_keys(account_info["username"])
        #username_button = driver.find_elements_by_xpath(
        #   '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[5]/div/div[2]/div/button')
        #username_button[0].click()
        sleep(1) 

        #username_button[0].click()
        passW = account_info["password"]
        passwordInput.send_keys(str(passW))
        sleep(1)

        sleep(2)
        passwordInput.send_keys(Keys.ENTER)
        driver.implicitly_wait(3)
        button = driver.find_elements_by_xpath(
            '//*[@id="igCoreRadioButtonageRadioabove_18"]')
        
        sleep(1)
        button[0].click()
        button = driver.find_elements_by_xpath(
            '/html/body/div[3]/div/div[3]/div/button')
        button[0].click()
        driver.implicitly_wait(4)
        if driver.find_elements_by_xpath('//*[@id="ssfErrorAlert"]'):
            print("error, trying with another proxy")
            self.run()
        else:    
            print("done")
            store(account_info)
            self.run()



def getRandomIdentity(country, what):
    ''' Greates random indentity for the bot
    '''
    gender = random.choice(["male", "female"])
    logging.info("Gender: {}".format(gender))
    URL = "https://it.fakenamegenerator.com/gen-{}-{}-{}.php".format(
        gender, country, country)
    logging.info("Url generated: {}".format(URL))
    browser = mechanicalsoup.StatefulBrowser(
        raise_on_404=True,
        user_agent='MyBot/0.1'
    )
    page = browser.get(URL)
    address_div = page.soup.find(
        "div",
        {"class": "address"}
    )
    completename = address_div.find(
        "h3"
    )

    extra_div = page.soup.find(
        "div",
        {"class": "extra"}
    )

    all_dl = page.soup.find_all(
        "dl",
        {'class': 'dl-horizontal'}
    )

    birthday = all_dl[5].find("dd").contents[0]
    logging.info("Birthday: {}".format(birthday))

    if what == 'name':
        return completename.contents[0]

    if what == 'gender':
        return gender

    if what == 'birthday':
        return birthday

    return(completename.contents[0], gender, birthday)


def username(identity):
    n = str(random.randint(1, 99))
    name = str(identity).lower().replace(" ", "")
    username = name + n
    logging.info("Username: {}".format(username))
    return(username)


def generatePassword():
    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(12))


def store(account):
    with open(BASE_DIR + '/usernames.pkl', 'a+') as f:
        logging.info("Storing username {}".format(account['username']))
        logging.info(account)
        pickle.dump(account, f, pickle.HIGHEST_PROTOCOL)


def new_account():
    account_info = {}
    identity, gender, birthday = getRandomIdentity('finland', 0)
    account_info["name"] = getRandomIdentity('finland', 'name')
    account_info["username"] = username(account_info["name"])
    account_info["password"] = 'Mypassword123'
    account_info["email"] = create_email()
    account_info["gender"] = gender
    account_info["birthday"] = birthday
    return(account_info)

def create_email():
    ''' Creates 10 minute mail which is used to verify the email address
    '''
        options = Options()

        #options.add_argument('headless')
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-infobars")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(chrome_options=options, executable_path=r'D:\chromedriver.exe')
        url = 'https://10minutemail.net/'
        driver.get(url)

        try:

            driver.implicitly_wait(10)
            print(username)

            sleep(0.5)

            emailRaw = driver.find_elements_by_xpath('//*[@id="fe_text"]')
            email = emailRaw[0].get_attribute("value")
            print(email)

            driver.implicitly_wait(10)

            print("email created succesfully!")
            return(email)

        except Exception as e:
            print('Error!, while creating email')


def confirm_email():
    options = Options()

    #options.add_argument('headless')
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'D:\chromedriver.exe')
    url = 'https://10minutemail.net/'
    driver.get(url)

    try:

        driver.implicitly_wait(10)
        print(username)

        sleep(1)

        emailRaw = driver.find_elements_by_xpath('//*[@id="fe_text"]')
        email = emailRaw.get_attribute("value")
        print(email)

        driver.implicitly_wait(10)

        print("email created succesfully!")
        return(email)

    except Exception as e:
        print('Error!, while creating email')


bot = InstagramBot()
bot.run()
