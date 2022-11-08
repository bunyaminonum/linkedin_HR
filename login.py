import time
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.link =  'https://www.linkedin.com/login'

        #ignore errors for Chrome
        # options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--disable-gpu')

        #alternative to Firefox
        # self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.driver = webdriver.Firefox(executable_path = GeckoDriverManager().install())

        self.driver.get(self.link)
        self.driver.implicitly_wait(10)

        id = self.driver.find_element_by_id('username')
        id.send_keys(self.email)

        id = self.driver.find_element_by_id('password')

        id.send_keys(self.password)
        self.driver.implicitly_wait(10)

        id.submit()
        time.sleep(6)
