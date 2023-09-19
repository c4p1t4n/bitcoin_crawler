import time
import awswrangler
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
def get_driver() -> webdriver:
    """
    Return a webdriver
    """
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Firefox(options=options)
    return driver
def get_table_of_prices(driver):
    """
    Return the table with all cryptocurrency's
    """
    driver.get("https://coinmarketcap.com/")
    time.sleep(5)
    div =  driver.find_element(By.CLASS_NAME,'sc-b28ea1c6-2')
    table = div.find_element(By.CLASS_NAME,'sc-b28ea1c6-3')

    return table

def get_bitcoin_price(driver) -> float:
    """
    Returt the current price of bitcoin
    """

    table = get_table_of_prices(driver)

    element = table.find_element(By.CLASS_NAME,'sc-a0353bbc-0')

    price= float(element.text[1:])
    driver.close()
    return price

def price_negative(price)-> bool:
    """
    Return True if the element price is have a element with class name  icon-Caret-up 
    Return False if the element don't have the element with the class name icon-Caret-up
    """
    try:
        price.find_element(By.CLASS_NAME,'icon-Caret-up')
        return False
    except NoSuchElementException:
        return True

def get_price_variation_last_hour(table_of_prices) -> float:
    """
    Return the variation of bitcoin price in the last hour
    """
    price_last_hour = table_of_prices.find_element(By.CLASS_NAME,'sc-d55c02b-0')
    if price_negative(price_last_hour):
        return float(price_last_hour.text[:-1]) * -1
    return float(price_last_hour.text[:-1])


def get_price_variations(driver) -> list:
    """
    Return a list of price variations
    the first element is the variation of the last hour
    the second element is the variation of the last 24 hour
    the third element is the variation of the last sevend days
    example of return [-0.14,-0.38,2.51]
    """

    table = get_table_of_prices(driver)
    soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
    print("---------")
    variation_last_hour = get_price_variation_last_hour(table)

    print(variation_last_hour)
    # driver.close()
    return [variation_last_hour]


firefox = get_driver()


def lambda_handler(event,context):
    get_price_variations(firefox)
    