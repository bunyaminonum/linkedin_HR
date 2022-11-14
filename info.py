import time
import getProfileLinks
from getProfileLinks import GetProfileLinks
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from connect_database import MDB
import pymongo

class Person:
    def __init__(self):
        self.infoList = {}

    def setName(self, name:dict):
        self.infoList.update(name)

    def setLocation(self, loc:dict):
        self.infoList.update(loc)

    def setWorksAt(self, worksAt:dict):
        self.infoList.update(worksAt)

    def setId(self, _id:dict):
        self.infoList.update(_id)

    # def setLink(self, link:dict):
    #     self.infoList.update(link)



class GetInfo(GetProfileLinks):
    GRADUATE_XPATH = '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[4]/div[3]/ul/li/div/div[2]/div/a/span[2]/span[1]'
    LOC_XPATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]'
    # LANGUAGE_PATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[8]/div[3]/ul/li/div/div[2]/div'
    NUM_CONNECTION_PATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[2]/div/div/div/p/span[1]'
    NUM_CONNECTION_PATH2 = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li/a/span/span'
    def __init__(self, email:str, password:str, pageNum = 1):
        super().__init__(email, password, pageNum)
        self.db = MDB()
        self.infoList = list
        self.person = Person()

    def start(self):
        self.getLink()

    def getInfo(self):
        pass

    def getLink(self):
        try:
            for link in self.linklist:

                self.driver.get(link)
                time.sleep(2)

                self.person.setId({'_id':link})
                src = self.driver.page_source

                soup = BeautifulSoup(src, 'lxml')
                intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
                # self.person.setLink({'link':link})
                try:
                    name_loc = intro.find("h1")
                    name = name_loc.get_text().strip()
                    self.person.setName({'name':name})
                except:
                    name_loc = None

                try:
                    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
                    works_at = works_at_loc.get_text().strip()
                    self.person.setWorksAt({'works at' : works_at})
                except:
                    works_at_loc = None

                try:
                    location = self.driver.find_element_by_xpath(self.LOC_XPATH).text
                    self.person.setLocation({'location' : location})
                except NoSuchElementException:
                    location = None

                self.db.collection.insert_one(self.person.infoList)

                print("Name -->", name,
                      "\nWorks At -->", works_at,
                      "\nLocation -->", location,
                        "",'\n')
                      # "\nnumber of connection -->", num_connection)
        except pymongo.errors.DuplicateKeyError:
            print("duplicate error!")



    # def chechkID(self, _id:dict):
    #     pass

            # print(graduate.text)

p = GetInfo('19701023@mersin.edu.tr', '19074747fb', 2)
p.start()

