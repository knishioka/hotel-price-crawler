"""Collect hotel price data."""
import argparse
import datetime
import logging
from time import sleep

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger("Hotel Crawling")
logger.setLevel(logging.DEBUG)
logfile_name = datetime.datetime.now().strftime("%b %d,%Y %H-%M-%S")
fh = logging.FileHandler(f"Flexible Dates Logs {logfile_name}.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def scrape_hotels(no_of_rooms, no_of_nights, no_of_adults, no_of_children):
    """Scrape hotel sites."""
    logger.debug("Script is starting....")

    driver = set_driver()
    search_with_conditions(driver, no_of_rooms, no_of_nights, no_of_adults, no_of_children)

    hotels_found = driver.find_elements_by_css_selector("div[data-map]")
    for hotel in hotels_found:
        hotel_name = hotel.find_element_by_css_selector(".l-property-name").text.strip()
        hotel_location = hotel.find_element_by_css_selector(".m-hotel-address").text.strip()
        print(hotel_name, hotel_location)

        view_rates_btn = hotel.find_element_by_css_selector(".js-view-rate-btn-link.analytics-click.l-float-right")
        driver.execute_script("arguments[0].click();", view_rates_btn)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
        html = BeautifulSoup(driver.page_source, "html.parser")
        table = html.select("tbody")[0]
        rows_found = table.select("tr.checkin-month")
        print(f"Found {len(rows_found)}")
        for row in rows_found:
            try:
                cells = row.select("td")
                for cell in cells:
                    try:
                        month = (cell.select(".l-l-display-none.t-num-month")[0].getText()).strip()
                        day = (cell.select(".l-l-display-none.t-font-bold")[0].getText()).strip()
                        print(month, day)
                        price = cell.select("#isSubtotalView .t-font-l")[0].getText()
                        print(hotel_name, hotel_location, price)
                    except Exception:
                        continue
            except Exception:
                continue


def set_driver():
    """Set selenium driver."""
    ua = UserAgent()
    user_agent = ua.random
    print(f"User Agent Selected => {user_agent}")
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1200x600")
    driver = webdriver.Chrome(options=options)
    return driver


def search_with_conditions(driver, no_of_rooms, no_of_nights, no_of_adults, no_of_children):
    """Search hotels with conditions."""
    logger.info("User typing the input fields as per Requirement....")

    wait = WebDriverWait(driver, 10)

    logger.debug("Executing driver to website....")
    driver.get("https://www.marriott.com/search/default.mi")

    logger.info("Filling the input fields in website as per Requirement....")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='destinationAddress.destination']"))).send_keys(
        "Japan"
    )

    check_in = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Check-in']")))
    for i in range(12):
        check_in.send_keys(Keys.BACKSPACE)

    flexible_date = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-tab-value='Flexible Dates']")))
    driver.execute_script("arguments[0].click();", flexible_date)
    try:
        nights = driver.find_element_by_xpath("//a[@aria-label='Add Nights']")
        if no_of_nights > 1:
            for _ in range(no_of_nights - 1):
                sleep(0.1)
                driver.execute_script("arguments[0].click();", nights)

        done_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'flex-done-button')]")))
        driver.execute_script("arguments[0].click();", done_button)
    except Exception:
        print("Kindly enter the No. of Nights in correct format i.e. 15")
        driver.close()
        return

    edit_rooms = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Rooms & Guests']")))
    driver.execute_script("arguments[0].click();", edit_rooms)

    add_rooms = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Add Rooms']")))
    if no_of_rooms > 1:
        for _ in range(no_of_rooms - 1):
            driver.execute_script("arguments[0].click();", add_rooms)

    add_adults = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Add Adults Per Room']")))
    if no_of_adults > 1:
        for _ in range(no_of_adults - 1):
            driver.execute_script("arguments[0].click();", add_adults)

    add_children = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Add Children Per Room']")))
    if no_of_children > 0:
        for _ in range(no_of_children):
            driver.execute_script("arguments[0].click();", add_children)
        sleep(0.5)
        child_age = driver.find_element_by_xpath("//a[@aria-label='Up Age']")
        child_age.click()

    edit_hotels = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'is-roomkey')]")))
    driver.execute_script("arguments[0].click();", edit_hotels)
    logger.info("Finding Hotels as per Requirements....")


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
