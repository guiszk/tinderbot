from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import pandas as pd
import shutil
import random
import time

class TinderBot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=selenium")
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.'
            '4044.113 Safari/537.36'
        )
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://tinder.com/app/recs')

    def getage(self):
        try:
            age = self.driver.find_elements_by_xpath('//*[@itemprop="age"]')[-1].get_attribute('innerText')
        except:
            age = self.river.find_element_by_xpath('//*[@class="Whs(nw) Fz($l)"]').get_attribute('innerText')
        return age

    def getimg(self, name):
        try:
            imgurl = self.driver.find_element_by_xpath(f'//*[@aria-label="Profile slider"]').get_attribute('style').split('url(\"')[1].split('\")')[0]
        except:
            imgurl = self.driver.find_element_by_xpath(f'//*[@aria-label="{name}"]').get_attribute('style').split('url(\"')[1].split('\")')[0]
        return imgurl

    def getname(self):
        try:
            name = self.driver.find_elements_by_xpath('//*[@itemprop="name"]')[-1].get_attribute('innerText')
        except:
            name = self.driver.find_element_by_xpath('//*[@class="Fz($xl) Fw($bold) Fxs(1) Fxw(w) Pend(8px) M(0) D(i)"]').get_attribute('innerText')
        return name

    def getabout(self):
        try:
            about = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[4]/div[4]/div/div[2]/div/div[2]').get_attribute('innerText')
        except:
            try:
                about = self.driver.find_elements_by_xpath('//*[@class="BreakWord Whs(pl) Fz($ms) Ta(start) Animn($anim-slide-in-left) Animdur($fast) LineClamp(5,118.125px)"]')[-1].get_attribute('innerText')
            except:
                about = ''
        try:
            extra = self.driver.find_element_by_xpath('//*[@class="P(16px) Us(t) C($c-secondary) BreakWord Whs(pl) Fz($ms)"]').get_attribute('innerText')
        except:
            extra = ''

        ret = about + extra
        if('away' not in ret):
            try:
                unsorted = self.driver.find_element_by_xpath('//*[@class="D(f) Jc(sb) Us(n) Px(16px) Py(10px)"]').get_attribute('innerText')
            except:
                unsorted = ''
        ret += unsorted
        return ret

    def getid(self):
        id = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[2]').get_attribute('id')
        return id

    def downloadphoto(self, url, name, age, id):
        response = requests.get(url, stream=True)
        fname = 'images/' + age + '_' + '_'.join(name.split()).lower() + '_' + id + '.png'
        with open(fname, 'wb') as fi:
            fi.write(response.content)
        print(fname + ' saved.')

    def like(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_RIGHT).perform()

    def dislike(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_LEFT).perform()

    def message(self, msg):
        matchtextarea = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[2]/div/div/div[1]/div/div[3]/div[3]/form/textarea')
        matchtextarea.send_keys(msg)
        matchtextarea.send_keys(Keys.ENTER)

    def checklimit(self):
        try:
            limtxt = self.driver.find_element_by_xpath('//*[@class="D(f) Jc(sb) Us(n) Px(16px) Py(10px)"]').get_attribute('innerText')
        except:
            limtxt = ''
        if(limtxt):
            return True
        else:
            return False

    def run(self):
        name = self.getname()
        age = self.getage()
        imgurl = self.getimg(name)
        about = self.getabout()
        id = self.getid()
        self.downloadphoto(imgurl, name, age, id)

        print(name, age)
        #debugging
        #print(imgurl)
        print(about)
        #print(id)

        fname = 'images/' + age + '_' + '_'.join(name.split()).lower() + '_' + id + '.png'

        info = {
            'name': [name],
            'age': [age],
            'about': [about],
            'id': [id],
            'fname': [fname]
        }

        #write data to csv (WIP)
        df = pd.DataFrame(info)
        df.to_csv("tinder.csv", header=False, na_rep='N/A', mode='a')

        #random sleep intervals to avoid bot detection
        time.sleep(random.randint(0, 70)/100)

        #will like 75% of people
        like_prob = 75

        if(random.randint(0, 100) < like_prob):
            self.like()
        else:
            self.dislike()

        try:
            #will message 70% of matches
            ans_prob = 70

            if(random.randint(0, 100) < 70):
                time.sleep(random.randint(0, 100)/100)

                #change your message here
                pers_message = 'Hey!'

                self.message(pers_message)
            else:
                time.sleep(random.randint(0, 100)/100)
                self.closematch()
        except:
            pass

        time.sleep(random.randint(0, 30)/100)
        if(checklimit()):
            gotitb = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/button')
            gotitb.click()
            print('Daily likes limit reached.')
        else:
            self.run()

bot = TinderBot()
time.sleep(10)
bot.run()
