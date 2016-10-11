# -*- coding: utf-8 -*-
import sys
import os
import time
import logging
import datetime
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

logger.setLevel(logging.DEBUG)


# this is to implement the singleton
# we do not want multiple instances of browser being implemented
class SingletonMetaClass(type):
    def __init__(cls,name,bases,dict):
        super(SingletonMetaClass,cls)\
          .__init__(name,bases,dict)
        original_new = cls.__new__
        def my_new(cls,*args,**kwds):
            if cls.instance == None:
                cls.instance = \
                  original_new(cls,*args,**kwds)
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
            self.browser = webdriver.PhantomJS()
            self.browser.set_window_size(1120, 550)

        # for logging
        self.logger = logging.getLogger()
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

    def __enter__(self):
        return self

    def hit_url(self):
        self.browser.get(the_url)
        self.logger.info("browser url: %s" % self.browser.current_url)

    def see_recomendations(self):
        WebDriverWait(self.browser, 50).until(
            EC.visibility_of_element_located((By.ID, "ide")))

        self.logger.info("browser url: %s" % self.browser.current_url)

        # find the recomendations
        for element in self.browser.find_elements_by_id("ide"):
            self.logger.info("element text: %s" % element.text)
            self.logger.info("element tag name: %s" % element.tag_name)
            self.logger.info("element parent: %s" % element.parent)
            self.logger.info("element location: %s" % element.location)
            self.logger.info("element size: %s" % element.size)

        time.sleep(10)

    def execute_steps(self):
        self.hit_url()
        self.fill_values()
        self.select_role()
        self.see_recomendations()

    def __exit__(self, *args):
        self.browser.quit()
        self.logger.info("The flow should be complete")
        logging.shutdown()


def main():
    try:
        #with Browser("PhantomJS") as b:
        with Browser("PhantomJS") as b:
            b.execute_steps()
    except Exception, e:
        logger.debug("Error got: %s" % e)
        raise e



if __name__ == '__main__':
    main()
