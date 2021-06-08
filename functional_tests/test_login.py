from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from main.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def teardown(self):
        self.browser.close()

    def test_no_projects_alert_is_displayed(self):
        self.browser.get(self.live_server_url)
        time.sleep(20)
    '''
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        password_input = self.selenium.find_element_by_name("password")

        self.selenium.find_element_by_xpath('//input[@value="Login"]').click()

        submit = self.selenium.find_element_by_id('submit')

        username_input.send_keys('s11085260')
        password_input.send_keys('password')

        submit.send_keys(Keys.RETURN)

        # assert "Hello, world!" in driver.title
    

    def testform(self):
        driver = webdriver.Chrome(
            'C:/Users/lovers12/Desktop/django_projects/JustFoods-master/functional_tests/chromedriver.exe')

        driver.get('http://127.0.0.1:8000/accounts/login/')

        time.sleep(3)

        user_name = driver.find_element_by_name('username')
        user_password = driver.find_element_by_name('password')

        time.sleep(3)

        submit = driver.find_element_by_id('submit')

        user_name.send_keys('s11085260')
        user_password.send_keys('password')

        submit.send_keys(Keys.RETURN)

        assert "Our Dishes" in driver.page_source
     '''
