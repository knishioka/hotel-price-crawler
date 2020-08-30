import argparse
import datetime
import logging
import random
from time import sleep

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger("Hotel Crawling")
logger.setLevel(logging.DEBUG)
logfile_name = datetime.datetime.now().strftime("%b %d,%Y %H-%M-%S")
fh = logging.FileHandler(f"Flexible Dates Logs {logfile_name}.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def scrape_hotels(no_of_rooms, no_of_nights, no_of_adults, no_of_children):
    logger.debug("Script is starting....")
    logger.info("User typing the input fields as per Requirement....")

    driver = set_driver()

    logger.debug("Executing driver to website....")
    driver.get("https://www.marriott.com/search/default.mi")
    driver.maximize_window()

    sleeping_time = random.randint(3, 7)
    sleep(sleeping_time)

    logger.info("Filling the input fields in website as per Requirement....")
    driver.find_element_by_xpath("//input[@name='destinationAddress.destination']").send_keys("Japan")
    sleep(1)

    check_in = driver.find_element_by_xpath("//input[@placeholder='Check-in']")
    for i in range(12):
        check_in.send_keys(Keys.BACKSPACE)
    sleep(1)

    flexible_date = driver.find_element_by_xpath("//span[@data-tab-value='Flexible Dates']")
    driver.execute_script("arguments[0].click();", flexible_date)
    try:
        nights = driver.find_element_by_xpath("//a[@aria-label='Add Nights']")
        if no_of_nights > 1:
            for _ in range(no_of_nights - 1):
                sleep(0.1)
                driver.execute_script("arguments[0].click();", nights)
        sleep(1)
        done_button = driver.find_element_by_xpath("//div[contains(@class,'flex-done-button')]")
        driver.execute_script("arguments[0].click();", done_button)
    except Exception:
        print("Kindly enter the No. of Nights in correct format i.e. 15")
        driver.close()
        return

    sleep(1)
    edit_rooms = driver.find_element_by_xpath("//a[@aria-label='Rooms & Guests']")
    driver.execute_script("arguments[0].click();", edit_rooms)

    add_rooms = driver.find_element_by_xpath("//a[@aria-label='Add Rooms']")
    if no_of_rooms > 1:
        for _ in range(no_of_rooms - 1):
            driver.execute_script("arguments[0].click();", add_rooms)

    add_adults = driver.find_element_by_xpath("//a[@aria-label='Add Adults Per Room']")
    if no_of_adults > 1:
        for _ in range(no_of_adults - 1):
            driver.execute_script("arguments[0].click();", add_adults)

    # add_children = driver.find_element_by_xpath("//a[@aria-label='Add Children Per Room']")
    # if no_of_children > 0:
    #     for _ in range(no_of_children - 1):
    #         driver.execute_script('arguments[0].click();', add_children)
    # child_age = driver.find_element_by_xpath("//a[@aria-label='Up Age']")
    # child_age.click()

    sleep(2)
    edit_hotels = driver.find_element_by_xpath("//button[contains(@class,'is-roomkey')]")
    driver.execute_script("arguments[0].click();", edit_hotels)
    logger.info("Finding Hotels as per Requirements....")


def set_driver():
    ua = UserAgent()
    user_agent = ua.random
    print(f"User Agent Selected => {user_agent}")
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=options)
    return driver


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("Month_name", help="Please Enter Month Name Required :", type=str)
    parser.add_argument("no_of_nights", help="Please Enter Number of Nights :", type=int)
    parser.add_argument("no_of_rooms", help="Please Enter Number of Rooms Required :", type=int)
    parser.add_argument("no_of_adults", help="Please Enter Number of Adults", type=int)
    parser.add_argument("no_of_children", help="Please Enter Number of Children :", type=int)

    args = parser.parse_args()
    month_name = args.Month_name
    no_of_nights = args.no_of_nights
    no_of_rooms = args.no_of_rooms
    no_of_adults = args.no_of_adults
    no_of_children = args.no_of_children
    scrape_hotels(no_of_rooms, no_of_nights, no_of_adults, no_of_children)