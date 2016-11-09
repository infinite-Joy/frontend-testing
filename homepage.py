# -*- coding: utf-8 -*-
import time
import logging
import datetime
from urllib.request import urlopen, HTTPError, URLError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://flawcode.com"
PATH = "/home/joy/github/frontend-testing/phantomjs"


def get_date():
    mylist = []
    today = datetime.date.today()
    mylist.append(today)
    return mylist[0]


logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

fileName = "heat_%s" % (get_date())
fileHandler = logging.FileHandler("{0}.log".format(fileName))
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

# this is to implement the singleton
# we do not want multiple instances of browser being implemented
class SingletonMetaClass(type):
    def __init__(cls, name, bases, dict):
        super(SingletonMetaClass, cls)\
          .__init__(name, bases, dict)
        original_new = cls.__new__

        def my_new(cls, *args, **kwds):
            if cls.instance is None:
                cls.instance = \
                  original_new(cls, *args, **kwds)
            return cls.instance
        cls.instance = None
        cls.__new__ = staticmethod(my_new)


class Browser(object):
    """
    implementation:
    with Browser("PhantomJS") as b:
        b.execute_steps()

    or
    with Browser("Firefox") as b:
        b.execute_steps()

    """
    __metaclass__ = SingletonMetaClass

    def __init__(self, browser_type):
        super(Browser, self).__init__()
        self.browser_type = browser_type

        if self.browser_type == "Firefox":
            self.browser = webdriver.Firefox()
            self.browser.set_window_size(1120, 550)

        elif self.browser_type == "PhantomJS":
            self.browser = webdriver.PhantomJS(PATH)
            self.browser.set_window_size(1120, 550)

        # for logging
        self.logger = logging.getLogger()
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

    def __enter__(self):
        return self

    def hit_url(self, the_url):
        self.browser.get(the_url)
        self.logger.info("browser url: %s" % self.browser.current_url)

    def get_all_buttons(self):
        try:
            for i in range(1, 10):
                yield self.browser.find_element(By.XPATH,
                                             ".//*[@id='app']/div[1]/a[%s]" % i)
        except:
            pass

    def validate_url(self, url):
        self.logger.info("To test the url %s" % url)
        try:
            r = urlopen(url)
            return True
        except HTTPError as e:
                print(e.code)
        except URLError as e:
                print(e.args)

    def execute_steps(self):
        url = URL
        self.hit_url(url)
        for a in self.get_all_buttons():
            pre_validated_url = a.get_attribute('href')
            if not self.validate_url(pre_validated_url):
                self.logger.debug("the url %s is not working"
                                  % pre_validated_url)

    def __exit__(self, *args):
        self.browser.quit()
        self.logger.info("The flow should be complete")
        logging.shutdown()


def main():
    try:
        # with Browser("PhantomJS") as b:
        with Browser("PhantomJS") as b:
            b.execute_steps()
    except Exception as e:
        logger.debug("Error got: %s" % e)
        raise e


if __name__ == '__main__':
    main()
