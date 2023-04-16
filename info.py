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
        print(self.infoList)
    def setLocation(self, loc:dict):
        self.infoList.update(loc)

    def setWorksAt(self, worksAt:dict):
        self.infoList.update(worksAt)

    def setId(self, _id:dict):
        self.infoList.update(_id)

    def setConnectionNum(self, con_num:dict):
        self.infoList.update(con_num)
    # def setLink(self, link:dict):
    #     self.infoList.update(link)

    def setEducation(self, edu:dict):
        self.infoList.update(edu)

    def setDescription(self, desc:dict):
        self.infoList.update(desc)

    def setSkills(self, skills:dict):
        self.infoList.update(skills)

class GetInfo(GetProfileLinks):
    GRADUATE_XPATH = '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[4]/div[3]/ul/li/div/div[2]/div/a/span[2]/span[1]'
    LOC_XPATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]'
    # LANGUAGE_PATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[8]/div[3]/ul/li/div/div[2]/div'
    FOLLOWERS = 'pvs-header__subtitle'
    NUM_CONNECTION_PATH2 = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li/a/span/span'
    # BEST_SKILLS_CLASS = 'pvs-list__outer-container'
    EDUCATION_INFO = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[4]/div[3]'
    DESCRIPTION_PATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[3]/div/div/div'

    def __init__(self, email:str, password:str, pageNum = 2):
        super().__init__(email, password, pageNum)
        self.db = MDB()
        self.personInfo = []
        self.person = Person()
    def start(self):
        self.getLink()

    def getInfo(self):
        pass

    def checkDuplicate(self, _id):
        info = self.db.collection.find({})
        for i in info:
            if i['_id'] == _id:
                break
        return _id

    def getLinklistFromDB(self):
        attr = self.db.collection.find({})
        for i in attr:
            self.linkListFromDB.append(i['_id'])
            
    def getLink(self):
        try:
            for link in self.linklist:
                linkInfo = self.db.collection.find_one({'_id':link})
                if link not in self.db.linklistFromDB:
                    self.driver.get(link)
                    time.sleep(2)

                    self.person.setId({'_id':link})
                    src = self.driver.page_source

                    soup = BeautifulSoup(src, 'lxml')
                    # print(soup)
                    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
                    # self.person.setLink({'link':link})
                    try:
                        name_loc = intro.find("h1")
                        name = name_loc.get_text().strip()
                        self.person.setName({'name':name})
                    except:
                        name_loc = ''

                    try:
                        works_at_loc = intro.find("div", {'class': 'text-body-medium'})
                        works_at = works_at_loc.get_text().strip()
                        self.person.setWorksAt({'works at' : works_at})

                    except:
                        works_at_loc = ''

                    try:
                        location = self.driver.find_element_by_xpath(self.LOC_XPATH).text
                        self.person.setLocation({'location' : location})
                    except NoSuchElementException:
                        location = ''

                    try:
                        follow = self.driver.find_element_by_class_name(self.FOLLOWERS).text
                        follow = float(str(follow).split()[0].strip().replace(',','.'))
                        self.person.setConnectionNum({'num followers':follow})
                    except NoSuchElementException:
                        follow = ''

                    try:
                        education = self.driver.find_element_by_xpath(self.EDUCATION_INFO)
                        edu = education.find_elements_by_tag_name("li")
                        edulist = list

                        for item in edu:
                            educationInfo = item.text
                            self.person.setEducation({'education':educationInfo})
                    except:
                        educationInfo = ''

                    try:
                        see_more = self.driver.find_element_by_class_name(
                            'inline-show-more-text__link-container-collapsed')
                        see_more.click()
                        self.driver.implicitly_wait(2)
                        ul = soup.find('ul')
                        description = self.driver.find_element_by_xpath(self.DESCRIPTION_PATH).text
                        self.person.setDescription({'description':description})
                    except:
                        description = ' '

                    self.db.collection.insert_one(self.person.infoList)

                    # self.personInfo.append(self.person.infoList)
                    # print(self.personInfo)
                    print("Name -->", name,
                          "\nWorks At -->", works_at,
                          "\nLocation -->", location,
                          "\n num followers -->", follow,
                          "\neducation -->", educationInfo,
                          "\ndescription -->", description)

                else:
                    continue
                      # "\nnumber of connection -->", num_connection)
        except pymongo.errors.DuplicateKeyError:
            print("duplicate error!")

    # def chechkID(self, _id:dict):
    #     pass

            # print(graduate.text)

p = GetInfo('19701023@mersin.edu.tr', '19074747fb', 2)
p.start()

