#! /usr/bin/env python3



import argparse
import logging
import re
import datetime

#from http.cookiejar import LWPCookieJar, Cookie

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
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
    driver = init_selenium.get_driver(headless=(not args.show))

    for dr in args.dr_id:
        pass

        # should fetch DTT info here...

        # now drive the avis site
        fetch_receipt(config, driver, "mccrindle", "12140177US0")


def fetch_receipt(config, driver, name, reservation):


    driver.get(config.AVIS_RECEIPT_URL)
    WebDriverWait(driver, 30).until(EC.title_contains(config.AVIS_RECEIPT_TITLE))

    log.debug(f"after page load")



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
