#! /usr/bin/env python3



import argparse
import logging
import re
import datetime
import time

#from http.cookiejar import LWPCookieJar, Cookie

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import requests_html

import neil_tools
import init_selenium
import config as config_static

log = logging.getLogger(__name__)


def main():
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    log.debug("running...")

    config = neil_tools.init_config(config_static, ".env")

    # initialize selenium
    try:
        driver = init_selenium.get_driver(headless=(not args.show))

        for dr in args.dr_id:
            pass

            # should fetch DTT info here...

            # now drive the avis site
            #fetch_receipt(config, driver, "mccrindle", "12140177US0")
            fetch_receipt(config, driver, "Mattimoe", "12445864US4")
    finally:
        driver.close()


def fetch_receipt(config, driver, name, reservation):


    driver.get(config.AVIS_RECEIPT_URL)
    WebDriverWait(driver, 30).until(EC.title_contains(config.AVIS_RECEIPT_TITLE))

    log.debug(f"after page load")

    time.sleep(0.5)

    # there's a marketing popup that shows up and has to be dismissed
    driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
    time.sleep(0.5)

    form = driver.find_element_by_name("receipt_form_hidden")
    form.find_element_by_id("lastName").send_keys(name)
    form.find_element_by_id("Confirmation-no").send_keys(reservation)
    button = form.find_element_by_tag_name("button").click()
    time.sleep(5)

    # check the title; 
    title = driver.title
    if title.startswith("Reservations"):
        pass
    elif title.startswith("Receipt Details"):
        download_receipt(config, driver)
    else:
        log.error(f"Could not find avis record for '{ name }' / '{ reservation }'")
        return

    time.sleep(15)



def download_receipt(config, driver):


    outer_dashboard = driver.find_element_by_class_name("dashboard-content-container")
    download_button = outer_dashboard.find_element_by_css_selector('a[ng-click="vm.downloadPdf()"]')
    download_button.click()

    

    



def parse_args():
    parser = argparse.ArgumentParser(
        description="tools to retrive rental confirmations and receipts from avis.com",
        allow_abbrev=False)
    parser.add_argument("--debug", help="turn on debugging output", action="store_true")
    parser.add_argument("--show", help="Show the selenium browser", action="store_true")
    parser.add_argument("--dr-id", help="the name of the DR (like 155-22)", required=True, action="append")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    neil_tools.init_logging(__name__)
    main()
