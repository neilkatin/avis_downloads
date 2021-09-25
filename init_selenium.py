
# webdriver: selenium bootstrap support

import argparse
import logging

#from http.cookiejar import LWPCookieJar, Cookie


from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)




def get_driver(headless=True):
    #log.debug("refreshing authorization cookies via selenium")

    selenium_driver_type = "chrome"

    if selenium_driver_type == "chrome":

        # initialize selenium
        options = webdriver.ChromeOptions()
        options.headless = headless

        # this is needed to allow app to run in a container.  One more reason to get rid of the selenium login stuff
        options.add_argument("--no-sandbox")

        # this is needed for headless to work: https://stackoverflow.com/questions/47061662/selenium-tests-fail-against-headless-chrome
        #options.add_argument("--window-size=1280,1024")
        #options.add_argument("--disable-gpu")
        #options.add_argument("--allow-insecure-localhost")

        #options.add_argument("test-type");
        #options.add_argument("enable-strict-powerful-feature-restrictions");
        options.add_argument("disable-geolocation");

        driver = webdriver.Chrome(options=options)

    elif selenium_driver_type == "firefox":

        options = webdriver.FirefoxOptions()
        options.headless = True

        driver = webdriver.Firefox(options=options)

    else:
        log.fatal("Unknown selenium driver type")
        return 1

    return driver




