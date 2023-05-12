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
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

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
    LOC_XPATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]'
    def __init__(self, email:str, password:str, pageNum = 2):
        super().__init__(email, password, pageNum)

        self.db = MDB()
        # self.personInfo = []
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
                personInfo = {
                    'education': [],
                    'experience': []
                }
                linkInfo = self.db.collection.find_one({'_id':link})
                if link not in self.db.linklistFromDB:
                    self.driver.get(link)
                    self.driver.implicitly_wait(10)
                    time.sleep(2)
                    profile_link = self.driver.current_url #must used for access to education and experience pages
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

                    #Education
                    education_list = self.education(profile_link)
                    experience_list = self.experience(profile_link)

                    personInfo['name'] = name
                    personInfo['works_at'] = works_at
                    personInfo['location'] = location
                    personInfo['num_followers'] = follow
                    personInfo['profile_url'] = profile_link
                    personInfo['education'].extend(education_list)
                    personInfo['experience'].extend(experience_list)
                    personInfo['skills'] = self.skills(profile_link)
                    self.db.collection.insert_one(personInfo)
                    # print(personInfo)
                    print("Name -->", name,
                          "\nWorks At -->", works_at,
                          "\nLocation -->", location,
                          "\nnum followers -->", follow,
                          f"\neducation {personInfo['education']},"
                          f"\nexperience {personInfo['experience']},"
                          f"\nskills {personInfo['skills']}")

                else:
                    continue
                      # "\nnumber of connection -->", num_connection)
        except pymongo.errors.DuplicateKeyError:
            print("duplicate error!")

    def scroll_down(self):
        SCROLL_PAUSE_TIME = 3
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(3):
            # scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait for load page
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def education(self, profile_link):
        """
        takes 1 parameter and returns the result
        param: profile_link
        return: education info list
        """
        infoList = []
        edu_link = f'{profile_link}details/education'
        src = self.get_src(edu_link)
        soup = BeautifulSoup(src, 'lxml')
        # print(soup)
        try:
            eduli = soup.find('div', {'class': 'pvs-list__container'})
            eduli = eduli.findAll('li')
        except:
            pass

        for li in eduli:
            try:
                school = li.find('span', {'class': 'mr1 hoverable-link-text t-bold'})
                school = school.find('span', {'class': 'visually-hidden'}).text.strip()
            except:
                school = ''
            try:
                department = li.find('span', {'class': 't-14 t-normal'})
                department = department.find('span', {'class': 'visually-hidden'}).text.strip()
            except:
                department = ''

            try:
                graduate_date = li.find('span', {'class': 't-14 t-normal t-black--light'})
                graduate_date = graduate_date.find('span', {'class': 'visually-hidden'}).text.strip()
            except:
                graduate_date = ''

            info ={
                    'school'        : school,
                    'department'    : department,
                    'graduate_date' : graduate_date
            }
            if school != '' and department != '' and graduate_date != '':
                infoList.append(info)
        return infoList


    def experience(self, link):
        pass

    def get_src(self, link):
        self.driver.get(link)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)
        src = self.driver.page_source
        return src

    def get_src_with_scroll(self, link, is_scroll:bool):
        self.driver.get(link)
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)
        current_url = self.driver.current_url
        self.scroll_down() if is_scroll else None
        src = self.driver.page_source
        return src, current_url

    def experience(self, profile_link):
        experience_link = f'{profile_link}details/experience'
        src = self.get_src(experience_link)
        soup = BeautifulSoup(src, 'lxml')
        experience = soup.find('div', {'class': 'pvs-list__container'})
        experience = experience.findAll('li')

        infoList = []

        is_called = False
        cn = None

        def is_there_link(li, driver):
            company = li.find('a', {'class': 'optional-action-target-wrapper display-flex flex-column full-width'})
            if company is not None:
                cn = company_name(li, driver)
                lilist = li.findAll('li', {'class': 'pvs-list__paged-list-item'})
                for myli in lilist:

                    try:
                        field = myli.find('span', {'class': 'mr1 hoverable-link-text t-bold'})
                        field = field.find('span', {'class': 'visually-hidden'}).text
                    #                 print(department)
                    except:
                        pass

                    try:
                        date = myli.find('span', {'class': 't-14 t-normal t-black--light'})
                        date = date.find_next('span', {'class': 'visually-hidden'}).text.strip()
                        date, working_time = get_working_time(date)
                    except:
                        pass

                    finally:
                        if field != None and date != None:
                            expInfo = {'company_name': cn, 'field': field, 'date': date, 'working_time': working_time}
                            if expInfo not in infoList:
                                infoList.append(expInfo)

            else:
                return infoList

        def company_name(li, driver):
            current_url = driver.current_url
            links = li.find('a')
            links = links.get('href')
            src = self.get_src(links)
            soup = BeautifulSoup(src, 'lxml')
            name = soup.find('h1').text.strip()
            return name

        def get_working_time(date):
            psDate = date.split('·')
            date = str(psDate[0]).strip()
            workink_time = str(psDate[1]).strip()
            return date, workink_time

        for li in experience:
            is_there_link(li, self.driver)

            try:
                company_name_ = li.find('span', {'class': 't-14 t-normal'})
                company_name_ = company_name_.find('span', {'class': 'visually-hidden'}).text.strip()
            except:
                pass

            try:
                field_ = li.find('span', {'class': 'mr1 t-bold'})
                field_ = field_.find('span', {'class': 'visually-hidden'}).text.strip()
            except:
                pass

            try:
                date_ = li.find('span', {'class': 't-14 t-normal t-black--light'})
                date_ = date_.find_next('span', {'class': 'visually-hidden'}).text.strip()
                date_, working_time = get_working_time(date_)

            except:
                pass

            finally:
                if field_ != None and date_ != None and company_name_ != None:
                    new_experience = {'company_name': company_name_, 'field': field_, 'date': date_,
                                      'working_time': working_time}
                    infoList.append(new_experience)

        return infoList

    def skills(self, profile_link):
        sklList = []

        src, current_url = self.get_src_with_scroll(profile_link, is_scroll = False)
        skillUrl = f'{current_url}details/skills'
        self.driver.get(skillUrl)
        wait = WebDriverWait(self.driver, 5)
        #####  sometimes showed button of "show more skills". If you see it you can following code:
        #####  important: if you will use following code you must find button which name of "show more skills" class name.
        # while True:
        #     try:
        #         time.sleep(1)
        #         container = self.driver.find_element_by_class_name("pvs-list__container")
        #         button = container.find_element_by_tag_name('button').find_element_by_class_name('show-more-class-name') #it doesnt work
        #         button.click()
        #     except (ElementClickInterceptedException, NoSuchElementException):
        #         break

        self.scroll_down()
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        # self.scroll_down()
        container = soup.find('div', {'class': 'artdeco-tabpanel active ember-view'})
        lilist = container.findAll('li')

        for skill in lilist:
            try:
                skill = skill.find('span', {'class': 'mr1 hoverable-link-text t-bold'})
                if skill is not None:
                    skill = skill.find('span', {'class': 'visually-hidden'})
                    sklList.append(skill.text)
            except:
                pass
        return sklList





