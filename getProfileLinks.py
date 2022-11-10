import time
from time import sleep
import requests
from bs4 import BeautifulSoup
from login import Login
from manupulation import Manipulation as mn
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager



class GetProfileLinks(Login):
    def __init__(self, email:str, password:str, pageNum = 1):
        super().__init__(email, password)
        self.pageNum = pageNum
        self.linklist = list()
        for num in range(1,pageNum+1):
            self.link = f'https://www.linkedin.com/search/results/people/?connectionOf=%5B%22ACoAAATqPu8BmSX7Z1r428v2N0re0E2zYhvoGGk%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page={num}&sid=Lj2'
            self.setProfile()
        self.removeDuplicateLink()

    def setProfile(self):
        self.driver.get(self.link)
        src = self.getSource()
        profileLinks = src.find_all('a')
        for link in profileLinks:
            link = str(link.get('href'))
            parseLink = link.split('/')
            if 'in' in parseLink:
                self.linklist.append(link)

    def getSource(self):
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        return soup

    def removeDuplicateLink(self):
        self.linklist = list(set(self.linklist))


# P = GetProfileLinks('19701023@mersin.edu.tr', '19074747fb')