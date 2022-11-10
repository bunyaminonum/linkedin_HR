import time
import getProfileLinks
from getProfileLinks import GetProfileLinks
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import requests
class GetInfo(GetProfileLinks):
    GRADUATE_XPATH = '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[4]/div[3]/ul/li/div/div[2]/div/a/span[2]/span[1]'
    cssSelector = 'html.theme.theme--mercado.artdeco.windows body.render-mode-BIGPIPE.nav-v2.ember-application.boot-complete.icons-loaded div.application-outlet div.authentication-outlet div#profile-content.extended.tetris.pv-profile-body-wrapper div.body div#ember32.artdeco-tabs.artdeco-tabs--size-t-48.ember-view div.scaffold-layout.scaffold-layout--breakpoint-none.scaffold-layout--main-aside.scaffold-layout--single-column.scaffold-layout--reflow.pv-profile div.scaffold-layout__inner.scaffold-layout-container.scaffold-layout-container--reflow div.scaffold-layout__row.scaffold-layout__content.scaffold-layout__content--main-aside.scaffold-layout__content--has-aside main#main.scaffold-layout__main section#ember86.artdeco-card.ember-view.relative.break-words.pb3.mt2 div.pvs-list__outer-container ul.pvs-list.ph5.display-flex.flex-row.flex-wrap li.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column div.pvs-entity.pvs-entity--padded.pvs-list__item--no-padding-when-nested div.display-flex.flex-column.full-width.align-self-center div.display-flex.flex-row.justify-space-between a.optional-action-target-wrapper.display-flex.flex-column.full-width'
    cssSelector = ''
    LOC_XPATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]'
    # LANGUAGE_PATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[8]/div[3]/ul/li/div/div[2]/div'
    NUM_CONNECTION_PATH = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[2]/div/div/div/p/span[1]'
    NUM_CONNECTION_PATH2 = '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li/a/span/span'
    def __init__(self, email:str, password:str, pageNum = 1):
        super().__init__(email, password, pageNum)

    def start(self):
        self.getLink()

    def getInfo(self):
        pass

    def getLink(self):
        for link in self.linklist:
            self.driver.get(link)
            time.sleep(2)
            # graduate = self.driver.find_element_by_xpath(self.GRADUATE_XPATH)

            src = self.driver.page_source

            # Now using beautiful soup
            soup = BeautifulSoup(src, 'lxml')
            intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
            try:
                name_loc = intro.find("h1")
                name = name_loc.get_text().strip()
            except:
                name_loc = None
            # Extracting the Name


            # strip() is used to remove any extra blank spaces
            try:
                works_at_loc = intro.find("div", {'class': 'text-body-medium'})
                works_at = works_at_loc.get_text().strip()
            except:
                works_at_loc = None
            # this gives us the HTML of the tag in which the Company Name is present
            # Extracting the Company Name


            # Ectracting the Location
            try:
                location = self.driver.find_element_by_xpath(self.LOC_XPATH).text
            except NoSuchElementException:
                location = None


            print("Name -->", name,
                  "\nWorks At -->", works_at,
                  "\nLocation -->", location,
                    "",'\n')
                  # "\nnumber of connection -->", num_connection)

            # print(graduate.text)
p = GetInfo('19701023@mersin.edu.tr', '19074747fb', 2)
p.start()

