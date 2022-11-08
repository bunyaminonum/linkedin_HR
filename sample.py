import requests
from bs4 import BeautifulSoup
import selenium
import login
from login import Login

class linkedin(Login):
    def __init__(self, email, passwd):
        super().__init__(email,passwd)
        self.