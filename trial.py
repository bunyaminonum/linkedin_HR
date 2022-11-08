import time
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import requests
from login import Login


class Trial(Login):
    def __init__(self, email,password,link='https://www.linkedin.com/in/olmezyusuf/'):
        super().__init__(email,password)
        self.r = requests.get(link)
        # bs = BeautifulSoup(self.r.content)
        print(self.r)

trial = Trial('19701023@mersin.edu.tr', '19074747fb')